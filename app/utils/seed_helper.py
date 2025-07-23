# app/utils/seed_helper.py

import random

def get_random_seed() -> int:
    return random.randint(1, 2**32 - 1)
