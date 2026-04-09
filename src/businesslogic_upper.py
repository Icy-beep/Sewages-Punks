import random
from src.businesslogic_lower import *
from src.constants import *
from src.entities import *

def create_dungeon():
    """
    Генерирует двумерную карту подземелья, интегрируя геометрию уровня и игровые объекты.

    Функция пошагово формирует структуру:
    1. Создает сетку стен и размещает выход - (`EXIT_TILE`).
    2. Генерирует проходимые пути и размещает игрока - (`PLAYER_TILE`).
    3. Случайно распределяет врагов, ловушки, сундуки и ключи на доступных участках пола.

    Зависимости от констант:
    - Размеры: `DUNGEON_HEIGHT`, `DUNGEON_WIDTH`.
    - Тайлы: `WALL_TILE`, `FLOOR_TILE`, `PLAYER_TILE`, `EXIT_TILE`, `ENEMY_TILE`, `TRAP_TILE`, `CHEST_TILE`, `KEY_TILE`.
    - Лимиты: `MIN_ENEMY`/`MAX_ENEMY`, `MIN_TRAPS`/`MAX_TRAPS`, `MIN_CHESTS`/`MAX_CHESTS`, `AMT_KEY`.

    Внешние вызовы:
    - `generate_passes()`: расчет координат проходов.
    - `generate_possible_tiles_for_...()`: фильтрация пустых клеток для спавна объектов.

    :return: list[list] — двумерный массив (сетка) игрового мира.
    """

    dungeon_map = initialize_empty_dungeon(DUNGEON_HEIGHT, DUNGEON_WIDTH, WALL_TILE)
    place_exit(dungeon_map)

    apply_passes(dungeon_map, generate_passes(), FLOOR_TILE, PLAYER_TILE)

    spawn_objects(dungeon_map, CHEST_TILE, random.randint(MIN_CHESTS, MAX_CHESTS),
                  near_wall=True)

    spawn_objects(dungeon_map, TRAP_TILE, random.randint(MIN_TRAPS, MAX_TRAPS),
                  forbidden={CHEST_TILE})

    spawn_objects(dungeon_map, ENEMY_TILE, random.randint(MIN_ENEMY, MAX_ENEMY),
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






