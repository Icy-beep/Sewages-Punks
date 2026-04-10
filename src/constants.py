"""
Constants.
Cleaned and organized version.
"""

# --- СИСТЕМНЫЕ НАСТРОЙКИ ---
RESET = '\033[0m'
ESC = b'\x1b'
PAUSE = "PAUSE"
HIDE_CURSOR = "\033[?25l"
SHOW_CURSOR = "\033[?25h"

# Координаты (индексы списков)
x_coord = 0
y_coord = 1

# --- ТАЙЛЫ И КАРТА ---
PLAYER_TILE, ENEMY_TILE, EXIT_TILE, KEY_TILE = 0, 1, 2, 3
CHEST_TILE, WALL_TILE, FLOOR_TILE, TRAP_TILE = 4, 5, 6, 7

DUNGEON_HEIGHT = 11
DUNGEON_WIDTH = 14
PLAYER_START_POSITION = (1, 1)

# --- БАЛАНС И ГЕНЕРАЦИЯ ---
MAX_ENEMY, MIN_ENEMY = 5, 2
MAX_TRAPS, MIN_TRAPS = 6, 0
MAX_CHESTS, MIN_CHESTS = 3, 1
AMT_KEY = 1
BASE_CHANCE = 1
HOW_MUCH_WALLS_WHERE_PASS = 4

# --- ИНДЕКСЫ ХАРАКТЕРИСТИК (ENTITY) ---
ENTITY_NAME = 0
ENTITY_HP = 1
ENTITY_INITIATIVE = 2
ENTITY_DAMAGE = 3
ENTITY_MISS_CHANCE = 4
ENTITY_TOXICITY = 5
PLAYER_ITEM_DEFUSAL_KIT = 6
PLAYER_ITEM_KEY = 7

# --- ИНДЕКСЫ ПРЕДМЕТОВ ---
ITEM_DEFUSAL_KIT = 1
ITEM_NOTHING = 0

# --- ИМЕНА ---
MAIN_CHARACTER_NAME = 'Elgeia'
NAME_ENEMY_PUNK = 'Punk'
NAME_ENEMY_SYNTH_HOUND = 'Synth - Hound'
NAME_ENEMY_GLITCH_BUTCHER = 'Ripper'
NAME_ENEMY_PSY_CODER = 'Psy - Coder'

# --- ЦВЕТОВАЯ ПАЛИТРА (Используемые цвета) ---
DARK_GRAY = '\033[90m'
RED_TEXT_BRIGHT = '\033[91m'
GREEN_TEXT_REGULAR = '\033[32m'
GREEN_TEXT_BRIGHT = '\033[92m'
YELLOW_TEXT_BRIGHT = '\033[93m'
MAGENTA_TEXT_BRIGHT = '\033[95m'
LIGHT_BLUE_TEXT_BRIGHT = '\033[96m'
WHITE_TEXT_REGULAR = '\033[37m'
WHITE_TEXT_BRIGHT = '\033[97m'

# Цвета интерфейса
PLAYER_HP_FONT = GREEN_TEXT_BRIGHT
ENEMY_HP_FONT = RED_TEXT_BRIGHT

# Иконки тайлов (Цвета)
PLAYER_ICON = MAGENTA_TEXT_BRIGHT
ENEMY_ICON = RED_TEXT_BRIGHT
EXIT_ICON = LIGHT_BLUE_TEXT_BRIGHT
KEY_ICON = MAGENTA_TEXT_BRIGHT
CHEST_ICON = YELLOW_TEXT_BRIGHT
WALL_ICON = LIGHT_BLUE_TEXT_BRIGHT
FLOOR_ICON = DARK_GRAY
TRAP_ICON = RED_TEXT_BRIGHT

# --- КОМАНДЫ УПРАВЛЕНИЯ ---
COMMAND_MOVE_UP, COMMAND_MOVE_LEFT = 'w', 'a'
COMMAND_MOVE_DOWN, COMMAND_MOVE_RIGHT = 's', 'd'

MOVEMENT_COMMANDS = ['w', 'a', 's', 'd', 'ф', 'ы', 'в', 'ц']
COMBAT_COMMANDS = ['a', 'd', 'h']
TRAP_COMMANDS = ['1', '2']
DOOR_INTERACTION_COMMANDS = ['1', '2', '3']

# Меню
NEW_GAME_COMMANDS = ['n', 'new', 'new game', 'newgame']
LOAD_GAME_COMMANDS = ['l', 'load', 'load game', 'loadgame']
SETTING_GAME_COMMANDS = ['s', 'save', 'save game', 'savegame']
EXIT_GAME_COMMANDS = ['e', 'exit', 'exit game', 'exitgame']
SKIP_PROLOGUE_COMMANDS_NO = ['no', 'n']


# Внутри игровое меню
RESUME = ['r', 'к']
SAVE = ['s', 'ы']
LOAD = ['l', 'д']
QUIT_TO_MAIN_MENU = ['q', 'й']
IN_GAME_MENU_COMMANDS = ['r', 'l', 's', 'q']

# --- СТАТУСЫ И СОСТОЯНИЯ ---
FIGHT = 'is_fight'
EXIT = 'exit'
EXFILL = 'exfill'
RETURN_TO_MAIN_MENU = 'return to main menu'
EXIT_TO_MAIN_MENU = 'exit to main menu'
CONTINUE_GAME = 'continue'
GAME_OVER = "GAME_OVER"

# --- СОХРАНЕНИЯ ---
SAVE_DIR = "saves"
SAVE_PATH = "saves/"
DEFAULT_SAVE_NAME = "savegame"