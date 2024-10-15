import os

from rooms import *
from player import Player
from items import *
from type import type
from ansi import *

player = Player()



def game():
    type(f"{BOLD}The Secret of the Abandoned Manor{NORMAL}\n")
    type("At any point that you are asked 'What would you like to do', you can enter (h)elp for help.\n")
    type("If a riddle is too difficult, you can type (q)uit to quit and look for some clues.\n")
    type("Press 'enter' to continue\n")

    game_continue = input()
    if not game_continue: time.sleep(0.1)
    os.system('cls')
    

    while True:
        if player.game_over:
            break
        if not player.current_room == player.previous_room or player.previous_room == None:
            player.current_room.traverse_room(player)

        # logic for traversing rooms
        while True:
            if player.game_over:
                break
            type("What would you like to do?\n")
            type("Command: ")
            choice = None
            choice = input().lower().strip()
            type("\n")
            if choice in ['h', 'help']:
                type(
                    "(i)nventory - Shows all items you currently have in your inventory\n"+
                    "(u)se - Use an item from your inventory\n"+
                    "(s)earch - Search the room for items\n"+
                    "(o)bserve - Observes the room and gives clues\n"+
                    "(l)ook - Look around the room for things to interact with\n"+
                    "(c)ontinue - Continue forward\n"+
                    "(d)escription - Gives the description of the room\n"
                )
            elif choice in ['i', 'inventory']:
                player.show_inventory()

            elif choice in ['u', 'use']:
                item = player.choose_item()
                if item: player.use_item(item)

            elif choice in ['o', 'observe']:
                player.current_room.observe()

            elif choice in ['l', 'look']:
                player.current_room.show_actions(player)

            elif choice in ['s', 'search']:
                player.current_room.show_items(player)

            elif choice in ['c', 'continue']:
                chosen_room = None
                while chosen_room == None:
                    chosen_room = player.current_room.choose_room()
                if player.enter_room(chosen_room):
                    break
                break

            elif choice in ['d', 'description']:
                player.current_room.show_description()

            else:
                type("Invalid choice.\n")



os.system('cls')
game()