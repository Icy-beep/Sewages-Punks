from src.businesslogic_upper import *
from src.display import *
from src.entities import *
from src.constants import *

import msvcrt
import json
import datetime


def adventuring(dungeon_map, player_data):
    return_to_main_menu = False
    adventuring_not_end = True

    while adventuring_not_end:
        clear_display()
        show_dungeon_map(dungeon_map, player_data)
        show_movement_legend()

        char = msvcrt.getch()

        if char == ESC:
            while True:
                show_ingame_menu()

                choice = input(f"\n    {MAGENTA_TEXT_BRIGHT}WAITING FOR INPUT... > {RESET}").lower()

                if choice in RESUME:
                    break

                if choice in SAVE:
                    save_game(player_data, dungeon_map)

                if choice in LOAD:
                    loaded = load_game()
                    if loaded:
                        dungeon_map, player_data = loaded
                        print(f"{GREEN_TEXT_BRIGHT}[ DATA OVERWRITTEN FROM RESTORE POINT ]{RESET}")

                if choice in QUIT_TO_MAIN_MENU:
                    return_to_main_menu = True
                    break

                if choice not in IN_GAME_MENU_COMMANDS:
                    print(f"    {RED_TEXT_BRIGHT}INVALID COMMAND. RE-ENTER.{RESET}")

        if return_to_main_menu:
            new_position = 0
            return RETURN_TO_MAIN_MENU, new_position

        user_input = char.decode('utf-8', errors='ignore').lower()

        if user_input in MOVEMENT_COMMANDS:
            new_position = movement_player(dungeon_map, user_input)
        else:
            continue

        if dungeon_map[new_position[x_coord]][new_position[y_coord]] == CHEST_TILE:

            item = open_chest()

            if item == ITEM_DEFUSAL_KIT:
                player_data[PLAYER_ITEM_DEFUSAL_KIT] += 1
                clear_display()
                loot_message(item)
                enter_continue()
                clear_display()
                dungeon_map[new_position[x_coord]][new_position[y_coord]] = FLOOR_TILE

            if item == ITEM_NOTHING:
                clear_display()
                loot_message(item)
                enter_continue()
                clear_display()
                dungeon_map[new_position[x_coord]][new_position[y_coord]] = FLOOR_TILE
                continue

        if dungeon_map[new_position[x_coord]][new_position[y_coord]] == EXIT_TILE:
            clear_display()
            print(YOU_TRY_OPEN_DOR_MESSAGE)
            enter_continue()

            door_case = True

            while door_case:
                clear_display()
                exit_interactions()
                user_input = input('>>')

                if user_input not in DOOR_INTERACTION_COMMANDS:
                    continue

                if user_input == '1':
                    if player_data[PLAYER_ITEM_KEY] >= 1:
                        clear_display()

                        choosing = True
                        while choosing:
                            key_card_options_menu()
                            user_input = input('>>')

                            if user_input == '1':
                                clear_display()
                                print(CARD_READER_MESSAGE)
                                enter_continue()
                                return EXFILL, new_position

                            if user_input == '2':
                                clear_display()
                                print(DOOR_INTERACTION_MESSAGE)
                                choosing = False
                                door_case = False

                if user_input == '2':
                    clear_display()
                    print(KICK_THE_DOOR_MESSAGE)
                    enter_continue()
                    continue

                if user_input == '3':
                    clear_display()
                    print(STEP_OUT_THE_DOOR_MESSAGE)
                    door_case = False

        if dungeon_map[new_position[x_coord]][new_position[y_coord]] == KEY_TILE:
            clear_display()
            print(YOU_FOUND_KEY_CARD_MESSAGE)
            player_data[PLAYER_ITEM_KEY] += 1
            enter_continue()
            dungeon_map[new_position[x_coord]][new_position[y_coord]] = FLOOR_TILE

        if dungeon_map[new_position[x_coord]][new_position[y_coord]] == TRAP_TILE:
            clear_display()
            print(TRAP_FORWARD_MESSAGE)

            trap_case = True

            while trap_case:
                trap_inputs()
                user_input = input('>>')
                if user_input not in TRAP_COMMANDS:
                    continue

                if user_input == '1':
                    defuse = defuse_trap(player_data)
                    if defuse:
                        player_data[PLAYER_ITEM_DEFUSAL_KIT] -= 1
                        clear_display()
                        print(TRAP_DEFUSED_MESSAGE)
                        enter_continue()
                        dungeon_map[new_position[x_coord]][new_position[y_coord]] = FLOOR_TILE
                        trap_case = False
                    if not defuse:
                        clear_display()
                        print(YOU_DONT_HAVE_DEFKIT_MESSAGE)
                        enter_continue()
                        continue


                if user_input == '2':
                    defuse = defuse_trap_run()
                    if defuse:
                        clear_display()
                        print(TRAP_ACTIVATED_MESSAGE)
                        enter_continue()
                        dungeon_map[new_position[x_coord]][new_position[y_coord]] = FLOOR_TILE
                        trap_case = False
                    else:
                        clear_display()
                        print(TRAP_DAMAGED_PLAYER_IF_HE_RUN_MESSAGE)
                        enter_continue()
                        player_data[ENTITY_HP] -= 5
                        dungeon_map[new_position[x_coord]][new_position[y_coord]] = FLOOR_TILE
                        trap_case = False


        is_fight = try_start_fight(dungeon_map, new_position)

        if is_fight:
            return FIGHT, new_position

    return EXIT


def fight(player_data):

    is_fight = True
    count_of_use_heal = 0
    enemy_data = create_enemy()
    clear_display()
    print(start_fight_message(enemy_data))
    enter_continue()

    initiative_throw_message()
    player_data, enemy_data = initiative_throw(player_data, enemy_data)
    throw_animation(player_data, enemy_data)
    enter_continue()
    clear_display()

    count_of_heal = 4

    enemy_step = False
    player_step = False

    enemy_win = False
    player_win = False

    if player_data[ENTITY_INITIATIVE] > enemy_data[ENTITY_INITIATIVE]:
        player_step = True
    else:
        enemy_step = True

    while is_fight:

        if player_win or enemy_win:
            break

        if player_step:
            print(message_about_step(enemy = 0, player = 1))

            show_combat_legend()
            user_input = input('>>')

            if user_input not in COMBAT_COMMANDS:
                clear_display()
                continue

            if user_input == 'a':

                damage = player_data[ENTITY_DAMAGE]
                damage = randomise_damage(damage)

                is_miss = try_ruin_attack_for_player(player_data)

                if is_miss:
                    clear_display()
                    print(player_miss())
                    enter_continue()
                    clear_display()
                    player_step = False
                    enemy_step = True
                    continue


                enemy_data[ENTITY_HP] -= damage

                clear_display()
                hit_message(damage, 'player')
                show_enemy_hp(enemy_data)
                enter_continue()
                clear_display()

                if enemy_data[ENTITY_HP] <= 0:
                    player_win = True

            if user_input == 'd':
                enemy_data[ENTITY_MISS_CHANCE] += 0.4

                clear_display()
                print(PLAYER_TRY_DODGE_MESSAGE)
                enter_continue()
                clear_display()

            if user_input == 'h':
                if count_of_heal > 0:

                    player_data[ENTITY_HP] = min(100, player_data[ENTITY_HP] + 10)
                    count_of_heal -= 1
                    count_of_use_heal += 1

                    print(heal_message())
                    show_player_hp(player_data)

                    if count_of_use_heal > 1:
                        player_data[ENTITY_TOXICITY] += 1
                        print(toxication_message())

                        if player_data[ENTITY_TOXICITY] >= 2:
                            player_data[ENTITY_HP] -= 5
                            toxication_damage_message()
                            show_player_hp(player_data)

                    enter_continue()
                    clear_display()

                else:
                    print(empty_heal_message())
                    enter_continue()
                    clear_display()

                continue

            if user_input == 'i':
                show_battle_information(player_data, enemy_data)
                enter_continue()

                continue


            player_step = False
            enemy_step = True

        if enemy_step:
            if enemy_data[ENTITY_HP] <= 0:
                continue

            who = ENEMY_WORD_VARIABLE
            print(message_about_step(player = 0, enemy = 1))

            damage = enemy_data[ENTITY_DAMAGE]
            damage = randomise_damage(damage)

            is_miss = try_ruin_attack_for_enemy(enemy_data)

            if is_miss:
                print(ENEMY_MISS_MESSAGE)
                enter_continue()
                clear_display()
                enemy_step = False
                player_step = True
                continue

            player_data[ENTITY_HP] -= damage
            hit_message(damage, who)
            show_player_hp(player_data)
            enter_continue()
            clear_display()

            if player_data[ENTITY_HP] <= 0:
                print(ENEMY_WIN_MESSAGE)
                enter_continue()
                enemy_win = True



            enemy_step = False
            player_step = True


def get_unique_filename(base_name):
    filename = os.path.join(SAVE_DIR, f"{base_name}.json")
    counter = 1

    while os.path.exists(filename):
        temp_name = f"{base_name}_{counter}"
        filename = os.path.join(SAVE_DIR, f"{temp_name}.json")
        counter += 1

    return filename


def save_game(player_data, dungeon):
    if not os.path.exists(SAVE_DIR):
        os.makedirs(SAVE_DIR)

    print(f"\n{MAGENTA_TEXT_BRIGHT}[ SAVE AS... ]{RESET}")
    user_name = input(f"{MAGENTA_TEXT_BRIGHT}>>> {RESET}").strip()

    if not user_name:
        user_name = "savegame"

    user_name = "".join(c for c in user_name if c.isalnum() or c in (' ', '_', '-')).rstrip()

    timestamp = datetime.datetime.now().strftime("%Y-%m-%d_%H-%M")

    full_name = f"{user_name}_{timestamp}"

    final_path = get_unique_filename(full_name)

    data = {
        "player": player_data,
        "dungeon": dungeon,
    }

    try:
        with open(final_path, "w", encoding="utf-8") as f:
            json.dump(data, f, ensure_ascii=False, indent=4)

        actual_name = os.path.basename(final_path)
        print(f"{GREEN_TEXT_BRIGHT}[ SYNCHRONIZE: {actual_name} WRITE SUCCESSFUL ]{RESET}")
        return True
    except Exception as e:
        print(f"{RED_TEXT_BRIGHT}[ SYNC INTERRUPTED: DATA LOSS DETECTED {e} ]{RESET}")
        return False


def load_game():
    """
    Выводит список всех файлов в папке saves и дает выбрать нужный.
    """
    if not os.path.exists(SAVE_DIR): return None

    files = [f for f in os.listdir(SAVE_DIR) if f.endswith('.json')]
    files.sort(key=lambda x: os.path.getmtime(os.path.join(SAVE_DIR, x)), reverse=True)

    if not files:
        print(f"{RED_TEXT_BRIGHT}[ ERROR: DATA IS NONE IN THAT SECTOR ]{RESET}")
        return None

    print(f"\n{MAGENTA_TEXT_BRIGHT}--- [ ACTIVE RESTORE POINTS ] ---{RESET}")
    for i, file in enumerate(files, 1):
        path = os.path.join(SAVE_DIR, file)
        mtime = os.path.getmtime(path)
        date_str = datetime.datetime.fromtimestamp(mtime).strftime('%d.%m %H:%M')

        print(f"  {i}. {file.ljust(25)} | {BLUE_TEXT_BRIGHT}{date_str}{RESET}")

    try:
        choice = int(input(f"\n{MAGENTA_TEXT_BRIGHT}CHOOSE THE INDEX > {RESET}")) - 1
        if 0 <= choice < len(files):
            with open(os.path.join(SAVE_DIR, files[choice]), "r", encoding="utf-8") as f:
                data = json.load(f)
                return data["dungeon"], data["player"]
    except (ValueError, IndexError):
        print(f"{RED_TEXT_BRIGHT}[ ERROR: WRONG INDEX ]{RESET}")

    return None


def get_player_nickname():
    while True:
        print(f"\n{LIGHT_BLUE_TEXT_BRIGHT}[ SYSTEM ]:# Identify yourself.{RESET}")
        nick = input(">> ").strip()
        if not nick:
            clear_display()
            print(f"{RED_TEXT_BRIGHT}[ ERROR ]:# Identification failed. Input cannot be empty.{RESET}")
        elif len(nick) > 16:
            clear_display()
            print(f"{RED_TEXT_BRIGHT}[ ERROR ]:# Identity too long (max 16 chars).{RESET}")
        else:
            clear_display()
            print(f"{MAGENTA_TEXT_BRIGHT}[ SYSTEM ]:# Identity confirmed. Your nickname:{nick}{RESET}\n")
            return nick










