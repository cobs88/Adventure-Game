# library imports
import random
import time

# import from other files in the project
from type import type
from items import items
from ansi import *
from puzzle import Puzzle
from actions import actions
from events import events

# create the room class
class Room:
    def __init__(self, name=None, description=None, observation=None, puzzle=None, actions=None, events=None, items=None, conditions=None, locked=False):
        self.name = name if name else "unnamed" # makes sure that the room has a name
        self.description = description if description else self.generate_description()
        self.observation = observation if observation else "There is nothing to observe here.\n"
        self.items = items if items else [] # if there are no items specified, create an empty list
        self.puzzle = puzzle # if puzzle else self.generate_puzzle()
        self.actions = actions if actions else []
        self.events = events
        self.exits = [] # creates an empty list to put all exits in
        self.conditions = conditions if conditions else []
        self.locked = locked if locked else False
        self.explored = False
        self.crumbled = False

        self.description_shown = False # this makes sure the description isnt shown every time you enter a room

        if self.name == "The Kitchen": self.cabinet_locked=True

        if self.name == "The Courtyard": self.can_escape=False
        if self.name == "The Crypt": self.can_escape=True
        
        if self.name == "The Entrance": self.can_give_note=False
    
    
    def unlock(self):
        self.locked = False

    # adds an exit to the room
    def add_exit(self, room):
        self.exits.append(room)
        # creates a two way path
        room.exits.append(self)

    def remove_exit(self, room):
        self.exits.remove(room)
        room.exits.remove(self)

    # shows all the items inside the room and prints them out
    def show_items(self, player):
        if not self.items:
            type("There are no items here.\n")
            return
        while True:
            type("You see the following items:\n")
            for i, item in enumerate(self.items):
                type(f"{i + 1}. {item.name}\n")
            type("Enter the number of the item you want to pick up, or (n)one: ")
            choice = input().lower()
            if choice in ["n", "none"]:
                type("\nYou do nothing.\n")
                return
            elif choice.isdigit() and 1 <= int(choice) <= len(self.items):
                type("\n")
                item = self.items.pop(int(choice) - 1)
                player.inventory.add_item(item) 
                return         
            else:
                type("\nInvalid choice.\n")
        
    def show_actions(self, player):
        incompleted_actions = [action for action in self.actions if action.is_completed==False]
        if not incompleted_actions:
            type("There is nothing to do in this room.\n")
            return
        else:
            type("As you look around the room, you see:\n")
            for i, action in enumerate(incompleted_actions):
                type(f"{i + 1}. {action.name}\n") 
            type("Enter the number of the thing you want to interact with, or (n)one: ")
            choice = input().lower()
            if choice in ["n", "none"]:
                type("\nYou do nothing.\n")
                return
            elif choice.isdigit() and 1 <= int(choice) <= len(incompleted_actions):
                type("\n")
                incompleted_actions[(int(choice) - 1)].perform(player)
            else:
                type("\nInvalid choice.\n")

    
    def add_item(self, item):
        self.items.append(item)

    def generate_puzzle(self):
        # chooses a random puzzle
        puzzles = [
            Puzzle("You hear an ominous voice that whispers a mysterious riddle...\nWhat has keys, but cannot open locks?\n", "piano"),
            Puzzle("You see strange writing on the wall, it seems like a riddle...\nWhat comes once in a minute, twice in a moment, but never in a thousand years?\n", "m")
        ]

        return random.choice(puzzles)


    def generate_description(self):
        # the description generator takes an adjective, noun and action and combines them to make the room's description
        adjectives = [" grand", " dusty", " mysterious", " foreboding", "n eerie", " dimly lit", " haunting", " gloomy", " shadowy", " faded", " forgotten"]

        nouns = ["hallway", "crypt", "corridor", "cellar", "gallery", "chamber", "sanctuary", "passage", "room"]

        actions = [
            "Faint whispers echo in the silence...\n", 
            "Dust motes swirl in the dim light...\n", 
            "A creaking floorboard breaks the silence...\n", 
            "Shadows stretch and flicker along the faded walls...\n", 
            "A faint scent of decay lingers in the air...\n",
            "A chill runs down your spine...\n", 
            "Cobwebs brush against your skin...\n", 
            "The candlelight flickers ominously...\n", 
            "A door slams shut with a resonant thud...\n", 
            "You feel an unseen presence watching you...\n", 
            "The floor shakes and shifts beneath your feet...\n", 
            "You hear soft footsteps approaching, but see nothing...\n", 
            "An eerie stillness settles...\n"]

        generated_description = f"You enter a{random.choice(adjectives)} {random.choice(nouns)}. {random.choice(actions)}"

        return generated_description

    def show_description(self):
        type(self.description)

    def observe(self):
        type(self.observation)

    def traverse_room(self, player):
        type(f"{BOLD}{self.name}{NORMAL}\n")
        if not self.description_shown:
            self.show_description()
            self.description_shown = True

        if self.events:
            for i, event in enumerate(self.events):
                event.check_criteria(player)

        if self.puzzle: 
            type(self.puzzle.question)
            type("Your answer: ")

            player_answer = input().lower()

            if player_answer in ["q", "quit"]:
                type("\nYou quit the puzzle.")

                player.current_room = player.previous_room
                type("\n")
                return

            while not self.puzzle.check_answer(player_answer):
                type("\nTry again!\n")
                type(self.puzzle.question)
                type("Your answer: ")
                player_answer = input()
            else:
               type("\nThat is the correct answer. You may now explore the room.\n")
               self.puzzle = None
               return True
        return True

    def choose_room(self):
        type("Where would you like to go next or (q)uit to quit?\n")
        for i, exit in enumerate(self.exits):
            type(f"{i + 1}. {exit.name} ", 0.004)
            if exit.explored == False:
                type(f"{BOLD}* {NORMAL}")
            if exit.locked == True:
                type(f"{BOLD}({RED}Locked{NORMAL})")
            type("\n", 0.004)
        type("Your choice: ")
        choice = input()

        if choice.isdigit() and 1 <= int(choice) <= len(self.exits):
            type("\n")
            return self.exits[int(choice) - 1]
        elif choice in ['q', 'quit']:
            type("\n")
            return self
        else:
            type("\nInvalid choice\n")
            return None

# ---------- Room Conditions ---------- 

def locked_condition(room, player):
    if room.locked:
        return f"This room is locked. You will need a key."

def injured_condition(room, player):
    if player.injured:
        return f"You are injured. Fix your injury before entering this room."

def crumbled_condition(room, player):
    if room.crumbled == True:
        return f"The entrance is crumbled. Find a way to clear the debris."

# name, description, observation, puzzle, actions, events, items, conditions, locked
rooms = {
    'courtyard': Room(
        "The Courtyard",
        ".....You stand with awe, but also uneasiness, as the towering mansion, overtaken by twisted vines and darkened from years of neglect, looms before you. The once-pristine cobblestone pathway, now fractured and swallowed by nature, leads through an overgrown garden, where evil thorny plants claw at the edges of the walkway. At the end of the path, stands the enormous wooden doors, leading to the main hall. The air is thick with the scent of rot and decay, and the wind whispers stories of gloom through the branches of the dead trees. As you look up, the mansion's windows stare you down like dark and hollow eyes, just daring you to go inside...\n",
        None, # observation
        None, # puzzle
        None, # actions
        [events['escape_courtyard_event']],
        [items['statue_gold_pig']],
        None, # conditions
        False # locked
    ),

    'entrance': Room(
        "The Entrance",
        "The entrance is grand, yet eerily empty. You see faded portraits of stern-faced people hanging on the walls, their eyes seeming to follow your every move. A chandelier above you sways ever so slighly, casting long flickering shadows across the decaying walls. A faint, cold draft travels the room, sending a shiver down your spine.\n",
        None, # observation
        None, # puzzle
        None, # actions
        [events['give_note_event']],
        [items['statue_gold_horse']],
        [crumbled_condition],
        False # locked
    ),

    'atrium': Room(
        f"The Central Atrium",
        "You find yourself in the vast arium - the heart of the mansion. The floors are made of marble and towering columns stretch torward the shadowy ceiling. Dust dances in the pale light that filters through the cracked stained-glass windows. Staircases lead both to the upstairs and down to the basement, while sevral doorways branch out into the unknown depths of the estate. Something about the air feels... heavy, as if something is watching you.\n",
        "There is a massive wooden door. It seems to be locked. It has no keyhole. You'll need something else to break it.",
        None, # puzzles
        None, # actions
        [events['entrance_crumble_event']],
        [items['old_book']], 
        None, # conditions
        False # locked
    ),
    
    # ---------- ATRIUM CHILD ROOMS ----------

    'library': Room(
        f"{RED}{BOLD}The Library{NORMAL}", 
        "The library is a vast, dimly lit room with towering bookshelves that seem to stretch endlessly into the shadows. Dusty books and forgotten scrolls fill the air with the scent of old parchment. The room is silent, broken only by the occasional rustling of pages, although no one else appears to be here...\n",
        "You notice a bookshelf that seems loose. Maybe there is something hidden behind it...",
        Puzzle("You see an old, but elegant mahogany desk centered in the room. Lying on it is an ancient book, its pages yellowed with age. In the center of the page, you see strange symbols written. The letters on the book shift and warp as if alive, and begin to form a riddle:\nI speak without a mouth, and hear without ears. I have no body, but I come alive with wind. What am I?\n", "echo"),
        [actions['library_lever_fake'], actions['library_lever_fake2'], actions['library_lever_action']],
        None, # events
        None, # items
        [injured_condition],
        False # locked
    ),

    'infirmary': Room(
        f"{GREEN}{BOLD}The Infirmary{NORMAL}",
        "You stumble into the old infirmary. The scent of dust and mildew fills the air. Broken medical cabinets line the walls, their contents long lost. Beds and curtains are scattered throughout the room. On the floor are assorted medical items. Most seem unusable.\n",
        "Maybe you can use some of these items to heal your injuries?\n",
        Puzzle("You hear a strange ghastly voice whisper to you:\nI have no legs, yet i run. I have no tongue, but I whisper. I heal the deepest wounds, yet leave no scar. What am i?\n", "time"),
        None,
        None,
        [items['bandage']],
        None, 
        False
    ),

    'armory': Room(
        f"{BLUE}{BOLD}The Armory{NORMAL}", 
        "The armory is a cold and dimly lit cellar, lined with racks of rusted weapons and dented armor. The air smells of metal. Swords, spears and shields of all shapes and sizes are mounted haphazardly on the stone walls, all long-forgotten and caked with dust.\n",
        None, # observations
        None, # puzzles
        None, # actions
        None, # events
        [items['pickaxe']],
        [locked_condition, injured_condition], # conditions
        True  # locked
    ),

    'dining_room': Room(
        f"The Dining Room",
        "The grand dining room stetches before you, with a massive oak table dominating the space. Plates and silverware remain set as though waiting for a meal that will never come. The chandelier above still sways gently, despite the still air, casting long shadows across the room.\n",
        None, # observations
        None, # puzzles
        None, # actions
        [events['dining_room_whisper_event']],
        items['black_pepper'],
        [injured_condition], # conditions
        False  # locked
    ),

    'kitchen': Room(
        f"The Kitchen",
        "The once-bustling kitchen now lies in a state of disarray. Pots and pans hang crookedly from the walls, and the wooden table is covered in remanants of old meals. The faint smell of rotting food lingers in the room.\n",
        "I can cook something inside this room.\n",
        None, # puzzles
        [actions['kitchen_cook_action'], actions['kitchen_cabinet_action']],
        None, # events
        [items['sea_salt']], # items
        None,
        False
    ),

    'greenhouse': Room(
        f"The Greenhouse",
        "Overgrown plants spill from broken pots, their vines creeping across the cracked glass ceiling. The air is thick with humidity and the scent of earth, as towering ferns and strange flowers loom in the dim light. Once a place of care and cultivation, now nature has reclaimed it, wild and untamed.\n",
        None,
        Puzzle("I have forests, but no trees. I have rivers, but no water. I have hills, but no ground. What am I?\n", "map"),
        None,
        None,
        [items['apple'], items['herbs']],
        [injured_condition],
        False
    ),
    

    'upstairs': Room(
        f"The Upstairs",
        "The upstairs has a large balcony with an elegant railing, overlooking the main atrium. Soft light penetrates the windows, casting shadows on the wooden floors. Dust hangs in the air, and the creaking of the floorboards echoes throughout the mansion.\n",
        None, # observations
        None, # puzzles
        None, # actions
        None, # events
        None, # items
        [injured_condition], # conditions
        False  # locked
    ),

    'downstairs': Room(
        f"The Basement",
        "The air grows colder as you descend into the damp, musty cellar. The stone walls feel like they are closing in, and flickering lights reveal shelves of dusty bottles and ancient, rusted tools.\n",
        None, # observations
        None, # puzzles
        None, # actions
        None, # events
        None, # items
        [injured_condition], # conditions
        False  # locked
    ),

    # ---------- BASEMENT CHILD ROOMS ----------

    'winery': Room(
        f"The Winery",
        "The"
    ),

    'crypt': Room(
        f"The Crypt",
        "The air grows cold and heavy as you descend into the crypt, where ancient stone tombs line the walls, etched with names long forgotten. The flicker of the distance torchlight casts eerie shadows, and the faint scent of decay kingers in the damp air. A sense of unease fills the dark passage, as though something buried here never truly rests.",
        None,
        None,
        None,
        [events['escape_crypt_event']],
        [locked_condition],
        True
    ),

    'alchemy_room': Room(
        f"{MAGENTA}{BOLD}The Alchemy Room{NORMAL}",
        "The dimly lit alchemy room is filled with the rich scent of herbs and bubbling concoctions simmering over flickering flames. Shelves crammed with vials, dusty tomes and peculiar ingredients line the walls, while a large wooden table in the center of the room is covered in a chaotic array of alchemical tools.",
        "Maybe I can brew a potion here?",
        None, # puzzles
        [actions['alchemy_brew_action']],
        None, # events
        [items['potion']], # items
        None, # conditions
        False # locked
    ),

    'artifact_room': Room(
        f"{YELLOW}{BOLD}The Artifact Room{NORMAL}",
        f"Hidden behind the massive wooden door, this dark, windowless chamber is dominated by a single pedestal in the center, where {items['artifact'].name} rests, bathed in an unnatural glow. The air is thick with a foreboding presence, and strange symbols are etched into the stone walls, as though the room itself is a vault designed to contain the ancient power within.\n",
        None,
        Puzzle(
            f"Suddenly, a deep, evil sounding voice growls: {ITALIC}'Answer the riddle, or die'\n"+
            "I have no life, but I can grow.\n"+
            "I have no lungs, but I need air.\n"+
            "I have no mouth, and yet I roar.\n"+
            f"What am I...?\n{NORMAL}", "fire"
        ),
        None, # actions
        None, # events
        [items['artifact']],
        None, # conditions
        False # locked
    ),

    # ---------- UPSTAIRS ATRIUM CHILD ROOMS ----------

    'study': Room(
        f"The study",
        "Dusty tomes and worn papers cover every single surface of the cramped study. A single oil lamp flickers weakly, casting eerie shadows on the walls. The shelves that line the room are crammed with oddities - small trinkets, mysterious artifacrs and strange diagrams. There is a map of the mansion, but parts of it have been thrown away, leaving gaps.\n",
        "You look at the bookshelf. Four books stand out. They are titled:\n"+
        "- 'The Secrets'\n"+
        "- 'Hidden Realms'\n"+
        "- 'Forgotten Lore'\n"+
        "- 'Ancient Spells'\n",
        None, # puzzles
        [actions['study_box_puzzle']], # actions
        None, # events
        [items['encyclopedia']],
        None, # conditions
        False # locked
    ),

    'servant_room': Room(
        f"The Servant's Quarters",
        "The servant's quarters are cramped, with wooden furniture and beds pushed up against the walls. Cobwebs stretch across the corners, and the air is thick with dust. A chest sits beneath one of the beds. The smell of burnt oil lingers in the air.\n",
        "There is a chest beneath one of the beds.\n",
    ),

    'safe': Room(
        f"{GREEN}The Safe{NORMAL}",
        "The safe is a secret room hidden behind bookshelves. The walls contain shelves of old decaying books written in a strange language. They seem to be instructions for an potion.\n",
        None, # observations
        None, # puzzles
        None, # actions
        None, # events
        [items['crystal_shard'], items['potion_recipe']],
        None, # conditions
        False # locked
    ),

}

# add all exits
rooms['courtyard'].add_exit(rooms['entrance']) # courtyard is first room, it connects to the entrance
rooms['entrance'].add_exit(rooms['atrium']) # the entrance leads to the atrium

# the atrium is the main hub. it connects to the different wings of the mansion
rooms['atrium'].add_exit(rooms['library']) # the library also connects to the safe, but this happens once you pull the secret lever
rooms['atrium'].add_exit(rooms['armory'])
rooms['atrium'].add_exit(rooms['infirmary'])
rooms['atrium'].add_exit(rooms['dining_room'])
rooms['atrium'].add_exit(rooms['greenhouse'])

rooms['dining_room'].add_exit(rooms['kitchen'])

rooms['atrium'].add_exit(rooms['upstairs'])
rooms['atrium'].add_exit(rooms['downstairs'])

rooms['downstairs'].add_exit(rooms['alchemy_room'])




# the upstairs atrium is the second hub. it connects to a few rooms
rooms['upstairs'].add_exit(rooms['study'])