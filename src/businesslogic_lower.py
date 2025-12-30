from src.constants import *

def generate_i_path():
    import random

    generate_i_pass_1 = random.randint(3, 8)

    return generate_i_pass_1

def generate_passes():
    import random
    from src.constants import HOW_MANY_PASSES_MAX, HOW_MUCH_WALLS_WHERE_PASS

    passes = []

    for i in range(HOW_MUCH_WALLS_WHERE_PASS):
        passes.append([])
        how_much_passes = random.randint(1, 2)
        for j in range(HOW_MANY_PASSES_MAX):
            if how_much_passes == 1:
                passes[i].append(generate_i_path())
                continue

            if how_much_passes == 2:
                passes[i].append(generate_i_path())
                passes[i].append(generate_i_path())

    return passes

def generate_possible_tiles_for_enemy(dungeon_map):
    from src.constants import DUNGEON_HEIGHT, DUNGEON_WIDTH, FLOOR_TILE

    possible_tiles = []
    for i in range(DUNGEON_HEIGHT):
        for j in range(DUNGEON_WIDTH):
            if dungeon_map[i][j] == FLOOR_TILE and dungeon_map[i][j] != PLAYER_TILE:
                if i == 1 and j <= 4:
                    continue
                possible_tiles.append((i, j))

    return possible_tiles

def generate_possible_tiles_for_traps(dungeon_map):
    from src.constants import DUNGEON_HEIGHT, DUNGEON_WIDTH, FLOOR_TILE, ENEMY_TILE

    possible_tiles = []
    for i in range(DUNGEON_HEIGHT):
        for j in range(DUNGEON_WIDTH):
            if dungeon_map[i][j] == FLOOR_TILE and dungeon_map[i][j] != PLAYER_TILE and dungeon_map[i][j] != ENEMY_TILE:
                if i == 1 and j <= 4:
                    continue
                possible_tiles.append((i, j))

    return possible_tiles

def generate_possible_tiles_for_chests(dungeon_map):
    from src.constants import DUNGEON_HEIGHT, DUNGEON_WIDTH, FLOOR_TILE, ENEMY_TILE, TRAP_TILE

    possible_tiles = []
    for i in range(DUNGEON_HEIGHT):
        for j in range(DUNGEON_WIDTH):
            if dungeon_map[i][j] == FLOOR_TILE and dungeon_map[i][j] != PLAYER_TILE and dungeon_map[i][j] != ENEMY_TILE and dungeon_map[i][j] != TRAP_TILE:
                if i == 1 and j <= 4:
                    continue

                if i % 2 == 0 or 1 < j < 12:
                    continue
                possible_tiles.append((i, j))

    return possible_tiles

def generate_possible_tiles_for_key(dungeon_map):
    from src.constants import DUNGEON_HEIGHT, DUNGEON_WIDTH, FLOOR_TILE, ENEMY_TILE, TRAP_TILE, CHEST_TILE

    possible_tiles = []
    for i in range(DUNGEON_HEIGHT):
        for j in range(DUNGEON_WIDTH):
            if dungeon_map[i][j] == FLOOR_TILE and dungeon_map[i][j] != PLAYER_TILE and dungeon_map[i][j] != ENEMY_TILE and dungeon_map[i][j] != TRAP_TILE and dungeon_map[i][j] != CHEST_TILE:
                if i == 1 and j <= 4:
                    continue

                if dungeon_map[i][j] == ENEMY_TILE:
                    if dungeon_map[i][j + 1] == FLOOR_TILE and dungeon_map[i][j + 1] != PLAYER_TILE and dungeon_map[i][j + 1] != ENEMY_TILE and dungeon_map[i][j + 1] != TRAP_TILE and dungeon_map[i][j + 1] != CHEST_TILE:
                        possible_tiles.append((i, j + 1))

                if i % 2 == 0 or 1 < j < 12:
                    continue

    if not possible_tiles:
        for i in range(DUNGEON_HEIGHT):
            for j in range(DUNGEON_WIDTH):
                if dungeon_map[i][j] == FLOOR_TILE and dungeon_map[i][j] != PLAYER_TILE and dungeon_map[i][j] != ENEMY_TILE and dungeon_map[i][j] != TRAP_TILE and dungeon_map[i][j] != CHEST_TILE:
                    if i == 1 and j <= 4:
                        continue

                    if i % 2 == 0 or 1 < j < 12:
                        continue
                    possible_tiles.append((i, j))



    return possible_tiles

def search_player_position(location: list[list[int]]) -> list[int] | None:

    rows = len(location)
    columns = len(location[0])

    player_position = []

    for x in range(rows):
        for y in range(columns):
            if location[x][y] == PLAYER_TILE:
                player_position.append(x)
                player_position.append(y)
                return player_position

    return None