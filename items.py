from type import type
from ansi import *

import time

class Item:
    def __init__(self, name, description, usable=False, action=None):
        self.name = name
        self.description = description

        self.usable = usable
        self.action = action if action else None

        if self.name == f"{YELLOW}{BOLD}The Artifact{NORMAL}":
            self.picked_up = False

    def use(self, player):
        if self.usable and self.action:
            self.action(self, player)
        else:
            type(f"The {self.name} cannot be used.\n")

    def __str__(self):
        return f"{self.name}: {self.description}"
            
class Inventory:
    def __init__(self):
        self.items = []

    def add_item(self, item):
        self.items.append(item)
        type(f"You picked up: {item.name}.\n")
        if item == items['artifact']:
            item.use(self)

    def remove_item(self, item_name):
        for item in self.items:
            if item.name == item_name:
                self.items.remove(item)
                return item
        type(f"You dont have {item_name} in your inventory.\n")
        return None

    def has_item(self, item_name):
        return any(item.name == item_name for item in self.items)

    def show_inventory(self):
        if not self.items:
            type("Your inventory is empty.\n")
        else:
            type("Your inventory contains:\n")
            for item in self.items:
                type(f"- {item.name}: {item.description}\n")

# ---------- Item Actions ----------

def unlock_armory_action(item, player): # code for the armory key
    from rooms import rooms
    if player.current_room == rooms['atrium'] and rooms['armory'].locked == True: # checks if you are in the right room
        type(f"You use the {item.name} to open the armory. The lock on the door seems untouched for centuries. The door makes a loud screeching sound as the large steel gates scrape against the marble floors.\n")
        rooms['armory'].locked = False # unlock the armory
        player.inventory.remove_item(item.name)
    else:
        type("This item cannot be used here.\n")

def unlock_crypt_action(item, player): # code for the armory key
    from rooms import rooms
    if player.current_room == rooms['downstairs'] and rooms['crypt'].locked == True: # checks if you are in the right room
        type(f"You use the {item.name} to open the crypt. With a deep rumble, the heavy stone door creaks open, revealing a dark passage lined with ancient carvings. A cold gust of air rushes out, carrying the scent of earth and decay, inviting you into the shadows\n")
        rooms['crypt'].locked = False # unlock the armory
        player.inventory.remove_item(item.name)
    else:
        type("This item cannot be used here.\n")

def heal_injury_action(item, player):
    from rooms import rooms
    rooms['infirmary'].observation = None
    type(f"You use the bandages to patch up your wound. You feel better.\n")
    player.inventory.remove_item(item.name)

    player.injured = False

def place_food_action(item, player):
    from rooms import rooms
    if player.current_room == rooms['dining_room']: # checks if you are in the right room
        type(f"You place the {item.name} on the plate. Suddenly, the food vanishes instantly. The same voice whispers: 'Thank-you for the food. I've unlocked the cabinet in the kitchen for you.")
        player.inventory.remove_item(item.name)
        player.inventory.remove_item(items['recipe_card'].name)
        rooms['kitchen'].cabinet_locked = False
    else:
        type("This item cannot be used here.\n")

def potion_recipe(item, player):
    type(f"The {item.name} reads:\n")
    type("----- Ingredients -----\n")
    type(
        f"- {items['crystal_shard'].name}\n"+
        f"- {items['herbs'].name}\n"
    )

def recipe_card(item, player):
    type(f"The {item.name} reads:\n")
    type(
        "- A fruit from a tree\n"+
        "- Something salty from the sea\n"+
        "- A seasoning thats spicy\n"
    )
    
def encyclopedia(item, player):
    type(f"The {item.name} reads:\n")
    type(f"{ITALIC}Among the tomes upon the shelf, Four titles hold the key themselves. Read each name and count the letters, Add them up to get the answer.{NORMAL}\n")

def entrance_note(item, player):
    type(f"The {item.name} reads:\n")
    type(f"The ancient artifact lies in the locked room in the entrance. Get it. \n")

def explode_door_action(item, player):
    from rooms import rooms
    if player.current_room == rooms['atrium']: # checks if you are in the right room
        type(f"You grab the {item.name} and throw it at the large wood door. The door explodes and starts to burn in flames.\n")
        player.current_room.add_exit(rooms['artifact_room'])
        player.inventory.remove_item(item.name)
    else:
        type("This item cannot be used here.\n")

def artifact_action(item, player):
    from rooms import rooms
    if item.picked_up:
        type(f"You feel the artifact whisper: {ITALIC}'Break me, end the curse,'{NORMAL} and {ITALIC}'Keep me, and claim my power.'{NORMAL} You are forced to decide between freedom and power.\n")
        type("Do you want to break the artifact? [y/n]\n")
        choice = input().lower()

        if choice in ['yes', 'y']:
            type("With a swift strike, the artifact shatters in your hands. A rush of air fills the room, and the darkness that clung to the mansion vanishes. The weight of the curse lifts, and for the first time, everything feels still and free.\n")
            player.inventory.remove_item(items['artifact'].name)
        elif choice in ['no', 'n']:
            type("You place the artifact in your bag. The voices fall silent. The curse remains undisturbed, but now the power it holds lingers, bound now to you, and the artifact.\n")
        else:
            type("Invalid choice.\n")
            type("You place the artifact in your bag. The voices fall silent. The curse remains undisturbed, but now the power it holds lingers, bound now to you, and the artifact.\n")
    else:
        type(f"As you reach out and grasp {item.name}, a chilling surge runs through your hand, as though the very air around you holds its breath. The object is far heavier than it looks, pulsing faintly with an eerie light. A low hum fills the room, and for a moment, it feels as if the walls themselves are watching.\n")
        item.picked_up = True
        artifact_action(item, player)

    
def pickaxe_clear_action(item, player):
    from rooms import rooms
    if player.current_room == rooms['atrium']: # checks if you are in the right room
        type(f"You use the {item.name} to start mining at the debris.\n")
        time.sleep(1)
        type("After around an hour of work, you manage to clear enough debris to squeeze through the opening.\n")
        rooms['entrance'].crumbled = False
        player.inventory.remove_item(item.name)

        rooms['entrance'].description = "You make it back to the entrance. Everything is crumbled and broken. You see the light at the end of the hallway. This is your chance to escape.\n"
        rooms['entrance'].description_shown = False

        rooms['courtyard'].can_escape = True
        rooms['entrance'].can_give_note = True

        rooms['courtyard'].description_shown = True
        
    else:
        type("This item cannot be used here.\n")

# -------------- Items --------------

items = {
    # items with clues in them
    'old_book': Item(f"{RED}Old Book{NORMAL}", f"An old book. {DIM}{BLACK}echo.{NORMAL}", usable=False), # found in the entrance

    'encyclopedia': Item(f"{RED}The Encyclopedia of Mysteries{NORMAL}", f"An old encyclopedia. Seems to be a clue.", usable=True, action=encyclopedia),

    'potion_recipe': Item(f"{RED}Potion Recipe{NORMAL}", f"A recipe for a mysterious potion.", usable=True, action=potion_recipe),

    'recipe_card': Item(f"{RED}Recipe Card{NORMAL}", f"A card containing a strange recipe.", usable=True, action=recipe_card),

    'entrance_note': Item(f"{RED}Note{NORMAL}", f"A small note, maybe this says something important.", usable=True, action=entrance_note),


    # collectible items
    'statue_gold_horse': Item(f"{BOLD}{YELLOW}Golden Horse Statue{NORMAL}", "A small, intricately crafted golden statue of a horse.", usable=False), # found in the entrance
    'statue_gold_pig': Item(f"{BOLD}{YELLOW}Golden Pig Statue{NORMAL}", "A small, intricately crafted golden statue of a pig.", usable=False), # found in the courtyard

    # keys
    'key_armory': Item(f"{BOLD}{BLUE}Armory Key{NORMAL}", "A rusted metal key. This can be used to unlock the armory.", usable=True, action=unlock_armory_action), # found in the library
    'key_crypt': Item(f"{BOLD}{BLUE}Crypt Key{NORMAL}", "A key made out of a strange material. Maybe bone.", usable=True, action=unlock_crypt_action), # found in the study

    # quest items

    # infirmary items
    'bandage': Item(f"{GREEN}{BOLD}Bandages{NORMAL}", "Some old bandages. They seem sterile enough.", usable=True, action=heal_injury_action),

    # --potion ingredients--
    'crystal_shard': Item(f"{MAGENTA}Crystal Shard{NORMAL}", "A brittle crystal shard. Maybe this can be useful later?", usable=False),
    'herbs': Item(f"{GREEN}Mysterious Herbs{NORMAL}", "Some mysterious herbs. Maybe these can be useful later?", usable=False),
    'potion': Item(f"{YELLOW}Potion{NORMAL}", "A strange potion. Maybe this can be useful later?", usable=False),

    'explosive_potion': Item(f"{MAGENTA}{BOLD}Explosive Potion{NORMAL}", "An explosive potion. Maybe this can be used to break something large?", usable=True, action=explode_door_action),


    # --kitchen ingredients--
    'apple': Item("Apple", "An apple. Maybe this can be useful later?", usable=False),
    'sea_salt': Item("Sea Salt", "Socme fine sea salt. Maybe this can be useful later?", usable=False),
    'black_pepper': Item("Black Pepper", "Some ground black pepper. Maybe this can be useful later?", usable=False),

    'strange_food': Item(f"{GREEN}Strange Food{NORMAL}", "A very strange meal to request. It smells weirdly good though.", usable=True, action=place_food_action),

    # pickaxe
    'pickaxe': Item(f"{YELLOW}Pickaxe{NORMAL}", "A rusty old pickaxe. Maybe you can use this to clear the debris?", usable=True, action=pickaxe_clear_action),

    # the artifact
    'artifact': Item(f"{YELLOW}{BOLD}The Artifact{NORMAL}", "The ancient artifact. DESTROY IT, DO NOT DESTROY IT", usable=True, action=artifact_action),
    'artifact_fragment': Item(f"{YELLOW}{BOLD}Artifact Fragment{NORMAL}", "A shard from the ancient artifact.", usable=False)
}