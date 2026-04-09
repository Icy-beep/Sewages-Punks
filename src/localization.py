from types import SimpleNamespace
from src.constants import *

MESSAGES = SimpleNamespace(
    system=SimpleNamespace(
        input_name="Enter your name",
        press_enter="Press ENTER to proceed",
    ),
    exploration=SimpleNamespace(
        door_try_open="You try open dor",
        card_reader_success="You ran the keycard across the scanner...",
        door_kick="You kick the door. The bang echoes...",
        door_step_out="You move away...",
        key_found="You found a keycard",
    ),
    traps=SimpleNamespace(
        detected="There's a trap right in front of you.",
        defused="Trap neutralized.",
        no_defkit="Required tools not detected...",
        evaded="You dashed through...",
        damage="Failed to evade. Damage taken: -5 HP",
    ),
    combat=SimpleNamespace(
        player_dodge=f"{LIGHT_BLUE_TEXT_BRIGHT}Evasion attempt successful.{RESET}",
        enemy_miss="The shot went wide.",
        enemy_win="You have been defeated.",
    )
)

MAIN_MENU = {
    'player_input': '\n' + MAGENTA_TEXT_BRIGHT + '[SYSTEM@{PLAYER_NAME}]:' + RESET,
    'decrypting_successful': GREEN_TEXT_BRIGHT + '[DECRYPTING SUCCESSFUL: OBJECT {MAIN_CHARACTER_NAME} ---> RESTORED]' + RESET,
    'no_data_on_sector': RED_TEXT_BRIGHT + '[ERROR: NO DATA ON SECTOR' + RESET + MAGENTA_TEXT_BRIGHT + ' 0xxxx256]' + RESET

}