from type import type
from items import items

class Action:
    def __init__(self, name=None, action=None, is_completed=False):
        self.action = action if action else None
        self.name = name

        self.is_completed = is_completed
        
        
    def perform(self, player):
        if self.is_completed == False:
            self.action(self, player)
    

# ---------- Actions Functions ----------

# ----- Library -----
def library_lever_action(action, player):
    from rooms import rooms
    action.is_completed = True
    actions['library_lever_fake'].is_completed = True
    actions['library_lever_fake2'].is_completed = True
    type("You pulled the book, and you hear a metallic click like a lever. Maybe this opened something?\n")
    rooms['library'].add_exit(rooms['safe'])
    rooms['library'].observation = "There is a new opening to a secret room. Maybe there is something inside?"

def library_lever_fake(action, player):
    type("You pull the torch, but nothing happens.\n")

def library_lever_fake2(action, player):
    type("You push on the stone, but nothing happens\n")


def study_box_puzzle(action, player):
    from rooms import rooms
    answer = "48"
    type("The lockbox requires a two-digit code to open.\n")
    type("Your answer: ")
    choice = input()
    if choice.isdigit():
        if choice == answer:
            action.is_completed = True
            type("\nYou unlock the box, and inside, you find a strange key.\n")
            player.inventory.add_item(items['key_crypt'])
            player.inventory.remove_item(items['encyclopedia'].name)
        else:
            type("\nThats not the right code.\n")
    else:
        type("\nInvalid entry.\n")

def kitchen_cook_action(action, player):
    from rooms import rooms
    from items import items
    if player.inventory.has_item(items['sea_salt'].name) and player.inventory.has_item(items['black_pepper'].name) and player.inventory.has_item(items['apple'].name):
        type("You place the items in the pot and they start to cook by themselves like magic.\n")
        player.inventory.remove_item(items['sea_salt'].name)
        player.inventory.remove_item(items['black_pepper'].name)
        player.inventory.remove_item(items['apple'].name)
        player.inventory.add_item(items['strange_food'])
        action.is_completed = True
    else:
        type("You don't have all the ingredients to cook yet.\n")

def kitchen_cabinet_action(action, player):
    from rooms import rooms
    from items import items
    if player.current_room == rooms['kitchen'] and rooms['kitchen'].cabinet_locked == False:
        type("You search the kitchen cabinet.\n")
        player.inventory.add_item(items['key_armory'])
        action.is_completed = True
    else:
        type("The cabinet is locked.\n")

def alchemy_brew_action(action, player):
    from rooms import rooms
    if player.inventory.has_item(items['crystal_shard'].name) and player.inventory.has_item(items['herbs'].name) and player.inventory.has_item(items['potion'].name):
        type("You place the items in the brewing stand and they start mix and combine.\n")
        player.inventory.remove_item(items['crystal_shard'].name)
        player.inventory.remove_item(items['herbs'].name)
        player.inventory.remove_item(items['potion'].name)
        player.inventory.add_item(items['explosive_potion'])
        action.is_completed = True
    else:
        type("You don't have all the ingredients to brew the potion yet.\n")

# --------------- Actions ---------------

actions = {
    # ----- Library -----
    'library_lever_action': Action("A dusty book that hangs slightly off the shelf", action=library_lever_action, is_completed=False),
    'library_lever_fake': Action("A suspicious torch hanging on the wall", action=library_lever_fake, is_completed=False),
    'library_lever_fake2': Action("A stone brick that protrudes slightly out of the wall", action=library_lever_fake2, is_completed=False),

    # ----- Study ------
    'study_box_puzzle': Action("A small box on the table.", action=study_box_puzzle, is_completed=False),

    # ----- Kitchen -----
    'kitchen_cook_action': Action("A pot on the stove.", action=kitchen_cook_action, is_completed=False),
    'kitchen_cabinet_action': Action("A cabinet above the stove.", action=kitchen_cabinet_action, is_completed=False),

    # ----- Alchemy Room -----
    'alchemy_brew_action': Action("A brewing stand centered in the room", action=alchemy_brew_action, is_completed=False),
}