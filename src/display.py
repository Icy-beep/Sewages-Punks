import os
import time

from src.constants import *

GAME_OVER_MESSAGE = r'GAME OVER'
INPUT_PLAYER_NAME_MESSAGE = r'Enter your name'
YOU_TRY_OPEN_DOR_MESSAGE = r'You try open dor'
CARD_READER_MESSAGE = r'You ran the keycard across the scanner. The device emitted a satisfying chime of access granted, and the door groaned open with a faint metallic screech'
DOOR_INTERACTION_MESSAGE = r"You move away from the entrance or exit... it's a matter of perspective."
KICK_THE_DOOR_MESSAGE = r'Вы бьёте ногой по двери грохот раздался по всей канализации но дверь не открылась'
STEP_OUT_THE_DOOR_MESSAGE = r"You move away from the entrance or exit... it's a matter of perspective."
YOU_FOUND_KEY_CARD_MESSAGE = r'You found a keycard'
TRAP_FORWARD_MESSAGE = r"There's a trap right in front of you."
TRAP_DEFUSED_MESSAGE = r"Trap neutralized."
YOU_DONT_HAVE_DEFKIT_MESSAGE = r"Required tools not detected. You need a disarm kit to proceed."
TRAP_ACTIVATED_MESSAGE = r"You dashed through, and the trap triggered behind your back."
TRAP_DAMAGED_PLAYER_IF_HE_RUN_MESSAGE = r"Failed to evade. Trap triggered. Damage taken: -5 HP"
PLAYER_TRY_DODGE_MESSAGE = r"Evasion attempt successful. Enemy accuracy decreased."
ENEMY_MISS_MESSAGE = r"The shot went wide."
ENEMY_WIN_MESSAGE = r"You have been defeated."

PLAYER_WORD_VARIABLE = 'player'
ENEMY_WORD_VARIABLE = 'enemy'

MISS_WORD = 'Miss!'

def show_dungeon_map(dungeon):

    for i in range(DUNGEON_HEIGHT):
        print()
        for j in range(DUNGEON_WIDTH):
            print(end=' ')

            if dungeon[i][j] == 0:
                print(PLAYER_ICON + '@' + RESET, end='')

            if dungeon[i][j] == 1:
                print(ENEMY_ICON + 'F' + RESET, end='')

            if dungeon[i][j] == 2:
                print(EXIT_ICON + 'E' + RESET, end='')

            if dungeon[i][j] == 3:
                print(KEY_ICON + 'K' + RESET, end='')

            if dungeon[i][j] == 4:
                print(CHEST_ICON + 'C' + RESET, end='')

            if dungeon[i][j] == 5:
                print(WALL_ICON + '█' + RESET, end='')

            if dungeon[i][j] == 6:
                print(FLOOR_ICON + '.' + RESET, end='')

            if dungeon[i][j] == 7:
                print(TRAP_ICON + '.' + RESET, end='')

    return ''


def show_movement_legend():
    print(WHITE_TEXT_BRIGHT + 'Movement' + RESET)
    print(WHITE_TEXT_BRIGHT + 'Up - w' + RESET)
    print(WHITE_TEXT_BRIGHT + 'Left - a' + RESET)
    print(WHITE_TEXT_BRIGHT + 'Down - s' + RESET)
    print(WHITE_TEXT_BRIGHT + 'Right - d' + RESET)


def initiative_throw_message():

    print(WHITE_TEXT_BRIGHT + 'Calculating initiative...' + RESET)


def throw_animation(player_data, enemy_data):
    import random
    import string
    import time

    chars = string.ascii_letters + string.digits + string.punctuation

    print()


    for i in range(50):
        fake_value = "".join(random.choice(chars) for _ in range(8))

        print(f"\rYour initiative: {fake_value}", end='')
        time.sleep(0.04)

    print(f'\rYour initiative: {player_data[ENTITY_INITIATIVE]}         ')

    for i in range(50):
        fake_value = "".join(random.choice(chars) for _ in range(8))

        print(f"\rEnemy initiative: {fake_value}", end='')
        time.sleep(0.04)

    print(f'\rEnemy initiative: {enemy_data[ENTITY_INITIATIVE]}        ')


def trap_inputs():

    print(MAGENTA_TEXT_BRIGHT + '1 - Disarming' + RESET)
    print(MAGENTA_TEXT_BRIGHT + '2 - Run through' + RESET)


def start_fight_message(enemy) -> str:

    if enemy[0] == NAME_ENEMY_PUNK:
        return f'{START_FIGHT_MESSAGE_FONT}You are entering a fight with a Punk{RESET}'

    if enemy[0] == NAME_ENEMY_SYNTH_HOUND:
        return f'{START_FIGHT_MESSAGE_FONT}You are entering a fight with a Synth - Hound{RESET}'

    if enemy[0] == NAME_ENEMY_GLITCH_BUTCHER:
        return f'{START_FIGHT_MESSAGE_FONT}You are entering a fight with the Ripper{RESET}'

    if enemy[0] == NAME_ENEMY_PSY_CODER:
        return f'{START_FIGHT_MESSAGE_FONT}You are entering a fight with Psy - Coder{RESET}'

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
        print(f'......................'
              f'Press ENTER to proceed'
              f'......................')
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

    print('You take a deep breath from your regen-inhaler. You feel the nanites repairing your tissues.')


def empty_heal_message():

    print('No doses left in your regenerative inhaler.')


def message_about_step(player = 0, enemy = 0):

    if player == 1:
        print(f'{PLAYER_HP_FONT}Initiative: Player')

    if enemy == 1:
        print(f'{ENEMY_HP_FONT}Initiative: Enemy')


def toxication_message():

    print('Toxicity level rising')


def toxication_damage_message():

    print('WARNING: Toxicity level critical. Health failing. -5 HP')


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
    c_reset = RESET

    logo = f"""
    {c_main}  ██████╗███████╗██╗    ██╗ █████╗  ██████╗ ███████╗███████╗
      ██╔════╝██╔════╝██║    ██║██╔══██╗██╔════╝ ██╔════╝██╔════╝
      ╚█████╗ █████╗  ██║ █╗ ██║███████║██║  ███╗█████╗  ███████╗
       ╚═══██╗██╔══╝  ██║███╗██║██╔══██║██║   ██║██╔══╝  ╚════██║
      ██████╔╝███████╗╚███╔███╔╝██║  ██║╚██████╔╝███████╗███████║
      ╚═════╝ ╚══════╝ ╚══╝╚══╝ ╚═╝  ╚═╝ ╚═════╝ ╚══════╝╚══════╝
                  {c_accent}>> S E W A G E S _ P U N K S <<{c_main}
    {c_accent}  ___________________________________________________________{c_reset}
        """
    print(logo)
    print(f"{c_main}[ 1 ]{c_reset} INITIALIZE NEURAL LINK (NEW GAME)")
    print(f"{c_main}[ 2 ]{c_reset} RECOVER MEMORY FRAGMENT (LOAD GAME)")
    print(f"{c_main}[ 3 ]{c_reset} SYSTEM CALIBRATION (SETTINGS)")
    print(f"{c_main}[ 4 ]{c_reset} TERMINATE SESSION (EXIT)")
    print(f"{c_accent}  ___________________________________________________________{c_reset}")


def show_setting_stub():
    c_main = LIGHT_BLUE_TEXT_BRIGHT
    c_accent = MAGENTA_TEXT_BRIGHT
    c_warn = RED_TEXT_BRIGHT
    c_reset = RESET

    print(f"\n{c_accent}[ ACCESS DENIED ]{c_reset}")
    print(f"{c_main}-----------------------------------------------------------{c_reset}")

    lines = [
        "FATAL ERROR: Settings module 'SYS_CONFIG_V.4.2' not found.",
        "ENCRYPTION LEVEL: MILITARY-GRADE (AES-512)",
        "STATUS: Operation suspended by Moon_City_Admin.",
        "REASON: Neural link synchronization in progress..."
    ]

    for line in lines:
        print(f"{c_main}[ LOG ]:{c_reset} {line}")
        time.sleep(0.1)

    print(f"\n{c_warn}>> ПОЖАЛУЙСТА, ОБРАТИТЕСЬ К БЛИЖАЙШЕМУ ПСИ-ДОКУ ДЛЯ ОБНОВЛЕНИЯ ПО <<{c_reset}")
    print(f"{c_main}-----------------------------------------------------------{c_reset}")

    input(f"\n{c_accent}Нажмите [ENTER], чтобы вернуться в терминал...{c_reset}")


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