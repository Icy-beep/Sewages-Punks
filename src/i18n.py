# src/i18n.py
import json
import random
from pathlib import Path

_data = {}
_current_lang = "ru"
_fallback = {}

# Маппинг цветов
_COLORS = {
    "RESET": "\033[0m",
    "MAGENTA": "\033[95m",
    "CYAN": "\033[96m",
    "RED": "\033[91m",
    "GREEN": "\033[92m",
    "YELLOW": "\033[93m",
    "WHITE": "\033[97m",
    "GRAY": "\033[90m",
    "DARK_GRAY": '\033[90m',
    "RED_TEXT_BRIGHT": '\033[91m',
    "GREEN_TEXT_REGULAR": '\033[32m',
    "GREEN_TEXT_BRIGHT": '\033[92m',
    "YELLOW_TEXT_BRIGHT": '\033[93m',
    "MAGENTA_TEXT_BRIGHT": '\033[95m',
    "LIGHT_BLUE_TEXT_BRIGHT": '\033[96m',
    "WHITE_TEXT_REGULAR": '\033[37m',
    "WHITE_TEXT_BRIGHT": '\033[97m',
}


def init(lang: str = "ru"):
    global _data, _current_lang, _fallback
    _current_lang = lang

    project_root = Path(__file__).resolve().parent.parent
    locales_dir = project_root / "locales"

    # Загружаем fallback (английский)
    fallback_path = locales_dir / "en.json"
    if fallback_path.exists():
        with open(fallback_path, encoding="utf-8") as f:
            _fallback = json.load(f)

    # Загружаем целевой язык
    file_path = locales_dir / f"{lang}.json"
    if file_path.exists():
        with open(file_path, encoding="utf-8") as f:
            _data = json.load(f)
        print(f"✅ [i18n] Loaded '{lang}': {len(_data)} keys")
    else:
        print(f"⚠️ [i18n] File not found: {file_path}")
        _data = _fallback.copy()


def apply_random_system_language() -> tuple[str, str]:
    """Случайно выбирает язык из доступных .json и переключает игру."""
    # Сканируем папку locales на наличие языковых файлов
    available = [f.stem for f in Path("locales").glob("*.json")]
    if not available:
        return "ru", "РУССКИЙ"  # Фолбэк если папка пуста

    chosen_code = random.choice(available)
    set_language(chosen_code)  # Переключаем глобальный язык

    # Маппинг кодов в красивые названия для лога
    lang_names = {
        "ru": "РУССКИЙ", "en": "ENGLISH", "de": "DEUTSCH",
        "fr": "FRANÇAIS", "ja": "日本語", "zh": "中文", "es": "ESPAÑOL"
    }
    return chosen_code, lang_names.get(chosen_code, chosen_code.upper())


def t(key: str, **kwargs) -> str:
    """Возвращает текст с подстановкой цветов и переменных."""
    if not _data:
        return f"[i18n_NOT_INIT: {key}]"

    text = _data.get(key, _fallback.get(key, f"[MISSING:{key}]"))

    # Сначала заменяем ЦВЕТА (они в фигурных скобках, но заглавными буквами)
    for color_name, color_code in _COLORS.items():
        text = text.replace("{" + color_name + "}", color_code)

    # Потом подставляем ПЕРЕМЕННЫЕ через format()
    if kwargs:
        try:
            return text.format(**kwargs)
        except KeyError as e:
            return f"{text} [ERR: Missing arg {e}]"

    return text


def set_language(lang: str):
    """Сменить язык на лету."""
    init(lang)


def get_language() -> str:
    return _current_lang