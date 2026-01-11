import sys

from src.core import *


def game_start():
    gamer = create_player()

    return gamer

def game_loop(player_data):
    is_fight = False
    game_is_run = True
    dungeon = create_dungeon()

    while game_is_run:
        while not is_fight:
            state_of_adventuring, new_position = adventuring(dungeon, player_data)

            if state_of_adventuring == STATE_OF_ADVENTURING_FIGHT:
                break

            if state_of_adventuring == STATE_OF_ADVENTURING_EXIT:
                exit(0)

        fight(player_data)
        if player_data[ENTITY_HP] <= 0:
            print('GAME OVER')
            sys.exit(0)
        dungeon[new_position[0]][new_position[1]] = FLOOR_TILE

def game_over():
    pass


if __name__ == '__main__':
    player = game_start()
    game_loop(player)
