import random
import time
import os

from src.businesslogic_upper import *
from src.display import *
from src.constants import *
from src.entities import *

def create_player():
    print('')


def adventuring():
    dungeon_map = create_dungeon()
    user_input = ''

    while user_input not in EXIT_COMMANDS:
        os.system('cls')
        print(show_dungeon_map(dungeon_map))
        show_movement_legend()
        user_input = input('>>')

        new_position = movement_player(dungeon_map, user_input)

        is_fight = try_start_fight(dungeon_map, new_position)

        if is_fight:
            return STATE_OF_ADVENTURING_FIGHT

    return STATE_OF_ADVENTURING_EXIT

def fight(player_data):
    import time
    is_fight = True
    enemy = create_enemy()
    os.system('cls')
    print(start_fight_message(enemy))

    while is_fight:
        pass









