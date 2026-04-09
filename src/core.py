import json
import datetime
from typing import Callable, Any, Tuple, Dict
from src.businesslogic_upper import *
from src.display import *
from src.constants import *

INTERACTIONS: dict[Any, Callable[..., Any]] = {
    CHEST_TILE: handle_chest,
    KEY_TILE: handle_key_pickup,
    TRAP_TILE: handle_trap,
}


def adventuring(dungeon_map: list[list[Any]], player_data: dict[str, Any]) -> (
        None | tuple[str, list[int]] | tuple[str, int]):
    """
    Основной игровой цикл исследования подземелья.

    Управляет отображением карты, обработкой перемещения игрока, взаимодействием
    с объектами и переходами между игровыми состояниями (бой, пауза, выход).

    Args:
        dungeon_map (list[list[Any]]): Двумерный массив, представляющий сетку карты.
        player_data (dict[str, Any]): Словарь с данными и характеристиками игрока.

    Returns:
        Tuple[str, Any]: Кортеж, содержащий флаг состояния (события) и текущую позицию игрока или код возврата.
    """
    while True:
        clear_display()
        show_dungeon_map(dungeon_map, player_data)
        show_movement_legend()

        command = get_user_command()

        if command == PAUSE:
            status = handle_pause_menu(player_data, dungeon_map)
            if status == RETURN_TO_MAIN_MENU:
                return RETURN_TO_MAIN_MENU, 0
            continue

        if command in MOVEMENT_COMMANDS:
            new_position = movement_player(dungeon_map, command)
            tile = dungeon_map[new_position[x_coord]][new_position[y_coord]]

            if tile == WALL_TILE:
                continue

            handler = INTERACTIONS.get(tile)
            if handler:
                handler(dungeon_map, player_data, new_position)
            elif tile == EXIT_TILE:
                if handle_exit(player_data):
                    return EXFILL, new_position

            if try_start_fight(dungeon_map, new_position):
                return FIGHT, new_position


def fight(player_data: Dict[str, Any]) -> bool | None:
    """
    Управляет процессом пошагового боя между игроком и противником.

    Функция инициализирует врага, рассчитывает инициативу и обрабатывает цикл
    сражения, включая выбор действий игроком (атака, лечение, уклонение)
    и автоматические ходы противника.

    Args:
        player_data (Dict[str, Any]): Словарь с текущими характеристиками игрока.

    Returns:
        bool: True, если игрок победил; False, если игрок погиб.
    """
    player_data[ENTITY_TOXICITY] = 0
    enemy_data = create_enemy()
    heals_left = 4
    dodge_active = False
    combat_log = ["Connection established.", f"Target: {enemy_data[ENTITY_NAME]} detected."]

    clear_display()
    print(f"\n{MAGENTA_TEXT_BRIGHT}ENCOUNTER_LOG:{RESET} {enemy_data[ENTITY_NAME]} has entered the sector.\n")
    enter_continue()

    player_data, enemy_data = initiative_throw(player_data, enemy_data)
    throw_animation(player_data, enemy_data)
    enter_continue()

    current_turn = "player" if player_data[ENTITY_INITIATIVE] >= enemy_data[ENTITY_INITIATIVE] else "enemy"

    while True:
        if player_data[ENTITY_HP] <= 0:
            return False

        if enemy_data[ENTITY_HP] <= 0:
            draw_combat_interface(player_data, enemy_data, heals_left, combat_log, current_turn)
            enemy_defeated_message(enemy_data)
            return True

        draw_combat_interface(player_data, enemy_data, heals_left, combat_log, current_turn)

        if current_turn == "player":
            action = input().lower()

            if action == 'h':
                msg, success = execute_player_heal(player_data, heals_left)
                combat_log.append(msg)
                if success:
                    heals_left -= 1
                continue

            elif action == 'a':
                combat_log.append(execute_player_attack(player_data, enemy_data))
                current_turn = "enemy"
            elif action == 'd':
                dodge_active = True
                combat_log.append("Evasive maneuvers active. Dodge chance UP.")
                current_turn = "enemy"

            else:
                continue

            time.sleep(0.4)

        else:
            time.sleep(1)
            orig_miss = enemy_data[ENTITY_MISS_CHANCE]
            if dodge_active:
                enemy_data[ENTITY_MISS_CHANCE] += 0.4

            combat_log.append(execute_enemy_attack(enemy_data, player_data))

            enemy_data[ENTITY_MISS_CHANCE] = orig_miss
            dodge_active = False
            current_turn = "player"


def handle_pause_menu(player_data, dungeon_map):
    """
    Управляет меню паузы.
    Возвращает CONTINUE_GAME или RETURN_TO_MAIN_MENU.
    """
    while True:
        show_ingame_menu()
        choice = input(f"\n    {MAGENTA_TEXT_BRIGHT}WAITING FOR INPUT... > {RESET}").lower()

        if choice in RESUME:
            return CONTINUE_GAME

        if choice in SAVE:
            save_game(player_data, dungeon_map)

        if choice in LOAD:
            loaded = load_game()
            if loaded:
                print(f"{GREEN_TEXT_BRIGHT}[ DATA OVERWRITTEN FROM RESTORE POINT ]{RESET}")

        if choice in QUIT_TO_MAIN_MENU:
            return RETURN_TO_MAIN_MENU

        if choice not in IN_GAME_MENU_COMMANDS:
            print(f"    {RED_TEXT_BRIGHT}INVALID COMMAND. RE-ENTER.{RESET}")


def execute_player_attack(player: Dict[str, Any], enemy: Dict[str, Any]) -> str:
    """
    Выполняет расчет и проведение атаки игрока по противнику.

    Проверяет вероятность промаха через внешнюю функцию и, в случае успеха,
    рассчитывает случайный урон на основе характеристик игрока, вычитая его
    из здоровья врага.

    Args:
        player (Dict[str, Any]): Данные игрока, включая базовый урон.
        enemy (Dict[str, Any]): Данные противника, включая текущее здоровье и имя.

    Returns:
        str: Сообщение о результате атаки (промах или нанесенный урон) для боевого лога.
    """
    if try_ruin_attack_for_player(player):
        return f"{RED_TEXT_BRIGHT}MISS!{RESET} Attack failed."
    else:
        dmg = randomise_damage(player[ENTITY_DAMAGE])
        enemy[ENTITY_HP] -= dmg
        return f"Strike successful. {dmg} damage dealt to {enemy[ENTITY_NAME]}."


def execute_player_heal(player: Dict[str, Any], heals_left: int) -> Tuple[str, bool]:
    """
    Выполняет попытку восстановления здоровья игрока с использованием нанитов.

    Каждое использование увеличивает уровень токсичности. При превышении порога
    токсичности (4) игрок получает штрафной урон от перегрузки системы.

    Args:
        player (Dict[str, Any]): Словарь с данными игрока (HP, токсичность).
        heals_left (int): Текущее количество доступных зарядов лечения.

    Returns:
        Tuple[str, bool]: Кортеж, содержащий:
            - str: Сообщение о результате действия для лога.
            - bool: Статус успеха операции (True, если лечение применено).
    """
    if heals_left <= 0:
        return f"{RED_TEXT_BRIGHT}ERROR!{RESET} No nanites left.", False

    player[ENTITY_HP] = min(100, player[ENTITY_HP] + 10)
    player[ENTITY_TOXICITY] += 1

    msg = f"Regen active. +10 HP. Toxicity: {player[ENTITY_TOXICITY]}/4."

    if player[ENTITY_TOXICITY] > 4:
        player[ENTITY_HP] -= 8
        player[ENTITY_TOXICITY] -= 1
        msg += f" {RED_TEXT_BRIGHT}TOXIC OVERLOAD!{RESET} -8 HP."

    return msg, True


def execute_enemy_attack(enemy: Dict[str, Any], player: Dict[str, Any]) -> str:
    """
    Выполняет расчет и проведение атаки противника по игроку.

    Сначала проверяется шанс промаха противника. Если атака успешна,
    рассчитывается случайный урон, который вычитается из здоровья игрока.

    Args:
        enemy (Dict[str, Any]): Данные противника (имя, урон, шанс промаха).
        player (Dict[str, Any]): Данные игрока (здоровье).

    Returns:
        str: Сообщение о результате атаки для боевого лога.
    """
    if random.random() < enemy[ENTITY_MISS_CHANCE]:
        return f"{enemy[ENTITY_NAME]} {LIGHT_BLUE_TEXT_BRIGHT}MISSED{RESET} their attack."
    else:
        dmg = randomise_damage(enemy[ENTITY_DAMAGE])
        player[ENTITY_HP] -= dmg
        return f"{enemy[ENTITY_NAME]} struck for {RED_TEXT_BRIGHT}{dmg}{RESET} damage."


def get_unique_filename(base_name: str) -> str:
    """
    Генерирует уникальное имя файла для сохранения, предотвращая перезапись существующих данных.

    Если файл с базовым именем уже существует, функция добавляет порядковый номер
    (например, base_name_1, base_name_2) до тех пор, пока не найдет свободное имя.

    Args:
        base_name (str): Желаемое имя файла (без расширения).

    Returns:
        str: Полный путь к уникальному файлу с расширением .json.
    """
    filename = os.path.join(SAVE_DIR, f"{base_name}.json")
    counter = 1

    while os.path.exists(filename):
        temp_name = f"{base_name}_{counter}"
        filename = os.path.join(SAVE_DIR, f"{temp_name}.json")
        counter += 1

    return filename


def save_game(player_data: Dict[Any, Any], dungeon: Any) -> bool:
    """
    Выполняет экспорт текущего состояния игрока и подземелья в JSON-файл.

    Функция создает директорию сохранений, если она отсутствует, запрашивает имя
    у пользователя, очищает его от недопустимых символов, добавляет метку времени
    и записывает данные в файл.

    Args:
        player_data (Dict[Any, Any]): Данные и характеристики игрока.
        dungeon (Any): Текущее состояние карты или объекта подземелья.

    Returns:
        bool: True, если сохранение прошло успешно, иначе False.
    """
    if not os.path.exists(SAVE_DIR):
        os.makedirs(SAVE_DIR)

    print(f"\n{MAGENTA_TEXT_BRIGHT}[ SAVE AS... ]{RESET}")
    user_name = input(f"{MAGENTA_TEXT_BRIGHT}>>> {RESET}").strip()

    if not user_name:
        user_name = "savegame"

    user_name = "".join(c for c in user_name if c.isalnum() or c in (' ', '_', '-')).rstrip()

    timestamp = datetime.datetime.now().strftime("%Y-%m-%d_%H-%M")

    full_name = f"{user_name}_{timestamp}"

    final_path = get_unique_filename(full_name)

    data = {
        "player": player_data,
        "dungeon": dungeon,
    }

    try:
        with open(final_path, "w", encoding="utf-8") as f:
            json.dump(data, f, ensure_ascii=False, indent=4)

        actual_name = os.path.basename(final_path)
        print(f"{GREEN_TEXT_BRIGHT}[ SYNCHRONIZE: {actual_name} WRITE SUCCESSFUL ]{RESET}")
        return True
    except Exception as e:
        print(f"{RED_TEXT_BRIGHT}[ SYNC INTERRUPTED: DATA LOSS DETECTED {e} ]{RESET}")
        return False


def load_game():
    """
    Выводит список всех файлов в папке saves и дает выбрать нужный.
    """
    if not os.path.exists(SAVE_DIR): return None

    files = [f for f in os.listdir(SAVE_DIR) if f.endswith('.json')]
    files.sort(key=lambda x: os.path.getmtime(os.path.join(SAVE_DIR, x)), reverse=True)

    if not files:
        print(f"{RED_TEXT_BRIGHT}[ ERROR: DATA IS NONE IN THAT SECTOR ]{RESET}")
        return None

    print(f"\n{MAGENTA_TEXT_BRIGHT}--- [ ACTIVE RESTORE POINTS ] ---{RESET}")
    for i, file in enumerate(files, 1):
        path = os.path.join(SAVE_DIR, file)
        mtime = os.path.getmtime(path)
        date_str = datetime.datetime.fromtimestamp(mtime).strftime('%d.%m %H:%M')

        print(f"  {i}. {file.ljust(25)} | {LIGHT_BLUE_TEXT_BRIGHT}{date_str}{RESET}")

    try:
        choice = int(input(f"\n{MAGENTA_TEXT_BRIGHT}CHOOSE THE INDEX > {RESET}")) - 1
        if 0 <= choice < len(files):
            with open(os.path.join(SAVE_DIR, files[choice]), "r", encoding="utf-8") as f:
                data = json.load(f)
                return data["dungeon"], data["player"]
    except (ValueError, IndexError):
        print(f"{RED_TEXT_BRIGHT}[ ERROR: WRONG INDEX ]{RESET}")

    return None