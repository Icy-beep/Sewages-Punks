from src.constants import *



def create_default_player():
    return [
        MAIN_CHARACTER_NAME, 100, 5, 10, 0.1, 0, 0, 0, 0, 4, 1, # 0-10
        1,      # 11: PLAYER_LEVEL
        0,      # 12: PLAYER_XP
        100,    # 13: PLAYER_XP_REQ
        50,     # 14: PLAYER_ENERGY
        50,     # 15: PLAYER_MAX_ENERGY
        [],      # 16: PLAYER_SKILLS
        100     # 17: PLAYER_MAX_HP
    ]

punk = [NAME_ENEMY_PUNK, 66, 5, 5, 0.1, 0]
synth_hound = [NAME_ENEMY_SYNTH_HOUND, 50, 7, 10, 0.1, 0]
glitch_butcher = [NAME_ENEMY_GLITCH_BUTCHER, 100, 5, 10, 0.3, 0]
psy_coder = [NAME_ENEMY_PSY_CODER, 75, 6, 10, 0.1, 0]