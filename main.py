import sys
import os

from src.core import *
from pregen_levels.tutorial_level import create_tutorial_dungeon
from src.display import draw_main_menu
from src.constants import *
from src.entities import create_default_player


def main_menu():
    in_main_menu = True
    while in_main_menu:
        clear_display()
        draw_main_menu()
        choice = input(f"{MAGENTA_TEXT_BRIGHT}[SYSTEM@{PLAYER_NAME}]:# {RESET}").strip()

        if choice == "1":
            dungeon = create_tutorial_dungeon()
            default_player = create_default_player()
            return dungeon, default_player

        elif choice == "2":
            saved_data = load_game()
            if saved_data:
                print(f"{GREEN_TEXT_BRIGHT}[DECRYPTING SUCCESSFUL: OBJECT {[PLAYER_NAME]} ---> RESTORED]{RESET}")
                return saved_data
            else:
                print(f"{RED_TEXT_BRIGHT}[ERROR: NO DATA ON SECTOR{RESET} {MAGENTA_TEXT_BRIGHT}0xxxx256]{RESET}")

        elif choice == "3":
            show_setting_stub()

        elif choice == "4":
            print(f"{RED_TEXT_REGULAR}DISCONNECTING...{RESET}")
            time.sleep(0.2)
            sys.exit()


def game_loop(player_data, first_dungeon):
    is_fight = False
    game_loop_is_run = True
    exfill = False
    dungeon = first_dungeon
    while game_loop_is_run:
        while not is_fight:
            if exfill:
                dungeon = create_dungeon()
                exfill = False

            state_of_adventuring, new_position = adventuring(dungeon, player_data)

            if state_of_adventuring == FIGHT:
                break

            if state_of_adventuring == EXFILL:
                exfill = True
                pass

            if state_of_adventuring == EXIT:
                exit(0)

            if state_of_adventuring == RETURN_TO_MAIN_MENU:
                return EXIT_TO_MAIN_MENU

        fight(player_data)
        if player_data[ENTITY_HP] <= 0:
            print(GAME_OVER_MESSAGE)
            sys.exit(0)
        dungeon[new_position[0]][new_position[1]] = FLOOR_TILE

def game_over():
    pass


if __name__ == '__main__':
    game_is_run = True
    while game_is_run:
        first_level, player = main_menu()
        exit_data = game_loop(player, first_level)
        if exit_data == EXIT_TO_MAIN_MENU:
            pass
