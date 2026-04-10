from collections import deque
from src.constants import *


def get_path_to_target(start, target_tiles, dungeon_map, occupied_targets):
    rows = len(dungeon_map)
    cols = len(dungeon_map[0])
    queue = deque([(start, [])])
    visited = {tuple(start)}

    while queue:
        (curr_x, curr_y), path = queue.popleft()

        if dungeon_map[curr_x][curr_y] in target_tiles:
            if [curr_x, curr_y] not in occupied_targets:
                return (path[0], [curr_x, curr_y]) if path else None

        for dx, dy in [(-1, 0), (1, 0), (0, -1), (0, 1)]:
            nx, ny = curr_x + dx, curr_y + dy

            if (0 <= nx < rows and 0 <= ny < cols and (nx, ny) not in visited):
                tile = dungeon_map[nx][ny]

                if tile == FLOOR_TILE or tile in target_tiles:
                    visited.add((nx, ny))
                    queue.append(((nx, ny), path + [[nx, ny]]))
    return None


def move_enemies(dungeon_map):
    """Двигает всех врагов к ближайшим СВОБОДНЫМ сундукам/ключам."""
    enemies = []
    for r in range(len(dungeon_map)):
        for c in range(len(dungeon_map[r])):
            if dungeon_map[r][c] == ENEMY_TILE:
                enemies.append((r, c))

    targets = [CHEST_TILE, KEY_TILE]
    occupied_targets = []

    for ex, ey in enemies:
        result = get_path_to_target([ex, ey], targets, dungeon_map, occupied_targets)

        if result:
            next_step, final_target = result
            nx, ny = next_step

            occupied_targets.append(final_target)

            if dungeon_map[nx][ny] == FLOOR_TILE:
                dungeon_map[ex][ey] = FLOOR_TILE
                dungeon_map[nx][ny] = ENEMY_TILE


def check_enemy_nearby(dungeon_map, pos):
    """Ищет врага в соседних клетках и возвращает его координаты."""
    x, y = pos
    for dx, dy in [(-1, 0), (1, 0), (0, -1), (0, 1)]:
        nx, ny = x + dx, y + dy
        if 0 <= nx < len(dungeon_map) and 0 <= ny < len(dungeon_map[0]):
            if dungeon_map[nx][ny] == ENEMY_TILE:
                return [nx, ny]
    return None