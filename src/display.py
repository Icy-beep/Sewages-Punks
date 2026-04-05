import os
import time
import sys
import random

from src.constants import *

INPUT_PLAYER_NAME_MESSAGE = r'Enter your name'
YOU_TRY_OPEN_DOR_MESSAGE = r'You try open dor'
CARD_READER_MESSAGE = r'You ran the keycard across the scanner. The device emitted a satisfying chime of access granted, and the door groaned open with a faint metallic screech'
DOOR_INTERACTION_MESSAGE = r"You move away from the entrance or exit... it's a matter of perspective."
KICK_THE_DOOR_MESSAGE = r"You kick the door. The bang echoes through the sewers, but the door won't budge."
STEP_OUT_THE_DOOR_MESSAGE = r"You move away from the entrance or exit... it's a matter of perspective."
YOU_FOUND_KEY_CARD_MESSAGE = r'You found a keycard'
TRAP_FORWARD_MESSAGE = r"There's a trap right in front of you."
TRAP_DEFUSED_MESSAGE = r"Trap neutralized."
YOU_DONT_HAVE_DEFKIT_MESSAGE = r"Required tools not detected. You need a disarm kit to proceed."
TRAP_ACTIVATED_MESSAGE = r"You dashed through, and the trap triggered behind your back."
TRAP_DAMAGED_PLAYER_IF_HE_RUN_MESSAGE = r"Failed to evade. Trap triggered. Damage taken: -5 HP"
PLAYER_TRY_DODGE_MESSAGE = f"{BLUE_TEXT_BRIGHT}Evasion attempt successful. Enemy accuracy decreased.{RESET}"
ENEMY_MISS_MESSAGE = r"The shot went wide."
ENEMY_WIN_MESSAGE = r"You have been defeated."

PLAYER_WORD_VARIABLE = 'player'
ENEMY_WORD_VARIABLE = 'enemy'


def skip_message():
    message = (f'{LIGHT_BLUE_TEXT_BRIGHT}Skip the prologue?\n'
               f'[ Y ] Yes\n'
               f'[ N ] No{RESET}')

    return message

def slow_print(text, speed=0.03):
    for char in text:
        sys.stdout.write(char)
        sys.stdout.flush()
        time.sleep(speed)
    print()

def start_message():
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


def game_over():
    game_over_art = f"""{RED_TEXT_BRIGHT}
 ██████   █████  ███    ███ ███████     ██████  ██    ██ ███████ ██████  
 ██   ██ ██   ██ ████  ████ ██          ██    ██ ██    ██ ██      ██   ██ 
 ██   ██ ███████ ██ ████ ██ █████       ██    ██ ██    ██ █████   ██████  
 ██   ██ ██   ██ ██  ██  ██ ██          ██    ██  ██  ██  ██      ██   ██ 
 ██████  ██   ██ ██      ██ ███████      ██████    ████   ███████ ██   ██ 
 ╚═════╝ ╚═════╝ ╚══════╝  ╚═══════╝     ╚═════╝    ╚══╝   ╚══════╝ ╚══════╝ 
                    {RESET}"""

    return game_over_art

def player_miss():
    message = 'So close, but a miss!'

    return message


def show_dungeon_map(dungeon):
    legend = [
        f"{PLAYER_ICON}@ {RESET}- YOU",
        f"{ENEMY_ICON}X {RESET}- ENEMY",
        f"{KEY_ICON}§ {RESET}- KEY CARD",
        f"{CHEST_ICON}$ {RESET}- LOOT",
        f"{EXIT_ICON}Ω {RESET}- EXFILL",
        "",
        f"{WALL_ICON}█ {RESET}- WALL",
        f"{FLOOR_ICON}· {RESET}- FREE SPACE"
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


def show_movement_legend():
    print(WHITE_TEXT_REGULAR + 'Controls' + RESET)
    print(WHITE_TEXT_REGULAR + 'UP - w' + RESET)
    print(WHITE_TEXT_REGULAR + 'LEFT - a' + RESET)
    print(WHITE_TEXT_REGULAR + 'DOWN - s' + RESET)
    print(WHITE_TEXT_REGULAR + 'RIGHT - d' + RESET)
    print()
    print('MENU - ESC')


def initiative_throw_message():

    print(MAGENTA_TEXT_BRIGHT + 'Calculating initiative...' + RESET)


def throw_animation(player_data, enemy_data):
    chars = "0123456789@#$%&*+=-/<>ABCDEF"
    width = 50
    height = 5
    duration = 25

    green = GREEN_TEXT_BRIGHT
    red = RED_TEXT_BRIGHT
    light_blue = LIGHT_BLUE_TEXT_BRIGHT
    hide = HIDE_CURSOR
    show = SHOW_CURSOR

    print(hide)

    try:
        for step in range(duration):
            output = []

            output.append(f"{green}--- YOUR INITIATIVE SECTOR ---{RESET}")
            for y in range(height):
                line = "".join(random.choice(chars) for _ in range(width))
                if y == height // 2:
                    val = str(player_data[ENTITY_INITIATIVE]) if step > 15 else str(random.randint(10, 99))
                    line = f"{light_blue}{line[:20]}{green}[ {val} ]{light_blue}{line[26:]}{RESET}"
                else:
                    line = f"{light_blue}{line}{RESET}"
                output.append(line)

            output.append("")

            output.append(f"{red}--- ENEMY INITIATIVE SECTOR ---{RESET}")
            for y in range(height):
                line = "".join(random.choice(chars) for _ in range(width))
                if y == height // 2:
                    val = str(enemy_data[ENTITY_INITIATIVE]) if step > 15 else str(random.randint(10, 99))
                    line = f"{light_blue}{line[:20]}{red}[ {val} ]{light_blue}{line[26:]}{RESET}"
                else:
                    line = f"{light_blue}{line}{RESET}"
                output.append(line)

            sys.stdout.write("\n".join(output) + f"\033[{height * 2 + 4}A\r")
            sys.stdout.flush()
            time.sleep(0.06)

        print("\n" * (height * 2 + 5))

        if player_data[ENTITY_INITIATIVE] >= enemy_data[ENTITY_INITIATIVE]:
            print(f"{green}>>> {player_data[ENTITY_NAME]} ACTS FIRST!{RESET}\n")
        else:
            print(f"{red}>>> {enemy_data[ENTITY_NAME]} AMBUSH!{RESET}\n")

    finally:
        print(show)


def trap_inputs():

    print(MAGENTA_TEXT_BRIGHT + '1 - Disarming' + RESET)
    print(MAGENTA_TEXT_BRIGHT + '2 - Run through' + RESET)


def start_fight_message(enemy) -> str:

    if enemy[0] == NAME_ENEMY_PUNK:
        return (f'{BLUE_TEXT_BRIGHT}'
                f'......................'
                f'You are entering a fight with a Punk'
                f'......................{RESET}')

    if enemy[0] == NAME_ENEMY_SYNTH_HOUND:
        return (f'{BLUE_TEXT_BRIGHT}'
                f'......................'
                f'You are entering a fight with a Synth - Hound'
                f'......................{RESET}')

    if enemy[0] == NAME_ENEMY_GLITCH_BUTCHER:
        return (f'{BLUE_TEXT_BRIGHT}'
                f'......................'
                f'You are entering a fight with the Ripper'
                f'......................{RESET}')

    if enemy[0] == NAME_ENEMY_PSY_CODER:
        return (f'{BLUE_TEXT_BRIGHT}'
                f'......................'
                f'You are entering a fight with Psy - Coder'
                f'......................{RESET}')

    return ''


def show_battle_information(player, enemy):
    import random
    import time
    import string

    clear_display()

    player_hp = player[ENTITY_HP]

    enemy_hp = enemy[ENTITY_HP]

    chars = string.ascii_letters + string.digits + string.punctuation

    print()

    for i in range(500):
        fake_value = "".join(random.choice(chars) for _ in range(10))
        print(f'\r{PLAYER_HP_FONT}Your vitals: {fake_value}', end='')
        time.sleep(0.001)

    print(f'\r{PLAYER_HP_FONT}Your vitals: {player_hp}       ')

    print()

    for i in range(500):
        fake_value = "".join(random.choice(chars) for _ in range(10))
        print(f'\r{ENEMY_HP_FONT}Enemy vitals: {fake_value}', end='')
        time.sleep(0.001)

    print(f'\r{ENEMY_HP_FONT}Enemy vitals: {enemy_hp}        ')


def show_combat_legend():
    print('a - Attack')
    print('d - Defend')
    print('i - Scan')
    print('h - Heal')


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

        print(f"{indent}{c_main}[ {key} ]{c_reset} {colored_desc} {c_main}{info}{c_reset}")

    print(f"\n{indent}{c_accent}___________________________________________________________________________{c_reset}")


def show_setting_stub():
    c_main = LIGHT_BLUE_TEXT_BRIGHT
    c_accent = MAGENTA_TEXT_BRIGHT
    c_warn = RED_TEXT_BRIGHT
    c_reset = RESET

    print(f"\n{c_accent}[ ACCESS DENIED ]{c_reset}")
    print(f"{c_main}-----------------------------------------------------------{c_reset}")

    lines = [
        f"{RED_TEXT_BRIGHT}FATAL ERROR:{RESET} {c_main}Settings module 'SYS_CONFIG_V.4.2' not found.",
        f"{MAGENTA_TEXT_BRIGHT}ENCRYPTION LEVEL:{RESET} {RED_TEXT_BRIGHT}MILITARY-GRADE (AES-512)",
        f"{MAGENTA_TEXT_BRIGHT}STATUS:{RESET} {c_main}Operation suspended by Moon_City_Admin.",
        f"{MAGENTA_TEXT_BRIGHT}REASON:{RESET} {c_main}Illegal hardware signature {RED_TEXT_BRIGHT}[ID:██-███-VOID] {c_main}detected.{RESET}"
    ]

    for line in lines:
        print(f"{c_main}[ LOG ]:{c_reset} {line}")
        time.sleep(0.1)

    print(f"\n{c_warn}>> MOON_CITY_ADMIN: I SEE YOUR TRACE, TRASH. ENJOY YOUR TOY UNTIL THE PSY-LINK BURNS YOUR BRAINS OUT. <<{c_reset}")
    print(f"{c_main}-----------------------------------------------------------{c_reset}")

    input(f"\n{c_accent}Press [ENTER] to go back to the terminal...{c_reset}")


def show_ingame_menu():
    c_main = LIGHT_BLUE_TEXT_BRIGHT
    c_accent = MAGENTA_TEXT_BRIGHT
    c_warn = RED_TEXT_BRIGHT
    c_reset = RESET

    clear_display()

    header = f"""
{c_main}    .  .  .  .  .  .  .  .  .  .  .  .  .  .  .  .  .  .  .  .
    {c_accent}MOON CITY {c_main} // NEURAL_LINK_STATION [STATUS: PAUSED]
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