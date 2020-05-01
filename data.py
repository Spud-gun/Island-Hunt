types = [str, str, int, int, eval, eval, eval, int, eval, eval]
""" name[0], status[1], xp[2], level[3], cooldowns[4], items[5], position[6] ([x,y,z]), world#[7], unlocks[8], world[9] """

items = {
    "sand": ["sand", 10],
    "sandfly": ["animals", 250],
    "sand grain": ["sand", 50],
    "large sand grain": ["sand", 1000],
    "huge sand grain": ["sand", 15000],
    "enormous sand grain": ["sand", 0],
    "gigantic sand grain": ["sand", 0],
    "biting sandfly": ["animals", 2000],
    "twig": ["wood", 50],
    "branch": ["wood", 500]
}

crafts = {
    "craft sand grain": [{"sand grain": 1},
                         {"sand": 5}],
    
    "craft large sand grain": [{"large sand grain": 1},
                               {"sand grain": 20}],
    
    "craft huge sand grain": [{"huge sand grain": 1},
                              {"large sand grain": 10, "sand grain": 100}],
    
    "craft branch": [{"branch": 1},
                     {"twig": 10}],

    "craft biting sandfly": [{"biting sandfly": 1},
                             {"sandfly": 8}],
    
    "break sand grain": [{"sand": 5},
                         {"sand grain": 1}],
    
    "break large sand grain": [{"sand": 100},
                               {"large sand grain": 1}],
    
    "break huge sand grain": [{"sand": 1500},
                              {"huge sand grain": 1}],

    "break branch": [{"twig": 10},
                     {"branch": 1}],
    
    "trade twig to sand": [{"sand": 10},
                            {"twig": 1}],

    "trade sand to twig": [{"twig": 1},
                            {"sand": 10}],

    "trade sandfly to sand": [{"sand": 25},
                               {"sandfly": 1}],

    "trade sand to sandfly": [{"sandfly": 1},
                               {"sand": 25}],
    
    "sell sand": [{"coins": 10},
                  {"sand": 1}],
    
    "sell twig": [{"coins": 100},
                  {"twig": 1}],
    
    "sell sand grain": [{"coins": 55},
                        {"sand grain": 1}],
    
    "sell large sand grain": [{"coins": 1150},
                              {"large sand grain": 1}],
    
    "sell huge sand grain": [{"coins": 17500},
                             {"huge sand grain": 1}]
}

worlds = ["beach hole", "beach", "forest"]

place_names = {
    "(0, 0, 0)": "The starting point.",
    "(0, 1, 0)": "The beach, just north of your starting point.",
    "(0, -1, 0)": "Most of your stuff was located here at first.",
    "(-1, 0, 0)": "The beach, just west of your starting point.",
    "(1, 0, 0)": "The beach, just east of your starting point.",
}

cd = {
    "look": 60,
    "walk": 120,
    "hunt": 300,
    "move": 0,
    "sleep": 43200,
    "daily": 86400,
    "weekly": 604800
}

unlock = {}

# things: name: blocking? takeable? command?

things = {
    "door #": [1,0],
    "brick wall": [1,0],
    "seed": [0,1],
    "sapling": [0,0],
    "young tree": [1,0],
    "tree": [1,0],
    "sand wall": [1,0],
    "strong sand wall": [1,0],
    "note #": [0,1]
}

loot = {
    "beach look": {
        "5x sand grain|One look at the beach and 5 sand grains popped out. Wow!": 500,
        "2x sandfly|You saw **2** sandflies on the beach. Why not just take _both_ of them, you thought.": 250,
        "3x sand grain|You looked around and found 3 sand **grains** lying right in front of you.": 150,
        "20x sand|You looked around and found **20** sand!": 150,
        "2x sand grain|You looked around and spotted 2 sand **grains**!": 50,
        "1x sand|You looked around again and a teeny grain of sand caught your attention. Apparently it was to distract you, because...": 100,
        "1x sandfly|You saw a sandfly on the beach. Why not just take it, you thought.": 50,
        "8x sand|You looked around and spotted **8** sand!": 10,
        "7x sand|You looked around and spotted **7** sand!": 7,
        "1x sand grain|You looked around and spotted a sand grain!": 6,
        "5x sand|You looked around and spotted 5 sand on the beach.": 5,
        "4x sand|You looked around and spotted 4 sand.": 3,
        "3x sand|You looked around and spotted 3 sand.": 2,
        "2x sand|You looked around and spotted just 2 sand.": 1
    },
    "beach walk": {
        "1x branch|Walking around, your foot caught on a branch and you tripped! Fortunately, the branch didn't run away.": 100,
        "3x twig|Walking around, you found **3** twigs on the beach!": 25,
        "2x twig|Walking around, both your feet caught on 2 twigs.": 10,
        "1x twig|Walking around, your foot caught on a twig.": 4,
        "7x sand|Walking around, you found nothing much but some sand.": 4,
        "5x sand|Walking around, you found nothing much but some sand.": 3,
        "1x sand grain|Walking around, you found a sand grain.": 9,
        "4x sand|Walking around, you found nothing much but some sand.": 2,
        "1x twig|Walking around, you found a twig.": 1
    },
    "beach hunt": {
        "1x starfish|Wow! You found a _rare_ starfish lying on the beach near the sea.": 500,
        "1x branch|The hunt was unsuccessful, but you saw a branch on the way, wondering where it came from.": 120,
        "7x sandfly|Wow! You found a sandfly colony but only managed to hunt down 7 sandflies.": 100,
        "6x sandfly|Wow! You found a sandfly colony but only managed to hunt down 6 sandflies.": 75,
        "5x sandfly|Wow! You found a sandfly colony but only managed to hunt down 5 sandflies.": 50,
        "10x sand grain|The hunt was unsuccessful, but you saw 10 nice sand grains on the way.": 50,
        "3x sandfly|You found **3** sandflies flying around!": 25,
        "1x twig|The hunt was unsuccessful, but you saw a twig on the way, wondering where it came from.": 12,
        "2x sandfly|You found **2** sandflies!": 8,
        "5x sand grain|The hunt was unsuccessful, but you saw 5 sand grains on the way.": 5,
        "5x sand|The hunt was unsuccessful, but you saw 5 sand on the way.": 2,
        "1x sandfly|You found a sandfly!": 1
    }
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
    "Get a twig": ["twig",1,"Twig!"],
    "Get 30 twigs": ["twig",30,"Crack goes the twig!"],
    "Get 500 twigs": ["twig",500,"Twig collector!"],
    "Get 2 branches": ["branch",2,"Branch!"],
    "Get 40 branches": ["branch",40,"Branch collector!"],
    "Get 250 branches": ["branch",250,"B R A N C H"],
    "Catch 1 sandfly": ["sandfly",1,"Sandflier"],
    "Catch 10 sandflies": ["sandfly",10,"Don't fly away!"],
    "Catch 100 sandflies": ["sandfly",100,"You can't fly away!"]
}

notes = {
    1: """
```Welcome to the Island Hunt! Collect resources and survive on the Island!
Wait something's not right with the island... let me find out...```

The note was typewrited and torn off after the last three full stops.
""",
    2: """"""
}

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
        return "You reached to the ground and picked up a **note 1**!"
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