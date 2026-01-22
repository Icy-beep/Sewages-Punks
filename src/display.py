import os
from _pyrepl.commands import clear_screen

from src.constants import *


def show_dungeon_map(dungeon):

    for i in range(DUNGEON_HEIGHT):
        print()
        for j in range(DUNGEON_WIDTH):
            print(end=' ')

            if dungeon[i][j] == 0:
                print(PLAYER_ICON + '@', end='')

            if dungeon[i][j] == 1:
                print(ENEMY_ICON + 'F', end='')

            if dungeon[i][j] == 2:
                print(EXIT_ICON + 'E', end='')

            if dungeon[i][j] == 3:
                print(KEY_ICON + 'K', end='')

            if dungeon[i][j] == 4:
                print(CHEST_ICON + 'C', end='')

            if dungeon[i][j] == 5:
                print(WALL_ICON + '█', end='')

            if dungeon[i][j] == 6:
                print(FLOOR_ICON + '.', end='')

            if dungeon[i][j] == 7:
                print(TRAP_ICON + '.', end='')

    return ''
def show_movement_legend():
    print('Передвижение')
    print('Верх - w')
    print('Лево - a')
    print('Низ - s')
    print('Право - d')

def initiative_throw_message():

    print('Решается чей ход первый')

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

    print()

    for i in range(50):
        fake_value = "".join(random.choice(chars) for _ in range(8))

        print(f"\rИнициатива врага: {fake_value}", end='')
        time.sleep(0.04)

    print(f'\rИнициатива врага: {enemy_data[ENTITY_INITIATIVE]}        ')

def trap_inputs():

    print('1 - Обезвредить')
    print('2 - Пробежать')

def start_fight_message(enemy) -> str:

    if enemy[0] == NAME_ENEMY_PUNK:
        return (f'{START_FIGHT_MESSAGE_FONT}Вы вступаете в бой с панком')

    if enemy[0] == NAME_ENEMY_SYNTH_HOUND:
        return (f'{START_FIGHT_MESSAGE_FONT}Вы вступаете в бой с синт. гончей')

    if enemy[0] == NAME_ENEMY_GLITCH_BUTCHER:
        return (f'{START_FIGHT_MESSAGE_FONT}Вы вступаете в бой с мясником')

    if enemy[0] == NAME_ENEMY_PSY_CODER:
        return (f'{START_FIGHT_MESSAGE_FONT}Вы вступаете в бой с пси-кодером')

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
