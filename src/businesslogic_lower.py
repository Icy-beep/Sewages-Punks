from src.constants import *

def generate_i_path():
    import random

    generate_i_pass_1 = random.randint(3, 8)

    return generate_i_pass_1

def generate_passes():
    import random
    from src.constants import HOW_MANY_PASSES_MAX, HOW_MUCH_WALLS_WHERE_PASS

    passes = []

    for i in range(HOW_MUCH_WALLS_WHERE_PASS):
        passes.append([])
        how_much_passes = random.randint(1, 2)
        for j in range(HOW_MANY_PASSES_MAX):
            if how_much_passes == 1:
                passes[i].append(generate_i_path())
                continue

            if how_much_passes == 2:
                passes[i].append(generate_i_path())
                passes[i].append(generate_i_path())

    return passes