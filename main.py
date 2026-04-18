# (c) 2026 Safonov Nikita Sergeevich
# Project: Sewages & Punks

from src.audio_manager import init_audio, play_theme, stop_audio
from src.core import *
from pregen_levels.tutorial_level import create_tutorial_dungeon
from src.display import draw_main_menu
from src.constants import *
from src.entities import create_default_player
from src.localization import MAIN_MENU


def main_menu() -> dict | tuple[list, list] | None:
    """
    Управляет логикой главного меню: запуск новой игры, загрузка или выход.

    Returns:
        dict | tuple[list, list] | None:
            Кортеж (карта, игрок) для новой игры,
            результат load_game() - словарь с data игрока и подземелья.
    """
    play_theme(MENU_INTRO, MENU_LOOP)

    in_main_menu: bool = True
    player_nick: str = 'Operator'

    while in_main_menu:
        clear_display()
        draw_main_menu()

        prompt: str = MAIN_MENU['player_input'].format(PLAYER_NAME=player_nick)
        choice: str = input(prompt).strip()

        if choice.lower() in NEW_GAME_COMMANDS:
            dungeon: list[list[int]] = create_tutorial_dungeon()
            default_player: list[int | float | str] = create_default_player()
            return dungeon, default_player

        elif choice.lower() in LOAD_GAME_COMMANDS:
            saved_data: dict | None = load_game()
            if saved_data:
                msg: str = MAIN_MENU['decrypting_successful'].format(
                    MAIN_CHARACTER_NAME=MAIN_CHARACTER_NAME
                )
                print(msg)
                enter_continue()
                return saved_data
            else:
                print(MAIN_MENU['no_data_on_sector'])
                enter_continue()

        elif choice.lower() in SETTING_GAME_COMMANDS:
            clear_display()
            show_setting_stub()

        elif choice.lower() in EXIT_GAME_COMMANDS:
            return None

    return None


def game_loop(player_data: list[int | float | str], first_dungeon: list[list[int]]) -> str:
    """
    Основной игровой цикл, переключающий состояния между исследованием и боем.

    Args:
        player_data: Список с характеристиками игрока.
        first_dungeon: Матрица подземелья.

    Returns:
        str: Код завершения цикла (например, GAME_OVER или EXIT_TO_MAIN_MENU).
    """
    play_theme(GAME_LOOP, fade_ms=1500)

    is_fight = False
    game_loop_is_run = True
    exfill = False
    dungeon = first_dungeon
    new_position = None

    while game_loop_is_run:
        while not is_fight:
            if exfill:
                dungeon = create_dungeon()
                exfill = False

            state_of_adventuring, new_position = adventuring(dungeon, player_data)

            if state_of_adventuring == FIGHT:
                break

            if state_of_adventuring == EXFILL:
                exfill = True
                continue

            if state_of_adventuring == RETURN_TO_MAIN_MENU:
                return EXIT_TO_MAIN_MENU

        state, enemy_data = fight(player_data)

        if player_data[ENTITY_HP] > 0:
            sp_gain = calculate_sp_reward(enemy_data)
            player_data[PLAYER_SKILL_POINTS] += sp_gain
            gain_xp(player_data, 40 + enemy_data[ENTITY_INITIATIVE])

        if player_data[ENTITY_HP] <= 0:
            stop_audio(500)
            art = game_over()
            flush_input()
            clear_display()
            slow_print(art, 0.01)
            flush_input()
            enter_continue()
            break

        old_pos = search_player_position(dungeon)
        dungeon[old_pos[0]][old_pos[1]] = FLOOR_TILE
        dungeon[new_position[0]][new_position[1]] = PLAYER_TILE

    return GAME_OVER


if __name__ == '__main__':
    init_audio()

    game_is_run: bool = True
    start_message_already_show: bool = False

    while game_is_run:
        result = main_menu()

        if result is None:
            print(f"{RED_TEXT_BRIGHT}DISCONNECTING", end=" ")
            waiting_animation(0.6)
            print(RESET)
            clear_display()
            break

        if isinstance(result, tuple):
            first_level, player = result
        else:
            first_level = result["dungeon"]
            player = result["player"]

        if not start_message_already_show:
            print(skip_message())
            skip: str = input('>>').lower()
            if skip in SKIP_PROLOGUE_COMMANDS_NO:
                play_theme(GAME_INTRO, fade_ms=1500)
                clear_display()
                start_message()
                flush_input()
                enter_continue()
                start_message_already_show = True

        exit_data: str = game_loop(player, first_level)
        if exit_data == EXIT_TO_MAIN_MENU:
            continue