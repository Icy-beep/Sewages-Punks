import msvcrt
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


def initialize_empty_dungeon(height: int, width: int, wall_tile: int) -> list[list[int]]:
    """
    Инициализирует базовую сетку подземелья, заполненную тайлами стен.

    :param height: Высота подземелья (количество строк).
    :param width: Ширина подземелья (количество столбцов).
    :param wall_tile: Значение (ID) тайла, представляющего стену.
    :return: list[list[int]] — Двумерный массив, представляющий каркас уровня.
    """
    return [[wall_tile for _ in range(width)] for _ in range(height)]


def place_exit(dungeon_map: list[list[int]]) -> None:
    """
    Размещает тайл выхода в случайном месте на нижней границе подземелья.

    :param dungeon_map: Сетка игрового мира, которую нужно модифицировать.
    """
    height = len(dungeon_map)
    width = len(dungeon_map[0])
    exit_col = random.randint(1, width - 2)
    dungeon_map[height - 1][exit_col] = EXIT_TILE


def apply_passes(dungeon_map: list[list[int]], passes: list[list[int]],
                 floor_tile: int, player_tile: int) -> None:
    """
    Прорубает в сетке стен горизонтальные коридоры и вертикальные проходы.
    Также устанавливает начальную позицию игрока.

    :param dungeon_map: Сетка подземелья для модификации.
    :param passes: Список колонок для вертикальных проходов между этажами.
    :param floor_tile: ID тайла пола.
    :param player_tile: ID тайла игрока.
    """
    for i in range(1, len(dungeon_map), 2):
        for j in range(1, len(dungeon_map[i]) - 1):
            dungeon_map[i][j] = floor_tile

    for idx, columns in enumerate(passes):
        row = (idx + 1) * 2
        if row < len(dungeon_map):
            for col in columns:
                if col < len(dungeon_map[row]):
                    dungeon_map[row][col] = floor_tile

    dungeon_map[1][1] = player_tile


def get_possible_tiles(dungeon_map: list[list[int]], forbidden_tiles: set[int] = None,
                       must_be_near_wall: bool = False, behind_enemy: bool = False) -> list[tuple[int, int]]:
    """
    Анализирует карту и возвращает список координат (row, col), доступных для спавна.

    Применяет базовые фильтры: тип пола, отсутствие игрока, безопасная зона спавна.
    Дополнительно поддерживает специфические режимы размещения.

    :param dungeon_map: Текущее состояние сетки мира.
    :param forbidden_tiles: Дополнительные тайлы-исключения.
    :param must_be_near_wall: Режим поиска мест в тупиках или вдоль стен.
    :param behind_enemy: Режим поиска клеток справа от тайла врага.
    :return: Список кортежей с координатами доступных клеток.
    """
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


def spawn_objects(dungeon_map: list[list[int]], tile_type: int, count: int,
                  forbidden: set[int] = None, near_wall: bool = False,
                  behind_enemy: bool = False) -> None:
    """
    Размещает заданное количество игровых объектов на карте, используя фильтрацию мест.

    :param dungeon_map: Сетка игрового мира.
    :param tile_type: Тип размещаемого объекта (враг, сундук и т.д.).
    :param count: Количество объектов для размещения.
    :param forbidden: Набор ID тайлов, на которые нельзя ставить данный объект.
    :param near_wall: Если True, объект будет приоритетно спавниться у стен/в тупиках.
    :param behind_enemy: Если True, ищет место за спиной существующих врагов.
    """
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


def get_user_command():
    char = msvcrt.getch()
    if char == b'\x1b':
        return "PAUSE"
    try:
        return char.decode('utf-8').lower()
    except UnicodeDecodeError:
        return None


