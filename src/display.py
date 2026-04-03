import os
import time

from src.constants import *

GAME_OVER_MESSAGE = 'GAME OVER'
INPUT_PLAYER_NAME_MESSAGE = 'Введите имя персонажа'
YOU_TRY_OPEN_DOR_MESSAGE = 'Вы пытаетесь открыть дверь'
CARD_READER_MESSAGE = 'Вы провели ключ-картой по считывателю, кардридер издал приятный одобрительный звук и дверь с небольшим скрипом приоткрылась'
DOOR_INTERACTION_MESSAGE = 'Вы отходите от двери'
KICK_THE_DOOR_MESSAGE = 'Вы бьёте ногой по двери грохот раздался по всей канализации но дверь не открылась'
STEP_OUT_THE_DOOR_MESSAGE = 'Вы отходите от двери'
YOU_FOUND_KEY_CARD_MESSAGE = 'Вы нашли ключ-карту'
TRAP_FORWARD_MESSAGE = 'Перед вами ловушка'
TRAP_DEFUSED_MESSAGE = 'Ловушка обезврежена'
YOU_DONT_HAVE_DEFKIT_MESSAGE = 'У вас нет набора для обезвреживания ловушки'
TRAP_ACTIVATED_MESSAGE = 'Вы пробежали, ловушка активировалась у вас за спиной'
TRAP_DAMAGED_PLAYER_IF_HE_RUN_MESSAGE = 'Вы не успели ловушка вас зацепила -5HP'
PLAYER_TRY_DODGE_MESSAGE = 'Вы пытаетесь уклониться шанс промаха противника увеличен'
ENEMY_MISS_MESSAGE = 'Враг промахнулся'
ENEMY_WIN_MESSAGE = 'Враг победил'

PLAYER_WORD_VARIABLE = 'player'
ENEMY_WORD_VARIABLE = 'enemy'

MISS_WORD = 'Промах!'

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
    print(WHITE_TEXT_BRIGHT + 'Передвижение' + RESET)
    print(WHITE_TEXT_BRIGHT + 'Верх - w' + RESET)
    print(WHITE_TEXT_BRIGHT + 'Лево - a' + RESET)
    print(WHITE_TEXT_BRIGHT + 'Низ - s' + RESET)
    print(WHITE_TEXT_BRIGHT + 'Право - d' + RESET)


def initiative_throw_message():

    print(WHITE_TEXT_BRIGHT + 'Решается чей ход первый' + RESET)


def throw_animation(player_data, enemy_data):
    import random
    import string
    import time

    chars = string.ascii_letters + string.digits + string.punctuation

    print()


    for i in range(50):
        fake_value = "".join(random.choice(chars) for _ in range(8))

        print(f"\rВаша инициатива: {fake_value}", end='')
        time.sleep(0.04)

    print(f'\rВаша инициатива: {player_data[ENTITY_INITIATIVE]}         ')

    for i in range(50):
        fake_value = "".join(random.choice(chars) for _ in range(8))

        print(f"\rИнициатива врага: {fake_value}", end='')
        time.sleep(0.04)

    print(f'\rИнициатива врага: {enemy_data[ENTITY_INITIATIVE]}        ')


def trap_inputs():

    print(MAGENTA_TEXT_BRIGHT + '1 - Обезвредить' + RESET)
    print(MAGENTA_TEXT_BRIGHT + '2 - Пробежать' + RESET)


def start_fight_message(enemy) -> str:

    if enemy[0] == NAME_ENEMY_PUNK:
        return f'{START_FIGHT_MESSAGE_FONT}Вы вступаете в бой с панком{RESET}'

    if enemy[0] == NAME_ENEMY_SYNTH_HOUND:
        return f'{START_FIGHT_MESSAGE_FONT}Вы вступаете в бой с синт. гончей{RESET}'

    if enemy[0] == NAME_ENEMY_GLITCH_BUTCHER:
        return f'{START_FIGHT_MESSAGE_FONT}Вы вступаете в бой с мясником{RESET}'

    if enemy[0] == NAME_ENEMY_PSY_CODER:
        return f'{START_FIGHT_MESSAGE_FONT}Вы вступаете в бой с пси-кодером{RESET}'

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
        print(f'\r{PLAYER_HP_FONT}Ваше здоровье: {fake_value}', end='')
        time.sleep(0.001)

    print(f'\r{PLAYER_HP_FONT}Ваше здоровье: {player_hp}       ')

    print()

    for i in range(500):
        fake_value = "".join(random.choice(chars) for _ in range(10))
        print(f'\r{ENEMY_HP_FONT}Здоровье противника: {fake_value}', end='')
        time.sleep(0.001)

    print(f'\r{ENEMY_HP_FONT}Здоровье противника: {enemy_hp}        ')


def show_combat_legend():
    print('a - атака')
    print('d - защита')
    print('i - информация о битве')
    print('h - лечение')


def show_enemy_hp(enemy_data):
    import random
    import string

    chars = string.ascii_letters + string.digits + string.punctuation

    for i in range(500):
        fake_value = "".join(random.choice(chars) for _ in range(3))
        print(f'\r{ENEMY_HP_FONT}Здоровье противника: {fake_value}', end='')

    print(f'\r{ENEMY_HP_FONT}Здоровье противника: {enemy_data[ENTITY_HP]}     ')


def enter_continue():

    showing = True
    while showing:
        print()
        print('нажмите ENTER чтобы продолжить')
        user_input = input('>>')
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
        print(f'\r{PLAYER_HP_FONT}Ваше здоровье: {fake_value}', end='')

    print(f'\r{PLAYER_HP_FONT}Ваше здоровье: {player_data[ENTITY_HP]}     ')


def heal_message():

    print('Вы использовали свой регенеративный ингалятор')


def empty_heal_message():

    print('Ваш регенеративный ингалятор пуст')


def message_about_step(player = 0, enemy = 0):

    if player == 1:
        print(f'{PLAYER_HP_FONT}Ваш ход')

    if enemy == 1:
        print(f'{ENEMY_HP_FONT}Ход противника')


def toxication_message():

    print('Уровень интоксикации увеличен')


def toxication_damage_message():

    print('Уровень интоксикации критический -5HP')


def hit_message(damage, who):

    if who == 'enemy':
        print(f'Попадание, враг нанес {damage} - урона')

    if who == 'player':
        print(f'Попадание, вы нанесли {damage} - урона')


def exit_interactions():

    print('1 - Открыть ключ-картой')
    print('2 - Выбить ногой')
    print('3 - Уйти')


def loot_message(loot):

    if loot == ITEM_DEFUSAL_KIT:
        print('Вы нашли набор для обезвреживания ловушек')

    if loot == ITEM_NOTHING:
        print('Вы ничего не нашли')


def key_card_options_menu():
    print('У вас есть ключ-карта, применить?')
    print('1 - Да')
    print('2 - Нет')


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