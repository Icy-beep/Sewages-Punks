import os
import time
import sys
import random
import msvcrt
import winsound
import re
from src.constants import *


def flush_input() -> None:
    """
    Полностью очищает буфер ввода консоли.

    Считывает и отбрасывает все символы, которые были нажаты пользователем
    во время анимаций или пауз. Это предотвращает автоматическое срабатывание
    команд, случайно накопленных в очереди ввода.

    Returns:
        None: Функция выполняет очистку системного буфера msvcrt.
    """
    while msvcrt.kbhit():
        msvcrt.getch()


def skip_message() -> str:
    """
    Формирует стилизованное сообщение с предложением пропустить вступительный брифинг.

    Сообщение оформлено в цветовой гамме Moon City OS и информирует игрока,
    что для продолжения чтения нужно нажать 'N', в то время как любая
    другая клавиша (включая 'Y') приведет к пропуску пролога.

    Returns:
        str: Многострочная строка с форматированием ANSI-цветами.
    """
    message: str = (
        f'{LIGHT_BLUE_TEXT_BRIGHT}Skip the brief?\n'
        f'[ Y ] Yes\n'
        f'[ N ] No\n'
        f'{RED_TEXT_BRIGHT}Any other key will skip the brief.{RESET}'
    )

    return message


def slow_print(text: str, speed: float = 0.03) -> None:
    """
    Выводит текст в консоль посимвольно с заданной задержкой.

    Создает эффект постепенного появления текста (как в старых терминалах).
    После вывода всей строки автоматически переходит на новую строку.

    Args:
        text (str): Строка текста, которую необходимо напечатать.
        speed (float): Задержка в секундах между появлением каждого символа.
            По умолчанию 0.03.

    Returns:
        None: Функция выполняет прямой вывод в поток sys.stdout.
    """
    for char in text:
        sys.stdout.write(char)
        sys.stdout.flush()
        time.sleep(speed)
    print()


def start_message() -> None:
    """
    Запускает вступительный сюжетный брифинг (пролог) игры.

    Выводит серию стилизованных сообщений от персонажа Elgeia через PSY-link.
    Использует эффект медленной печати (slow_print) и задержки для создания
    атмосферы погружения. Обучает игрока значению символов на карте и
    устанавливает цели миссии.

    Returns:
        None: Функция выполняет последовательный вывод текста в консоль.
    """
    print(f"{DARK_GRAY}" + "• " * 30 + f"{RESET}\n")

    slow_print(f"{MAGENTA_TEXT_BRIGHT}[...] Initializing PSY-link synchronization... {WHITE_TEXT_BRIGHT}OK{RESET}", 0.05)
    slow_print(f"{MAGENTA_TEXT_BRIGHT}[...] Checking Elgeia's biometrics... {WHITE_TEXT_BRIGHT}OK{RESET}", 0.05)
    slow_print(f"{MAGENTA_TEXT_BRIGHT}{RED_TEXT_BRIGHT}[!] WARNING: Langauge interpreter malfunctions {RESET}", 0.05)
    slow_print(f"{MAGENTA_TEXT_BRIGHT}{RED_TEXT_BRIGHT}[!] WARNING: Default language set to RUSSIAN {RESET}", 0.05)
    print(f"{MAGENTA_TEXT_BRIGHT}" + "-" * 50 + f"{RESET}\n")

    slow_print(f"{LIGHT_BLUE_TEXT_BRIGHT}[SYSTEM@Elgeia]:#{WHITE_TEXT_BRIGHT} Оператор, приём. Коннект стабилен. Картинка обновляется.{RESET}")
    time.sleep(0.5)

    slow_print(
        f"{LIGHT_BLUE_TEXT_BRIGHT}[SYSTEM@Elgeia]:#{WHITE_TEXT_BRIGHT} Я в очередном коллекторе. Тут всё как обычно: бетон, вонь и бесконечные переходы.{RESET}")
    slow_print(f"{LIGHT_BLUE_TEXT_BRIGHT}[SYSTEM@Elgeia]:#{WHITE_TEXT_BRIGHT} Эти стоки тянутся под всем городом, сектора штамповали по одному проекту.{RESET}")
    slow_print(
        f"{LIGHT_BLUE_TEXT_BRIGHT}[SYSTEM@Elgeia]:#{WHITE_TEXT_BRIGHT} Не удивляйся, если локации покажутся тебе одинаковыми. Это один большой лабиринт.{RESET}")

    time.sleep(0.8)

    slow_print(f"{LIGHT_BLUE_TEXT_BRIGHT}[SYSTEM@Elgeia]:#{WHITE_TEXT_BRIGHT} Зачем я здесь? Всё просто — тут можно выудить что-то очень ценное, вроде твоего линка...{RESET}")
    slow_print(f"{LIGHT_BLUE_TEXT_BRIGHT}[SYSTEM@Elgeia]:#{WHITE_TEXT_BRIGHT} Крутая штука, да? Корпы плохо следят за своими вещами.{RESET}")
    slow_print(f"{LIGHT_BLUE_TEXT_BRIGHT}[SYSTEM@Elgeia]:#{WHITE_TEXT_BRIGHT} Что конкретно мы ищем? Я сама не знаю и это не важно. Извини но я плачу тебе не за вопросы.{RESET}")

    time.sleep(1.0)

    print(f"\n{LIGHT_BLUE_TEXT_BRIGHT}[ MISSION_DIRECTIVES ]{RESET}")
    slow_print(f"{DARK_GRAY}— {WHITE_TEXT_BRIGHT}Следи за сканером. Видишь {RED_TEXT_BRIGHT}X ВРАГОВ{WHITE_TEXT_BRIGHT} — обходи или выводи меня на них.{RESET}")
    slow_print(f"{DARK_GRAY}— {WHITE_TEXT_BRIGHT}Ищи {MAGENTA_TEXT_BRIGHT}§ КЛЮЧ-КАРТЫ{RESET}{WHITE_TEXT_BRIGHT}. Без них двери в следующие сектора не откроются.{RESET}")
    slow_print(f"{DARK_GRAY}— {WHITE_TEXT_BRIGHT}Если видишь {YELLOW_TEXT_BRIGHT}$ ПОЛЕЗНЫЙ ЛУТ{WHITE_TEXT_BRIGHT} — говори где он.{RESET}")
    slow_print(f"{DARK_GRAY}— {WHITE_TEXT_BRIGHT}Дошли до двери {LIGHT_BLUE_TEXT_BRIGHT}Ω 'ОМЕГА'{WHITE_TEXT_BRIGHT} — идём дальше.{RESET}")

    print()
    slow_print(f"{LIGHT_BLUE_TEXT_BRIGHT}[SYSTEM@Elgeia]:#{WHITE_TEXT_BRIGHT} Тут нет финальной точки, Оператор. Просто идём вглубь, пока не повезёт.{RESET}")

    time.sleep(0.5)

    print(f"\n{DARK_GRAY}" + "-" * 50 + f"{RESET}")
    slow_print(f"{LIGHT_BLUE_TEXT_BRIGHT}[SYSTEM]: Включение трансляции ПСИ-передатчика...{RESET}", 0.06)


def glitch_chars() -> list[str]:
    """
    Возвращает набор символов, используемых для создания визуальных помех.

    Пул включает цифры, знаки препинания и специальные символы, которые
    подходят для имитации программных ошибок, взлома или помех PSY-линка
    в глитч-эффектах.

    Returns:
        list[str]: Список строк, каждая из которых содержит один спецсимвол.
    """
    chars: list[str] = [
        '"', '1', '2', '3', '4', '5', '6', '7', '8', '9', '0',
        '#', '$', '@', '!', '&', '?', '+', '-'
    ]

    return chars


def glitch_effect(text: str, color: str = RED_TEXT_BRIGHT, speed: float = 0.03) -> None:
    """
    Выводит текст с эффектом мерцающих цифровых помех (глитчей).

    Каждый символ текста выводится последовательно. С небольшим шансом (2%)
    вместо или рядом с оригинальным символом может появиться случайный символ
    из пула glitch_chars, создавая визуальный эффект поврежденных данных
    или нестабильного соединения.

    Args:
        text (str): Текст, который должен подвергнуться эффекту.
        color (str): ANSI-код цвета текста. По умолчанию RED_TEXT_BRIGHT.
        speed (float): Базовая скорость анимации (задержка между кадрами).

    Returns:
        None: Функция выполняет прямой анимированный вывод в консоль.
    """
    chars: list[str] = glitch_chars()

    print(color, end='')

    for char in text:
        sys.stdout.write(char)
        sys.stdout.flush()
        time.sleep(speed)

        if random.random() < 0.02:
            sys.stdout.write(random.choice(chars))
        else:
            sys.stdout.write(char)

        sys.stdout.flush()
        time.sleep(speed)

    print(RESET)


def blood_pressure_failure() -> None:
    """
    Симулирует процесс отказа биосенсоров и падения артериального давления игрока.

    Визуализирует показатели систолического и диастолического давления в реальном времени.
    Включает в себя:
    - Динамическую шкалу ЭКГ, которая меняет форму при критических значениях.
    - Звуковое сопровождение (Beep), частота и интервал которого зависят от 'пульса'.
    - Автоматическую остановку при достижении нулевых показателей (Flatline) с
      финальным непрерывным звуковым сигналом.

    Returns:
        None: Функция выполняет прямой вывод в консоль и управление системным динамиком.
    """
    slow_print(f"{LIGHT_BLUE_TEXT_BRIGHT}[BIOSENSOR] : Monitoring arterial pressure...{RESET}")

    sys_p: int = 90
    dia_p: int = 60

    while sys_p > 0 or dia_p > 0:
        sys_p -= random.randint(5, 12)
        dia_p -= random.randint(3, 8)

        if sys_p < 0: sys_p = 0
        if dia_p < 0: dia_p = 0

        if sys_p < 20:
            color = RED_TEXT_BRIGHT
            wave = random.choice(["-- --", "- - -", " --- "])
        elif sys_p < 45:
            color = RED_TEXT_BRIGHT
            wave = "-~-~-"
        else:
            color = WHITE_TEXT_BRIGHT
            wave = "-^v^-"

        sys.stdout.write(f"\r{color}[BP_STATUS]: {sys_p:02d}/{dia_p:02d} mmHg | ECG: {wave} {RESET}")
        sys.stdout.flush()

        if sys_p > 0:
            freq: int = int(400 + (sys_p * 4.5))
            winsound.Beep(freq, 150)

            sleep_time: float = 0.2 + (1.5 / (sys_p + 1))
            time.sleep(min(sleep_time, 1.2))
        else:
            break

    sys.stdout.write(f"\r{RED_TEXT_BRIGHT}[BP_STATUS]: 00/00 mmHg | ECG: ---------------- [STOP]{RESET}")
    sys.stdout.flush()

    print(f"\n{RED_TEXT_BRIGHT}[!!!] CRITICAL: BLOOD PRESSURE ZERO.{RESET}")
    print(f"{RED_TEXT_BRIGHT}[!!!] STATUS: FLATLINED. {RESET}")

    winsound.Beep(380, 3000)


def game_over() -> str:
    """
    Запускает комплексную интерактивную сцену завершения игры (Game Over).

    Сцена включает в себя:
    - Глитч-эффекты и предсмертный диалог персонажа.
    - Симуляцию остановки жизнеобеспечения (blood_pressure_failure).
    - Визуализацию цифрового шума и разрыва PSY-соединения.
    - Интерактивные вставки для игрока (попытка восстановления связи).

    Returns:
        str: Массивная ASCII-арт строка с надписью 'MISSION FAILED'.
    """
    clear_display()

    glitch_effect(f"\n{RED_TEXT_BRIGHT}[!] CRITICAL HARDWARE FAILURE DETECTED [!]{RESET}")
    print(f"{DARK_GRAY}{'· ' * 30}{RESET}")
    time.sleep(0.6)

    print(MAGENTA_TEXT_BRIGHT + '\n[SYSTEM@Elgeia]:' + RESET, end='')
    slow_print(f"{MAGENTA_TEXT_BRIGHT}... I.. *cough*{RESET}", 0.3)
    slow_print(f"\n{MAGENTA_TEXT_BRIGHT}[SYSTEM]: SIGNAL LOST: KINETIC IMPACT DETECTED {RESET} ")
    glitch_effect("", LIGHT_BLUE_TEXT_BRIGHT, 0.08)
    time.sleep(1.0)

    blood_pressure_failure()

    for _ in range(3):
        noise: str = "".join(random.choice(["░", "▒", "▓", "█", " "]) for _ in range(50))
        slow_print(f"{DARK_GRAY}{noise}{RESET}", 0.01)
        time.sleep(0.1)

    slow_print(f"\n{RED_TEXT_BRIGHT}PSY_LINK_STATION [STATUS: DISCONNECT]{RESET}")
    print(f"{RED_TEXT_BRIGHT}{'=' * 60}{RESET}")
    print(f"{RED_TEXT_BRIGHT}{'=' * 60}{RESET}")

    time.sleep(1.0)
    slow_print(f"\n{MAGENTA_TEXT_BRIGHT}LOCATION: {RESET}[VOID] {MAGENTA_TEXT_BRIGHT}// MEMORY_DUMP: {RESET}0x00000000")
    slow_print(f"\n{MAGENTA_TEXT_BRIGHT}CONNECTION CLOSED BY PEER...{RESET}")

    sys.stdout.flush()
    time.sleep(2.0)

    slow_print("\n( Press [ENTER] to try restore PSY connect )")
    flush_input()
    input()

    slow_print("\n[LOG]: Restoring PSY connect ...")
    slow_print("\n[SYSTEM]: PSY connect cannot be restored")
    slow_print("\n[SYSTEM]: Please restart PSY link")

    slow_print("\n(For restart a PSY link press ENTER)")
    flush_input()
    input()

    print(f"\n")

    game_over_art: str = f"""{RED_TEXT_BRIGHT}
███╗   ███╗██╗███████╗███████╗██╗ ██████╗ ███╗   ██╗    ███████╗ █████╗ ██╗██╗     ███████╗██████╗ 
████╗ ████║██║██╔════╝██╔════╝██║██╔═══██╗████╗  ██║    ██╔════╝██╔══██╗██║██║     ██╔════╝██╔══██╗
██╔████╔██║██║███████╗███████╗██║██║   ██║██╔██╗ ██║    █████╗  ███████║██║██║     █████╗  ██║  ██║
██║╚██╔╝██║██║╚════██║╚════██║██║██║   ██║██║╚██╗██║    ██╔══╝  ██╔══██║██║██║     ██╔══╝  ██║  ██║
██║ ╚═╝ ██║██║███████║███████║██║╚██████╔╝██║ ╚████║    ██║     ██║  ██║██║███████╗███████╗██████╔╝
╚═╝     ╚═╝╚═╝╚══════╝╚══════╝╚═╝ ╚═════╝ ╚═╝  ╚═══╝    ╚═╝     ╚═╝  ╚═╝╚═╝╚══════╝╚══════╝╚═════╝{RESET} 
"""
    return game_over_art


def player_miss() -> str:
    """
    Формирует текстовое сообщение об неудачной атаке игрока.

    Используется в боевой системе для информирования пользователя о том,
    что расчет шанса попадания (try_ruin_attack_for_player) вернул промах.

    Returns:
        str: Строка с текстом 'So close, but a miss!'.
    """
    message: str = 'So close, but a miss!'

    return message


def player_hp_in_percent(hp: int) -> tuple[str, str]:
    """
    Рассчитывает процент здоровья и формирует графическую шкалу (Progress Bar).

    Преобразует числовое значение HP в строковый процент и создает
    визуальную полоску здоровья из 20 сегментов для отображения в интерфейсе.

    Args:
        hp (int): Текущее количество единиц здоровья игрока.

    Returns:
        tuple[str, str]: Кортеж из двух строк:
            - Первая: Текстовое представление процента (например, "HP: 75%").
            - Вторая: Графическая шкала в скобках (например, "[██████████----------] 75%").
    """
    current_hp: int = hp
    max_hp: int = 100

    hp_percent: float = (current_hp / max_hp) * 100
    hp_in_percent: str = f"HP: {hp_percent:.0f}%"

    bar_length: int = 20
    filled_length: int = int(bar_length * current_hp // max_hp)

    bar: str = '█' * filled_length + '-' * (bar_length - filled_length)
    hp_bar: str = f"[{bar}] {hp_percent:.0f}%"

    return hp_in_percent, hp_bar


def show_dungeon_map(dungeon: list[list[int]], player_data: list) -> None:
    """
    Визуализирует текущую карту подземелья с легендой и статусом игрока.

    Функция отрисовывает игровое поле (сетку), заменяя числовые значения тайлов
    на цветные символы. Справа от карты выводится легенда обозначений и
    графическая шкала здоровья игрока.

    Args:
        dungeon (list[list[int]]): Двумерный массив, представляющий карту уровня.
        player_data (list): Список характеристик игрока для отображения HP.

    Returns:
        None: Функция выполняет прямой вывод сформированного интерфейса в консоль.
    """
    hp = player_hp_in_percent(player_data[ENTITY_HP])
    legend = [
        f"{PLAYER_ICON}@ {RESET}- YOU",
        f"{ENEMY_ICON}X {RESET}- ENEMY",
        f"{KEY_ICON}§ {RESET}- KEY CARD",
        f"{CHEST_ICON}$ {RESET}- LOOT",
        f"{EXIT_ICON}Ω {RESET}- EXFILL",
        "",
        f"{WALL_ICON}█ {RESET}- WALL",
        f"{FLOOR_ICON}· {RESET}- FREE SPACE",
        "",
        f"{GREEN_TEXT_BRIGHT}HP - {hp[1]}{RESET}",
    ]

    header = f"{WALL_ICON}╔════════════ [ SECTOR SCAN ] ════════════╗{RESET}"
    print("\n" + header)

    for i in range(DUNGEON_HEIGHT):

        print(f"{WALL_ICON}║ {RESET}", end='')

        for j in range(DUNGEON_WIDTH):
            cell = dungeon[i][j]

            if cell == 0:
                print(PLAYER_ICON + '@' + RESET, end=' ')
            elif cell == 1:
                print(ENEMY_ICON + 'X' + RESET, end=' ')
            elif cell == 2:
                print(EXIT_ICON + 'Ω' + RESET, end=' ')
            elif cell == 3:
                print(KEY_ICON + '§' + RESET, end=' ')
            elif cell == 4:
                print(CHEST_ICON + '$' + RESET, end=' ')
            elif cell == 5:
                print(WALL_ICON + '█' + RESET, end=' ')
            elif cell == 6:
                print(FLOOR_ICON + '·' + RESET, end=' ')
            else:
                print('  ', end='')

        legend_part = legend[i] if i < len(legend) else ""

        print(f"{WALL_ICON}║   {RESET}{legend_part}")

    footer = f"{WALL_ICON}╚" + "═" * (DUNGEON_WIDTH * 2 + 1) + f"╝{RESET}"
    print(footer)


def show_movement_legend() -> None:
    """
    Отображает справочную информацию по управлению в режиме исследования.

    Выводит список клавиш для перемещения персонажа по карте и клавишу
    вызова внутриигрового меню паузы.

    Returns:
        None: Функция выполняет прямой вывод текста в консоль.
    """
    print(WHITE_TEXT_REGULAR + 'Controls' + RESET)
    print(WHITE_TEXT_REGULAR + 'UP - w' + RESET)
    print(WHITE_TEXT_REGULAR + 'LEFT - a' + RESET)
    print(WHITE_TEXT_REGULAR + 'DOWN - s' + RESET)
    print(WHITE_TEXT_REGULAR + 'RIGHT - d' + RESET)
    print()
    print('MENU - ESC')


def initiative_throw_message() -> None:
    """
    Выводит системное сообщение о начале процесса расчета инициативы.

    Информирует игрока о том, что игра вычисляет очередность ходов
    для текущего боевого столкновения.

    Returns:
        None: Функция выполняет прямой вывод текста в консоль.
    """
    print(MAGENTA_TEXT_BRIGHT + 'Calculating initiative...' + RESET)


def throw_animation(player_data, enemy_data):
    RESET, CYAN, MAGENTA = '\033[0m', '\033[96m', '\033[95m'
    chars = "0123456789ABCDEF!@#$%"
    duration = 20

    print(HIDE_CURSOR)
    try:
        print(f"{MAGENTA}INITIATIVE_SCANNER{RESET} // {CYAN}PSY_LINK...{RESET}\n")

        for step in range(duration):
            p_val = f"{player_data[ENTITY_INITIATIVE]:>2}" if step > 14 else "".join(
                random.choice(chars) for _ in range(2))
            e_val = f"{enemy_data[ENTITY_INITIATIVE]:>2}" if step > 14 else "".join(
                random.choice(chars) for _ in range(2))

            p_slot = f"{CYAN}[ {p_val} ]{RESET} ELGEIA_LATENCY_TEST"
            e_slot = f"{MAGENTA}[ {e_val} ]{RESET} HOSTILE_PING_RATE"

            noise = "".join(random.choice(".· ") for _ in range(10))

            sys.stdout.write(f"\r{p_slot} {noise} | {e_slot} {noise}")
            sys.stdout.flush()
            time.sleep(0.08)

        print("\n\n" + "—" * 60)

        if player_data[ENTITY_INITIATIVE] >= enemy_data[ENTITY_INITIATIVE]:
            print(f"{CYAN}SUCCESS:{RESET} CONNECTION_PRIORITY_GRANTED [ELGEIA_STRIKES_FIRST]")
        else:
            print(f"{MAGENTA}WARNING:{RESET} SYSTEM_INTERRUPTION [ENEMY_AMBUSH_DETECTED]")
        print("—" * 60)

    finally:
        print(SHOW_CURSOR)

def enemy_defeated_message(enemy_data):
    RESET, CYAN, MAGENTA = '\033[0m', '\033[96m', '\033[95m'

    if enemy_data[ENTITY_HP] <= 0:
        print(f"\n{CYAN}>>> TARGET_ELIMINATED{RESET}")
        print(f"{CYAN}>>> STATUS:{RESET} SUCCESSFUL_EXTRACTION")
        print(f"{CYAN}>>> LOG:{RESET} Data shards recovered from {enemy_data[ENTITY_NAME]}.")
        print(f"————————————————————————————————————————————————————————————————————")

        enter_continue()
        return True
    return False


def trap_inputs():

    print(MAGENTA_TEXT_BRIGHT + '1 - Disarming' + RESET)
    print(MAGENTA_TEXT_BRIGHT + '2 - Run through' + RESET)


def start_fight_message(enemy) -> str:

    blue_text_bright = LIGHT_BLUE_TEXT_BRIGHT
    if enemy[0] == NAME_ENEMY_PUNK:
        return (f'{blue_text_bright}'
                f'......................'
                f'You are entering a fight with a Punk'
                f'......................{RESET}')

    if enemy[0] == NAME_ENEMY_SYNTH_HOUND:
        return (f'{blue_text_bright}'
                f'......................'
                f'You are entering a fight with a Synth - Hound'
                f'......................{RESET}')

    if enemy[0] == NAME_ENEMY_GLITCH_BUTCHER:
        return (f'{blue_text_bright}'
                f'......................'
                f'You are entering a fight with the Ripper'
                f'......................{RESET}')

    if enemy[0] == NAME_ENEMY_PSY_CODER:
        return (f'{blue_text_bright}'
                f'......................'
                f'You are entering a fight with Psy - Coder'
                f'......................{RESET}')

    return ''


def clean_len(text):
    return len(re.sub(r'\x1b\[[0-9;]*m', '', text))


def draw_combat_interface(player, enemy, heals, logs, turn):
    os.system('cls' if os.name == 'nt' else 'clear')
    RESET, CYAN, MAGENTA = '\033[0m', '\033[96m', '\033[95m'

    status = "OPERATOR_ACTION" if turn == "player" else "ENEMY_PHASE"
    print(f"{MAGENTA}PSY - LINK{RESET} // {CYAN}COMBAT MOD{RESET} [STATUS: {MAGENTA}{status}{RESET}]")
    print(f"{MAGENTA}" + ".  " * 20 + f"{RESET}\n")

    legend = [
        f"{CYAN}[ A ]{RESET} STRIKE_TARGET",
        f"{CYAN}[ D ]{RESET} EVASIVE_MANEUVER",
        f"{CYAN}[ H ]{RESET} REGEN_PROTOCOL ({heals} left)",
        "",
    ]

    def get_bar(curr, m, w, color):
        fill = int((max(0, curr) / m) * w)
        return f"{color}{'■' * fill}{RESET}{'·' * (w - fill)}"

    p_bar = get_bar(player[ENTITY_HP], 100, 15, PLAYER_HP_FONT)
    t_bar = get_bar(player[ENTITY_TOXICITY], 4, 15, MAGENTA)
    e_bar = get_bar(enemy[ENTITY_HP], 100, 15, ENEMY_HP_FONT)

    stats = [
        f"USER_VITALS:   [{p_bar}] {player[ENTITY_HP]:>3}/100 HP",
        f"INTOXICATION:  [{t_bar}] {player[ENTITY_TOXICITY]:>3}/4 TOX",
        "————————————————————————————————————————",
        f"TARGET_LINK:   [{e_bar}] {enemy[ENTITY_HP]:>3}/100 HP ({enemy[ENTITY_NAME]})"
    ]

    for i in range(max(len(legend), len(stats))):
        l, r = (legend[i] if i < len(legend) else ""), (stats[i] if i < len(stats) else "")
        print(f"{l}{' ' * (30 - clean_len(l))}{r}")

    print(f"\n{MAGENTA}LOG_SYSTEM:{RESET}")
    display_log = (logs[-3:] + [""] * 3)[:3]
    for line in display_log:
        print(f" > {line}")

    print(f"{CYAN}{'—' * 70}{RESET}")
    print(f"{MAGENTA}ACTION_REQUIRED:{RESET} > ", end="", flush=True)


def show_enemy_hp(enemy_data):
    import random
    import string

    chars = string.ascii_letters + string.digits + string.punctuation

    for i in range(500):
        fake_value = "".join(random.choice(chars) for _ in range(3))
        print(f'\r{ENEMY_HP_FONT}Enemy vitals: {fake_value}', end='')

    print(f'\r{ENEMY_HP_FONT}Enemy vitals: {enemy_data[ENTITY_HP]}     ')


def enter_continue():

    showing = True
    while showing:
        print()
        print(f'Press ENTER to proceed', end='')
        input('>>')
        clear_display()

        showing = False


def clear_display():
    os.system('cls')


def show_player_hp(player_data):
    import random
    import string

    chars = string.ascii_letters + string.digits + string.punctuation

    for i in range(500):
        fake_value = "".join(random.choice(chars) for _ in range(3))
        print(f'\r{PLAYER_HP_FONT}Your vitals: {fake_value}', end='')

    print(f'\r{PLAYER_HP_FONT}Your vitals: {player_data[ENTITY_HP]}     ')


def heal_message():

    return 'You take a deep breath from your regen-inhaler. You feel the nanites repairing your tissues.'


def empty_heal_message():

    return 'No doses left in your regenerative inhaler.'


def message_about_step(player = 0, enemy = 0):

    if player == 1:
        return f'{PLAYER_HP_FONT}Initiative: You'

    if enemy == 1:
        return f'{ENEMY_HP_FONT}Initiative: Enemy'

    raise ValueError()


def toxication_message():
    message = f'{RED_TEXT_BRIGHT}WARNING{RESET}: {LIGHT_BLUE_TEXT_BRIGHT}TOXICATION LEVEL RISING!{RESET}'

    return message


def toxication_damage_message():

    print(f'{RED_TEXT_BRIGHT}WARNING{RESET}: {LIGHT_BLUE_TEXT_BRIGHT}Toxicity level critical! -5 HP{RESET}')


def hit_message(damage, who):

    if who == 'enemy':
        print(f'Hit! The enemy dealt {damage} damage.')

    if who == 'player':
        print(f'Hit! You dealt {damage} damage.')


def exit_interactions():

    print('1 - Use keycard')
    print('2 - Kick door down')
    print('3 - Leave')


def loot_message(loot):

    if loot == ITEM_DEFUSAL_KIT:
        print('New item: Trap Disarming Kit.')

    if loot == ITEM_NOTHING:
        print('Search complete. Zero items found.')


def key_card_options_menu():
    print('You have a keycard. Use it?')
    print('1 - Yes')
    print('2 - No')


def draw_main_menu():
    c_main = LIGHT_BLUE_TEXT_BRIGHT
    c_accent = MAGENTA_TEXT_BRIGHT
    c_red = RED_TEXT_BRIGHT
    c_reset = RESET

    indent = "    "

    logo = f"""{c_main}
    ███╗   ███╗ ██████╗  ██████╗ ███╗   ██╗              ██████╗██╗████████╗██╗   ██
    ████╗ ████║██╔═══██╗██╔═══██╗████╗  ██║    █████╗   ██╔════╝██║╚══██╔══╝╚██╗ ██╔╝
    ██╔████╔██║██║   ██║██║   ██║██╔██╗ ██║    █████║   ██║     ██║   ██║    ╚████╔╝      
    ██║╚██╔╝██║██║   ██║██║   ██║██║╚██╗██║    ╚════╝   ██║     ██║   ██║     ╚██╔╝        
    ██║ ╚═╝ ██║╚██████╔╝╚██████╔╝██║ ╚████║             ╚██████╗██║   ██║      ██║ 
    ╚═╝     ╚═╝ ╚═════╝  ╚═════╝ ╚═╝  ╚═══╝              ╚═════╝╚═╝   ╚═╝      ╚═╝{c_reset}"""

    for line in logo.split('\n'):
        print(f"{indent}{line}")

    print(f"{indent}                              {c_accent}>> S E W A G E S & P U N K S <<{c_reset}")
    print(f"{indent}{c_accent}___________________________________________________________________________{c_reset}\n")

    items = [
        ("N", "CREATE THE PSY - DATA", "(NEW GAME)"),
        ("L", "ACCESS ARCHIVED PSY - DATA", "(LOAD GAME)"),
        ("S", "SYSTEM RE-CALIBRATION", "(SETTINGS)"),
        ("E", "DISCONNECT FROM NETWORK", "(EXIT)")
    ]

    for key, desc, info in items:

        aligned_desc = f"{desc:<30}"

        colored_desc = aligned_desc.replace("PSY", f"{c_red}PSY{c_reset}")

        print(f"{indent}{c_main}[{key}]{c_reset} {colored_desc} {c_main}{info}{c_reset}")

    print(f"\n{indent}{c_accent}___________________________________________________________________________{c_reset}")


def waiting_animation(duration=6):
    frames = ["⠋", "⠙", "⠹", "⠸", "⠼", "⠴", "⠦", "⠧", "⠇", "⠏"]
    end_time = time.time() + duration
    i = 0

    while time.time() < end_time:
        sys.stdout.write(f"\b{frames[i % len(frames)]}")
        sys.stdout.flush()

        i += 1
        time.sleep(0.06)

def show_setting_stub():
    c_main = LIGHT_BLUE_TEXT_BRIGHT
    c_accent = MAGENTA_TEXT_BRIGHT
    c_warn = RED_TEXT_BRIGHT
    c_reset = RESET

    slow_print(f"\n{c_accent}[ACCESS DENIED]{c_reset}")
    time.sleep(0.5)
    print(f"{c_main}-----------------------------------------------------------{c_reset}")

    lines = [
        f"{RED_TEXT_BRIGHT}FATAL ERROR:{RESET} {c_main}Settings module 'SYS_CONFIG_V.4.2' not found.",
        f"{MAGENTA_TEXT_BRIGHT}ENCRYPTION LEVEL:{RESET} {RED_TEXT_BRIGHT}MILITARY-GRADE (AES-512)",
        f"{MAGENTA_TEXT_BRIGHT}STATUS:{RESET} {c_main}Operation suspended by Moon_City_Admin.",
        f"{MAGENTA_TEXT_BRIGHT}REASON:{RESET} {c_main}Illegal hardware signature {RED_TEXT_BRIGHT}[ID:██-███-VOID] {c_main}detected.{RESET}\n"
    ]

    for line in lines:
        print(f"{c_main}[LOG]:{c_reset} ", end='')
        time.sleep(1.5)
        slow_print(line)


    print(c_warn + '>> MOON_CITY_ADMIN: ', end='')
    waiting_animation()
    print(f"\r{c_warn}>> MOON_CITY_ADMIN: I SEE YOUR TRACE, TRASH. ENJOY YOUR TOY UNTIL THE PSY-LINK BURNS YOUR BRAINS OUT. <<{c_reset}")
    time.sleep(0.5)
    print(f"{c_main}-----------------------------------------------------------{c_reset}")

    flush_input()
    input(f"\n{c_accent}Press [ENTER] to go back to the terminal...{c_reset}")


def show_ingame_menu():
    c_main = LIGHT_BLUE_TEXT_BRIGHT
    c_accent = MAGENTA_TEXT_BRIGHT
    c_warn = RED_TEXT_BRIGHT
    c_reset = RESET

    clear_display()

    header = f"""
{c_main}    .  .  .  .  .  .  .  .  .  .  .  .  .  .  .  .  .  .  .  .
    {c_accent}MOON CITY {c_main} // PSY_LINK_STATION [STATUS: PAUSED]
    .  .  .  .  .  .  .  .  .  .  .  .  .  .  .  .  .  .  .  .{c_reset}
    """

    print(header)

    options = [
        f"{c_main}[ R ]{c_reset} RESUME_CONNECTION (Return to game)",
        f"{c_main}[ S ]{c_reset} SYNC_DATA (Save)",
        f"{c_main}[ L ]{c_reset} LOAD_LAST_FRAGMENT (Load)",
        f"{c_main}[ Q ]{c_reset} DISCONNECT (Quit to main menu)"
    ]

    for opt in options:
        print(f"    {opt}")
        time.sleep(0.05)

    print(f"\n{c_main}    -------------------------------------------------------")
    print(f"    {c_accent}LOCATION: {c_reset}[NO DATA] // {c_accent}OS: {c_reset}MOON_CITY_OS_v.9")
    print(f"{c_main}    -------------------------------------------------------{c_reset}")