from src.display import *
from src.businesslogic_lower import *
from src.entities import *
from src.localization import MESSAGES

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
    """
    Обрабатывает логику перемещения игрока по карте.

    Вычисляет новые координаты на основе команды. Если целевая клетка
    проходима (FLOOR_TILE), обновляет карту, перемещая маркер игрока.
    Если на пути препятствие или интерактивный объект (стена, враг, сундук),
    позиция на карте не меняется, но возвращаются координаты препятствия
    для последующей обработки.

    Args:
        location (list[list[int]]): Двумерный массив (карта) текущей локации.
        command (str): Команда направления (из констант COMMAND_MOVE_...).

    Returns:
        list[int]: Новые координаты игрока [x, y] после попытки движения.
    """
    position: list[int] = search_player_position(location)
    old_position: list[int] = position
    new_position: list[int] = position[:]

    if command == COMMAND_MOVE_UP:
        new_position[x_coord] -= 1
    elif command == COMMAND_MOVE_LEFT:
        new_position[y_coord] -= 1
    elif command == COMMAND_MOVE_DOWN:
        new_position[x_coord] += 1
    elif command == COMMAND_MOVE_RIGHT:
        new_position[y_coord] += 1

    target_tile: int = location[new_position[x_coord]][new_position[y_coord]]

    blocking_tiles: list[int] = [
        WALL_TILE, ENEMY_TILE, TRAP_TILE,
        CHEST_TILE, KEY_TILE, EXIT_TILE
    ]

    if target_tile in blocking_tiles:
        return new_position

    location[old_position[x_coord]][old_position[y_coord]] = FLOOR_TILE
    location[new_position[x_coord]][new_position[y_coord]] = PLAYER_TILE

    return new_position


def handle_trap(location: list[list[int]], player_data: list, position: list[int] | tuple[int, int]) -> None:
    """
    Обрабатывает взаимодействие игрока с ловушкой.

    Предоставляет игроку выбор: попытаться разминировать ловушку при наличии набора
    инструментов (DEFUSAL_KIT) или попытаться пробежать сквозь неё.
    В зависимости от выбора и удачи игрок может обезвредить ловушку,
    получить урон или успешно проскочить.

    Args:
        location (list[list[int]]): Двумерный массив текущей карты уровня.
        player_data (list): Список данных игрока (HP, инвентарь и т.д.).
        position (list[int] | tuple[int, int]): Координаты ловушки [x, y] на карте.

    Returns:
        None: Функция модифицирует данные игрока и карту на месте.
    """
    x, y = position
    clear_display()
    print(MESSAGES.traps.detected)

    while True:
        trap_inputs()
        user_input: str = input('>>').strip()

        if user_input not in TRAP_COMMANDS:
            continue

        if user_input == '1':
            if defuse_trap(player_data):
                player_data[PLAYER_ITEM_DEFUSAL_KIT] -= 1
                clear_display()
                print(MESSAGES.traps.defused)
                enter_continue()
                location[x][y] = FLOOR_TILE
                return
            else:
                clear_display()
                print(MESSAGES.traps.no_defkit)
                enter_continue()

        elif user_input == '2':
            if defuse_trap_run():
                clear_display()
                print(MESSAGES.traps.defused)
            else:
                clear_display()
                print(MESSAGES.traps.damage)
                player_data[ENTITY_HP] -= 5

            enter_continue()
            location[x][y] = FLOOR_TILE
            return


def handle_exit(player_data: list) -> bool:
    """
    Управляет процессом взаимодействия игрока с дверью выхода из сектора.

    Предоставляет игроку меню действий: использование ключ-карты, попытка
    силового взлома или отступление. Функция проверяет наличие ключа в инвентаре
    и обрабатывает логику успешного выхода (эвакуации).

    Args:
        player_data (list): Список данных игрока, содержащий инвентарь и характеристики.

    Returns:
        bool:
            - True, если игрок успешно использовал ключ и покидает уровень (EXFILL).
            - False, если игрок решил отойти от двери и продолжить исследование.
    """
    clear_display()
    print(MESSAGES.exploration.door_try_open)
    enter_continue()

    while True:
        clear_display()
        exit_interactions()
        user_input: str = input('>>').strip()

        if user_input not in DOOR_INTERACTION_COMMANDS:
            continue

        if user_input == '1':
            if player_data[PLAYER_ITEM_KEY] >= 1:
                while True:
                    clear_display()
                    key_card_options_menu()
                    choice: str = input('>>').strip()

                    if choice == '1':
                        clear_display()
                        print(MESSAGES.exploration.card_reader_success)
                        enter_continue()
                        return True

                    if choice == '2':
                        break

        elif user_input == '2':
            clear_display()
            print(MESSAGES.exploration.door_kick)
            enter_continue()

        elif user_input == '3':
            clear_display()
            print(MESSAGES.exploration.door_step_out)
            return False

    return False


def handle_chest(location: list[list[int]], player_data: list, position: list[int] | tuple[int, int]) -> None:
    """
    Обрабатывает логику открытия сундука и получения добычи.

    Функция определяет содержимое сундука через генератор лута, выводит
    соответствующее сообщение и обновляет инвентарь игрока. После взаимодействия
    сундук удаляется с карты, заменяясь на тайл пола.

    Args:
        location (list[list[int]]): Двумерный массив (карта) текущей локации.
        player_data (list): Список характеристик и инвентаря игрока.
        position (list[int] | tuple[int, int]): Координаты сундука [x, y] на карте.

    Returns:
        None: Функция вносит изменения непосредственно в объекты игрока и карты.
    """
    x, y = position

    item: str = open_chest()

    clear_display()
    loot_message(item)

    if item == ITEM_DEFUSAL_KIT:
        player_data[PLAYER_ITEM_DEFUSAL_KIT] += 1

    enter_continue()

    location[x][y] = FLOOR_TILE


def handle_key_pickup(location: list[list[int]], player_data: list, position: list[int] | tuple[int, int]) -> None:
    """
    Обрабатывает подбор ключ-карты игроком.

    Функция оповещает игрока о находке, увеличивает счетчик ключей в инвентаре
    и удаляет объект ключа с карты, заменяя его на тайл пола.

    Args:
        location (list[list[int]]): Двумерный массив (карта) текущей локации.
        player_data (list): Список характеристик и инвентаря игрока.
        position (list[int] | tuple[int, int]): Координаты ключа [x, y] на карте.

    Returns:
        None: Функция модифицирует данные игрока и карту на месте.
    """
    x: int
    y: int
    x, y = position

    clear_display()
    print(MESSAGES.exploration.key_found)

    player_data[PLAYER_ITEM_KEY] += 1

    location[x][y] = FLOOR_TILE

    enter_continue()


def try_start_fight(location: list[list[int]], new_position: list[int] | tuple[int, int]) -> bool:
    """
    Проверяет, приведет ли перемещение в указанную точку к началу сражения.

    Функция анализирует тип тайла по заданным координатам. Если в целевой
    клетке находится противник (ENEMY_TILE), функция подает сигнал
    для инициации боевого режима.

    Args:
        location (list[list[int]]): Двумерный массив текущей карты уровня.
        new_position (list[int] | tuple[int, int]): Координаты [x, y],
            которые игрок пытается занять.

    Returns:
        bool:
            - True, если на целевой позиции обнаружен враг (ENEMY_TILE).
            - False, если враг отсутствует.
    """
    if_fight: bool = False

    if location[new_position[0]][new_position[1]] == ENEMY_TILE:
        if_fight = True

    return if_fight


def create_enemy() -> list:
    """
    Создает независимый экземпляр противника для текущего сражения.

    Функция выбирает шаблон врага и создает его поверхностную копию.
    Это необходимо, чтобы изменения характеристик (например, HP) во время боя
    не перезаписывали базовые значения (пресеты) в глобальных переменных.

    Returns:
        list: Список с характеристиками конкретного экземпляра врага.
    """
    enemy: list = choose_enemy()

    copy_of_enemy: list = enemy[:]

    return copy_of_enemy


def initiative_throw(player_data: list, enemy_data: list) -> tuple[list, list]:
    """
    Выполняет расчет инициативы для определения очередности ходов в бою.

    К базовым показателям инициативы игрока и врага добавляется случайное значение (бросок кубика).
    Результат ограничивается максимальным значением 10. Цикл повторяется до тех пор,
    пока значения инициативы не станут различными, чтобы исключить одновременный ход.

    Args:
        player_data (list): Список характеристик игрока.
        enemy_data (list): Список характеристик противника.

    Returns:
        tuple[list, list]: Кортеж, содержащий обновленные данные игрока и врага
            с установленными значениями инициативы для текущего боя.
    """
    left_border: int = 0
    right_border: int = 5
    throw_is_good: bool = False

    while not throw_is_good:

        player_initiative: int = player_data[ENTITY_INITIATIVE]
        enemy_initiative: int = enemy_data[ENTITY_INITIATIVE]

        player_throw: int = random.randint(left_border, right_border)
        enemy_throw: int = random.randint(left_border, right_border)

        player_initiative += player_throw
        enemy_initiative += enemy_throw

        if player_initiative > 10:
            player_initiative = 10

        if enemy_initiative > 10:
            enemy_initiative = 10

        if player_initiative != enemy_initiative:
            throw_is_good = True

    player_data[ENTITY_INITIATIVE] = player_initiative
    enemy_data[ENTITY_INITIATIVE] = enemy_initiative

    return player_data, enemy_data


def randomise_damage(damage: int) -> int:
    """
    Добавляет случайный разброс к базовому значению урона.

    Используется для создания вариативности в бою, чтобы атаки не наносили
    всегда одинаковое количество повреждений. Базовое значение корректируется
    в диапазоне от -2 до +2 единиц.

    Args:
        damage (int): Базовый показатель урона персонажа или врага.

    Returns:
        int: Итоговое значение урона с учетом случайного модификатора.
    """
    left_border: int = -2
    right_border: int = 2

    random_damage: int = random.randint(left_border, right_border)

    damage += random_damage

    return max(1, damage)


def try_ruin_attack_for_player(player_data: list) -> bool:
    """
    Проверяет, промахнется ли игрок при попытке атаки.

    Генерирует случайное число с плавающей запятой от 0.0 до 1.0 и сравнивает его
    с базовым шансом промаха персонажа (ENTITY_MISS_CHANCE).

    Args:
        player_data (list): Список характеристик игрока.

    Returns:
        bool:
            - True, если атака сорвана (промах).
            - False, если атака прошла успешно.
    """
    throw: float = random.random()

    if throw < player_data[ENTITY_MISS_CHANCE]:
        return True

    return False


def try_ruin_attack_for_enemy(enemy_data: list) -> bool:
    """
    Выполняет расчет вероятности промаха для текущей атаки противника.

    Сравнивает случайное число с индивидуальным показателем шанса промаха врага.
    Используется для определения, нанесет ли враг урон в текущем ходу.

    Args:
        enemy_data (list): Список характеристик противника, содержащий ENTITY_MISS_CHANCE.

    Returns:
        bool:
            - True, если враг промахнулся.
            - False, если атака достигла цели.
    """
    throw: float = random.random()

    if throw < enemy_data[ENTITY_MISS_CHANCE]:
        return True

    return False


def defuse_trap(player_data: list) -> bool:
    """
    Проверяет наличие в инвентаре игрока набора для разминирования (DEFUSAL_KIT).

    Функция используется перед началом процесса разминирования ловушки,
    чтобы подтвердить наличие необходимых ресурсов в данных игрока.

    Args:
        player_data (list): Список данных игрока, включая количество предметов.

    Returns:
        bool:
            - True, если в инвентаре есть хотя бы один набор для разминирования.
            - False, если инструменты отсутствуют.
    """
    if player_data[PLAYER_ITEM_DEFUSAL_KIT] >= 1:
        return True

    return False


def defuse_trap_run() -> bool:
    """
    Рассчитывает шанс игрока успешно проскочить сквозь ловушку без получения урона.

    Использует базовый системный шанс (BASE_CHANCE), уменьшенный на фиксированный
    штраф сложности (0.70). Если случайное число оказывается меньше итогового
    значения, попытка считается успешной.

    Returns:
        bool:
            - True, если игроку удалось успешно проскочить (ловушка не сработала).
            - False, если попытка неудачна (игрок получает урон).
    """
    chance: float = BASE_CHANCE - 0.70

    if random.random() < chance:
        return True

    return False


def open_chest() -> int:
    """
    Определяет содержимое сундука при взаимодействии.

    Генерирует случайный числовой идентификатор предмета.
    Используется для случайного распределения наград между инструментами
    разминирования (DEFUSAL_KIT) и другими типами лута.

    Returns:
        int: Идентификатор выпавшего предмета (0 или 1).
    """
    item: int = random.randint(0, 1)

    return item






