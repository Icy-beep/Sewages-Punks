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

    return dungeon_map