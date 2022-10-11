import random
import sys
import math


LOWER_BOUND = 1000003      # PRIME
MAX_BOUND = 9999991        # PRIME


def create_random(max_bound=MAX_BOUND) -> int:
    return random.randint(LOWER_BOUND, max_bound)


def is_prime(n: int) -> bool:
    return not any(n % i == 0 for i in range(2, int(math.sqrt(n))))


def create_random_prime():
    rand = create_random()

    while not is_prime(rand):
        if rand % 2 == 0:
            rand += 1
        else:
            rand += 2
    return rand
