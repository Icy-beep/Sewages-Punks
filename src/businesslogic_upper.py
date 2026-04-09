import random

from src.display import *
from src.businesslogic_lower import *
from src.constants import *
from src.entities import *

def create_dungeon() -> list[list[int]]:
    """
    Генерирует процедурное подземелье, используя пошаговый алгоритм наполнения.

    Порядок работы:
    1. Инициализация пустой сетки и размещение выхода.
    2. Прокладка геометрии коридоров и установка игрока.
    3. Последовательный спавн объектов с контролем наложения (forbidden tiles):
       - Сундуки (приоритет: тупики и стены).
       - Ловушки (исключая сундуки).
       - Враги (исключая сундуки и ловушки).
       - Ключи (приоритет: позиции за спиной врагов).

    :return: list[list[int]] — двумерный массив (сетка), представляющий игровой мир.
    """

    dungeon_map = initialize_empty_dungeon(DUNGEON_HEIGHT, DUNGEON_WIDTH, WALL_TILE)
    place_exit(dungeon_map)

    apply_passes(dungeon_map, generate_passes(), FLOOR_TILE, PLAYER_TILE)

    spawn_objects(dungeon_map, tile_type=CHEST_TILE, count=random.randint(MIN_CHESTS, MAX_CHESTS),
                  near_wall=True)

    spawn_objects(dungeon_map, tile_type=TRAP_TILE, count=random.randint(MIN_TRAPS, MAX_TRAPS),
                  forbidden={CHEST_TILE})

    spawn_objects(dungeon_map, tile_type=ENEMY_TILE, count=random.randint(MIN_ENEMY, MAX_ENEMY),
                  forbidden={CHEST_TILE, TRAP_TILE})

    spawn_objects(dungeon_map, KEY_TILE, AMT_KEY,
                  forbidden={ENEMY_TILE, TRAP_TILE, CHEST_TILE},
                  behind_enemy=True)

    return dungeon_map

def movement_player(location: list[list[int]], command: str) -> list[int]:

    position = search_player_position(location)
    old_position = position
    new_position = position[:]

    if command == COMMAND_MOVE_UP:
        new_position[x_coord] -= 1
    if command == COMMAND_MOVE_LEFT:
        new_position[y_coord] -= 1
    if command == COMMAND_MOVE_DOWN:
        new_position[x_coord] += 1
    if command == COMMAND_MOVE_RIGHT:
        new_position[y_coord] += 1

    target_tile = location[new_position[x_coord]][new_position[y_coord]]

    if target_tile == WALL_TILE:
        return new_position

    if target_tile == ENEMY_TILE:
        return new_position

    if target_tile == TRAP_TILE:
        return new_position

    if target_tile == CHEST_TILE:
        return new_position

    if target_tile == KEY_TILE:
        return new_position

    if target_tile == EXIT_TILE:
        return new_position


    location[old_position[x_coord]][old_position[y_coord]] = FLOOR_TILE
    location[new_position[x_coord]][new_position[y_coord]] = PLAYER_TILE

    return new_position


def handle_trap(location, player_data, position):
    x, y = position
    clear_display()
    print(TRAP_FORWARD_MESSAGE)

    while True:
        trap_inputs()
        user_input = input('>>')

        if user_input not in TRAP_COMMANDS:
            continue

        if user_input == '1':  # Разминировать
            if defuse_trap(player_data):
                player_data[PLAYER_ITEM_DEFUSAL_KIT] -= 1
                clear_display()
                print(TRAP_DEFUSED_MESSAGE)
                enter_continue()
                location[x][y] = FLOOR_TILE
                return  # Выходим из функции, ловушка обезврежена
            else:
                clear_display()
                print(YOU_DONT_HAVE_DEFKIT_MESSAGE)
                enter_continue()
                # Не выходим из цикла, даем выбрать другой вариант

        if user_input == '2':  # Пробежать
            if defuse_trap_run():  # Шанс успеха
                clear_display()
                print(TRAP_ACTIVATED_MESSAGE)
            else:
                clear_display()
                print(TRAP_DAMAGED_PLAYER_IF_HE_RUN_MESSAGE)
                player_data[ENTITY_HP] -= 5

            enter_continue()
            location[x][y] = FLOOR_TILE
            return


def handle_exit(player_data):
    clear_display()
    print(YOU_TRY_OPEN_DOR_MESSAGE)
    enter_continue()

    while True:
        clear_display()
        exit_interactions()
        user_input = input('>>')

        if user_input not in DOOR_INTERACTION_COMMANDS:
            continue

        if user_input == '1': # Использовать ключ
            if player_data[PLAYER_ITEM_KEY] >= 1:
                while True:
                    clear_display()
                    key_card_options_menu()
                    choice = input('>>')
                    if choice == '1':
                        clear_display()
                        print(CARD_READER_MESSAGE)
                        enter_continue()
                        return True # СИГНАЛ НА ВЫХОД (EXFILL)
                    if choice == '2':
                        break # Возврат к выбору у двери
            else:
                # Тут можно добавить сообщение "У вас нет ключа"
                pass

        if user_input == '2': # Выбить дверь
            clear_display()
            print(KICK_THE_DOOR_MESSAGE)
            enter_continue()

        if user_input == '3': # Отойти
            clear_display()
            print(STEP_OUT_THE_DOOR_MESSAGE)
            return False # Игрок остается в игре


def handle_chest(location, player_data, position):
    x, y = position
    item = open_chest()
    clear_display()
    loot_message(item)

    if item == ITEM_DEFUSAL_KIT:
        player_data[PLAYER_ITEM_DEFUSAL_KIT] += 1

    enter_continue()
    location[x][y] = FLOOR_TILE


def handle_key_pickup(location, player_data, position):
    x, y = position
    clear_display()
    print(YOU_FOUND_KEY_CARD_MESSAGE)

    player_data[PLAYER_ITEM_KEY] += 1
    location[x][y] = FLOOR_TILE

    enter_continue()


def try_start_fight(location, new_position) -> bool:

    if_fight = False

    if location[new_position[0]][new_position[1]] == ENEMY_TILE:
        if_fight = True

    return if_fight

def create_enemy():

    enemy = choose_enemy()

    copy_of_enemy = enemy[:]

    return copy_of_enemy

def initiative_throw(player_data, enemy_data):
    import random
    left_border = 0
    right_border = 5

    throw_is_good = False

    while not throw_is_good:
        player_initiative = player_data[ENTITY_INITIATIVE]
        enemy_initiative = enemy_data[ENTITY_INITIATIVE]

        player_throw = random.randint(left_border, right_border)
        enemy_throw = random.randint(left_border, right_border)

        player_initiative += player_throw
        enemy_initiative += enemy_throw

        if player_initiative > 10:
            player_initiative = 10

        if enemy_initiative > 10:
            enemy_initiative = 10

        if player_initiative > enemy_initiative or enemy_initiative > player_initiative:
            throw_is_good = True

    player_data[ENTITY_INITIATIVE] = player_initiative
    enemy_data[ENTITY_INITIATIVE] = enemy_initiative

    return player_data, enemy_data

def randomise_damage(damage):
    import random

    left_border = -2
    right_border = 2

    random_damage = random.randint(left_border, right_border)

    damage += random_damage
    return damage

def try_ruin_attack_for_player(player_data):
    import random

    throw = random.random()

    if throw < player_data[ENTITY_MISS_CHANCE]:
        return True

    return False

def try_ruin_attack_for_enemy(enemy_data):
    import random

    throw = random.random()

    if throw < enemy_data[ENTITY_MISS_CHANCE]:
        return True

    return False

def defuse_trap(player_data):

    if player_data[PLAYER_ITEM_DEFUSAL_KIT] >= 1:
        return True
    else:
        return False

def defuse_trap_run():
    import random

    chance = BASE_CHANCE - 0.70

    if random.random() < chance:
        return True
    else:
        return False

def open_chest():
    import random

    item = random.randint(0, 1)

    return item






