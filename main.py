import discord, datetime, asyncio, random, importlib, webserver

client = discord.Client(activity=discord.Game(name="Island Hunt"))

# game data
import data
types = data.types
""" name[0], status[1], xp[2], level[3], cooldowns[4], items[5], position[6] ([x,y,z]), world#[7], unlocks[8], world[9] """

# retrieve data
saves = data.load()
help_text = open("help.txt","r").read()
version_text = open("versions.txt","r").read()

# functions

def new_profile(user):
    if user.id in saves:
        return []
    else:
        return [user.name, "No status", 0, 0, data.new_cooldowns(), {}, [0,0,0], 1, data.new_unlocks(), {}]
        
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
    return ":ballot_box_with_check:"

def cross():
    return ":negative_squared_cross_mark:"

def feedback(s):
    file = open("feedback.txt","a")
    file.write(s + "\n")
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


# /ready

@client.event
async def on_ready():
    print('We have logged in as {0.user}'.format(client))


# IDs

ids = {
    "dev": "535980912471441438",
    "me": 0,
    "mei": "583121082844971026",
    "testing": "000000000000000000"
}    

# message

@client.event
async def on_message(message):
    
    if message.author == client.user:
        return
    
    s = ""
    sav = False
    
    content = message.content
    c = message.channel
    
    if content.startswith("."):
        content = content[1:].lower()
        m = content.split()
        command = m[0]
        user = message.author
        
        p = profile(message.author)

        # variables
        got = {}
        world_num = p[7]
        unlocks = p[8]
        world = p[9]
        cd = p[4]
        inv = p[5]
        pos = p[6]
        xp = p[2]
        level = p[3]
        name = p[0]
        
        ##### command handling


        # check if it's /me
        
        if str(message.author.id) == ids["dev"]:
            if command == "reload":
                global saves, data
                saves = data.load()
                importlib.reload(data)
            if command == "save":
                sav = True
            if command == "data_reload":
                importlib.reload(data)
            if command == "addd":
                world_add(get_coord_str([int(m[1]), int(m[2]), int(m[3])]), eval(" ".join(m[4:])))
            if command == "give":
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
                else:
                    s = "Who?"
            if command == "resetcd":
                if m[1][3:-1] in saves:
                    m[1] = m[1][3:-1]
                    reset_cd(m[1], m[2])
                else:
                    s = "Who?"
                    

        ### /reset

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

        # /tutorial complete
        
        elif command == "tutorial" or command == "tut":
            if unlocks["tutorial"] == 10:
                unlocks["tutorial"] = 11
                s = "Welcome to Island Hunt, " + bold(name) + "!\n\n"
                s += "You have completed the tutorial! You deserve a reward!\n"
                s += "You noticed a tutorial shell suddenly appearing in front of you."
                got["tutorial shell"] = 1
                
        elif command == "versions" or command == "ver" or command == "version" or command == "v":
            s = version_text

        elif command == "recipes" or command == "r":
            if len(m) == 1:
                s = recipes()
            else:
                s = recipe(" ".join(m[1:]).strip())
                if not s:
                    s = "No such recipe! Check `.recipes` for a list of all the recipes!"

        # /cooldown
        
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
                    s += tick() + " - " + mono(i)
                else:
                    s += cross() + " - " + mono(i) + ": " + str(data.cd[i] - get_cd(user, i)) + " seconds left"
                s += "\n"

        # loot data

        elif command == "loot":
            s = loot_data(" ".join(m[1:]))
        
        ### stats

        # /inventory
        
        elif command == "inventory" or command == "inv" or command == "i":
            if message.mentions:
                for member in message.mentions:
                    if str(member.id) in saves:
                        temp = saves[str(member.id)]
                        inv = temp[5]
                        name = temp[0]
                        break
            s = bold(name + "'s inventory\n")
            for i in sorted(inv.keys()):
                s += "\n" + mono(i) + ": " + str(inv[i])

        elif command == "profile" or command == "prof" or command == "p":
            if message.mentions:
                for member in message.mentions:
                    if str(member.id) in saves:
                        temp = saves[str(member.id)]
                        xp = temp[2]
                        level = temp[3]
                        name = temp[0]
                        break
            s = bold(name + "'s profile") + "\nTitle: " + p[1] + "\n\nXP: " + str(xp - get_xp(level - 1)) + "/" + str(get_xp(level) - get_xp(level - 1)) + "\nLevel: " + str(level)


        # /place
        
        elif command == "place" or command == "pl":
            s = bold(name + "'s position") + "\nCoordinates: " + get_coord_str(pos) + "\n\n" + data.place_names[get_coord_str(pos)]


        # /achievements
        
        elif command == "achievements" or command == "ac" or command == "a":
            s = underline("Achievements") + "\n"
            a = data.achievements
            num = 0
            for i in a:
                num += 1
                done = False
                if a[i][0] in inv:
                    if inv[a[i][0]] >= a[i][1]:
                        done = True
                if done:
                    s += "\n" + tick() + " - " + i + " - Title: " + mono(a[i][2]) + "(#" + str(num) + ")"
                else:
                    s += "\n" + cross() + " - " + i + " - Title: " + mono(a[i][2]) + "(#" + str(num) + ")"


        # /title
        
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
                        if a[i][0] in inv:
                            if inv[a[i][0]] >= a[i][1]:
                                done = True
                                title = a[i][2]
                if done:
                    p[1] = title
                    s = "Title successfully set to " + mono(title) + "!"
                else:
                    s = "You don't have that achievement!"
            except:
                s = "What? That's not a valid title number!"

        # /walk
        
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
                s += "Wait for " + str(data.cd["walk"] - get_cd(user, "walk")) + " more seconds!"

        # /look
        
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
                s += "Wait for " + str(data.cd["look"] - get_cd(user, "look")) + " more seconds!"

        # /hunt
        
        elif command == "hunt" or command == "h":
            sav = True
            s = bold(name + ": hunt\n")
            if get_cd(user, "hunt") > data.cd["hunt"]:
                await send(c, s + "You walked around on the beach looking for a creature to hunt and catch.")
                set_cd(user, "hunt")
                L = loot(data.worlds[world_num] + " hunt")
                s += L[0]
                got[L[2]] = L[1]
                got["xp"] = int(L[3])
                set_cd(user, "hunt")
                await sendwait(c, s, 30)
                s = ""
            else:
                s += "Wait for " + str(data.cd["hunt"] - get_cd(user, "hunt")) + " more seconds!"


        # /daily
        
        elif command == "daily":
            sav = True
            s = bold(name + ": daily\n")
            if get_cd(user, "daily") > data.cd["daily"]:
                set_cd(user, "daily")
                got["coins"] = world_num * 1000
                got["xp"] = world_num * 500
            else:
                s += "Wait for " + str(data.cd["daily"] - get_cd(user, "daily")) + " more seconds!"

        # /weekly
        
        elif command == "weekly":
            sav = True
            s = bold(name + ": weekly\n")
            if get_cd(user, "weekly") > data.cd["weekly"]:
                set_cd(user, "weekly")
                got["coins"] = world_num * 3000
                got["xp"] = world_num * 2000
            else:
                s += "Wait for " + str(data.cd["weekly"] - get_cd(user, "weekly")) + " more seconds!"

        # /move
        
        elif command == "move" or command == "m":
            sav = True
            s = bold(name + ": move\n")
            if len(m) > 1:
                d = m[1]
                block = False
                if d == "north" or d == "n":
                    block = move(0,1,0,pos,world)
                    s += "You " + ["moved", "ran", "walked"][random.randint(0, 2)] + " 10 metres **north**."
                elif d == "sorth" or d == "s":
                    block = move(0,-1,0,pos,world)
                    s += "You " + ["moved", "ran", "walked"][random.randint(0, 2)] + " 10 metres **south**."
                elif d == "east" or d == "e":
                    block = move(1,0,0,pos,world)
                    s += "You " + ["moved", "ran", "walked"][random.randint(0, 2)] + " 10 metres **east**."
                elif d == "east" or d == "w":
                    block = move(-1,0,0,pos,world)
                    s += "You " + ["moved", "ran", "walked"][random.randint(0, 2)] + " 10 metres **west**."
                elif d == "up" or d == "u":
                    if unlocks["flying"] == 2:
                        block = move(0,0,1,pos,world)
                        s += "You flew up 10 metres **up** into the air."
                    else:
                        s += "You can't fly, can you?"
                elif d == "down" or d == "d":
                    if pos[2] > 0:
                        if unlocks["flying"] == 2:
                            block = move(0,0,1,pos,world)
                            s += "You flew **down** 10 metres."
                        else:
                            s += "You can't fly, can you?"
                    else:
                        if unlocks["digging"] == 2:
                            block = move(0,0,1,pos,world)
                            s += "You dug **down** 10 metres."
                        else:
                            s += "You can't dig down!"
                else:
                    s += "Where in the world did you move? I don't seem to understand!"
                if block:
                    s += "\nHowever, you got blocked by a " + bold(block) + "!"
            else:
                s += "You need to specify in which direction you need to move, for example, `.move north`"

        # /craft
        
        if command in ["craft", "break", "trade", "sell", "buy"]:
            m = " ".join(m)
            inside = False
            sav = True
            n = 0
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
                        s += str(n * c[1][i]) + "x " + i + " used!\n"
                    for i in c[0]:
                        if i in inv:
                            inv[i] += n * c[0][i]
                        else:
                            inv[i] = n * c[0][i]
                        s += "You made " + str(n * c[0][i]) + "x " + i + "!\n"
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
        return
    
    if s:
        await message.channel.send(s)

    if len(got) > 0:
        sav = True
        s = ""
        for i in got:
            s += bold(name) + " got " + str(got[i]) + " x **" + i + "**!\n"
            if i in inv:
                inv[i] += got[i]
            else:
                if i.lower() == "xp":
                    p[2] += got[i]
                    await check_level(c, str(user.id))
                else:
                    inv[i] = got[i]
        await message.channel.send(s)
    
    if sav:
        save()


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
    item.append(item[1] * data.items[item[2]][1])
    if name in data.loot:
        t = data.loot[name]
        percent = 100.00
        for i in t:
            chance = percent / t[i]
            percent *= (1 - 1 / t[i])
            if i == j:
                item.append(int(200 / chance))
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

def move(x,y,z, pos, world):
    p = pos
    pos[0] += x
    pos[1] += y
    pos[2] += z
    if get_coord_str(pos) in world:
        if data.things[world[get_coord_str(pos)]][0] == 1:
            pos = p
            return world[get_coord_str(pos)]
    return ""


# adds stuff to everybody's world

def world_add(pos, things):
    for user in saves:
        world = saves[user][9]
        world[pos] = things
    save()


# /recipes

def recipes():
    s = underline("List of all recipes") + "\n\n```"
    c = data.crafts
    num = 0
    for i in c:
        num += 1
        s += str(num) + ". " + i + "\n"
    s += "```"
    return s

def recipe(r):
    if r in data.crafts:
        s = underline("How to " + r) + "\n\n**Uses**:\n"
        c = data.crafts[r]
        for i in c[1]:
            s += str(c[1][i]) + "x " + i + "\n"
        s += "\n**Makes**:\n"
        for i in c[0]:
            s += str(c[0][i]) + "x " + i + "\n"
        return s
    else:
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
        if command == "hunt" or command == "hu":
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
        if command == "pickup" or command == "take":
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