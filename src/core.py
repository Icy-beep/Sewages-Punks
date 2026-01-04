import random

from src import enemies
from src.businesslogic_upper import *
from src.display import *
from src.constants import *
from src.enemies import *
from src.player import *

def adventuring():

    dungeon_map = create_dungeon()

    user_input = ''
    while user_input not in EXIT_COMMANDS:
        print(show_dungeon_map(dungeon_map))
        print('command')
        print('up - w')
        print('left - a')
        print('down - s')
        print('right - d')
        user_input = input('>>')

        new_position = movement_player(dungeon_map, user_input)

        is_fight = try_start_fight(dungeon_map, new_position)

        if is_fight:
            return is_fight

    return None

def fight():
    enemy = create_enemy()

    print(enemy)
    print(start_fight_message(enemy))







