import random
import time
import os

from src.businesslogic_upper import *
from src.display import *
from src.constants import *
from src.entities import *

def create_player():
    global player_name
    global player

    print('Введите своё имя')
    user_input = input('>>')

    player_name = user_input

    return player


def adventuring(dungeon_map, player_data):
    user_input = ''

    while user_input not in EXIT_COMMANDS:
        clear_display()
        print(show_dungeon_map(dungeon_map))
        show_movement_legend()
        user_input = input('>>')

        new_position = movement_player(dungeon_map, user_input)

        if dungeon_map[new_position[x_coord]][new_position[y_coord]] == CHEST_TILE:

            item = open_chest()

            if item == ITEM_DEFUSAL_KIT:
                player_data[PLAYER_ITEM_DEFUSAL_KIT] += 1
                dungeon_map[new_position[x_coord]][new_position[y_coord]] = FLOOR_TILE

            if item == ITEM_NOTHING:
                dungeon_map[new_position[x_coord]][new_position[y_coord]] = FLOOR_TILE
                continue

        if dungeon_map[new_position[x_coord]][new_position[y_coord]] == EXIT_TILE:
            clear_display()
            print('Вы пытаетесь открыть дверь')
            enter_continue()

            door_case = True

            while door_case:
                clear_display()
                exit_interactions()
                user_input = input('>>')

                if user_input not in DOOR_INTERACTION_COMMANDS:
                    continue

                if user_input == '1':
                    if player_data[PLAYER_ITEM_KEY] >= 1:
                        clear_display()

                        choosing = True
                        while choosing:
                            print('У вас есть ключ-карта, применить?')
                            print('1 - Да')
                            print('2 - Нет')
                            user_input = input('>>')

                            if user_input == '1':
                                clear_display()
                                print('Вы провели ключ-картой по считывателю, кардридер издал приятный одобрительный звук и дверь с небольшим скрипом приоткрылась')
                                enter_continue()
                                return STATE_OF_ADVENTURING_EXFILL, new_position

                            if user_input == '2':
                                clear_display()
                                print('Вы отходите от двери')
                                choosing = False
                                door_case = False

                if user_input == '2':
                    clear_display()
                    print('Вы бьёте ногой по двери грохот раздался по всей канализации но дверь не открылась')
                    enter_continue()
                    continue

                if user_input == '3':
                    clear_display()
                    print('Вы отходите от двери')
                    door_case = False

        if dungeon_map[new_position[x_coord]][new_position[y_coord]] == KEY_TILE:
            clear_display()
            print('Вы нашли ключ-карту')
            player_data[PLAYER_ITEM_KEY] += 1
            enter_continue()
            dungeon_map[new_position[x_coord]][new_position[y_coord]] = FLOOR_TILE

        if dungeon_map[new_position[x_coord]][new_position[y_coord]] == TRAP_TILE:
            print('Перед вами ловушка')
            trap_inputs()
            user_input = input('>>')

            trap_case = True

            while trap_case:
                if user_input not in TRAP_COMMANDS:
                    continue

                if user_input == '1':
                    defuse = defuse_trap(player_data)
                    if defuse:
                        print('Ловушка обезврежена')
                        dungeon_map[new_position[x_coord]][new_position[y_coord]] = FLOOR_TILE
                        trap_case = False
                    if not defuse:
                        print('У вас нет набора для обезвреживания ловушки')
                        continue


                if user_input == '2':
                    defuse = defuse_trap_run()
                    if defuse:
                        print('Вы пробежали, ловушка активировалась у вас за спиной')
                        dungeon_map[new_position[x_coord]][new_position[y_coord]] = FLOOR_TILE
                        trap_case = False
                    else:
                        print('Вы не успели ловушка вас зацепила -5HP')
                        player_data[ENTITY_HP] -= 5
                        dungeon_map[new_position[x_coord]][new_position[y_coord]] = FLOOR_TILE
                        trap_case = False


        is_fight = try_start_fight(dungeon_map, new_position)

        if is_fight:
            return STATE_OF_ADVENTURING_FIGHT, new_position

    return STATE_OF_ADVENTURING_EXIT

def fight(player_data):
    import time

    is_fight = True
    enemy_data = create_enemy()
    os.system('cls')
    print(start_fight_message(enemy_data))

    player_data, enemy_data = initiative_throw(player_data, enemy_data)

    count_of_heal = 4

    enemy_step = False
    player_step = False

    enemy_win = False
    player_win = False

    if player_data[ENTITY_INITIATIVE] > enemy_data[ENTITY_INITIATIVE]:
        player_step = True
    else:
        enemy_step = True

    while is_fight:

        if player_win or enemy_win:
            break

        if player_step:
            print(f'{PLAYER_HP_FONT}Ваше ход')

            show_combat_legend()
            user_input = input('>>')

            if user_input == 'a':

                damage = player_data[ENTITY_DAMAGE]
                damage = randomise_damage(damage)

                is_miss = try_ruin_attack_for_player(player_data)

                if is_miss:
                    print('Промах!')
                    player_step = False
                    enemy_step = True
                    continue


                enemy_data[ENTITY_HP] -= damage

                os.system('cls')
                print(f'Попадание, вы нанесли {damage} - урона')
                time.sleep(2)

                show_enemy_hp(enemy_data)
                print()
                time.sleep(2)
                os.system('cls')

                if enemy_data[ENTITY_HP] <= 0:
                    player_win = True

            if user_input == 'd':
                enemy_data[ENTITY_MISS_CHANCE] += 0.4

                print('Вы пытаетесь уклониться шанс промаха противника увеличен')
                time.sleep(2)
                os.system('cls')

            if user_input == 'h':
                if count_of_heal >= 0:
                    player_data[ENTITY_HP] += 10

                    count_of_heal -= 1

                    heal_message()
                else:
                    empty_heal_message()

                continue

            if user_input == 'i':
                enter_continue(show_battle_information(player_data, enemy_data))

                continue


            player_step = False
            enemy_step = True

        if enemy_step:

            print(f'{ENEMY_HP_FONT}Ход противника')
            time.sleep(2)
            os.system('cls')

            damage = enemy_data[ENTITY_DAMAGE]
            damage = randomise_damage(damage)

            is_miss = try_ruin_attack_for_enemy(enemy_data)

            if is_miss:
                print('Враг промахнулся')
                time.sleep(2)
                os.system('cls')
                enemy_step = False
                player_step = True
                continue

            player_data[ENTITY_HP] -= damage
            print(f'Попадание враг нанес {damage} урона')
            show_player_hp(player_data)
            time.sleep(2)
            os.system('cls')

            if player_data[ENTITY_HP] <= 0:
                print('Враг победил')
                enemy_win = True



            enemy_step = False
            player_step = True














