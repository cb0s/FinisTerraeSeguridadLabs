import random
from dataclasses import dataclass
from typing import List


UPPER_BOUND: int = 999
LOWER_BOUND: int = 100

LOWER_BOUND_COPRIME: int = 41


@dataclass
class RSA:
    n: int
    d: int

    e: int = -1     # -1 means no encryption functionality

    def encrypt(self, msg: str) -> str:
        encrypted_list = [None] * len(msg)

        for index, c in enumerate(msg):
            i = ord(c)
            encrypted_list[index] = chr(self.encrypt_num(i))
        
        return ''.join(encrypted_list)

    
    def encrypt_num(self, i: int) -> int:
        return i ** self.e % self.n
    
    def decrypt(self, msg: str) -> str:
        decrypted_list = [None] * len(msg)

        for index, c in enumerate(msg):
            i = ord(c)
            decrypted_list[index] = chr(self.decrypt_num(i))
        
        return ''.join(decrypted_list)

    def decrypt_num(self, i: int) -> int:
        return i ** self.d % self.n


def gen_rsa_params() -> RSA:
    p = _get_random_prime()
    q = _get_random_prime(black_list=[p])

    n = p * q
    phi_n = (p - 1) * (q - 1)

    # we don't use even numbers -> more difficult to fit coprime constraint
    e = LOWER_BOUND_COPRIME + 1 \
        if LOWER_BOUND_COPRIME % 2 == 0 else LOWER_BOUND_COPRIME
    while not _is_coprime(e, phi_n):
        e += 2

    d = pow(e, -1, phi_n)

    return RSA(n, d, e)


def _is_coprime(a: int, b: int) -> bool:
    return False if (a == 1 or b == 1) else _gcd(a, b) == 1


# from https://math.stackexchange.com/a/2156132/759013
def _gcd(a: int, b: int) -> int:
    while (b):
        a, b = b, a % b
    return a


# slightly optimized method with 6k+/-1 optimization
def _is_prime(num: int) -> bool:
    if num <= 3:
        return num > 1

    if not num % 2 or not num % 3:
        return False
    
    if any(num % i == 0 or num % (i + 2) == 0 for i in range(5, int(num ** (1/2)) + 1, 6)):
        return False

    return True


def _get_random_prime(lower_bound: int = LOWER_BOUND,
                      upper_bound: int = UPPER_BOUND,
                      black_list: List[int] = None) -> int:
    if not black_list:
        black_list = list()

    rand = random.randint(lower_bound, upper_bound)
    if _is_prime(rand) and rand not in black_list:
        return rand

    if rand % 2 == 0:
        rand += 1
    
    while not _is_prime(rand) or rand in black_list:
        rand += 2
    
    return rand
