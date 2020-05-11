import random

types = [str, str, int, int, eval, eval, eval, int, eval, eval, eval, eval, eval]
""" name[0], status[1], xp[2], level[3], cooldowns[4], items[5], position[6] ([x,y,z]), world#[7], unlocks[8], world[9], achievements[10], map[11], combat[12] """

items = {
    "coins": [1, "currency", 1],
    "sand": [10, "sand", 10],
    "sand grain": [50, "sand", 55],
    "large sand grain": [1000, "sand", 1150],
    "huge sand grain": [15000, "sand", 17500],
    "enormous sand grain": [300000, "sand", 360000],
    "gigantic sand grain": [1500000, "sand", 2000000],
    "sandfly": [250, "animals", 250],
    "biting sandfly": [2000, "animals", 2500],
    "starfish": [5000, "animals", 10000],
    "wood": [20, "wood", 20],
    "twig": [100, "wood", 110],
    "branch": [1000, "wood", 1250],
    "shell": [1000, "shell", 2000],
    "good shell": [10000, "shell", 20000],
    "tutorial shell": [1500, "shell", 1500],
    "equipment bag": [1000, "combat", 1000],
    "sandfly wing": [2000, "combat", 2000],
    "biting sandfly wing": [7000, "combat", 7000],
    "wooden shield": [10000, "combat", 10000],
    "sandfly shield": [25000, "combat", 25000],
    "twig knife": [1200, "combat", 1200],
    "branch knife": [3200, "combat", 3200],
    "sand dagger": [9500, "combat", 9500],
    "twig sword": [18000, "combat", 30000],
    "common box": [0, "boxes", 200],
    "uncommon box": [0, "boxes", 500],
    "rare box": [0, "boxes", 1500],
    "very rare box": [0, "boxes", 5000],
    "note": [0, "storyline", 0],
    "xp": [0, "XP", 1],
    "level": [0, "Level", 1],
    "cow": [0,"pending"]
}

crafts = {
    "craft sand grain": [
        {"sand grain": 1},
        {"sand": 5}
    ],
    "craft large sand grain": [
        {"large sand grain": 1},           
        {"sand grain": 20}
    ],
    "craft huge sand grain": [
        {"huge sand grain": 1},
        {"large sand grain": 10, "sand grain": 100}
    ],
    "craft enormous sand grain": [
        {"enormous sand grain": 1},
        {"huge sand grain": 10, "large sand grain": 150}
    ],
    "craft twig": [
        {"twig": 1},
        {"wood": 5}
    ],
    "craft branch": [
        {"branch": 1},
        {"twig": 10}
    ],
    "craft uncommon box": [
        {"uncommon box": 1},
        {"common box": 2, "sand": 1}
    ],
    "craft rare box": [
        {"rare box": 1},
        {"uncommon box": 2, "sand": 10}
    ],
    "craft very rare box": [
        {"very rare box": 1},
        {"rare box": 3, "sand": 100}
    ],
    "craft equipment bag": [
        {"equipment bag": 1},
        {"wood": 50, "sand": 100},
        {"common box": 1, "level": 10}
    ],
    "craft sandfly wing": [
        {"sandfly wing": 1},
        {"sandfly": 8},
        {"equipment bag": 1, "level": 15}
    ],
    "craft wooden shield": [
        {"wooden shield": 1},
        {"wood": 500},
        {"equipment bag": 1, "level": 20}
    ],
    "craft sandfly shield": [
        {"sandfly shield": 1},
        {"sandfly": 100},
        {"equipment bag": 1, "level": 25}
    ],
    "craft biting sandfly wing": [
        {"biting sandfly wing": 1, "sand": 100},
        {"sandfly": 12, "biting sandfly": 1, "sandfly wing": 1},
        {"equipment bag": 1, "level": 20}
    ],
    "craft twig knife": [
        {"twig knife": 1},
        {"twig": 12},
        {"equipment bag": 1, "level": 10}
    ],
    "craft branch knife": [
        {"branch knife": 1},
        {"branch": 2, "twig knife": 1},
        {"equipment bag": 1, "level": 15}
    ],
    "craft sand dagger": [
        {"sand dagger": 1},
        {"sand": 650, "wood": 150},
        {"equipment bag": 1, "level": 20}
    ],
    "craft twig sword": [
        {"twig sword": 1},
        {"twig": 150, "branch": 3},
        {"equipment bag": 1, "level": 25}
    ],
    "break sand grain": [
        {"sand": 5},
        {"sand grain": 1}
    ],
    "break large sand grain": [
        {"sand": 100},       
        {"large sand grain": 1}
    ],
    "break huge sand grain": [
        {"sand": 1500},
        {"huge sand grain": 1}
    ],
    "break enormous sand grain": [
        {"sand": 30000},
        {"enormous sand grain": 1}
    ],
    "break twig": [
        {"wood": 5},
        {"twig": 1}
    ],
    "break branch": [
        {"twig": 10},
        {"branch": 1}
    ],
    "break biting sandfly": [
        {"sandfly": 7, "sand": 50},
        {"biting sandfly": 1}
    ],
    "trade wood to sand": [
        {"sand": 2},
        {"wood": 1}
    ],
    "trade sand to wood": [
        {"wood": 1},
        {"sand": 2}
    ],
    "trade twig to sand": [
        {"sand": 10},
        {"twig": 1}
    ],
    "trade sand to twig": [
        {"twig": 1},
        {"sand": 10}
    ],
    "trade sandfly to sand": [
        {"sand": 25},
        {"sandfly": 1}
    ],
    "trade sand to sandfly": [
        {"sandfly": 1},
        {"sand": 25}
    ],
    "trade shell to sand": [
        {"sand": 100},
        {"shell": 1}
    ],
    "trade tutorial shell to sand": [
        {"sand": 100},
        {"tutorial shell": 1}
    ],
}

equipment = { # +[atk, def, health]
    "sandfly wing": [0, 1, 0],
    "biting sandfly wing": [0, 5, 0],
    "wooden shield": [0, 6, 0],
    "sandfly shield": [0, 16, 0],
    "twig knife": [1, 0, 0],
    "branch knife": [3, 0, 0],
    "sand dagger": [10, 0, 0],
    "twig sword": [20, 0, 0],
}

hits = {
    "nothing": {"damage": 0},
    "basic": {"damage": 1},
    "basic poison": {"poison damage": 1},
    "basic lightning": {"lightning damage": 1},
    "basic stun": {"stun": 0},
    "basic stun hit": {"stun damage": 1},
    "basic heal": {"heal": 0.1},
    "full heal": {"heal": 1},
    "ant hit": {"damage": 1},
    "ant sting": {"poison damage": 1}
}

abilities = {
    "nothing": {
        "hits": [["nothing", 100, 1]],
        "number": 1000
    },
    "stunned": {
        "hits": [["nothing", 100, 1]],
        "number": 1000
    },
    "hit": {
        "hits": [["basic", 100, 1]],
        "number": 1000
    },
    "bite": {
        "hits": [["basic", 70, 2]],
        "number": 1000
    },
    "baby ant hit": {
        "hits": [["basic", 25, 1]],
        "number": 1000
    },
    "ant hit": {
        "hits": [["basic", 50, 1]],
        "number": 1000
    },
}

enemies = {
    # name: [attack, defense, health, abilities]
    "baby ant": {"attack": 1, "defense": 1, "health": 5, "abilities": ["baby ant hit"]},
    "ant": {"attack": 1, "defense": 1, "health": 10, "abilities": ["ant hit"]},
}

worlds = ["beach hole", "beach", "cave", "forest", "sea"]

place_names = {
    "(0, 0, 0)": "The starting point.",
    "(0, 1, 0)": "The beach, just north of your starting point.",
    "(0, -1, 0)": "Most of your stuff was located here at first.",
    "(-1, 0, 0)": "The beach, just west of your starting point.",
    "(1, 0, 0)": "The beach, just east of your starting point.",
    "(-1, -1, 0)": "The beach. A few pieces of dirt lie here and there.",
    "(-1, -2, 0)": "The beach. The word `cave` is written on the sand along with a northward pointing arrow.",
    "(1, 1, 0)": "The beach. The sand is slightly lighter-coloured here.",
    "(0, 2, 0)": "The beach. Yes, the beach.",
    "(-2, -1, 0)": "The beach. Quite a lot of pieces of dirt is scattered around."
}

maps = {
    "(0, 0, 0)": "beach",
    "(0, 1, 0)": "beach",
    "(0, -1, 0)": "beach",
    "(-1, 0, 0)": "beach",
    "(1, 0, 0)": "beach",
    "(-1, -1, 0)": "beach2",
    "(-1, -2, 0)": "beach",
    "(1, 1, 0)": "beach2",
    "(0, 2, 0)": "beach",
    "(-2, -1, 0)": "beach2",
    "(-1, -3, 0)": "sandwall",
    "(-2, -2, 0)": "sandwall",
    "(0, -2, 0)": "sandwall",
    "(-3, -1, 0)": "sandwall",
    "(1, -1, 0)": "sandwall",
    "(-2, 0, 0)": "sandwall",
    "(2, 0, 0)": "sandwall",
    "(-1, 1, 0)": "sandwall",
    "(2, 1, 0)": "sandwall",
    "(-1, 2, 0)": "sandwall",
    "(1, 2, 0)": "sandwall",
    "(-1, 3, 0)": "sandwall",
    "(0, 3, 0)": "sandwall",
    "(1, 3, 0)": "sandwall",
}

cd = {
    "look": 60,
    "walk": 120,
    "hunt": 300,
    "fight": 600,
    "heal": 150,
    "move": 10,
    "sleep": 21600,
    "daily": 86400,
    "weekly": 604800
}

unlock = {}

# things: name: blocking? takeable? display?

things = {
    "door": [1,0,"A door lies here."],
    "brick wall": [1,0,"A brick wall stands firmly to the ground."],
    "seed": [0,1,"A seed is growing here."],
    "sapling": [0,0,"A sapling is growing here."],
    "young tree": [1,0,"A young tree grows here."],
    "tree": [1,0,"A tree."],
    "sand wall": [1,0,"A sand wall is fixed to the ground."],
    "strong sand wall": [1,0,"A strong sand wall is firmly fixed into the ground."],
    "note": [0,1,"A note lies here."],
    "bed": [0,0,"A bed _lies_ here. You get more XP from `.sleep` when you are here!"],
    "sandcastle": [0,1,"A nice decorated sandcastle stands in front of you."]
}

loot = {
    "beach look": {
        "1x large sand grain|WOW! A LARGE SAND GRAIN!": 400,
        "1x shell|A SHELL IS SPOTTED!": 300,
        "3x sandfly|You saw **3** sandflies on the beach. Why not just take _all_ of them, you thought.": 250,
        "2x sandfly|You saw **2** sandflies on the beach. Why not just take _both_ of them, you thought.": 120,
        "5x sand grain|One look at the beach and 5 sand grains popped out. Wow!": 50,
        "1x sandfly|You saw a sandfly on the beach. Why not just take it, you thought.": 50,
        "20x sand|You looked around and found **20** sand!": 40,
        "3x sand grain|You looked around and found 3 sand **grains** lying right in front of you.": 25,
        "2x sand grain|You looked around and spotted 2 sand **grains**!": 15,
        "1x sand|You looked around again and a teeny grain of sand caught your attention. Apparently it was to distract you, because...": 20,
        "8x sand|You looked around and spotted **8** sand!": 9,
        "7x sand|You looked around and spotted **7** sand!": 7,
        "1x sand grain|You looked around and spotted a sand grain!": 6,
        "5x sand|You looked around and spotted 5 sand on the beach.": 5,
        "4x sand|You looked around and spotted 4 sand.": 3,
        "3x sand|You looked around and spotted 3 sand.": 2,
        "2x sand|You looked around and spotted just 2 sand.": 1
    },
    "beach walk": {
        "2x branch|NICE! Walking around, both your feet caught on 2 BRANCHES and you tripped!": 500,
        "2x shell|NICE! Your foot caught on two shells!": 200,
        "1x large sand grain|WOW! A LARGE SAND GRAIN!": 200,
        "1x branch|Walking around, your foot caught on a BRANCH and you tripped! WOW!": 150,
        "1x shell|Walking around, your foot caught on a SHELL! WOW!": 100,
        "3x twig|Walking around, you found **3** twigs on the beach!": 30,
        "2x twig|Walking around, both your feet caught on 2 twigs.": 15,
        "1x twig|Walking around, your foot caught on a twig.": 4,
        "7x sand|Walking around, you found nothing much but some sand.": 4,
        "5x sand|Walking around, you found nothing much but some sand.": 3,
        "1x sand grain|Walking around, you found a sand grain.": 5,
        "4x sand|Walking around, you found nothing much but some sand.": 2,
        "1x twig|Walking around, you found a twig.": 1
    },
    "beach hunt": {
        "1x starfish|RARE!!! You found a _rare_ starfish lying on the beach near the sea.": 500,
        "10x sandfly|NICE!!! You found a sandfly colony and hunted down **all** the sandflies!": 200,
        "3x shell|You didn't hunt anything, but you found **3** SHELLS on the way!": 150,
        "7x sandfly|Wow! You found a sandfly colony but only managed to hunt down 7 sandflies.": 120,
        "6x sandfly|Wow! You found a sandfly colony but only managed to hunt down 6 sandflies.": 100,
        "2x shell|You didn't hunt anything, but you found TWO SHELLS on the way!": 100,
        "2x biting sandfly|Wow! You found TWO BITING sandflies!": 80,
        "5x sandfly|Wow! You found a sandfly colony but only managed to hunt down 5 sandflies.": 75,
        "1x large sand grain|WOW! A LARGE SAND GRAIN!": 50,
        "1x shell|You didn't hunt anything, but you found a SHELL on the way!": 50,
        "1x branch|You didn't hunt anything, but you saw a branch on the way, wondering where it came from.": 50,
        "3x sandfly|You found **3** sandflies flying around!": 25,
        "1x biting sandfly|You found a sandfly! It was BITING you!": 20,
        "1x twig|You didn't hunt anything, but you saw a twig on the way, wondering where it came from.": 15,
        "10x sand grain|You didn't hunt anything, but you saw 10 nice sand grains on the way.": 10,
        "2x sandfly|You found **2** sandflies!": 8,
        "5x sand grain|You didn't hunt anything, but you saw 5 sand grains on the way.": 4,
        "10x sand|You didn't hunt anything, but you saw 10 sand on the way.": 2,
        "1x sandfly|You found a sandfly!": 1
    },
    "beach fight": {
        "1x baby ant|A baby ant crawls towards you as if it wants to eat you.": 2,
        "1x ant|An ant approaches you on all 6 legs.": 1,
    },
    "beach box": {
        "1x very rare box|A **VERY RARE** box crashed through the clouds onto the sand...": 1200,
        "1x rare box|A RARE box dropped from the sky...": 250,
        "1x uncommon box|An uncommon box dropped from the sky...": 100,
        "1x common box|A common box dropped from the sky...": 30,
        "0x common box|": 1
    },
    "beach common box": {
        "1x shell|": 150,
        "1x large sand grain|": 100,
        "1x branch|": 90,
        "1x sandfly|": 20,
        "1x twig|": 9,
        "1x sand grain|": 3,
        "1x sand|": 1
    },
    "beach uncommon box": {
        "1x biting sandfly|": 150,
        "1x shell|": 70,
        "1x large sand grain|": 50,
        "1x branch|": 40,
        "1x sandfly|": 10,
        "1x twig|": 3,
        "1x sand grain|": 2,
        "1x sand|": 1
    },
    "beach rare box": {
        "1x huge sand grain|": 300,
        "1x biting sandfly|": 50,
        "1x shell|": 30,
        "1x large sand grain|": 20,
        "1x branch|": 15,
        "1x sandfly|": 5,
        "1x twig|": 2,
        "1x sand grain|": 2,
        "1x sand|": 1
    },
    "beach very rare box": {
        "1x starfish|": 250,
        "1x huge sand grain|": 100,
        "1x biting sandfly|": 15,
        "1x shell|": 10,
        "1x large sand grain|": 6,
        "1x branch|": 5,
        "1x sandfly|": 2,
        "1x twig|": 2,
        "1x sand grain|": 2,
    }
}

lootboxes = {
    "common box": [5],
    "uncommon box": [10],
    "rare box": [15],
    "very rare box": [20]
}

achievements = {
    "Finish the tutorial": ["tutorial shell",1,"Tutorial Finisher"],
    "Get sand": ["sand",1,"Sand!"],
    "Get 10 sand": ["sand",10,"More sand!"],
    "Get 100 sand": ["sand",100,"SAND!"],
    "Get 1000 sand": ["sand",1000,"A Large Sand Pile"],
    "Get 10K sand": ["sand",10000,"It's raining sand over here!"],
    "Get a sand grain": ["sand grain",1,"Sand!!!"],
    "Get 10 sand grains": ["sand grain",10,"Sand Grain!"],
    "Get a large sand grain": ["large sand grain",1,"LARGE sand!"],
    "Get a HUGE sand grain": ["huge sand grain",1,"HUGE sand grain!"],
    "Get 5 huge sand grains": ["huge sand grain",5,"MANY huge sand grains!"],
    "Get 10 huge sand grains": ["huge sand grain",10,"10 HUGE sand grains!"],
    "Get a twig": ["twig",1,"Twig!"],
    "Get 30 twigs": ["twig",30,"Crack goes the twig!"],
    "Get 500 twigs": ["twig",500,"Twig collector!"],
    "Get 2 branches": ["branch",2,"Branch!"],
    "Get 40 branches": ["branch",40,"Branch collector!"],
    "Get 250 branches": ["branch",250,"B R A N C H"],
    "Catch 1 sandfly": ["sandfly",1,"Sandflier"],
    "Catch 10 sandflies": ["sandfly",10,"Don't fly away!"],
    "Catch 100 sandflies": ["sandfly",100,"You can't fly away!"],
    "Catch 1 biting sandfly": ["biting sandfly",1,"Bite!"],
    "Catch 10 biting sandflies": ["biting sandfly",10,"Don't bite me!"],
    "Get a shell": ["shell",1,"Shell!"],
    "Get 5 shells": ["shell",5,"SHELL!"],
    "Get a common box": ["common box",1,"Box!"],
    "Get an uncommon box": ["uncommon box",1,"Boxx!"],
    "Get a rare box": ["rare box",1,"Boxxx!"],
    "Get an very rare box": ["very rare box",1,"BOX!"],
}

notes = {
    1: """
    ```Welcome to the Island Hunt! Collect resources and survive on the Island!
    Wait something's not right with the island... let me find out...```

    The note was typewrited, and torn off after the last three dots...
    """,
    2: """
    ```Just a note:
    Anybody who reads this, please do NOT go into the deep hole in the beach, there is no way out.
    I repeat: do NOT go into the deep hole east of here."""
}

island_picture = "https://i.ibb.co/8m8fxsm/island.png"

server_ids = [705736619457642567, 705737067732140034, 706097681977835582]

emojis = {}

# classes

class Enemy:
    def __init__(self, name, **kwargs):
        self.name = name
        self.stats = {}
        self.stats = enemies[name]
        self.abilities = enemies[name]["abilities"]
        self.effects = {
            "health": self.stats["health"],
            "poison": 0,
            "combat": 1,
            "stunned": 0,
            "dead": 0,
        }
        self.ability_nums = {}
        for i in self.abilities:
            self.ability_nums[i] = abilities[i]["number"]

        # keyword modifiers

        for i,j in kwargs:
            if i in self.stats:
                if i == "abilities":
                    self.abilities[i].extend(j)
                    self.stats["abilities"].extend(j)
                else:
                    self.stats[i] *= j
    
    # just some getter functions
    
    def attack(self):
        return self.stats["attack"]
    def defense(self):
        return self.stats["defense"]
    def max_health(self):
        return self.stats["health"]
    def health(self):
        return self.effects["health"]
    def poison(self):
        return self.effects["poison"]
    def effect(self, eff):
        return self.effects[eff]
    def die(self):
        if self.health() <= 0:
            self.effects["dead"] = 1
            return True
        else:
            self.effects["dead"] = 0
            return False
    
    def do_poison(self):
        if self.poison() > 0:
            self.effects["health"] -= self.effects["poison"]
            self.effects["poison"] //= 2
            return True
        else:
            return False
    
    def remove_stun(self):
        if self.effects["stunned"] > 0:
            self.effects["stunned"] -= 1
    
    def use_ability(self, ability):
        self.ability_nums[ability] -= 1
    
    def check_ability(self, ability):
        return self.ability_nums[ability] > 0
    
    def heal(self, ability):
        if ability:
            a = abilities[ability]
            for i in a:
                if random.randint(1, 100) <= i[1]:
                    heal_name = i[0]
                    heal_mult = i[2]
                    break
            h = hits[heal_name]
            for i in h:
                if "heal" in h:
                    heal = h[i] * heal_mult * self.max_health()
                    if "poison" in h:
                        self.effects["poison"] -= heal
                    else:
                        self.effects["health"] += heal
    
    def hit(self, ability, opponent):
        if ability:
            a = abilities[ability]
            for i in a:
                if random.randint(1, 100) <= i[1]:
                    hit_name = i[0]
                    hit_mult = i[2]
                    break
            h = hits[hit_name]
            for i in h:
                if "damage" in h:
                    damage = h[i] * hit_mult * opponent.damage()
                    if "lightning" not in h:
                        damage -= self.stats["defense"]
                    if damage < 0:
                        damage = 0
                    if "poison" in h:
                        self.effects["poison"] += damage
                    else:
                        self.effects["health"] -= damage
    
    def turn(self, ability, opponent):
        self.hit(self, ability, opponent)
        self.do_poison()
        
        if self.die():
            return ""
        else:
            a = []
            for i in self.abilities:
                if self.check_ability(i):
                    a.append(i)
            if a:
                if self.effects["stunned"] > 0:
                    return "stunned"
                else:
                    a = a[random.randint(0, len(a) - 1)]
                    self.use_ability(a)
                    return a[random.randint(0, len(a) - 1)]
            else:
                return "nothing"

class You(Enemy):

    # overriding

    def __init__(self, combat):
        self.stats = combat
        self.abilities = combat["abilities"]
        self.effects = {
            "health": self.stats["health"],
            "poison": 0,
            "combat": 1,
            "stunned": 0,
            "dead": 0,
        }
        self.ability_nums = {}
        for i in self.abilities:
            self.ability_nums[i] = abilities[i]["number"]
    
    # more overriding
    
    def turn(self, ability, opponent):
        self.hit(self, ability, opponent)
        if self.die():
            return "lose"
        else:
            if ability:
                return "next"
            else:
                return "win"



# functions

def load():
    file = open("progress.txt","r")
    lines = file.read().split("\n")
    saves = {}
    for line in lines:
        line = line.split("|")
        saves[line[0]] = [types[i](line[i + 1]) for i in range(len(line) - 1)]
    file.close()
    return saves

def save(saves):
    open('progress.txt', 'w').close()
    file = open("progress.txt","w")
    for i in saves:
        if i:
            file.write(str(i) + "|" + "|".join([str(x) for x in saves[i]]) + "\n")
    file.close()

def new_cooldowns():
    cds = {}
    for i in cd:
        cds[i] = 0
    return cds

def new_unlocks():
    unlock = ["tutorial","storyline","research","flying","digging"]
    unlocks = {}
    for i in unlock:
        unlocks[i] = 0
    return unlocks

def new_world():
    return load()["000000000000000000"][9]

def new_achievements():
    ac = {}
    for i in achievements:
        ac[i] = 0
    return ac

def new_map():
    return {"(0, 0, 0)": 1}

def new_combat():
    return {}

def init_combat():
    return {
        "init": 1,
        "attack": 0,
        "defence": 0,
        "health": 20,
        "abilities": {"hit": 1},
        "kills": 0,
        "deaths": 0,
        "animals": {},
        "effects": {
            "health": 20,
            "poison": 0,
            "combat": 0,
            "stunned": 0,
            "dead": 0,
        },
    }

def get_emojis(servers):
    global emojis
    for server in servers:
        e = server.emojis
        for i in e:
            emojis[i.name] = str(i)
    return emojis

def tutorial_text(num):
    if num == 0:
        s = "Welcome to Island Hunt!\n\nThis is the start of the Island Hunt tutorial.\n"
        s += "You realise you were on an island one day with no one in sight. Could you survive on the island?\n"
        s += "Type `.look` to look around you to see where you are first, then `.walk` to walk around!"
        return s
    if num == 1:
        return "You looked around, seeing a great expanse of sand to your north and south with the sea to the west. This is definitely the beach, you thought."
    if num == 2:
        return "You walked around and saw a weird wooden signboard firmly stuck to the sand: _hunt_. Use the `.hunt` command to hunt."
    if num == 3:
        return "You walked around, thinking of what you should catch. No moving creature in sight. Your eyes scanned the ground...\n\nYou spotted a sandfly lying stationary on the sand near your legs."
    if num == 4:
        s = "You looked around and saw some large good-quality particles of sand below you. You picked it up and put it into your backpack, which was lying on the sand just a few metres south of you.\n"
        s += "Nice! You just got a few items! Try typing `.inventory` or `.i` to check the items that you have."
        return s
    if num == 5:
        return "**Your** inventory\n\n`sandfly`: 1\n`sand`: 3\n\nUse the `.walk` command to walk again! It might _give_ you something!"
    if num == 6:
        s = "You walked around and saw a note lying on the sand to the west.\n"
        s += "Use `.move west` to move to the west and `.pickup` to pickup the note!"
        return s
    if num == 7:
        return "You move 10 metres **west**."
    if num == 8:
        return "You reached to the ground and picked up a **note**!"
    if num == 9:
        return "Coordinates: (-1, 0, 0)\n\n" + place_names["(-1, 0, 0)"] + "\n\nYou're done with the tutorial! Type `.help` to know more and find out more commands!"

def tutorial_help(num):
    if num == 0:
        return "Check the tutorial by doing `.tutorial`!"
    if num == 1:
        return "You do not know where you are, so you must look around! Use the `.look` command to look around."
    if num == 2:
        return "You looked around, seeing sand and more sand. Where could you go? Use the `.walk` command to walk."
    if num == 3:
        return "Looking at the wooden signboard, you realised you must `.hunt`."
    if num == 4:
        return "You felt like looking around a bit. Use the `.look` command to look around!"
    if num == 5:
        return "Have you checked your items yet? Use `.inventory` or `.i` to check your items!"
    if num == 6:
        return "Use the `.walk` command to walk, it might be useful!"
    if num == 7:
        return "Use `.move west` or `.move w` to move to the west!"
    if num == 8:
        return "Use the `.take` or `.pickup` function to pick up the note!"
    if num == 9:
        return "Check where you are by typing `.place`!"