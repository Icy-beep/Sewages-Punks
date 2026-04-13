from collections import deque
from src.constants import *


def get_path_to_target(start: list[int], target_tiles: list[int], dungeon_map: list[list[int]], occupied_targets: list[int]):
    """
        Находит кратчайший путь к ближайшей доступной целевой клетке с помощью алгоритма BFS.

        Функция сканирует карту подземелья, начиная от стартовой позиции, в поиске клеток,
        типы которых указаны в target_tiles. При этом игнорируются цели, координаты которых
        уже содержатся в списке occupied_targets.

        Args:
            start (list[int]): Координаты начала поиска [x, y].
            target_tiles (list[int]): Список ID тайлов, которые считаются целью (например, [EXIT, GOLD]).
            dungeon_map (list[list[int]]): Двумерный массив (сетка), представляющий карту подземелья.
            occupied_targets (list[int]): Список координат [x, y] целей, которые уже заняты другими агентами.

        Returns:
            tuple[list[int], list[int]] | None: Кортеж, где:
                - Первый элемент: координаты следующего шага [nx, ny] для достижения цели.
                - Второй элемент: координаты самой найденной цели [tx, ty].
                Возвращает None, если путь не найден или если персонаж уже стоит на цели.
    """
    rows = len(dungeon_map)
    cols = len(dungeon_map[0])
    queue = deque([(tuple(start), [])])
    visited = {tuple(start)}

    while queue:
        (curr_x, curr_y), path = queue.popleft()

        if dungeon_map[curr_x][curr_y] in target_tiles:
            if [curr_x, curr_y] not in occupied_targets:
                return (path[0], [curr_x, curr_y]) if path else None

        for dx, dy in [(-1, 0), (1, 0), (0, -1), (0, 1)]:
            nx, ny = curr_x + dx, curr_y + dy

            if 0 <= nx < rows and 0 <= ny < cols and (nx, ny) not in visited:
                tile = dungeon_map[nx][ny]

                if tile == FLOOR_TILE or tile in target_tiles:
                    visited.add((nx, ny))
                    queue.append(((nx, ny), path + [[nx, ny]]))
    return None


def move_enemies(dungeon_map: list[list[int]]):
    """
    Управляет перемещением всех врагов на карте к ближайшим доступным целям.

    Функция сканирует карту для поиска всех врагов (ENEMY_TILE). Для каждого найденного
    врага вычисляется кратчайший путь к ближайшему сундуку (CHEST_TILE) или ключу (KEY_TILE).
    Чтобы враги не шли к одной и той же цели, используется список 'occupied_targets'.
    Если путь найден и следующая клетка свободна (FLOOR_TILE), враг перемещается.

    Логика работы:
    1. Собирает координаты всех врагов на текущем шаге.
    2. Для каждого врага ищет путь к ближайшей незанятой цели.
    3. Резервирует конечную цель, чтобы другие враги её игнорировали.
    4. Обновляет сетку 'dungeon_map', перемещая символ врага на одну клетку.

    Args:
        dungeon_map (list[list[int]]): Двумерный массив, представляющий игровую карту.
            Модифицируется на месте при перемещении врагов.

    Note:
        Враги перемещаются только на клетки с типом FLOOR_TILE. Если путь к цели
        заблокирован другим врагом или препятствием, текущий враг останется на месте.
    """
    enemies = []
    for x in range(len(dungeon_map)):
        for y in range(len(dungeon_map[x])):
            if dungeon_map[x][y] == ENEMY_TILE:
                enemies.append((x, y))

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


def check_enemy_nearby(dungeon_map: list[list[int]], pos: list[int]) -> list[int] | None:
    """
    Проверяет наличие врага в четырёх соседних клетках от заданной позиции.

    Функция сканирует клетки сверху, снизу, слева и справа от указанной точки.
    Если в одной из них обнаружен тайл врага (ENEMY_TILE), возвращаются его координаты.

    Args:
        dungeon_map (list[list[int]]): Двумерный массив, представляющий карту подземелья.
        pos (list[int]): Координаты центральной точки (x, y) для проверки.

    Returns:
        list[int] | None: Координаты первого найденного врага [nx, ny] или None,
            если врагов в соседних клетках нет.
    """
    x, y = pos
    for dx, dy in [(-1, 0), (1, 0), (0, -1), (0, 1)]:
        nx, ny = x + dx, y + dy
        if 0 <= nx < len(dungeon_map) and 0 <= ny < len(dungeon_map[0]):
            if dungeon_map[nx][ny] == ENEMY_TILE:
                return [nx, ny]
    return None