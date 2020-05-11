import data, webserver, discord, datetime, asyncio, random, importlib, os

client = discord.Client(activity=discord.Game(name="Island Hunt"))

# game data
types = data.types
""" name[0], status[1], xp[2], level[3], cooldowns[4], items[5], position[6] ([x,y,z]), world#[7], unlocks[8], world[9], achievements[10], map[11], combat[12] """

# retrieve data
saves = data.load()
help_text = open("help.txt","r").read()
version_text = open("versions.txt","r").read()
servers = []
emojis = {}
help_words = {}
help_alias = {}
enemies = {}

# functions

def emoji(name):
    name = name.replace(" ", "")
    if name in data.emojis:
        return data.emojis[name]
    else:
        return data.emojis["blank"]

def new_profile(user):
    if user.id in saves:
        return []
    else:
        return [user.name, "No status", 0, 0, data.new_cooldowns(), {}, [0,0,0], 1, data.new_unlocks(), data.new_world(), data.new_achievements(), data.new_map(), {}]
        
def profile(user):
    if str(user.id) in saves:
        return saves[str(user.id)]
    else:
        saves[str(user.id)] = new_profile(user)
        save()
        return saves[str(user.id)]

def help_str(s):
    if s in help_words:
        return help_words[s]
    else:
        return ""
    
def load_help():
    global help_words
    help_words = {}
    help_file = open("keywords.txt").read().split("### ")[1:]
    for i in help_file:
        i = i.split("\n", 1)
        i[0] = i[0].split("/")
        help_words[i[0][0]] = i[1].strip()
        for j in i[0]:
            help_alias[j] = i[0][0]

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

def get_attack(inv):
    attack = 1
    for i in inv:
        if i in data.equipment:
            attack += data.equipment[i][0] * inv[i]
    return attack

def get_defense(inv):
    defense = 0
    for i in inv:
        if i in data.equipment:
            defense += data.equipment[i][1] * inv[i]
    return defense

def get_health(inv):
    health = 0
    for i in inv:
        if i in data.equipment:
            health += data.equipment[i][2] * inv[i]
    return health

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

def embed(title, desc, color, fields, footer, thumbnail, name, picture):
    embed=discord.Embed(title=title, description=desc, color=color)
    embed.set_author(name=name, icon_url=picture)
    embed.set_thumbnail(url=thumbnail)
    for i in fields:
        embed.add_field(name=i[0], value=i[1], inline=i[2])
    embed.set_footer(text=footer)
    return embed


# /ready

@client.event
async def on_ready():
    global emojis
    for i in data.server_ids:
        servers.append(client.get_guild(i))
    emojis = data.get_emojis(servers)
    load_help()
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
    global saves, data, help_text, version_text, emojis

    # ignore if sent by bot
    if message.author == client.user:
        return
    
    s = ""
    sav = False
    disp_fight = False
    
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
        combat = p[12]

        combat_ = "init" in combat

        is_embed = False
        fields = []
        embed_title = ""
        embed_desc = ""
        embed_color = 0xffa51f
        embed_footer = ""
        embed_thumb = ""
        embed_name = "Island Hunt"
        embed_picture = "https://i.ibb.co/8m8fxsm/island.png"
        
        ##### command handling

        # combat

        if combat_:
            fight_ = combat["effects"]["combat"] > 0
            if fight_:
                sav = True
                enemy = combat["effects"]["enemy"]
                you = data.You(combat)
                abilities = combat["abilities"]
                m = " ".join(m)
                ability = ""
                if m in abilities:
                    ability = m
                else:
                    try:
                        m = int(m)
                        ability = abilities[m - 1]
                    except:
                        ability = ""
                        s = "You have no such ability!"
                if ability:
                    disp_fight = True
                    if you.check_ability(ability):
                        you.heal(ability)
                        a = enemy.turn(ability, you)
                        enemy.heal(a)
                        result = you.turn(a, enemy)
                        if result == "win":
                            s = "You won!"
                        elif result == "lose":
                            s = "You died!"
                        else:
                            s = ""
                    else:
                        s = "You have run out of uses for this ability!"
        else:
            fight_ = False

        # check if it's me
        
        if str(message.author.id) == ids["mei"] or str(message.author.id) == ids["dev"]:
            if command == "reload":
                importlib.reload(data)
                emojis = data.get_emojis(servers)
                saves = data.load()
                load_help()
                help_text = open("help.txt","r").read()
                version_text = open("versions.txt","r").read()
                s = "Successfully reloaded!"

        if str(message.author.id) == ids["dev"]:
            
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
        
        elif command == "help" or command == "hl":
            if len(m) == 1:
                is_embed = True
                embed_title = "HELP"
                embed_desc = ""
                embed_footer = "made by .?#7696"
                fields = [["grey text", help_text, True]]
            else:
                m = " ".join(m[1:])
                if m in help_alias:
                    m = help_alias[m]
                    s = help_str(m)
                    if not s:
                        s = "not done! please fill in"
                    is_embed = True
                    embed_title = "HELP"
                    embed_desc = ""
                    embed_footer = "made by .?#7696"
                    fields = [[m, s, False]]
                    if m in data.cd:
                        fields.append(["cooldown", str(data.cd[m]) + " seconds", True])
                    if m in data.items:
                        fields.append(["Type", data.items[m][1], True])
                        fields.append(["Sell Price", str(data.items[m][2]) + " coins", True])
                        fields.append(["XP worth", str(data.items[m][0]), True])
                    s = ""
                else:
                    if m == "keywords":
                        s = "List of help keywords:```"
                        num = 0
                        for i in help_alias:
                            if i == help_alias[i]:
                                num += 1
                                s += "\n" + str(num) + ". " + i
                            else:
                                s += "/" + i
                        s += "\n```"
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
            is_embed = True
            v = version_text.split("###")
            for i in range(1,len(v)):
                i = v[i].split("|")
                fields.append([i[0],i[1],True])

        elif command == "recipes" or command == "r":
            if len(m) == 1:
                s = recipes()
            else:
                s = recipe(" ".join(m[1:]).strip())
                if s == "":
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
            is_embed = True
            embed_thumb = user.avatar_url
            embed_picture = user.avatar_url
            embed_name = name + "'s cooldowns"
            s = ""
            for i in cd:
                if combat_ or i not in ["fight", "heal"]:
                    if get_cd(user, i) > data.cd[i]:
                        s += tick() + " - " + mono(i) + "\n"
                    else:
                        s += clock() + " - " + mono(i) + ": " + wait_for(data.cd[i] - get_cd(user, i))[9:-6] + "\n"
            fields = [["Cooldowns", s, True]]
            s = ""

        # ready

        elif command == "ready" or command == "rd":
            if message.mentions:
                for member in message.mentions:
                    if str(member.id) in saves:
                        cd = saves[str(member.id)][4]
                        name = saves[str(member.id)][0]
                        user = member
                        break
            is_embed = True
            embed_thumb = user.avatar_url
            embed_picture = user.avatar_url
            embed_name = name + "'s ready"
            for i in cd:
                if get_cd(user, i) > data.cd[i]:
                    s += tick() + " - " + mono(i) + "\n"
            fields = [["Ready", s, True]]
            s = ""

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
                        user = member
                        break
            is_embed = True
            embed_thumb = user.avatar_url
            embed_picture = user.avatar_url
            embed_name = name + "'s inventory"
            t = ""
            adding = False
            for i in data.items.keys():
                if data.items[i][1] != t:
                    if adding:
                        fields.append([t, s, True])
                        s = ""
                    t = data.items[i][1]
                    adding = False
                if i in inv:
                    if inv[i] > 0:
                        s += "\n" + emoji(i) + " " + bold(i) + ": " + str(inv[i])
                        adding = True
            s = ""

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
            is_embed = True
            embed_thumb = user.avatar_url
            embed_picture = user.avatar_url
            embed_name = name + "'s profile"
            embed_title = title
            current_xp = xp - get_xp(level - 1)
            target_xp = get_xp(level) - get_xp(level - 1)
            fields = [["Level", str(level) + " (" + str(int(10000 * current_xp / target_xp) / 100) + "%)", True], ["XP", str(current_xp) + "/" + str(target_xp), True]]

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
            is_embed = True
            embed_name = name + "'s place"
            embed_thumb = user.avatar_url
            embed_picture = user.avatar_url
            pl = get_place(user_id, pos)
            embed_title = pl[0]
            if pl[1]:
                fields.append(["Description", pl[1], True])
            if pl[2]:
                fields.append(["Things", pl[2], True])
        
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
            s = bold(name + "'s map") + emoji("here") + " - You are here"
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
            is_embed = True
            s = emoji("compass")
            embed_desc = "compass"
            embed_thumb = "https://pxt.azureedge.net/blob/d3e34ce80d0f558d6dda199a5c33f9770ab93d2f/static/mb/projects/a5-compass.png"

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
            s = bold(name + "'s achievements") + "\n\n"
            num = 0
            completed = 0
            total = len(a.keys())
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
                    completed += 1
                    s += "\n" + tick() + " - " + i + " " + emoji(a[i][0]) + " - Title: " + mono(a[i][2]) + "(#" + str(num) + ")"
                    if title == a[i][2]:
                        s += " [current title]"
                else:
                    s += "\n" + cross() + " - " + i + " " + emoji(a[i][0]) + " - Title: " + mono(a[i][2]) + "(#" + str(num) + ")"
            s += "\n\nCompleted " + str(completed) + " out of " + str(total) + " achievements"

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


        # abilities

        elif command == "ability" or command == "abilities" or command == "ab":
            if combat_:
                sav = True
                disp_fight = False
                a = combat["abilities"]
                is_embed = True
                embed_thumb = user.avatar_url
                embed_picture = user.avatar_url
                embed_name = name + "'s abilities"
                embed_title = ""
                embed_desc = "Number of abilities: " + str(len(a))
                fields = []
                s = ""
                for i in a:
                    s = ""
                    for j in data.abilities[i]["hits"]:
                        h = data.hits[j[0]]
                        s += str(j[1]) + "% chance to do: "
                        for i in h.keys():
                            s += str(j[2] * h[i] * 100) + "% " + i + " "
                        s += "\n"
                    fields.append([i, s, False])
            else:
                s = "Unlock combat to use this function!"

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
                L = loot_box(data.worlds[world_num])
                if len(L) > 0:
                    got[L[2]] = L[1]
                    s += "\n\n" + L[0]
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
                L = loot_box(data.worlds[world_num])
                if len(L) > 0:
                    got[L[2]] = L[1]
                    s += "\n\n" + L[0]
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
                L = loot_box(data.worlds[world_num])
                if len(L):
                    got[L[2]] = L[1]
                    s += "\n\n" + L[0]
            else:
                s += wait_for(data.cd["hunt"] - get_cd(user, "hunt"))

        # fight

        elif command == "fight" or command == "f":
            if combat_:
                sav = True
                health = combat["health"]
                effects = combat["effects"]
                L = loot(data.worlds[world_num] + " fight")
                s = L[0]
                enemy = data.Enemy(L[2])
                if enemy.name in combat["enemies"]:
                    combat["enemies"][enemy.name] += 1
                else:
                    combat["enemies"][enemy.name] = 1
                effects["combat"] = True
                effects["enemy"] = enemy
                effects[""]
                disp_fight = True
                s = "NOT DONE YET!"
            else:
                s = "Craft an equipment bag to unlock combat!"
        
        # heal

        elif command == "heal" or command == "he":
            if combat_:
                sav = True
                health = combat["health"]
                effects = combat["effects"]
                if int(effects["health"]) < int(health):
                    if get_cd(user, "heal") > data.cd["heal"]:
                        heal = health * 0.2
                        old = effects["health"]
                        effects["health"] = max(health, effects["health"] + heal)
                        s = "Successfully healed " + str(effects["health"] - old) + " health!"
                    else:
                        s += wait_for(data.cd["heal"] - get_cd(user, "heal"))
                else:
                    s = "You are already at full health!"
            else:
                s = "Craft an equipment bag to unlock combat!"

        # sleep

        elif command == "sleep" or command == "sl":
            sav = True
            if get_coord_str(pos) in world:
                bed = "bed" in world[get_coord_str(pos)]
            else:
                bed = False
            user_id = str(user.id)
            s = bold(name + ": sleep\n")
            if get_cd(user, "sleep") > data.cd["sleep"]:
                set_cd(user, "sleep")
                if bed:
                    s += "You slept comfortably on the bed and felt recharged!\n"
                else:
                    s += "You slept for a while on the sand and felt recharged!\n"
                s += "The cooldowns for look, walk, hunt, and fight are reset!"
                got["coins"] = world_num ** 2 * random.randint(25, 50) * 10
                if bed:
                    got["xp"] = world_num ** 2 * random.randint(75, 125) * 10
                else:
                    got["xp"] = world_num ** 2 * random.randint(50, 100) * 10
                reset_cd(user_id, "look")
                reset_cd(user_id, "walk")
                reset_cd(user_id, "hunt")
                reset_cd(user_id, "fight")
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
                user_id = str(user.id)
                set_cd(user, "weekly")
                got["coins"] = world_num ** 2 * random.randint(200, 500) * 10
                got["xp"] = world_num ** 2 * random.randint(150, 300) * 10
                s += "All your cooldowns except daily are reset!"
                reset_cd(user_id, "look")
                reset_cd(user_id, "walk")
                reset_cd(user_id, "hunt")
                reset_cd(user_id, "fight")
                reset_cd(user_id, "sleep")
            else:
                s += wait_for(data.cd["weekly"] - get_cd(user, "weekly"))

        # move
        
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
                        is_embed = True
                        embed_name = name + "'s place"
                        embed_thumb = user.avatar_url
                        embed_picture = user.avatar_url
                        pl = get_place(str(user.id), pos)
                        embed_title = pl[0]
                        fields = [["Description", pl[1], True], ["Things", pl[2], True]]
                else:
                    s += "You need to specify in which direction you need to move, for example, `.move north`"
            else:
                s += wait_for(data.cd["move"] - get_cd(user, "move"))

        # pickup

        elif command in ["pickup","take","pk","tk"]:
            s = bold(name)
            if len(m) == 1:
                pos = get_coord_str(pos)
                s += "NOT WORKING YET"
            else:
                s += "NOT WORKING YET"


        # open

        elif command == "open" or command == "o":
            boxes = []
            box = ""
            num = 0
            m = m[1:]
            for i in inv:
                if data.items[i][1] == "boxes" and inv[i] > 0:
                    boxes.append([i, inv[i]])
            if len(boxes) == 0:
                s = "You have no boxes in your inventory!"
            elif len(boxes) == 1:
                box = boxes[0][0]
                num = 1
            elif len(m) > 0:
                rarities = [x[0] for x in boxes]
                try:
                    n = int(m[:-1])
                    if len(m) == 1:
                        box = rarities[n - 1]
                        num = 1
                    else:
                        num = n
                        try:
                            r = int(m[:-1])
                            box = rarities[r - 1]
                        except:
                            if " ".join(m[:-1]) + " box" in rarities:
                                box = " ".join(m[:-1]) + " box"
                except:
                    if " ".join(m) + " box" in rarities:
                        box = " ".join(m) + " box"
                        num = 1
                    elif " ".join(m[:-1]) + " box" in rarities:
                        box = " ".join(m) + " box"
                        try:
                            num = int(m[:-1])
                        except:
                            num = 1
                if box == "":
                    s = "Please enter a valid number or rarity!"
            else:
                s = "You have more than one type of box to open in your inventory! Please state the rarity or number of the box that you want to open."
            if box and not s:
                for i in boxes:
                    if i[0] == box:
                        if i[1] < num:
                            num = i[1]
                        inv[i[0]] -= num
                        break
                s = bold(name) + " opened " + str(num) + " " + box + "es" * int(num != 1) + "..."
                for n in range(num):
                    for x in range(data.lootboxes[box][0]):
                        L = loot(data.worlds[world_num] + " " + box)
                        if L[2] in got:
                            got[L[2]] += L[1]
                        else:
                            got[L[2]] = L[1]

        # craft

        if command in ["craft", "cr", "break", "br", "trade", "tr", "buy", "bu", "make", "mk"]:
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
                if command == "cr":
                    m[0] = "craft"
                if command == "br":
                    m[0] = "break"
                if command == "tr":
                    m[0] = "trade"
                if command == "bu":
                    m[0] = "buy"
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
                    can_make = True
                    if len(c) == 3:
                        if m == "craft equipment bag":
                            combat = data.init_combat()
                        for i in c[2]:
                            if i in inv:
                                if inv[i] < c[2][i]:
                                    can_make = False
                                    break
                            elif i == "level":
                                if level < c[2][i]:
                                    can_make = False
                                    break
                            else:
                                can_make = False
                                break
                    if can_make:
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
                        s = "You don't meet the requirements for the recipe!"
            else:
                s = "That doesn't exist."
        
        if command == "sell" or command == "sl":
            inside = False
            m = " ".join(m[1:])
            n = 0
            sav = True
            for i in data.items:
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
                if m in inv:
                    if n > inv[m]:
                        n = inv[m]
                    price = data.items[m][2] * n
                    inv[m] -= n
                    s += "You sold " + str(n) + " " + emoji(m) + " " + m + " for " + str(price) + " coins!"
                    got["coins"] = price
                else:
                    s = "You don't have that in your inventory!"
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
    
        # display fight

    if disp_fight:
        s = ""
        you = data.You()
        enemy = enemies[str(message.author.id)]
        is_embed = True
        embed_title = "Fight between " + name + " and " + enemy.name
        embed_desc = "Round " + enemy.round
        fields = [["You", y, True], ["Enemy", e, True]]

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
    if is_embed:
        await message.channel.send(embed=embed(embed_title, embed_desc, embed_color, fields, embed_footer, embed_thumb, embed_name, embed_picture))

    # gives stuff (got)
    if len(got) > 0:
        sav = True
        s = ""
        embed_name = name + " got..."
        embed_thumb = user.avatar_url
        embed_picture = user.avatar_url
        fields = []
        t = ""
        level_check = False
        adding = False
        for i in got:
            if data.items[i][1] != t:
                    if adding:
                        fields.append([t, s, True])
                        s = ""
                    t = data.items[i][1]
                    adding = True
            if i in inv:
                s += str(got[i]) + " x " + emoji(i) + " " + bold(i) + "!\n"
                inv[i] += got[i]
            else:
                s += "+" + str(got[i]) + " XP!\n"
                if i.lower() == "xp":
                    p[2] += got[i]
                    level_check = True
                else:
                    s += str(got[i]) + " x " + emoji(i) + " " + bold(i) + "!\n"
                    inv[i] = got[i]
        
        fields.append([t, s, True])
        s = ""
        await message.channel.send(embed=embed(embed_title, embed_desc, embed_color, fields, embed_footer, embed_thumb, embed_name, embed_picture))
        if level_check:
            await check_level(c, str(user.id))
    
    # save
    if sav:
        save()

# place
def get_place(user, pos):
    s = ""
    if get_coord_str(pos) in saves[user][9]:
        for i in saves[user][9][get_coord_str(pos)]:
            s += data.things[i][2] + '\n'
    return ["Coordinates: " + get_coord_str(pos), data.place_names[get_coord_str(pos)], s]

# loot
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
    item.extend(item.pop(0).split("x", 1))
    item[1] = int(item[1])
    if item[1] == 0:
        return []
    else:
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

def loot_box(world):
    return loot(world + " box")

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
    if r in data.crafts.keys():
        s = underline("How to " + r) + "\n\n**Uses**:\n"
        c = data.crafts[r]
        for i in c[1]:
            s += str(c[1][i]) + "x " + emoji(i) + " " + i + "\n"
        s += "\n**Makes**:\n"
        for i in c[0]:
            s += str(c[0][i]) + "x " + emoji(i) + " " + i + "\n"
        if len(c) == 3:
            s += "\n**Requires**:\n"
            for i in c[2]:
                s += str(c[2][i]) + "x " + emoji(i) + " " + i + "\n"
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
client.run(os.getenv("SECRET_TOKEN_1"))