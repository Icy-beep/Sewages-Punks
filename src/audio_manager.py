import os
try:
    import pygame

    _PYGAME_INSTALLED = True
except ImportError:
    _PYGAME_INSTALLED = False

_AUDIO_ENABLED = False
_current_volume = 0.5


def init_audio():
    """Безопасная инициализация звука"""
    global _AUDIO_ENABLED
    if not _PYGAME_INSTALLED:
        print("[System] Предупреждение: библиотека pygame-ce не найдена. Игра будет без звука.")
        return

    try:
        pygame.mixer.init()
        _AUDIO_ENABLED = True
    except Exception as e:
        print(f"[System] Ошибка звуковой карты: {e}. Звук отключен.")
        _AUDIO_ENABLED = False


def play_theme(intro_path, loop_path=None, fade_ms=2000):
    """Проигрывание музыки с проверкой доступности аудио"""
    if not _AUDIO_ENABLED:
        return

    try:
        pygame.mixer.music.fadeout(fade_ms)

        if not os.path.exists(intro_path):
            return

        pygame.mixer.music.load(intro_path)
        pygame.mixer.music.set_volume(_current_volume)

        if loop_path and os.path.exists(loop_path):
            pygame.mixer.music.play(0)
            pygame.mixer.music.queue(loop_path, loops=-1)
        else:
            pygame.mixer.music.play(-1)
    except Exception:
        pass


def stop_audio(fade_ms=1000):
    if _AUDIO_ENABLED:
        pygame.mixer.music.fadeout(fade_ms)


def set_volume(volume):
    global _current_volume
    _current_volume = volume
    if _AUDIO_ENABLED:
        pygame.mixer.music.set_volume(volume)