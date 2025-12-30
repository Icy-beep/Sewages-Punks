from src.businesslogic_lower import *
from src.constants import *

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







        return dungeon_map