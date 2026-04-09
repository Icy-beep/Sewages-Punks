import random
from src.constants import *
from src.entities import *

def generate_i_path():
    generate_i_pass_1 = random.randint(3, 8)

    return generate_i_pass_1

def generate_passes():
    passes = []

    for _ in range(HOW_MUCH_WALLS_WHERE_PASS):
        count = random.randint(1, 2)

        current_wall_passes = set()
        while len(current_wall_passes) < count:
            current_wall_passes.add(generate_i_path())

        passes.append(list(current_wall_passes))

    return passes


def initialize_empty_dungeon(height, width, wall_tile):
    return [[wall_tile for _ in range(width)] for _ in range(height)]


def place_exit(dungeon_map):
    height = len(dungeon_map)
    width = len(dungeon_map[0])
    exit_col = random.randint(1, width - 2)
    dungeon_map[height - 1][exit_col] = EXIT_TILE


def apply_passes(dungeon_map, passes, floor_tile, player_tile):
    for i in range(1, len(dungeon_map), 2):
        for j in range(1, len(dungeon_map[i]) - 1):
            dungeon_map[i][j] = floor_tile

    for idx, columns in enumerate(passes):
        row = (idx + 1) * 2.
        if row < len(dungeon_map):
            for col in columns:
                if col < len(dungeon_map[row]):
                    dungeon_map[row][col] = floor_tile

    dungeon_map[1][1] = player_tile


def get_possible_tiles(dungeon_map, forbidden_tiles=None, must_be_near_wall=False, behind_enemy=False):

    forbidden = {PLAYER_TILE, ENEMY_TILE, WALL_TILE, CHEST_TILE, KEY_TILE, EXIT_TILE, TRAP_TILE}
    if forbidden_tiles:
        forbidden.update(forbidden_tiles)

    possible_tiles = []

    for i in range(DUNGEON_HEIGHT):
        for j in range(DUNGEON_WIDTH):
            if behind_enemy:
                if dungeon_map[i][j] == ENEMY_TILE:
                    if j + 1 < DUNGEON_WIDTH and dungeon_map[i][j + 1] == FLOOR_TILE:
                        if (i, j + 1) not in forbidden:
                            possible_tiles.append((i, j + 1))
                continue

            if dungeon_map[i][j] == FLOOR_TILE and dungeon_map[i][j] not in forbidden:
                if i == 1 and j <= 4:
                    continue

                if must_be_near_wall:
                    if i % 2 == 0 or (j <= 1 or j >= 12):
                        possible_tiles.append((i, j))
                else:
                    possible_tiles.append((i, j))

    if behind_enemy and not possible_tiles:
        return get_possible_tiles(dungeon_map, forbidden_tiles, must_be_near_wall=True)

    return possible_tiles


def spawn_objects(dungeon_map, tile_type, count, forbidden=None, near_wall=False, behind_enemy=False):
    possible = get_possible_tiles(dungeon_map, forbidden_tiles=forbidden,
                                  must_be_near_wall=near_wall, behind_enemy=behind_enemy)

    count = min(len(possible), count)
    for r, c in random.sample(possible, count):
        dungeon_map[r][c] = tile_type


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

def choose_enemy():
     import random

     choosing = random.randint(1, 4)

     if choosing == 1:
         enemy = punk[:]

     if choosing == 2:
         enemy = synth_hound[:]

     if choosing == 3:
         enemy = glitch_butcher[:]

     if choosing == 4:
         enemy = psy_coder[:]

     return enemy


