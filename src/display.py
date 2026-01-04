from src.constants import *


def show_dungeon_map(dungeon):

    for i in range(DUNGEON_HEIGHT):
        print()
        for j in range(DUNGEON_WIDTH):
            print(end=' ')

            if dungeon[i][j] == 0:
                print(PLAYER_ICON + '@', end='')

            if dungeon[i][j] == 1:
                print(ENEMY_ICON + 'F', end='')

            if dungeon[i][j] == 2:
                print(EXIT_ICON + 'E', end='')

            if dungeon[i][j] == 3:
                print(KEY_ICON + 'K', end='')

            if dungeon[i][j] == 4:
                print(CHEST_ICON + 'C', end='')

            if dungeon[i][j] == 5:
                print(WALL_ICON + '█', end='')

            if dungeon[i][j] == 6:
                print(FLOOR_ICON + '.', end='')

            if dungeon[i][j] == 7:
                print(TRAP_ICON + '.', end='')

    return ''

def START_FIGHT_MESSAGE(enemy_name):

    if enemy_name[0][0]:
        print(f'{START_FIGHT_MESSAGE_FONT} Вы вступаете в бой с панком')
