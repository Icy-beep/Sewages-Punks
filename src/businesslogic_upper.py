from src.businesslogic_lower import *
from src.constants import *
from src.entities import *

def create_dungeon():
    """

    :return: Возвращает карту подземелья
    """
    import random
    dungeon_map = []

    exit_index = random.randint(1, 12)

    for i in range(0, DUNGEON_HEIGHT):
        dungeon_map.append([])
        for j in range(0, DUNGEON_WIDTH):
            if i == 0:
                dungeon_map[i].append(WALL_TILE)

            if 0 < i < 10:
                dungeon_map[i].append(WALL_TILE)

            if i == 10:
                if j == exit_index:
                    dungeon_map[i].append(EXIT_TILE)

                dungeon_map[i].append(WALL_TILE)

    passes = generate_passes()

    for i in range(0, DUNGEON_HEIGHT):
        for j in range(0, DUNGEON_WIDTH):
            if i % 2 != 0 and 1 <= j <= 12:
                dungeon_map[i][j] = FLOOR_TILE
                dungeon_map[1][1] = PLAYER_TILE
            if i == 2:
                dungeon_map[i][passes[0][0]] = FLOOR_TILE
                dungeon_map[i][passes[0][1]] = FLOOR_TILE
            if i == 4:
                dungeon_map[i][passes[1][0]] = FLOOR_TILE
                dungeon_map[i][passes[1][1]] = FLOOR_TILE
            if i == 6:
                dungeon_map[i][passes[2][0]] = FLOOR_TILE
                dungeon_map[i][passes[2][1]] = FLOOR_TILE
            if i == 8:
                dungeon_map[i][passes[3][0]] = FLOOR_TILE
                dungeon_map[i][passes[3][1]] = FLOOR_TILE

    possible_tiles = generate_possible_tiles_for_enemy(dungeon_map)
    how_many_enemies = random.randint(MIN_ENEMY, MAX_ENEMY)
    enemy_coordinates = random.sample(possible_tiles, how_many_enemies)

    for tile, how_many in enemy_coordinates:
        dungeon_map[tile][how_many] = ENEMY_TILE

    possible_tiles = generate_possible_tiles_for_traps(dungeon_map)
    how_many_traps = random.randint(MIN_TRAPS, MAX_TRAPS)
    traps_coordinates = random.sample(possible_tiles, how_many_traps)

    for tile, how_many in traps_coordinates:
        dungeon_map[tile][how_many] = TRAP_TILE

    possible_tiles = generate_possible_tiles_for_chests(dungeon_map)
    how_many_chests = random.randint(MIN_CHESTS, MAX_CHESTS)
    chests_coordinates = random.sample(possible_tiles, how_many_chests)

    for tile, how_many in chests_coordinates:
        dungeon_map[tile][how_many] = CHEST_TILE

    possible_tiles = generate_possible_tiles_for_key(dungeon_map)
    how_many_keys = AMT_KEY
    key_coordinates = random.sample(possible_tiles, how_many_keys)

    for tile, how_many in key_coordinates:
        dungeon_map[tile][how_many] = KEY_TILE


    return dungeon_map

def movement_player(location: list[list[int]], command: str) -> list[int]:

    position = search_player_position(location)
    old_position = position
    new_position = position[:]

    if command == COMMAND_MOVE_UP:
        new_position[0] -= 1
    if command == COMMAND_MOVE_LEFT:
        new_position[1] -= 1
    if command == COMMAND_MOVE_DOWN:
        new_position[0] += 1
    if command == COMMAND_MOVE_RIGHT:
        new_position[1] += 1

    target_tile = location[new_position[0]][new_position[1]]

    if target_tile == WALL_TILE:
        return new_position

    if target_tile == ENEMY_TILE:
        return new_position

    location[old_position[0]][old_position[1]] = FLOOR_TILE
    location[new_position[0]][new_position[1]] = PLAYER_TILE

    return new_position

def try_start_fight(location, new_position) -> bool:

    if_fight = False

    if location[new_position[0]][new_position[1]] == ENEMY_TILE:
        if_fight = True

    return if_fight

def create_enemy():
    #import random

    enemy = choose_enemy()
    copy_of_enemy = enemy[:]

    # hp_random = random.randint(0, 40)
    # initiative_random = random.randint(1, 2)
    #
    # if random.random() < BASE_CHANCE - 0.80:
    #     if enemy[ENTITY_HP] <= 70:
    #         enemy[ENTITY_HP] = enemy[ENTITY_HP] + hp_random
    #     else:
    #         enemy[ENTITY_HP] = enemy[ENTITY_HP] - hp_random
    #
    # if enemy[ENTITY_INITIATIVE] < 5:
    #     if random.random() <= BASE_CHANCE - 0.50:
    #         enemy[ENTITY_INITIATIVE] + initiative_random
    # if enemy[ENTITY_INITIATIVE] > 5:
    #     if random.random() <= BASE_CHANCE - 0.50:
    #         enemy[ENTITY_INITIATIVE] - initiative_random

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








