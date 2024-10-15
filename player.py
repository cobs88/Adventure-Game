from items import *
from rooms import rooms

class Player:
    def __init__(self):
        self.inventory = Inventory()
        self.current_room = rooms['courtyard']
        self.current_room.explored = True
        self.previous_room = None

        self.injured = False
        self.game_over = False
        self.ending = None

    def show_inventory(self):
        self.inventory.show_inventory()

    def use_item(self, item):
        item.use(self)

    def enter_room(self, room):
        self.previous_room = self.current_room
        if room.conditions:
            for i, condition in enumerate(room.conditions):
                if condition(room, self):
                    type(f"{condition(room, self)}\n")
                    return False
        self.current_room = room
        self.current_room.explored = True

        return True
        

    def choose_item(self):
        usable_items = [item for item in self.inventory.items if item.usable]

        if not usable_items:
            type("You have no usable items in your inventory.\n")

            return None

        type("You have the following usable items:\n")

        for i, item in enumerate(usable_items):
            type(f"{i + 1}. {item.name}\n")
        type("Enter the number of the item you want to use, or type (n)one: ")
        choice = input().lower()

        if choice.isdigit() and 1 <= int(choice) <= len(usable_items):
            type("\n")
            return usable_items[int(choice) - 1]
        elif choice in ["n", "none"]:
            type("\nYou do nothing.\n")
            return
        else:
            type("\nInvalid choice\n")
            self.choose_item()