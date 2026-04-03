import sys

import entities
from src.core import *
from pregen_levels.tutorial_level import create_tutorial_dungeon
from src.display import draw_main_menu
from src.constants import *
from entities import create_default_player

def main_menu():
    in_main_menu = True
    while in_main_menu:
        draw_main_menu()
        choice = input(f"{MAGENTA_TEXT_BRIGHT}[SYSTEM@USER]:# {RESET}").strip()

        if choice == "1":
            dungeon = create_tutorial_dungeon()
            default_player = create_default_player()
            return dungeon, default_player

        elif choice == "2":
            saved_data = load_game()
            if saved_data:
                print(f"{GREEN_TEXT_BRIGHT}[DECRYPTING SUCCESSFUL...]{RESET}")
                return saved_data
            else:
                print(f"{RED_TEXT_BRIGHT}[ERROR: NO DATA ON SECTOR 0]{RESET}")

        elif choice == "3":
            show_setting_stub()

        elif choice == "4":
            print(f"{RED_TEXT_REGULAR}DISCONNECTING...{RESET}")
            sys.exit()


def game_loop(player_data, first_dungeon):
    is_fight = False
    game_is_run = True
    exfill = False
    dungeon = first_dungeon
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
    first_level, player = main_menu()
    game_loop(player, first_level)
