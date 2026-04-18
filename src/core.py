import json
import datetime
from typing import Callable, Tuple, Dict
from src.businesslogic_upper import *
from src.display import *
from src.ai import *

INTERACTIONS: Dict[Any, Callable[..., Any]] = {
    CHEST_TILE: handle_chest,
    KEY_TILE: handle_key_pickup,
    TRAP_TILE: handle_trap,
}

def adventuring(dungeon_map: list[list[Any]], player_data: list[int | float | str]) -> (
        None | tuple[str, list[int]] | tuple[str, int]):
    while True:
        clear_display()
        show_dungeon_map(dungeon_map, player_data)
        show_movement_legend()

        command = get_user_command()

        if command == INVENTORY:
            handle_inventory_menu(player_data)

        if command == PAUSE:
            status = handle_pause_menu(player_data, dungeon_map)
            if status == RETURN_TO_MAIN_MENU:
                return RETURN_TO_MAIN_MENU, 0
            continue

        if command in MOVEMENT_COMMANDS:
            old_pos = search_player_position(dungeon_map)
            new_position = movement_player(dungeon_map, command)

            if try_start_fight(dungeon_map, new_position):
                return FIGHT, new_position

            if new_position != old_pos:
                move_enemies(dungeon_map)

            enemy_pos = check_enemy_nearby(dungeon_map, new_position)
            if enemy_pos:
                return FIGHT, enemy_pos

            tile = dungeon_map[new_position[0]][new_position[1]]

            if tile == EXIT_TILE:
                if handle_exit(player_data):
                    return EXFILL, new_position

            handler = INTERACTIONS.get(tile)
            if handler:
                old_p = search_player_position(dungeon_map)
                dungeon_map[old_p[0]][old_p[1]] = FLOOR_TILE

                handler(dungeon_map, player_data, new_position)

                dungeon_map[new_position[0]][new_position[1]] = PLAYER_TILE


def fight(player_data: list[int | float | str]) -> None | tuple[bool, list] | bool:
    """
    Управляет процессом пошагового боя между игроком и противником.

    Функция инициализирует врага, рассчитывает инициативу и обрабатывает цикл
    сражения, включая выбор действий игроком (атака, лечение, уклонение)
    и автоматические ходы противника.

    Args:
        player_data list[int | float | str]: Список с текущими характеристиками игрока.

    Returns:
        bool: True, если игрок победил; False, если игрок погиб.
    """
    player_data[ENTITY_TOXICITY] = 0
    enemy_data = create_enemy()
    dodge_active = False
    combat_log = ["Connection established.", f"Target: {enemy_data[ENTITY_NAME]} detected."]

    clear_display()
    print(f"\n{MAGENTA_TEXT_BRIGHT}ENCOUNTER_LOG:{RESET} {enemy_data[ENTITY_NAME]} has entered the sector.\n")
    enter_continue()

    player_initiative, enemy_initiative = initiative_throw(player_data, enemy_data)
    throw_animation(player_initiative, enemy_initiative)
    enter_continue()

    current_turn = "player" if player_data[ENTITY_INITIATIVE] >= enemy_data[ENTITY_INITIATIVE] else "enemy"

    while True:
        if player_data[ENTITY_HP] <= 0:
            return False, enemy_data

        if enemy_data[ENTITY_HP] <= 0:
            draw_combat_interface(player_data, enemy_data, combat_log, current_turn)
            enemy_defeated_message(enemy_data)
            return True, enemy_data

        draw_combat_interface(player_data, enemy_data, combat_log, current_turn)

        if current_turn == "player":
            action = input().lower()

            if action == 'h':
                msg, success = execute_player_heal(player_data)
                combat_log.append(msg)
                if success:
                    player_data[PLAYER_ITEM_REGEN_INHALER] -= 1
                continue

            elif action == 'a':
                combat_log.append(execute_player_attack(player_data, enemy_data))
                current_turn = "enemy"
            elif action == 'd':
                if dodge_active:
                    combat_log.append(f"{RED_TEXT_BRIGHT}Evasive maneuvers already active!{RESET}")
                    continue
                else:
                    dodge_active = True
                    combat_log.append("Evasive maneuvers active. Dodge chance UP.")
                    continue
            elif action == 'k':
                if not player_data[PLAYER_SKILLS]:
                    combat_log.append(f"{RED_TEXT_BRIGHT}NO SKILLS INSTALLED!{RESET}")
                    continue

                clear_display()
                print(f"\n{MAGENTA_TEXT_BRIGHT}SELECT SKILL:{RESET}")
                for i, skill in enumerate(player_data[PLAYER_SKILLS], 1):
                    print(f"  [{i}] {skill}")
                print(f"  [0] CANCEL")

                try:
                    choice = input(f"\n{MAGENTA_TEXT_BRIGHT}> {RESET}").strip()

                    if choice == '0':
                        continue

                    skill_index = int(choice) - 1

                    if 0 <= skill_index < len(player_data[PLAYER_SKILLS]):
                        selected_skill = player_data[PLAYER_SKILLS][skill_index]
                        msg = execute_player_skill(player_data, enemy_data, selected_skill)
                        combat_log.append(msg)
                        current_turn = "enemy"
                    else:
                        combat_log.append(f"{RED_TEXT_BRIGHT}INVALID SELECTION!{RESET}")

                except ValueError:
                    combat_log.append(f"{RED_TEXT_BRIGHT}INVALID INPUT!{RESET}")

                continue

            else:
                continue

        else:
            time.sleep(0.4)
            orig_miss = enemy_data[ENTITY_MISS_CHANCE]
            if dodge_active:
                enemy_data[ENTITY_MISS_CHANCE] += 0.4

            combat_log.append(execute_enemy_attack(enemy_data, player_data))

            enemy_data[ENTITY_MISS_CHANCE] = orig_miss
            dodge_active = False
            current_turn = "player"


def handle_pause_menu(player_data: list[int | float | str], dungeon_map: list[list[int]]):
    """
    Управляет меню паузы.
    Args:
        player_data: list[int | float | str]
        dungeon_map: list[list[int]]
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


def execute_player_skill(player: list, enemy: list, skill_id: str) -> str:
    """
    Выполняет активный навык через систему взлома.
    """
    if skill_id not in player[PLAYER_SKILLS]:
        return f"{RED_TEXT_BRIGHT}ERROR: SKILL NOT INSTALLED.{RESET}"

    if skill_id not in HACK_SKILLS:
        return f"{RED_TEXT_BRIGHT}ERROR: UNKNOWN SKILL PROTOCOL.{RESET}"

    skill_data = HACK_SKILLS[skill_id]

    cost = skill_data["energy_cost"]

    if player[PLAYER_ENERGY] < cost:
        return f"{RED_TEXT_BRIGHT}ERROR: INSUFFICIENT PSY ENERGY (Need {cost}).{RESET}"

    player[PLAYER_ENERGY] -= cost

    full_success, message = hacking_mini_game(skill_id)

    if skill_id == "NEURAL_SHOCK":
        if full_success:
            dmg = skill_data["success_damage"]
        else:
            dmg = skill_data["partial_damage"] if "partial" in message else skill_data["fail_damage"]

        if dmg > 0:
            enemy[ENTITY_HP] -= dmg
            return f"{message}\n{LIGHT_BLUE_TEXT_BRIGHT}NEURAL_SHOCK: {dmg} damage inflicted.{RESET}"
        else:
            return apply_fail_effect(skill_data, player, enemy)

    elif skill_id == "SYSTEM_RESTORE":
        if full_success:
            heal = skill_data["success_heal"]
        else:
            heal = skill_data["partial_heal"] if "partial" in message else skill_data["fail_heal"]

        player[ENTITY_HP] = min(100, player[ENTITY_HP] + heal)

        if heal <= skill_data["fail_heal"]:
            return apply_fail_effect(skill_data, player, enemy)

        return f"{message}\n{GREEN_TEXT_BRIGHT}SYSTEM_RESTORE: {heal} HP restored.{RESET}"

    elif skill_id == "OVERCLOCK":
        if full_success:
            bonus = skill_data["success_bonus"]
        else:
            bonus = skill_data["partial_bonus"] if "partial" in message else skill_data["fail_bonus"]

        player[ENTITY_DAMAGE] += bonus
        dmg = randomise_damage(player[ENTITY_DAMAGE])
        enemy[ENTITY_HP] -= dmg
        player[ENTITY_DAMAGE] -= bonus

        if bonus == 0:
            return apply_fail_effect(skill_data, player, enemy)

        return f"{message}\n{YELLOW_TEXT_BRIGHT}OVERCLOCK: Systems boosted. {dmg} damage.{RESET}"

    return f"{message}\n{RED_TEXT_BRIGHT}Skill effect not implemented.{RESET}"


def hacking_mini_game(skill_name: str) -> tuple[bool, str]:
    """
    Запускает мини-игру взлома для навыка.
    Returns: (успех_полный, сообщение)
    """
    if skill_name not in HACK_SKILLS:
        return False, "Unknown hack protocol."

    skill_data = HACK_SKILLS[skill_name]
    hack_type = skill_data["hack_type"]

    clear_display()
    print(f"\n{MAGENTA_TEXT_BRIGHT}PSY-LINK // HACKING_PROTOCOL_INITIATED{RESET}")
    print(f"{LIGHT_BLUE_TEXT_BRIGHT}Target: {skill_name}{RESET}")
    print(f"{DARK_GRAY}{'—' * 60}{RESET}\n")

    time.sleep(1)

    if hack_type == HACK_TIMING:
        return timing_hack(skill_data)
    elif hack_type == HACK_SEQUENCE:
        return sequence_hack(skill_data)
    elif hack_type == HACK_REACTION:
        return reaction_hack(skill_data)

    return False, "Hack protocol error."


def timing_hack(skill_data: dict) -> tuple[bool, str]:
    """
    Мини-игра: нажатие в нужный момент.
    Индикатор движется, игрок должен нажать ПРОБЕЛ в зелёной зоне.
    """
    stages = skill_data["stages"]
    successful_hits = 0
    bar_width = 40
    zone_size = 8

    print(f"{LIGHT_BLUE_TEXT_BRIGHT}BYPASSING FIREWALL...{RESET}")
    print(f"{DARK_GRAY}Press SPACE when indicator is in GREEN zone{RESET}\n")

    enter_continue()

    for stage in range(1, stages + 1):
        clear_display()
        print(f"\n{MAGENTA_TEXT_BRIGHT}FIREWALL LAYER {stage}/{stages}{RESET}")
        print(f"{DARK_GRAY}{'—' * 60}{RESET}\n")


        zone_start = random.randint(5, bar_width - zone_size - 5)
        zone_end = zone_start + zone_size

        position = 0
        direction = 1
        speed = 0.05 + (stage * 0.01)

        print(f"Layer security: {'█' * stage}{'░' * (4 - stage)}\n")


        while True:
            sys.stdout.write('\r' + ' ' * (bar_width + 20) + '\r')

            bar = ''
            for i in range(bar_width):
                if i == position:
                    bar += f"{RED_TEXT_BRIGHT}►{RESET}"
                elif zone_start <= i <= zone_end:
                    bar += f"{GREEN_TEXT_BRIGHT}█{RESET}"
                else:
                    bar += f"{DARK_GRAY}·{RESET}"

            sys.stdout.write(f"[{bar}]")
            sys.stdout.flush()

            if msvcrt.kbhit():
                key = msvcrt.getch()
                if key == b' ':
                    if zone_start <= position <= zone_end:
                        successful_hits += 1
                        sys.stdout.write(f"\r{GREEN_TEXT_BRIGHT} ACCESS GRANTED! {RESET}\n")
                        time.sleep(0.5)
                    else:
                        sys.stdout.write(f"\r{RED_TEXT_BRIGHT} ACCESS DENIED! {RESET}\n")
                        time.sleep(0.5)
                    break

            position += direction
            if position >= bar_width - 1 or position <= 0:
                direction *= -1

            time.sleep(speed)

        sys.stdout.write('\n')
        time.sleep(0.3)

    success_rate = successful_hits / stages

    if success_rate >= 0.7:
        return True, f"Hack successful: {successful_hits}/{stages} layers breached."
    elif success_rate >= 0.4:
        return False, f"Partial success: {successful_hits}/{stages} layers breached."
    else:
        return False, f"Hack failed: {successful_hits}/{stages} layers breached."


def sequence_hack(skill_data: dict) -> tuple[bool, str]:
    """
    Мини-игра: запоминание последовательности.
    Показываем последовательность цифр/символов, игрок повторяет.
    """
    stages = skill_data["stages"]
    sequence_length = 4
    correct_inputs = 0

    print(f"{LIGHT_BLUE_TEXT_BRIGHT}DECRYPTING SECURITY CODE...{RESET}")
    print(f"{DARK_GRAY}Memorize and repeat the sequence{RESET}\n")

    enter_continue()

    for stage in range(1, stages + 1):
        clear_display()
        print(f"\n{MAGENTA_TEXT_BRIGHT}ENCRYPTION LAYER {stage}/{stages}{RESET}\n")

        sequence = [str(random.randint(0, 9)) for _ in range(sequence_length)]

        print(f"{LIGHT_BLUE_TEXT_BRIGHT}Sequence:{RESET} ", end='', flush=True)
        for num in sequence:
            print(f"{GREEN_TEXT_BRIGHT}{num}{RESET} ", end='', flush=True)
            time.sleep(0.4)

        time.sleep(1)
        clear_display()
        print(f"\n{MAGENTA_TEXT_BRIGHT}Layer {stage}/{stages}{RESET}")
        print(f"{DARK_GRAY}Enter the sequence:{RESET} ", end='')

        user_input = input().strip()

        if user_input == ''.join(sequence):
            correct_inputs += 1
            print(f"{GREEN_TEXT_BRIGHT}Correct!{RESET}")
        else:
            print(f"{RED_TEXT_BRIGHT}Incorrect!{RESET} Expected: {''.join(sequence)}")

        time.sleep(1)
        sequence_length += 1

    success_rate = correct_inputs / stages

    if success_rate >= 0.7:
        return True, f"Decryption complete: {correct_inputs}/{stages} correct."
    elif success_rate >= 0.4:
        return False, f"Partial decryption: {correct_inputs}/{stages} correct."
    else:
        return False, f"Decryption failed: {correct_inputs}/{stages} correct."


def reaction_hack(skill_data: dict) -> tuple[bool, str]:
    """
    Мини-игра: реакция.
    Нажать клавишу когда появится сигнал.
    """
    stages = skill_data["stages"]
    successful_reactions = 0

    print(f"{LIGHT_BLUE_TEXT_BRIGHT}SYSTEM OVERCLOCK PROTOCOL{RESET}")
    print(f"{DARK_GRAY}Press SPACE when you see [SIGNAL]{RESET}\n")

    enter_continue()

    for stage in range(1, stages + 1):
        clear_display()
        print(f"\n{MAGENTA_TEXT_BRIGHT}PULSE SYNC {stage}/{stages}{RESET}\n")
        delay = random.uniform(1.0, 3.0)
        time.sleep(delay)

        start_time = time.time()

        clear_display()
        print(f"\n{MAGENTA_TEXT_BRIGHT}PULSE SYNC {stage}/{stages}{RESET}\n")
        print(f"{GREEN_TEXT_BRIGHT}[SIGNAL]{RESET}")
        print(f"{DARK_GRAY}PRESS SPACE NOW!{RESET}")

        while True:
            if msvcrt.kbhit():
                key = msvcrt.getch()
                if key == b' ':
                    reaction_time = (time.time() - start_time) * 1000

                    if reaction_time < 300:
                        successful_reactions += 1
                        print(f"\n{GREEN_TEXT_BRIGHT}PERFECT! {reaction_time:.0f}ms{RESET}")
                    elif reaction_time < 500:
                        successful_reactions += 0.5
                        print(f"\n{LIGHT_BLUE_TEXT_BRIGHT}GOOD! {reaction_time:.0f}ms{RESET}")
                    else:
                        print(f"\n{RED_TEXT_BRIGHT}TOO SLOW! {reaction_time:.0f}ms{RESET}")
                    break

            if time.time() - start_time > 1.0:
                print(f"\n{RED_TEXT_BRIGHT}TIMEOUT!{RESET}")
                break

        time.sleep(1)

    success_rate = successful_reactions / stages

    if success_rate >= 0.7:
        return True, f"Sync complete: {successful_reactions:.0f}/{stages} successful."
    elif success_rate >= 0.4:
        return False, f"Partial sync: {successful_reactions:.0f}/{stages} successful."
    else:
        return False, f"Sync failed: {successful_reactions:.0f}/{stages} successful."


def run_timing_hack(stages: int = 3) -> str:
    """Мини-игра: нажатие ПРОБЕЛА в зелёной зоне."""
    import msvcrt
    bar_width = 40
    zone_size = 8
    hits = 0

    clear_display()
    print(f"\n{LIGHT_BLUE_TEXT_BRIGHT}INITIATING HACK PROTOCOL...{RESET}")
    time.sleep(0.8)

    for stage in range(1, stages + 1):
        clear_display()
        print(f"\n{MAGENTA_TEXT_BRIGHT}FIREWALL LAYER {stage}/{stages}{RESET}")
        print(f"{DARK_GRAY}Press [SPACE] when cursor is in GREEN zone{RESET}\n")

        zone_start = random.randint(5, bar_width - zone_size - 5)
        zone_end = zone_start + zone_size
        pos = 0
        direction = 1
        speed = 0.04 + (stage * 0.01)

        while True:
            sys.stdout.write('\r' + ' ' * (bar_width + 10) + '\r')
            bar = ''
            for i in range(bar_width):
                if i == pos:
                    bar += f"{RED_TEXT_BRIGHT}►{RESET}"
                elif zone_start <= i <= zone_end:
                    bar += f"{GREEN_TEXT_BRIGHT}█{RESET}"
                else:
                    bar += f"{DARK_GRAY}·{RESET}"
            sys.stdout.write(f"[{bar}]")
            sys.stdout.flush()

            if msvcrt.kbhit() and msvcrt.getch() == b' ':
                if zone_start <= pos <= zone_end: hits += 1
                break

            pos += direction
            if pos >= bar_width - 1 or pos <= 0: direction *= -1
            time.sleep(speed)
        time.sleep(0.4)

    success_rate = hits / stages
    if success_rate >= 0.7: return "success"
    if success_rate >= 0.4: return "partial"
    return "fail"


def apply_fail_effect(skill_data: dict, player: list, enemy: list) -> str:
    """
    Обрабатывает негативные последствия провала мини-игры.
    """
    fail_effect = skill_data.get("fail_effect", "none")
    fail_value = skill_data.get("fail_value", 0)

    if fail_effect == "backfire":
        player[ENTITY_HP] -= fail_value
        return f"{RED_TEXT_BRIGHT}HACK FAILED! NEURAL FEEDBACK! {fail_value} DMG taken.{RESET}"

    elif fail_effect == "overload":
        player[ENTITY_HP] -= fail_value
        return f"{RED_TEXT_BRIGHT}HACK FAILED! SYSTEM OVERLOAD! {fail_value} DMG taken.{RESET}"

    elif fail_effect == "skip_turn":
        return f"{RED_TEXT_BRIGHT}HACK FAILED! SYSTEM CRASH. TURN ENDED.{RESET}"

    else:
        return f"{RED_TEXT_BRIGHT}HACK FAILED. Signal lost.{RESET}"


def apply_skill_effect(skill_name: str, db: dict, result: str, player: list, enemy: list) -> str | None:
    """
    Применяет эффект в зависимости от результата мини-игры.
    """
    base_val = db['base_val']

    if result == 'success':
        if db['type'] == 'damage':
            enemy[ENTITY_HP] -= base_val
            return f"{GREEN_TEXT_BRIGHT}HACK SUCCESSFUL! {base_val} DMG dealt via {skill_name}.{RESET}"
        elif db['type'] == 'heal':
            player[ENTITY_HP] = min(100, player[ENTITY_HP] + base_val)
            return f"{GREEN_TEXT_BRIGHT}HACK SUCCESSFUL! {base_val} HP restored.{RESET}"
        elif db['type'] == 'buff':
            player[ENTITY_DAMAGE] += base_val
            return f"{GREEN_TEXT_BRIGHT}SYSTEM OVERCLOCKED! +{base_val} DMG this turn.{RESET}"
        return None

    elif result == 'partial':
        half_val = base_val // 2
        if db['type'] == 'damage':
            enemy[ENTITY_HP] -= half_val
            return f"{YELLOW_TEXT_BRIGHT}PARTIAL SUCCESS. {half_val} DMG dealt.{RESET}"
        elif db['type'] == 'heal':
            player[ENTITY_HP] = min(100, player[ENTITY_HP] + half_val)
            return f"{YELLOW_TEXT_BRIGHT}PARTIAL SUCCESS. {half_val} HP restored.{RESET}"
        else:
            return f"{YELLOW_TEXT_BRIGHT}WEAK SIGNAL. NO EFFECT.{RESET}"

    else:
        fail_val = db.get('fail_val', 0)
        effect = db['fail_effect']

        if effect == 'backfire':
            player[ENTITY_HP] -= fail_val
            return f"{RED_TEXT_BRIGHT}HACK FAILED! NEURAL FEEDBACK! {fail_val} DMG taken.{RESET}"
        elif effect == 'overload':
            player[ENTITY_HP] -= fail_val
            return f"{RED_TEXT_BRIGHT}HACK FAILED! SYSTEM OVERLOAD! {fail_val} DMG taken.{RESET}"
        elif effect == 'system_error':
            return f"{RED_TEXT_BRIGHT}HACK FAILED! SYSTEM CRASH. TURN ENDED.{RESET}"


def handle_inventory_menu(player_data: list[int | float | str]):
    """
    Отображает инвентарь и характеристики игрока.
    """
    inventory_log = [
        f"> {LIGHT_BLUE_TEXT_BRIGHT}Connection established.{RESET}",
        f"> {GREEN_TEXT_BRIGHT}BIOSENSORS: {LIGHT_BLUE_TEXT_BRIGHT}ACTIVE.{RESET}"
    ]

    needs_status_check = True

    while True:
        if needs_status_check:
            if player_data[ENTITY_HP] < 20:
                msg = f"> {GREEN_TEXT_BRIGHT}BIOSENSORS: {RED_TEXT_BRIGHT}VITALS CRITICAL!{RESET}"
            elif player_data[ENTITY_HP] <= 43:
                msg = f"> {GREEN_TEXT_BRIGHT}BIOSENSORS: {MAGENTA_TEXT_BRIGHT}Vitals low{RESET}"
            elif player_data[ENTITY_HP] >= 50:
                msg = f"> {GREEN_TEXT_BRIGHT}BIOSENSORS: Vitals stabilized{RESET}"
            elif player_data[ENTITY_HP] >= 70:
                msg = f"> {GREEN_TEXT_BRIGHT}BIOSENSORS: Vitals high{RESET}"
            else:
                msg = None

            if msg and (not inventory_log or inventory_log[-1] != msg):
                inventory_log.append(msg)

            if player_data[ENTITY_TOXICITY] >= 3:
                msg_tox = f"> {GREEN_TEXT_BRIGHT}BIOSENSORS: {RED_TEXT_BRIGHT}Very high toxicity!{RESET}"
            elif player_data[ENTITY_TOXICITY] >= 2:
                msg_tox = f"> {GREEN_TEXT_BRIGHT}BIOSENSORS: {MAGENTA_TEXT_BRIGHT}Toxicity high.{RESET}"
            else:
                msg_tox = None

            if msg_tox and (not inventory_log or inventory_log[-1] != msg_tox):
                inventory_log.append(msg_tox)

            needs_status_check = False

        clear_display()
        draw_inventory(player_data, inventory_log)

        choice = input(f"\n    {MAGENTA_TEXT_BRIGHT}> {RESET}").lower().strip()

        if not choice or (choice not in INVENTORY_ACTIONS and choice not in EXIT_INVENTORY):
            continue

        if choice == DETOX_FROM_INVENTORY:
            if player_data[PLAYER_ITEM_DETOX_INHALER] > 0:
                if player_data[ENTITY_TOXICITY] > 0:
                    player_data[PLAYER_ITEM_DETOX_INHALER] -= 1
                    player_data[ENTITY_TOXICITY] = 0
                    inventory_log.append(
                        f"> {GREEN_TEXT_BRIGHT}BIOSENSORS: {LIGHT_BLUE_TEXT_BRIGHT}Toxins neutralized.{RESET}")
                    needs_status_check = True
                else:
                    inventory_log.append(f"> {RED_TEXT_BRIGHT}BIOSENSORS: No toxins detected.{RESET}")
            else:
                inventory_log.append(f"> {RED_TEXT_BRIGHT}BIOSENSORS: No detox units found.{RESET}")
            continue

        if choice == HEAL_FROM_INVENTORY:
            if player_data[PLAYER_ITEM_REGEN_INHALER] > 0:
                msg, success = execute_player_heal(player_data)
                if success:
                    player_data[PLAYER_ITEM_REGEN_INHALER] -= 1
                    inventory_log.append(f"> {msg}")
                    needs_status_check = True
                else:
                    inventory_log.append(f"> {RED_TEXT_BRIGHT}BIOSENSORS: Vitals max level.{RESET}")
            else:
                inventory_log.append(f"> {RED_TEXT_BRIGHT}BIOSENSORS: No inhalers found.{RESET}")
            continue

        if choice in EXIT_INVENTORY:
            break


def execute_player_attack(player: list[Any], enemy: list[Any]) -> str:
    """
    Выполняет расчет и проведение атаки игрока по противнику.

    Проверяет вероятность промаха через внешнюю функцию и, в случае успеха,
    рассчитывает случайный урон на основе характеристик игрока, вычитая его
    из здоровья врага.

    Args:
        player (list[str, Any]): Данные игрока, включая базовый урон.
        enemy (list[str, Any]): Данные противника, включая текущее здоровье и имя.

    Returns:
        str: Сообщение о результате атаки (промах или нанесенный урон) для боевого лога.
    """
    if try_ruin_attack_for_player(player):
        return f"{RED_TEXT_BRIGHT}MISS!{RESET} Attack failed."
    else:
        dmg = randomise_damage(player[ENTITY_DAMAGE])
        enemy[ENTITY_HP] -= dmg
        return f"Strike successful. {dmg} damage dealt to {enemy[ENTITY_NAME]}."


def execute_player_heal(player: list[Any]) -> Tuple[str, bool]:
    """
    Выполняет попытку восстановления здоровья игрока с использованием нанитов.

    Каждое использование увеличивает уровень токсичности. При превышении порога
    токсичности (4) игрок получает штрафной урон от перегрузки системы.

    Args:
        player (list[str, Any]): Словарь с данными игрока (HP, токсичность).

    Returns:
        Tuple[str, bool]: Кортеж, содержащий:
            - str: Сообщение о результате действия для лога.
            - bool: Статус успеха операции (True, если лечение применено).
    """
    if player[PLAYER_ITEM_REGEN_INHALER] <= 0:
        return f"{RED_TEXT_BRIGHT}ERROR!{RESET} No inhaler uses left.", False

    player[ENTITY_HP] = min(100, player[ENTITY_HP] + 10)
    player[ENTITY_TOXICITY] += 1

    msg = f"Regen active. +10 HP. Toxicity: {player[ENTITY_TOXICITY]}/4."

    if player[ENTITY_TOXICITY] > 4:
        player[ENTITY_HP] -= 8
        player[ENTITY_TOXICITY] -= 1
        msg += f" {RED_TEXT_BRIGHT}TOXIC OVERLOAD!{RESET} -8 HP."

    return msg, True


def execute_enemy_attack(enemy: list[Any], player: list[Any]) -> str:
    """
    Выполняет расчет и проведение атаки противника по игроку.

    Сначала проверяется шанс промаха противника. Если атака успешна,
    рассчитывается случайный урон, который вычитается из здоровья игрока.

    Args:
        enemy (list[str, Any]): Данные противника (имя, урон, шанс промаха).
        player (list[str, Any]): Данные игрока (здоровье).

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


def save_game(player_data: list[Any], dungeon: Any) -> bool:
    """
    Выполняет экспорт текущего состояния игрока и подземелья в JSON-файл.

    Функция создает директорию сохранений, если она отсутствует, запрашивает имя
    у пользователя, очищает его от недопустимых символов, добавляет метку времени
    и записывает данные в файл.

    Args:
        player_data (list[Any, Any]): Данные и характеристики игрока.
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


def calculate_sp_reward(enemy_data: list) -> int:
    base_sp = 5
    power_bonus = int(enemy_data[ENTITY_HP] * 0.1)
    initiative_bonus = int(enemy_data[ENTITY_INITIATIVE] * 0.1)

    return base_sp + power_bonus + initiative_bonus