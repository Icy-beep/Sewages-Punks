from src.businesslogic_upper import *
from src.display import *
from src.entities import *
from src.constants import *

import msvcrt
import json
import datetime


INTERACTIONS = {
    CHEST_TILE: handle_chest,
    KEY_TILE: handle_key_pickup,
    TRAP_TILE: handle_trap,
}


def adventuring(dungeon_map, player_data):
    while True:
        clear_display()
        show_dungeon_map(dungeon_map, player_data)
        show_movement_legend()

        command = get_user_command()

        if command == PAUSE:
            status = handle_pause_menu(player_data, dungeon_map)
            if status == RETURN_TO_MAIN_MENU:
                return RETURN_TO_MAIN_MENU, 0
            continue

        if command in MOVEMENT_COMMANDS:
            new_position = movement_player(dungeon_map, command)
            tile = dungeon_map[new_position[x_coord]][new_position[y_coord]]

            if tile == WALL_TILE:
                continue

            handler = INTERACTIONS.get(tile)
            if handler:
                handler(dungeon_map, player_data, new_position)
            elif tile == EXIT_TILE:
                if handle_exit(player_data):
                    return EXFILL, new_position

            if try_start_fight(dungeon_map, new_position):
                return FIGHT, new_position


def fight(player_data):
    player_data[ENTITY_TOXICITY] = 0
    enemy_data = create_enemy()
    heals_left = 4
    dodge_active = False
    combat_log = ["Connection established.", f"Target: {enemy_data[ENTITY_NAME]} detected."]

    clear_display()
    print(f"\n{MAGENTA_TEXT_BRIGHT}ENCOUNTER_LOG:{RESET} {enemy_data[ENTITY_NAME]} has entered the sector.\n")
    enter_continue()

    player_data, enemy_data = initiative_throw(player_data, enemy_data)
    throw_animation(player_data, enemy_data)
    enter_continue()

    current_turn = "player" if player_data[ENTITY_INITIATIVE] >= enemy_data[ENTITY_INITIATIVE] else "enemy"

    while True:
        if player_data[ENTITY_HP] <= 0:
            return False

        if enemy_data[ENTITY_HP] <= 0:
            draw_combat_interface(player_data, enemy_data, heals_left, combat_log, current_turn)
            enemy_defeated_message(enemy_data)
            return True

        draw_combat_interface(player_data, enemy_data, heals_left, combat_log, current_turn)

        if current_turn == "player":
            action = input().lower()

            if action == 'h':
                msg, success = execute_player_heal(player_data, heals_left)
                combat_log.append(msg)
                if success:
                    heals_left -= 1
                continue

            elif action == 'a':
                combat_log.append(execute_player_attack(player_data, enemy_data))
                current_turn = "enemy"
            elif action == 'd':
                dodge_active = True
                combat_log.append("Evasive maneuvers active. Dodge chance UP.")
                current_turn = "enemy"

            else:
                continue

            time.sleep(0.4)

        else:
            time.sleep(1)
            orig_miss = enemy_data[ENTITY_MISS_CHANCE]
            if dodge_active:
                enemy_data[ENTITY_MISS_CHANCE] += 0.4

            combat_log.append(execute_enemy_attack(enemy_data, player_data))

            enemy_data[ENTITY_MISS_CHANCE] = orig_miss
            dodge_active = False
            current_turn = "player"


def handle_pause_menu(player_data, dungeon_map):
    """
    Управляет меню паузы.
    Возвращает CONTINUE_GAME или RETURN_TO_MAIN_MENU.
    """
    while True:
        show_ingame_menu()
        choice = input(f"\n    {MAGENTA_TEXT_BRIGHT}WAITING FOR INPUT... > {RESET}").lower()

        if choice in RESUME:
            return CONTINUE_GAME

        if choice in SAVE:
            save_game(player_data, dungeon_map)

        if choice in LOAD:
            loaded = load_game()
            if loaded:
                print(f"{GREEN_TEXT_BRIGHT}[ DATA OVERWRITTEN FROM RESTORE POINT ]{RESET}")

        if choice in QUIT_TO_MAIN_MENU:
            return RETURN_TO_MAIN_MENU

        if choice not in IN_GAME_MENU_COMMANDS:
            print(f"    {RED_TEXT_BRIGHT}INVALID COMMAND. RE-ENTER.{RESET}")


def execute_player_attack(player, enemy):
    if try_ruin_attack_for_player(player):
        return f"{RED_TEXT_BRIGHT}MISS!{RESET} Attack failed."
    else:
        dmg = randomise_damage(player[ENTITY_DAMAGE])
        enemy[ENTITY_HP] -= dmg
        return f"Strike successful. {dmg} damage dealt to {enemy[ENTITY_NAME]}."


def execute_player_heal(player, heals_left):
    if heals_left <= 0:
        return f"{RED_TEXT_BRIGHT}ERROR!{RESET} No nanites left.", False

    player[ENTITY_HP] = min(100, player[ENTITY_HP] + 10)
    player[ENTITY_TOXICITY] += 1

    msg = f"Regen active. +10 HP. Toxicity: {player[ENTITY_TOXICITY]}/4."

    if player[ENTITY_TOXICITY] > 4:
        player[ENTITY_HP] -= 8
        player[ENTITY_TOXICITY] -= 1
        msg += f" {RED_TEXT_BRIGHT}TOXIC OVERLOAD!{RESET} -8 HP."

    return msg, True


def execute_enemy_attack(enemy, player):
    if random.random() < enemy[ENTITY_MISS_CHANCE]:
        return f"{enemy[ENTITY_NAME]} {LIGHT_BLUE_TEXT_BRIGHT}MISSED{RESET} their attack."
    else:
        dmg = randomise_damage(enemy[ENTITY_DAMAGE])
        player[ENTITY_HP] -= dmg
        return f"{enemy[ENTITY_NAME]} struck for {RED_TEXT_BRIGHT}{dmg}{RESET} damage."


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










