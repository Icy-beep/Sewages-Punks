import sys
import os
import msvcrt

from src.core import *
from pregen_levels.tutorial_level import create_tutorial_dungeon
from src.display import draw_main_menu
from src.constants import *
from src.entities import create_default_player
from src.localization import MAIN_MENU


def main_menu():
    in_main_menu = True
    player_nick = 'Operator'
    while in_main_menu:
        clear_display()
        draw_main_menu()
        prompt = MAIN_MENU['player_input'].format(PLAYER_NAME=player_nick)
        choice = input(prompt).strip()

        if choice.lower() in NEW_GAME_COMMANDS:
            dungeon = create_tutorial_dungeon()
            default_player = create_default_player()
            return dungeon, default_player

        elif choice.lower() in LOAD_GAME_COMMANDS:
            saved_data = load_game()
            if saved_data:
                prompt = MAIN_MENU['decrypting_successful'].format(MAIN_CHARACTER_NAME = MAIN_CHARACTER_NAME)
                print(prompt)
                enter_continue()
                return saved_data
            else:
                print(MAIN_MENU['no_data_on_sector'])
                enter_continue()

        elif choice.lower() in SETTING_GAME_COMMANDS:
            clear_display()
            show_setting_stub()

        elif choice.lower() in EXIT_GAME_COMMANDS:
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
            art = game_over()
            flush_input()
            clear_display()
            slow_print(art, 0.01)
            flush_input()
            enter_continue()

            break
        dungeon[new_position[0]][new_position[1]] = FLOOR_TILE


if __name__ == '__main__':
    game_is_run = True
    start_message_already_show = False
    while game_is_run:
        first_level, player, = main_menu()
        if not start_message_already_show:
            print(skip_message())
            skip = input('>>').lower()
            if skip in SKIP_PROLOGUE_COMMANDS_NO:
                clear_display()
                start_message()

                flush_input()
                enter_continue()

                start_message_already_show = True

        exit_data = game_loop(player, first_level)
        if exit_data == EXIT_TO_MAIN_MENU:
            continue
