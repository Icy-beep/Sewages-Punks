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
        os.system('cls')
        print(show_dungeon_map(dungeon_map))
        show_movement_legend()
        user_input = input('>>')

        new_position = movement_player(dungeon_map, user_input)

        if dungeon_map[new_position[0]][new_position[1]] == TRAP_TILE:
            print('Вы попали в ловушку -5HP')
            player_data[ENTITY_HP] -= 5
            enter_continue()


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














