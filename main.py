import data, webserver, discord, datetime, asyncio, random, importlib

client = discord.Client(activity=discord.Game(name="Island Hunt"))

# game data
types = data.types
""" name[0], status[1], xp[2], level[3], cooldowns[4], items[5], position[6] ([x,y,z]), world#[7], unlocks[8], world[9], achievements[10], map[11] """

# retrieve data
saves = data.load()
help_text = open("help.txt","r").read()
version_text = open("versions.txt","r").read()
servers = []
emojis = {}

# functions

def emoji(name):
    name = name.replace(" ", "")
    return data.emojis[name]

def new_profile(user):
    if user.id in saves:
        return []
    else:
        return [user.name, "No status", 0, 0, data.new_cooldowns(), {}, [0,0,0], 1, data.new_unlocks(), data.new_world(), data.new_achievements()]
        
def profile(user):
    if str(user.id) in saves:
        return saves[str(user.id)]
    else:
        saves[str(user.id)] = new_profile(user)
        save()
        return saves[str(user.id)]

def save():
    data.save(saves)

def now():
    return int(datetime.datetime.utcnow().timestamp())    

def bold(s):
    return "**" + s + "**"

def underline(s):
    return "__" + s + "__"

def italic(s):
    return "_" + s + "_"

def mono(s):
    return "`" + s + "`"

def tick():
    return ":white_check_mark:"

def cross():
    return ":regional_indicator_x:"

def clock():
    return ":clock" + str(random.randint(1,12)) + ":"

def feedback(s):
    file = open("feedback.txt","a")
    file.write("\n" + s)
    file.close()

async def sleep(t):
    await asyncio.sleep(t)

async def send(channel, s):
    await channel.send(s)

async def sendwait(channel, s, t):
    await sleep(t)
    await send(channel, s)

def get_level(xp):
    return int((xp // 100) ** 0.5) + 1

def get_xp(level):
    return int((level ** 2) * 100)

async def check_level(channel, user):
    xp = saves[user][2]
    level = saves[user][3]
    diff = get_level(xp) - level
    if diff > 0:
        level += diff
        saves[user][3] = level
        await channel.send(bold(saves[user][0]) + " leveled up " + str(diff) + " level" + "s" * int(diff > 1) + "!")

def get_coord_str(pos):
    return "(" + str(pos[0]) + ", " + str(pos[1]) + ", " + str(pos[2]) + ")"

def set_cd(user, s):
    saves[str(user.id)][4][s] = now()

def reset_cd(user_id, s):
    saves[user_id][4][s] = 0

def get_cd(user, s):
    return int(now() - saves[str(user.id)][4][s])

def embed(title, desc, color, fields, footer, thumbnail):
    embed=discord.Embed(title="title", description="desc", color=0x71ff4d)
    embed.set_thumbnail(url=thumbnail)
    for i in fields:
        embed.add_field(name=i[0], value=i[1], inline=i[2])
    embed.set_footer(text=footer)
    await client.bot.say(embed=embed)


# /ready

@client.event
async def on_ready():
    global emojis
    for i in data.server_ids:
        servers.append(client.get_guild(i))
    emojis = data.get_emojis(servers)
    print('We have logged in as {0.user}'.format(client))


# IDs

ids = {
    "dev": "535980912471441438",
    "me": "704880485721178172",
    "mei": "583121082844971026",
    "testing": "000000000000000000"
}

# message

@client.event
async def on_message(message):

    # ignore if sent by bot
    if message.author == client.user:
        return
    
    s = ""
    sav = False
    
    content = message.content
    c = message.channel
    
    if content.startswith("."):
        content = content[1:].lower()
        m = content.split()
        if len(m) == 0:
            command = ""
        else:
            command = m[0]
        user = message.author
        
        p = profile(message.author)

        # variables
        got = {}
        world_num = p[7]
        unlocks = p[8]
        world = p[9]
        ach = p[10]
        cd = p[4]
        inv = p[5]
        pos = p[6]
        xp = p[2]
        level = p[3]
        name = p[0]
        title = p[1]
        maps = p[11]
        
        ##### command handling


        # check if it's me
        
        if str(message.author.id) == ids["dev"]:
            global saves, data, help_text, version_text, emojis
            if command == "reload":
                emojis = data.get_emojis(servers)
                saves = data.load()
                importlib.reload(data)
                help_text = open("help.txt","r").read()
                version_text = open("versions.txt","r").read()
                s = "Successfully reloaded!"
            
            if command == "save":
                sav = True
                s  = "Successfully saved!"
            
            if command == "data_reload":
                importlib.reload(data)
                help_text = open("help.txt","r").read()
                version_text = open("versions.txt","r").read()
                s  = "Successfully reloaded data!"
            
            # world_add
            
            if command == "addd":
                things = eval(" ".join(m[4:]))
                world_add(get_coord_str([int(m[1]), int(m[2]), int(m[3])]), things)
                s  = "Successfully added " + str(things) + " to position " + get_coord_str([int(m[1]), int(m[2]), int(m[3])]) + "!"
            
            if command == "replace" or command == "rep":
                things = eval(" ".join(m[4:]))
                world_replace(get_coord_str([int(m[1]), int(m[2]), int(m[3])]), things)
                s  = "Successfully replaced " + str(things) + " in position " + get_coord_str([int(m[1]), int(m[2]), int(m[3])]) + "!"
            
            if command == "adddd":
                achievement_add()
                s = "Successfully added all achievements!"
            
            if command == "give":
                sav = True
                if m[1][3:-1] in saves:
                    m[1] = m[1][3:-1]
                    thing = " ".join(m[3:])
                    if thing in saves[m[1]][5]:
                        saves[m[1]][5][thing] += int(m[2])
                        s = m[2] + " " + bold(thing) + " given!"
                    else:
                        if thing == "xp":
                            saves[m[1]][2] += int(m[2])
                            await check_level(c, m[1])
                            s = m[2] + " XP given!"
                        else:
                            saves[m[1]][5][thing] = int(m[2])
                            s = m[2] + " " + bold(thing) + " given!"
                else:
                    s = "Who?"
            
            if command == "resetcd":
                if m[1][3:-1] in saves:
                    m[1] = m[1][3:-1]
                    reset_cd(m[1], m[2])
                    s = mono(m[2]) + " successfully resetted!"
                else:
                    s = "Who?"

            if command == "move":
                if len(m) == 5:
                    if m[1][3:-1] in saves:
                        m[1] = m[1][3:-1]
                        saves[m[1]][6] = [int(m[2]),int(m[3]),int(m[4])]
                        await message.channel.send("<@!" + m[1] + "> successfully moved to " + get_coord_str(saves[m[1]][6]) + "!")
                        return
                    else:
                        await message.channel.send("Who?")

            if command == "emoji":
                s = emoji(m[1])

        ### reset

        if command == "reset" or command == "reeeset":
            s = bold(name + ": reset\n")
            confirm = False
            if len(m) >= 5:
                if m[1] == "reset" and m[2] == "reset" and m[3] == "reset" and m[4] == "reeeset":
                    confirm = True
            if confirm or command == "reeeset":
                sav = True
                s += tick() + " Your game is successfully reeesetted!"
                saves[str(user.id)] = new_profile(user)
            else:
                s += "Are you sure you want to reset your entire game??? If so, type `.reset reset reset reset reeeset`."

        ### tutorial
        
        elif unlocks["tutorial"] < 10:
            s = tutorial(m, unlocks, inv, world)
            await message.channel.send(s)
            save()
            return

        ### display stuff
        
        elif command == "help" or command == "help":
            if len(m) == 1:
                s = help_text
            else:
                s = "What are you trying to find help for? Type a valid item/command."

        # tutorial complete
        
        elif command == "tutorial" or command == "tut":
            if unlocks["tutorial"] == 10:
                unlocks["tutorial"] = 11
                s = "Welcome to Island Hunt, " + bold(name) + "!\n\n"
                s += "You have completed the tutorial! You deserve a reward!\n"
                s += "You noticed a tutorial shell suddenly appearing in front of you."
                got["tutorial shell"] = 1
            elif unlocks["tutorial"] == 11:
                s = "Welcome to Island Hunt, " + bold(name) + "!\n\n"
                s += "You have completed the tutorial! You have received your tutorial shell!"
                
        elif command == "versions" or command == "ver" or command == "version" or command == "v":
            s = version_text

        elif command == "recipes" or command == "r":
            if len(m) == 1:
                s = recipes()
            else:
                s = recipe(" ".join(m[1:]).strip())
                if not s:
                    s = "No such recipe! Check `.recipes` for a list of all the recipes!"

        # cooldown
        
        elif command == "cooldown" or command == "cd":
            if message.mentions:
                for member in message.mentions:
                    if str(member.id) in saves:
                        cd = saves[str(member.id)][4]
                        name = saves[str(member.id)][0]
                        user = member
                        break
            s = bold(name + "'s cooldowns\n\n")
            for i in cd:
                if get_cd(user, i) > data.cd[i]:
                    s += tick() + " - " + mono(i) + "\n"
                else:
                    s += clock() + " - " + mono(i) + ": " + wait_for(data.cd[i] - get_cd(user, i)) + "\n"

        # ready

        elif command == "ready" or command == "rd":
            if message.mentions:
                for member in message.mentions:
                    if str(member.id) in saves:
                        cd = saves[str(member.id)][4]
                        name = saves[str(member.id)][0]
                        user = member
                        break
            s = bold(name + "'s ready\n\n")
            for i in cd:
                if get_cd(user, i) > data.cd[i]:
                    s += tick() + " - " + mono(i) + "\n"

        # loot data

        elif command == "loot":
            s = loot_data(" ".join(m[1:]))

        # inventory
        
        elif command == "inventory" or command == "inv" or command == "i":
            if message.mentions:
                for member in message.mentions:
                    if str(member.id) in saves:
                        temp = saves[str(member.id)]
                        inv = temp[5]
                        name = temp[0]
                        break
            s = bold(name + "'s inventory")
            t = ""
            add = ""
            adding = False
            for i in data.items.keys():
                if data.items[i][1] != t:
                    if adding:
                        s += add
                    t = data.items[i][1]
                    add = "\n\n" + underline(t)
                    adding = False
                if i in inv:
                    if inv[i] > 0:
                        add += "\n" + emoji(i) + " " + bold(i) + ": " + str(inv[i])
                        adding = True

        # profile

        elif command == "profile" or command == "prof" or command == "p":
            if message.mentions:
                for member in message.mentions:
                    if str(member.id) in saves:
                        temp = saves[str(member.id)]
                        xp = temp[2]
                        level = temp[3]
                        name = temp[0]
                        title = temp[1]
                        break
            s = bold(name + "'s profile") + "\nTitle: " + title + "\n\nXP: " + str(xp - get_xp(level - 1)) + "/" + str(get_xp(level) - get_xp(level - 1)) + "\nLevel: " + str(level)

        # place
        
        elif command == "place" or command == "pl":
            user_id = str(user.id)
            if message.mentions:
                for member in message.mentions:
                    if str(member.id) in saves:
                        temp = saves[str(member.id)]
                        user_id = str(member.id)
                        pos = temp[6]
                        break
            s = get_place(user_id, pos)
        
        elif command == "map" or command == "mp":
            m = maps
            min_x = 1000
            max_x = -1000
            min_y = 1000
            max_y = -1000
            for i in maps:
                i = i.split(", ")
                i[0] = int(i[0][1:])
                i[1] = int(i[1])
                i[2] = int(i[2][:-1])
                x = i[0]
                y = i[1]
                if x < min_x:
                    min_x = x
                if y < min_y:
                    min_y = y
                if x > max_x:
                    max_x = x
                if y > max_y:
                    max_y = y
            s = bold(name + "'s map") + " " + emoji("here") + " You are here\n"
            for j in range(max_y, min_y - 1, -1):
                s += "\n"
                for i in range(min_x, max_x + 1):
                    key = "(" + str(i) + ", " + str(j) + ", 0)"
                    e = ""
                    if key in maps.keys():
                        if maps[key] and key in data.maps.keys():
                            e = data.maps[key]
                        if key == get_coord_str(pos):
                            e += "here"
                    if e:
                        s += emoji(e)
                    else:
                        s += emoji("void")
        
        elif command == "bigmap" or command == "bmp":
            m = maps
            min_x = 1000
            max_x = -1000
            min_y = 1000
            max_y = -1000
            for i in maps:
                i = i.split(", ")
                i[0] = int(i[0][1:])
                i[1] = int(i[1])
                i[2] = int(i[2][:-1])
                x = i[0]
                y = i[1]
                if x < min_x:
                    min_x = x
                if y < min_y:
                    min_y = y
                if x > max_x:
                    max_x = x
                if y > max_y:
                    max_y = y
            for j in range(max_y, min_y - 1, -1):
                for i in range(min_x, max_x + 1):
                    key = "(" + str(i) + ", " + str(j) + ", 0)"
                    e = ""
                    if key in maps.keys():
                        if maps[key] and key in data.maps.keys():
                            e = data.maps[key]
                        if key == get_coord_str(pos):
                            e += "here"
                    if e:
                        s += emoji(e)
                    else:
                        s += emoji("void")
                s += "\n"

        elif command == "compass" or command == "cp":
            s = emoji("compass")

        # achievements
        
        elif command == "achievements" or command == "ac" or command == "a":
            a = data.achievements
            if message.mentions:
                for member in message.mentions:
                    if str(member.id) in saves:
                        temp = saves[str(member.id)]
                        name = temp[0]
                        title = temp[1]
                        ach = temp[10]
                        inv = temp[5]
                        break
            s = bold(name + "'s achievements") + "\n"
            num = 0
            for i in a:
                num += 1
                done = False
                if i in ach:
                    if ach[i] > 0:
                        done = True
                if not done:
                    if a[i][0] in inv:
                        if inv[a[i][0]] >= a[i][1]:
                            sav = True
                            done = True
                            ach[i] = now()
                if done:
                    s += "\n" + tick() + " - " + i + " " + emoji(a[i][0]) + " - Title: " + mono(a[i][2]) + "(#" + str(num) + ")"
                    if title == a[i][2]:
                        s += " [current title]"
                else:
                    s += "\n" + cross() + " - " + i + " " + emoji(a[i][0]) + " - Title: " + mono(a[i][2]) + "(#" + str(num) + ")"

        # title
        
        elif command == "title":
            try:
                num = int(m[1])
                n = 0
                a = data.achievements
                done = False
                title = ""
                for i in a:
                    n += 1
                    if n == num:
                        if i in ach:
                            if ach[i] > 0:
                                done = True
                                title = a[i][2]
                        if not done:
                            if a[i][0] in inv:
                                if inv[a[i][0]] >= a[i][1]:
                                    sav = True
                                    ach[i] = now()
                                    done = True
                                    title = a[i][2]
                if done:
                    p[1] = title
                    s = "Title successfully set to " + mono(title) + "!"
                else:
                    s = "You don't have that achievement!"
            except:
                s = "What? That's not a valid title number!"

        # walk
        
        elif command == "walk" or command == "w":
            sav = True
            s = bold(name + ": walk\n")
            if get_cd(user, "walk") > data.cd["walk"]:
                L = loot(data.worlds[world_num] + " walk")
                s += L[0]
                got[L[2]] = L[1]
                got["xp"] = int(L[3])
                set_cd(user, "walk")
            else:
                s += wait_for(data.cd["walk"] - get_cd(user, "walk"))

        # look
        
        elif command == "look" or command == "l":
            sav = True
            s = bold(name + ": look\n")
            if get_cd(user, "look") > data.cd["look"]:
                L = loot(data.worlds[world_num] + " look")
                s += L[0]
                got[L[2]] = L[1]
                got["xp"] = L[3]
                set_cd(user, "look")
            else:
                s += wait_for(data.cd["look"] - get_cd(user, "look"))

        # hunt
        
        elif command == "hunt" or command == "h":
            sav = True
            s = bold(name + ": hunt\n")
            if get_cd(user, "hunt") > data.cd["hunt"]:
                await send(c, s + "You walked around on the beach looking for a creature to hunt.")
                set_cd(user, "hunt")
                L = loot(data.worlds[world_num] + " hunt")
                s += L[0]
                got[L[2]] = L[1]
                got["xp"] = int(L[3])
                set_cd(user, "hunt")
                await sendwait(c, s, 30)
                s = ""
            else:
                s += wait_for(data.cd["hunt"] - get_cd(user, "hunt"))

        # sleep

        elif command == "sleep" or command == "sl":
            sav = True
            bed = "bed" in world[get_coord_str(pos)]
            user_id = str(user.id)
            s = bold(name + ": sleep\n")
            if get_cd(user, "sleep") > data.cd["sleep"]:
                set_cd(user, "sleep")
                if bed:
                    s += "You slept comfortably on the bed and felt recharged!\n"
                else:
                    s += "You slept for a while on the sand and felt recharged!\n"
                s += "The cooldowns for look, walk and hunt are reset!"
                got["coins"] = world_num ** 2 * random.randint(25, 50) * 10
                if bed:
                    got["xp"] = world_num ** 2 * random.randint(75, 125) * 10
                else:
                    got["xp"] = world_num ** 2 * random.randint(50, 100) * 10
                reset_cd(user_id, "look")
                reset_cd(user_id, "walk")
                reset_cd(user_id, "hunt")
            else:
                s += wait_for(data.cd["sleep"] - get_cd(user, "sleep"))

        # /daily
        
        elif command == "daily":
            sav = True
            s = bold(name + ": daily\n")
            if get_cd(user, "daily") > data.cd["daily"]:
                set_cd(user, "daily")
                got["coins"] = world_num ** 2 * random.randint(75, 125) * 10
                got["xp"] = world_num ** 2 * random.randint(25, 75) * 10
            else:
                s += wait_for(data.cd["daily"] - get_cd(user, "daily"))

        # /weekly
        
        elif command == "weekly":
            sav = True
            s = bold(name + ": weekly\n")
            if get_cd(user, "weekly") > data.cd["weekly"]:
                set_cd(user, "weekly")
                got["coins"] = world_num ** 2 * random.randint(200, 500) * 10
                got["xp"] = world_num ** 2 * random.randint(150, 300) * 10
                s += "All your cooldowns except daily are reset!"
                reset_cd(user, "look")
                reset_cd(user, "walk")
                reset_cd(user, "hunt")
                reset_cd(user, "sleep")
            else:
                s += wait_for(data.cd["weekly"] - get_cd(user, "weekly"))

        # /move
        
        elif command == "move" or command == "m":
            sav = True
            s = bold(name + ": move\n")
            if get_cd(user, "move") > data.cd["move"]:
                if len(m) > 1:
                    d = m[1]
                    block = "unknown object (ERROR!)"
                    if d == "north" or d == "n":
                        set_cd(user, "move")
                        block = move(0,1,0,pos,world,maps)
                        s += "You " + ["moved", "ran", "walked"][random.randint(0, 2)] + " 10 metres **north**."
                    elif d == "sorth" or d == "s":
                        set_cd(user, "move")
                        block = move(0,-1,0,pos,world,maps)
                        s += "You " + ["moved", "ran", "walked"][random.randint(0, 2)] + " 10 metres **south**."
                    elif d == "east" or d == "e":
                        set_cd(user, "move")
                        block = move(1,0,0,pos,world,maps)
                        s += "You " + ["moved", "ran", "walked"][random.randint(0, 2)] + " 10 metres **east**."
                    elif d == "east" or d == "w":
                        set_cd(user, "move")
                        block = move(-1,0,0,pos,world,maps)
                        s += "You " + ["moved", "ran", "walked"][random.randint(0, 2)] + " 10 metres **west**."
                    elif d == "up" or d == "u":
                        if unlocks["flying"] == 2:
                            set_cd(user, "move")
                            block = move(0,0,1,pos,world,maps)
                            s += "You flew up 10 metres **up** into the air."
                        else:
                            s += "You can't fly, can you?"
                    elif d == "down" or d == "d":
                        if pos[2] > 0:
                            if unlocks["flying"] == 2:
                                set_cd(user, "move")
                                block = move(0,0,1,pos,world,maps)
                                s += "You flew **down** 10 metres."
                            else:
                                block = False
                                s += "You can't fly, can you?"
                        else:
                            if unlocks["digging"] == 2:
                                set_cd(user, "move")
                                block = move(0,0,1,pos,world,maps)
                                s += "You dug **down** 10 metres."
                            else:
                                block = False
                                s += "You can't dig down!"
                    else:
                        block = False
                        s += "Where in the world did you move? I don't seem to understand!"
                    if block:
                        s += "\nHowever, you got blocked by a " + bold(block) + "!"
                    else:
                        pos = p[6]
                        s += "\n\n" + get_place(str(user.id), pos) 
                else:
                    s += "You need to specify in which direction you need to move, for example, `.move north`"
            else:
                s += wait_for(data.cd["move"] - get_cd(user, "move"))

        # /pickup

        elif command in ["pickup","take","pk","tk"]:
            s = bold(name)
            if len(m) == 1:
                pos = get_coord_str(pos)
                s += "NOT WORKING YET"
            else:
                s += "NOT WORKING YET"

        # /craft

        if command in ["craft", "break", "trade", "sell", "buy", "make", "mk"]:
            inside = False
            if command == "make" or command == "mk":
                try:
                    num = int(m[1])
                    if len(m) > 2:
                        if m[2] == "all" or m[2] == "a" or m[2] == "spr":
                            n = 10000000000000000000
                        else:
                            n = int(m[2])
                    else:
                        n = 1
                    for i in data.crafts:
                        num -= 1
                        if num == 0:
                            m = i
                            inside = True
                            break
                except:
                    m = ""
            else:
                m = " ".join(m)
                n = 0
                sav = True
                for i in data.crafts:
                    if m.startswith(i):
                        inside = True
                        n = m[len(i):].strip()
                        m = i
                        if n:
                            if n == "all" or n == "a":
                                n = 10000000000000000000
                            else:
                                try:
                                    n = int(n)
                                except:
                                    inside = False
                                    s = "That number doesn't exist."
                        else:
                            n = 1
                        break
            if inside:
                c = data.crafts[m]
                for i in c[1]:
                    num = 0
                    if i in inv:
                        num = inv[i]
                    num = num // c[1][i]
                    if num < n:
                        n = num
                if n < 1:
                    s = "You don't have enough resources to " + mono(m) + "!"
                else:
                    s = ""
                    for i in c[1]:
                        inv[i] -= n * c[1][i]
                        s += str(n * c[1][i]) + "x " + emoji(i) + " " + i + " used!\n"
                    for i in c[0]:
                        if i in inv:
                            inv[i] += n * c[0][i]
                        else:
                            inv[i] = n * c[0][i]
                        s += "You made " + str(n * c[0][i]) + "x " + emoji(i) + " " + i + "!\n"
            else:
                s = "That doesn't exist."

        # /suggest /bug /change /add /request
        
        if command in ["suggest", "bug", "change", "add", "request"]:
            m = " ".join(m[1:])
            feedback(command + ": \"" + m + "\"")
            s = mono(m) + " successfully submitted!"

        # /pm
        
        if command == "privatemessage" or command == "pm":
            m = " ".join(m[1:])
            await client.get_user(ids["dev"]).send(mono(m) + "\nsent by " + bold(message.author.name))

        # /hi /hello
        
        if command == "hi" or command == "hello":
            await message.author.send("Hi!")

        # more commands go here
        
    else:
        # return if message does not start with .
        return
    
    # send
    if s:
        if len(s) > 2000:
            s = s.split("\n")
            total = 0
            cut = [0]
            for i in range(len(s)):
                total += len(s[i])
                if total > 2000:
                    cut.append(i - 1)
                    total = len(s[i])
            string = []
            cut.append(len(s))
            pos = 0
            for i in range(1,len(cut)):
                string.append("")
                for j in range(cut[i-1], cut[i]):
                    string[i - 1] += s[j] + "\n"
            for i in string:
                await message.channel.send(i)
        else:
            await message.channel.send(s)

    # gives stuff (got)
    if len(got) > 0:
        sav = True
        s = ""
        for i in got:
            if i in inv:
                s += bold(name) + " got " + str(got[i]) + " x " + emoji(i) + " " + bold(i) + "!\n"
                inv[i] += got[i]
            else:
                s += bold(name) + " got " + str(got[i]) + " XP!\n"
                if i.lower() == "xp":
                    p[2] += got[i]
                    await check_level(c, str(user.id))
                else:
                    inv[i] = got[i]
        await message.channel.send(s)
    
    # save
    if sav:
        save()

# place
def get_place(user, pos):
    s = ""
    if get_coord_str(pos) in saves[user][9]:
        for i in saves[user][9][get_coord_str(pos)]:
            s += "\n" + data.things[i][2]
    return bold(saves[user][0] + "'s position") + "\nCoordinates: " + get_coord_str(pos) + "\n\n" + data.place_names[get_coord_str(pos)] + s

def get_map(user):
    p = saves[str(user.id)]
    world = p[9]

# /loot
def loot(name):
    t = data.loot[name]
    item = ""
    j = ""
    for i in t:
        if random.randint(1,t[i]) == 1:
            item = i
            j = i
            break
    item = item.split("|")
    item.extend(item.pop(0).split("x"))
    item[1] = int(item[1])
    item[2] = item[2][1:]
    item.append(item[1] * data.items[item[2]][0])
    if name in data.loot:
        t = data.loot[name]
        percent = 100.00
        for i in t:
            chance = percent / t[i]
            percent *= (1 - 1 / t[i])
            if i == j:
                item.append(chance)
                break
    return item

# /loot data
def loot_data(name):
    if name in data.loot:
        t = data.loot[name]
        s = underline("Chances for loot " + name) + "\n\n"
        percent = 100.00
        for i in t:
            chance = percent / t[i]
            percent *= (1 - 1 / t[i])
            s += bold(i.split("|")[0]) + ": " + str(chance) + "%\n"
        return s
    else:
        return "No such loot tier!"

# actual /move
def move(x,y,z, pos, world, maps):
    p = [i for i in pos]
    p[0] += x
    p[1] += y
    p[2] += z
    maps[get_coord_str(p)] = 1
    if get_coord_str(p) in world:
        for i in world[get_coord_str(p)]:
            if data.things[i][0] == 1:
                return i
    pos[0] += x
    pos[1] += y
    pos[2] += z
    return ""

# wait message (cooldown)
def wait_for(num):
    s = "Wait for "
    n = num
    days = n//86400
    n -= days * 86400
    hours = n//3600
    n -= hours * 3600
    minutes = n//60
    n -= minutes * 60
    seconds = n
    if num < 60:
        s += str(seconds) + " second" + "s" * int(seconds != 1)
    elif num < 3600:
        s += str(minutes) + " minute" + "s" * int(minutes != 1) + " and " + str(seconds) + " second" + "s" * int(seconds != 1)
    elif num < 86400:
        s += str(hours) + " hour" + "s" * int(hours != 1) + ", " + str(minutes) + " minute" + "s" * int(minutes != 1) + " and " + str(seconds) + " second" + "s" * int(seconds != 1)
    else:
        s += str(days) + " day" + "s" * int(days != 1) + ", " + str(hours) + " hour" + "s" * int(hours != 1) + ", " + str(minutes) + " minute" + "s" * int(minutes != 1) + " and " + str(seconds) + " second" + "s" * int(seconds != 1)
    return s + " more!"

# adds stuff to everybody's world
def world_add(pos, things):
    for user in saves:
        if user:
            world = saves[user][9]
            if pos in world.keys():
                world[pos].extend(things)
            else:
                world[pos] = things
    save()

def world_replace(pos, things):
    for user in saves:
        if user:
            world = saves[user][9]
            world[pos] = things
    save()

def achievement_add():
    for user in saves:
        if user:
            if len(saves[user]) == 11:
                ac = saves[user][10]
                for i in data.achievements.keys():
                    if i not in ac:
                        ac[i] = 0
    save()

# /recipes
def recipes():
    s = underline("List of all recipe names") + "\n\n```"
    c = data.crafts
    num = 0
    for i in c:
        num += 1
        s += str(num) + ". " + i + "\n"
    s += "```"
    return s

def recipes_all():
    s = underline(bold("List of all recipes - FULL")) + "\n\n"
    c = data.crafts
    num = 0
    for i in c:
        num += 1
        s += recipe(i) + "\n\n"
    return s

def recipe(r):
    if r in data.crafts:
        s = underline("How to " + r) + "\n\n**Uses**:\n"
        c = data.crafts[r]
        for i in c[1]:
            s += str(c[1][i]) + "x " + emoji(i) + " " + i + "\n"
        s += "\n**Makes**:\n"
        for i in c[0]:
            s += str(c[0][i]) + "x " + emoji(i) + " " + i + "\n"
        return s
    else:
        if r == "all" or r == "a":
            return recipes_all()
        else:
            try:
                r = int(r)
                num = 0
                for i in data.crafts.keys():
                    num += 1
                    if num == r:
                        return recipe(i)
                return ""
            except:
                return ""
 
# the /tutorial (words in data.py)

def tutorial(m, unlocks, inv, world):
    command = m[0]
    tut = unlocks["tutorial"]
    if tut == 0:
        if command == "tutorial" or command == "tut":
            unlocks["tutorial"] = 1
            return data.tutorial_text(0)
        else:
            return data.tutorial_help(0)
    elif tut == 1:
        if command == "look" or command == "l":
            unlocks["tutorial"] = 2
            return data.tutorial_text(1)
        else:
            return data.tutorial_help(1)
    elif tut == 2:
        if command == "walk" or command == "w":
            unlocks["tutorial"] = 3
            return data.tutorial_text(2)
        else:
            return data.tutorial_help(2)
    elif tut == 3:
        if command == "hunt" or command == "h":
            unlocks["tutorial"] = 4
            inv["sandfly"] = 1
            return data.tutorial_text(3)
        else:
            return data.tutorial_help(3)
    elif tut == 4:
        if command == "look" or command == "look":
            unlocks["tutorial"] = 5
            inv["sand"] = 3
            return data.tutorial_text(4)
        else:
            return data.tutorial_help(4)
    elif tut == 5:
        if command == "inventory" or command == "inv" or command == "i":
            unlocks["tutorial"] = 6
            return data.tutorial_text(5)
        else:
            return data.tutorial_help(5)
    elif tut == 6:
        if command == "walk" or command == "w":
            unlocks["tutorial"] = 7
            world["(-1, 0, 0)"] = ["note 1"]
            return data.tutorial_text(6)
        else:
            return data.tutorial_help(6)
    elif tut == 7:
        if (command == "move" or command == "m") and (m[1] == "west" or m[1] == "w"):
            unlocks["tutorial"] = 8
            return data.tutorial_text(7)
        else:
            return data.tutorial_help(7)
    elif tut == 8:
        if command in ["pickup","take","pk","tk"]:
            unlocks["tutorial"] = 9
            world["(-1, 0, 0)"] = []
            return data.tutorial_text(8)
        else:
            return data.tutorial_help(8)
    elif tut == 9:
        if command == "place" or command == "pl":
            unlocks["tutorial"] = 10
            return data.tutorial_text(9)
        else:
            return data.tutorial_help(9)
        
    return "What? Please contact .?#7696 with the following error:\nError 001 Tutorial End"

# /run
webserver.keep()
client.run("NzA0ODgwNDg1NzIxMTc4MTcy.XqjnVQ.7QtQBz6ebMHoGf6sryB47gdZpgw")