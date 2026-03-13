import sys

from src.core import *
from pregen_levels.test_level import *

def main_menu():
    pass

def game_loop(player_data):
    is_fight = False
    game_is_run = True
    exfill = False
    dungeon = test_level
    while game_is_run:
        while not is_fight:
            if exfill:
                dungeon = create_dungeon()
                exfill = False

            state_of_adventuring, new_position = adventuring(dungeon, player_data)

            if state_of_adventuring == STATE_OF_ADVENTURING_FIGHT:
                break

            if state_of_adventuring == STATE_OF_ADVENTURING_EXFILL:
                exfill = True
                pass

            if state_of_adventuring == STATE_OF_ADVENTURING_EXIT:
                exit(0)

        fight(player_data)
        if player_data[ENTITY_HP] <= 0:
            print(GAME_OVER_MESSAGE)
            sys.exit(0)
        dungeon[new_position[0]][new_position[1]] = FLOOR_TILE

def game_over():
    pass


if __name__ == '__main__':
    player = game_start()
    game_loop(player)
