from type import type

import time

class Event:
    def __init__(self, event=None, criteria=None, is_completed=False):
        self.event = event if event else None

        self.criteria = criteria

        self.is_completed = is_completed

    def check_criteria(self, player):
        criteria_met = self.criteria(self, player)
        if criteria_met == True:
            self.perform_event(player)


    def perform_event(self, player):
        if not self.is_completed == True:
            self.event(self, player)

# ---------- Event Criteria ----------

def entrance_crumble_criteria(event, player):
    return True # no criteria

def dining_room_whisper_event_criteria(event, player):
    return True # no criteria

def give_note_event_criteria(event, player):
    from rooms import rooms
    if rooms['entrance'].can_give_note:
        return True
    return False

# --------------- ENDING CRITERIA ---------------

def escape_courtyard_event_criteria(event, player):
    from rooms import rooms

    if rooms['courtyard'].can_escape == True:
        return True
    return False

def escape_crypt_event_criteria(event, player):
    from rooms import rooms

    if rooms['crypt'].can_escape == True:
        return True
    return False


# ---------- Event Functions ----------

def entrance_crumble_event(event, player):
    from rooms import rooms
    event.is_completed = True
    player.injured = True
    rooms['entrance'].crumbled = True
    type("Suddenly, the ground begins to shake, and the wall behind you begins to crumble. You fall over, as you see a giant stone flying straight towards your head-.........\n")
    time.sleep(1)
    type("You wake up, and look around you to see that the entrance behind you is completely blocked. You try to think, but you cannot remember why you entered the mansion in the first place. Blood trickles from your head. You will need to quickly find a way to fix your injury.\nYou need to escape, but first, you'll need to find a way to clear the debris...\n")

def dining_room_whisper_event(event, player):
    from items import items
    from rooms import rooms
    event.is_completed = True
    rooms['dining_room'].observation = "The plates are empty. I'll need to cook something to fill the plates.\n"
    type("A strange voice whispers to you from the shadows: 'I'm hungry. Cook something for me, and I will give you the key.'\n")
    player.inventory.add_item(items['recipe_card'])

def give_note_event(event, player):
    from items import items
    event.is_completed = True

    if not player.inventory.has_item(items['artifact']):
            player.inventory.add_item(items['entrance_note'])

# --------------- ENDINGS ---------------

def escape_courtyard_event(event, player):
    from items import items
    from rooms import rooms
    event.is_completed = True
    
    if player.inventory.has_item(items['artifact']):
        type("Clutching the artifact tightly, you flee through the courtyard. The eerie glow it emits grows stronger with every step you take. The mansion fades from view, but a sense of dread lingers. You escaped with the artifact, but its power now rests in your hands - wether thats a blessing or a curse remains to be seen.....\n")
        player.game_over = True

    elif player.inventory.has_item(items['artifact_fragment']):
        type("As you sprint through the courtyard, you feel a strange weight lift from your shoulders, the air clears, and the once dark and cursed mansion appears to breathe its last breath, crumbling to the ground, its dark grip on the world broken at last.....\n")
        player.game_over = True

    else: 
        type("You leave the artifact behind, and race through the courtyard, the curse lingering in the shadows. While you've escaped the mansion's grasp, you know its power remains unbroken, waiting for the next unfortunate soul to uncover its secrets.....\n")
        player.game_over = True

def escape_crypt_event(event, player):
    from items import items
    from rooms import rooms
    event.is_completed = True
    
    if player.inventory.has_item(items['artifact']):
        type("As you continue into the crypt with the artifact in your possession, the air grows heavier. The stone doors seal behind you, and you realize the curse now binds you to the mansion. The artifact's power hums in your bad, but escape is no longer an option - you are part of the curse now, forever trapped in the crypt's cold embrace.\n")
        player.game_over = True

    elif player.inventory.has_item(items['artifact_fragment']):
        type("With the artifact shattered, as you continue into the crypt, the once opresive atmosphere fades. The stone doors in front of you open, and a path of light guides you out. The curse has lifted, and the crypt, once a place of death, feels at peace. You walk away free at last, leaving the mansion and its dark history behind.\n")
        player.game_over = True

    else: 
        type("You descend further into the crypt, empty-handed, knowing the artifact remains behind. The curse lingers, and as you push through the crypt's stone doors, the shadows seem to stretch towards you, as if the mansion calls for your return. You've escped, but without breaking the curse, the darkness still holds sway over the mansion, waiting for another to fall into its trap.\n")
        player.game_over = True


# --------------- Events ---------------

events = {
    'entrance_crumble_event': Event(event=entrance_crumble_event, criteria=entrance_crumble_criteria, is_completed=False),
    'dining_room_whisper_event': Event(event=dining_room_whisper_event, criteria=dining_room_whisper_event_criteria),
    'escape_courtyard_event' : Event(event=escape_courtyard_event, criteria=escape_courtyard_event_criteria),
    'escape_crypt_event' : Event(event=escape_crypt_event, criteria=escape_crypt_event_criteria),
    'give_note_event': Event(event=give_note_event, criteria=give_note_event_criteria),
}
        
