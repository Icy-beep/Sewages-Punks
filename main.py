from src.core import *


def start():
    pass

def game_loop():
    is_fight = False

    while not is_fight:
        is_fight = adventuring()

    fight()

def game_over():
    pass



if __name__ == '__main__':
    game_loop()
