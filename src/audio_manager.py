import pygame
import os

_current_volume = 0.5


def init_audio():
    """Инициализация микшера"""
    if not pygame.mixer.get_init():
        pygame.mixer.init()


def play_theme(intro_path, loop_path=None, fade_ms=2000):
    """
    Плавно переключает музыку.
    Если задан loop_path, он встанет в очередь после интро.
    """
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


def stop_audio(fade_ms=1000):
    """Плавная остановка всей музыки"""
    pygame.mixer.music.fadeout(fade_ms)


def set_volume(volume):
    """Изменение громкости (от 0.0 до 1.0)"""
    global _current_volume
    _current_volume = volume
    pygame.mixer.music.set_volume(volume)