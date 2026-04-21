"""
Constants.
Cleaned and organized version.
"""

# --- СИСТЕМНЫЕ НАСТРОЙКИ ---
RESET = '\033[0m'
ESC = b'\x1b'
I = b'\x69'
HIDE_CURSOR = "\033[?25l"
SHOW_CURSOR = "\033[?25h"

# Координаты (индексы списков)
x_coord = 0
y_coord = 1

# --- ТАЙЛЫ И КАРТА ---
PLAYER_TILE, ENEMY_TILE, EXIT_TILE, KEY_TILE = 0, 1, 2, 3
CHEST_TILE, WALL_TILE, FLOOR_TILE, TRAP_TILE = 4, 5, 6, 7
TERMINAL_TILE, TERMINAL_SYMBOL = 8, '▣'

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
PLAYER_SKILL_POINTS = 8
PLAYER_ITEM_REGEN_INHALER = 9
PLAYER_ITEM_DETOX_INHALER = 10
# --- ПРОКАЧКА И НАВЫКИ ---
PLAYER_LEVEL = 11        # Уровень персонажа
PLAYER_XP = 12           # Текущий опыт
PLAYER_XP_REQ = 13       # Сколько опыта нужно для след. уровня
PLAYER_ENERGY = 14       # Текущая энергия (Мана)
PLAYER_MAX_ENERGY = 15   # Максимальная энергия
PLAYER_SKILLS = 16       # Список названий навыков (строки)
PLAYER_MAX_HP = 17       # Максимум ХП

# --- ИНДЕКСЫ ПРЕДМЕТОВ ---
ITEM_DETOX_INHALER = 3
ITEM_REGEN_INHALER = 2
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
PAUSE = "pause"

# Константы для работы с инвентарём
INVENTORY = "inventory"

HEAL_FROM_INVENTORY = 'r'
DETOX_FROM_INVENTORY = 'd'
INVENTORY_ACTIONS = [HEAL_FROM_INVENTORY, DETOX_FROM_INVENTORY]
EXIT_INVENTORY = ['inventory', 'i', 'inv', 'in', 'invent']
INVENTORY_COMMANDS = [INVENTORY_ACTIONS, EXIT_INVENTORY]

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

# --- МУЗЫКА ---
MENU_INTRO = "audio/main_menu_intro.mp3"
MENU_LOOP = "audio/main_menu_loop.mp3"
GAME_INTRO = "audio/intro_music.mp3"
GAME_LOOP = "audio/gameplay_music_loop.mp3"

# --- HACKING SYSTEM ---
HACKING_SUCCESS_ZONES = 3  # Количество успешных попаданий для полного взлома
HACKING_TOLERANCE = 2  # Допустимое отклонение от идеальной зоны

# Типы взлома
HACK_TIMING = "timing"
HACK_SEQUENCE = "sequence"
HACK_REACTION = "reaction"

# --- БАЗА ДАННЫХ НАВЫКОВ ---
# type: 'damage', 'heal', 'debuff'
# fail_effect: что происходит при провале мини-игры
SKILL_DATABASE = {
    "NEURAL_SHOCK": {
        "name": "NEURAL SHOCK",
        "shard_cost": 20,
        "energy_cost": 15,
        "desc": "Взлом нейроимпланта врага",
        "type": "damage",
        "base_val": 25,
        "fail_effect": "backfire", # Враг наносит урон игроку
        "fail_val": 10
    },
    "SYSTEM_RESTORE": {
        "name": "SYSTEM RESTORE",
        "shard_cost": 30,
        "energy_cost": 25,
        "desc": "Аварийное восстановление HP",
        "type": "heal",
        "base_val": 30,
        "fail_effect": "overload", # Игрок получает урон
        "fail_val": 15
    },
    "OVERCLOCK": {
        "name": "OVERCLOCK",
        "shard_cost": 15,
        "energy_cost": 10,
        "desc": "Разгон атакующих систем",
        "type": "buff",
        "base_val": 15, # Бонус к урону на 1 ход
        "fail_effect": "system_error", # Пропуск хода
        "fail_val": 0
    }
}

# Навыки-взломы
HACK_SKILLS = {
    "NEURAL_SHOCK": {
        "name": "NEURAL SHOCK",
        "shard_cost": 20,   # Цена покупки в терминале
        "energy_cost": 15,  # Цена использования в бою (Энергия)
        "desc": "Взлом нейроимпланта",
        "hack_type": "timing", # Тип мини-игры
        "stages": 3,
        "success_damage": 25,
        "partial_damage": 10,
        "fail_damage": 0,
        "fail_effect": "backfire", # Эффект при полном провале
        "fail_value": 10     # Сила негативного эффекта (урон себе)
    },
    "SYSTEM_RESTORE": {
        "name": "SYSTEM RESTORE",
        "shard_cost": 30,
        "energy_cost": 25,
        "desc": "Аварийное восстановление HP",
        "hack_type": "timing",
        "stages": 4,
        "success_heal": 35,
        "partial_heal": 15,
        "fail_heal": 5,
        "fail_effect": "overload",
        "fail_value": 10
    },
    "OVERCLOCK": {
        "name": "OVERCLOCK",
        "shard_cost": 15,
        "energy_cost": 10,
        "desc": "Разгон атакующих систем",
        "hack_type": "reaction",
        "stages": 5,
        "success_bonus": 15,
        "partial_bonus": 5,
        "fail_bonus": 0,
        "fail_effect": "skip_turn", # Пропуск хода
        "fail_value": 0
    }
}

TERMINAL_PROGRAMS = {
    '1': {'name': 'DARKNET_MARKET', 'func': 'shop', 'desc': 'Buy skill augmentations'},
    '2': {'name': 'SYS_MONITOR', 'func': 'status', 'desc': 'View operator biometrics'},
    '3': {'name': 'MISSION_LOG', 'func': 'logs', 'desc': 'Access mission archive'},
    '4': {'name': 'NET_SCANNER', 'func': 'scanner', 'desc': 'Scan local sector (WIP)'},
    '0': {'name': 'DISCONNECT', 'func': 'exit', 'desc': 'Terminate connection'}
}

TERMINAL_COMMANDS = ['1', '2', '3', '4', '0', 'shop', 'status', 'logs', 'exit']

# Команда на использование навыка
SKILL_COMMAND = 'k'