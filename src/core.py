from src.businesslogic_upper import *
from src.display import *
from src.entities import *
from src.constants import *

import msvcrt

def adventuring(dungeon_map, player_data):
    user_input = ''

    while user_input not in EXIT_COMMANDS:
        clear_display()
        print(show_dungeon_map(dungeon_map))
        show_movement_legend()
        char = msvcrt.getch()
        user_input = char.decode('utf-8', errors='ignore').lower()

        if user_input in MOVEMENT_COMMANDS:
            new_position = movement_player(dungeon_map, user_input)

        else:
            continue

        if dungeon_map[new_position[x_coord]][new_position[y_coord]] == CHEST_TILE:

            item = open_chest()

            if item == ITEM_DEFUSAL_KIT:
                player_data[PLAYER_ITEM_DEFUSAL_KIT] += 1
                clear_display()
                loot_message(item)
                enter_continue()
                clear_display()
                dungeon_map[new_position[x_coord]][new_position[y_coord]] = FLOOR_TILE

            if item == ITEM_NOTHING:
                clear_display()
                loot_message(item)
                enter_continue()
                clear_display()
                dungeon_map[new_position[x_coord]][new_position[y_coord]] = FLOOR_TILE
                continue

        if dungeon_map[new_position[x_coord]][new_position[y_coord]] == EXIT_TILE:
            clear_display()
            print(YOU_TRY_OPEN_DOR_MESSAGE)
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
                            key_card_options_menu()
                            user_input = input('>>')

                            if user_input == '1':
                                clear_display()
                                print(CARD_READER_MESSAGE)
                                enter_continue()
                                return STATE_OF_ADVENTURING_EXFILL, new_position

                            if user_input == '2':
                                clear_display()
                                print(DOOR_INTERACTION_MESSAGE)
                                choosing = False
                                door_case = False

                if user_input == '2':
                    clear_display()
                    print(KICK_THE_DOOR_MESSAGE)
                    enter_continue()
                    continue

                if user_input == '3':
                    clear_display()
                    print(STEP_OUT_THE_DOOR_MESSAGE)
                    door_case = False

        if dungeon_map[new_position[x_coord]][new_position[y_coord]] == KEY_TILE:
            clear_display()
            print(YOU_FOUND_KEY_CARD_MESSAGE)
            player_data[PLAYER_ITEM_KEY] += 1
            enter_continue()
            dungeon_map[new_position[x_coord]][new_position[y_coord]] = FLOOR_TILE

        if dungeon_map[new_position[x_coord]][new_position[y_coord]] == TRAP_TILE:
            clear_display()
            print(TRAP_FORWARD_MESSAGE)

            trap_case = True

            while trap_case:
                trap_inputs()
                user_input = input('>>')
                if user_input not in TRAP_COMMANDS:
                    continue

                if user_input == '1':
                    defuse = defuse_trap(player_data)
                    if defuse:
                        clear_display()
                        print(TRAP_DEFUSED_MESSAGE)
                        enter_continue()
                        dungeon_map[new_position[x_coord]][new_position[y_coord]] = FLOOR_TILE
                        trap_case = False
                    if not defuse:
                        clear_display()
                        print(YOU_DONT_HAVE_DEFKIT_MESSAGE)
                        enter_continue()
                        continue


                if user_input == '2':
                    defuse = defuse_trap_run()
                    if defuse:
                        clear_display()
                        print(TRAP_ACTIVATED_MESSAGE)
                        enter_continue()
                        dungeon_map[new_position[x_coord]][new_position[y_coord]] = FLOOR_TILE
                        trap_case = False
                    else:
                        clear_display()
                        print(TRAP_DAMAGED_PLAYER_IF_HE_RUN_MESSAGE)
                        enter_continue()
                        player_data[ENTITY_HP] -= 5
                        dungeon_map[new_position[x_coord]][new_position[y_coord]] = FLOOR_TILE
                        trap_case = False


        is_fight = try_start_fight(dungeon_map, new_position)

        if is_fight:
            return STATE_OF_ADVENTURING_FIGHT, new_position

    return STATE_OF_ADVENTURING_EXIT

def fight(player_data):

    is_fight = True
    enemy_data = create_enemy()
    clear_display()
    print(start_fight_message(enemy_data))
    enter_continue()

    initiative_throw_message()
    player_data, enemy_data = initiative_throw(player_data, enemy_data)
    throw_animation(player_data, enemy_data)
    enter_continue()
    clear_display()

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
            who = PLAYER_WORD_VARIABLE
            count_of_use_heal_in_step = 0
            message_about_step(enemy = 0, player = 1)

            show_combat_legend()
            user_input = input('>>')

            if user_input not in COMBAT_COMMANDS:
                clear_display()
                continue

            if user_input == 'a':

                damage = player_data[ENTITY_DAMAGE]
                damage = randomise_damage(damage)

                is_miss = try_ruin_attack_for_player(player_data)

                if is_miss:
                    clear_display()
                    print(MISS_WORD)
                    enter_continue()
                    clear_display()
                    player_step = False
                    enemy_step = True
                    continue


                enemy_data[ENTITY_HP] -= damage

                clear_display()
                hit_message(damage, who)
                enter_continue()
                clear_display()

                show_enemy_hp(enemy_data)
                print()
                enter_continue()
                clear_display()

                if enemy_data[ENTITY_HP] <= 0:
                    player_win = True

            if user_input == 'd':
                enemy_data[ENTITY_MISS_CHANCE] += 0.4

                print(PLAYER_TRY_DODGE_MESSAGE)
                enter_continue()
                clear_display()

            if user_input == 'h':
                if count_of_heal >= 0:
                    player_data[ENTITY_HP] += 10

                    count_of_use_heal_in_step += 1

                    if count_of_use_heal_in_step > 1:
                        toxication_message()
                        player_data[ENTITY_TOXICITY] += 1

                        if player_data[ENTITY_TOXICITY] >= 5:
                            player_data[ENTITY_HP] -= 5
                            toxication_damage_message()
                            enter_continue()
                            clear_display()


                    if player_data[ENTITY_HP] >= 100:
                        player_data[ENTITY_HP] = 100

                    count_of_heal -= 1

                    heal_message()
                    show_player_hp(player_data)
                    enter_continue()
                    clear_display()
                else:
                    empty_heal_message()
                    enter_continue()
                    clear_display()

                continue

            if user_input == 'i':
                show_battle_information(player_data, enemy_data)
                enter_continue()

                continue


            player_step = False
            enemy_step = True

        if enemy_step:
            if enemy_data[ENTITY_HP] <= 0:
                continue

            who = ENEMY_WORD_VARIABLE
            message_about_step(player = 0, enemy = 1)

            damage = enemy_data[ENTITY_DAMAGE]
            damage = randomise_damage(damage)

            is_miss = try_ruin_attack_for_enemy(enemy_data)

            if is_miss:
                print(ENEMY_MISS_MESSAGE)
                enter_continue()
                clear_display()
                enemy_step = False
                player_step = True
                continue

            player_data[ENTITY_HP] -= damage
            hit_message(damage, who)
            enter_continue()
            clear_display()
            show_player_hp(player_data)
            enter_continue()

            if player_data[ENTITY_HP] <= 0:
                print(ENEMY_WIN_MESSAGE)
                enter_continue()
                enemy_win = True



            enemy_step = False
            player_step = True














