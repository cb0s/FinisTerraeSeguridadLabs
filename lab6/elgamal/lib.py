import random
from dataclasses import dataclass
from typing import List, Tuple

import numba as nb
# because of Deprecation warnings in Numba
import warnings
warnings.filterwarnings("ignore")


LOWER_BOUND: int = 100_000_000_000_000 # 1_000_000_007
UPPER_BOUND: int = 1_000_000_000_000_000

ENDIAN: str = 'little'

BYTE_COUNT: int = 16


@dataclass
class ElGamal:
    p: int
    g: int

    y: int
    x: int = -1 # Private Key

    r: int = -1 # Public Key

    def encrypt(self, msg: str) -> bytes:
        if self.r == -1:    # Encryption not possible
            return None
        
        encrypted_list = [None] * len(msg) * BYTE_COUNT * 2

        for index, c in enumerate(msg):
            stop_index = (base_index := 2 * index*BYTE_COUNT) + BYTE_COUNT

            i = ord(c)
            enc_p = self.encrypt_num(i)

            encrypted_list[base_index:stop_index] = enc_p[0].to_bytes(BYTE_COUNT, ENDIAN)
            encrypted_list[stop_index:stop_index + BYTE_COUNT] =\
                enc_p[1].to_bytes(BYTE_COUNT, ENDIAN)
                
        return bytes(encrypted_list)
    
    def encrypt_num(self, i: int) -> Tuple[int, int]:
        return pow(self.g, self.r, self.p), (i * pow(self.y, self.r, self.p)) % self.p

    def decrypt(self, msg: bytes) -> str:
        # Note: This implementation only works with the default Python encoding
        if self.x == -1:    # Decryption not possible
            return None

        decrypted_list = [None] * (len(msg) // (BYTE_COUNT * 2))

        for i in range(len(msg) // (BYTE_COUNT * 2)):
            stop_index = (start_index := 2 * i * BYTE_COUNT) + BYTE_COUNT

            x1 = int.from_bytes(msg[start_index:stop_index], ENDIAN)
            x2 = int.from_bytes(msg[stop_index:stop_index + BYTE_COUNT], ENDIAN)

            decrypted_list[i] = chr(self.decrypt_pair((x1, x2)))
        
        return ''.join(decrypted_list)
    
    def decrypt_pair(self, dec_p: Tuple[int, int]) -> int:
        c1, c2 = dec_p
        return (c2 * pow(c1, self.p - 1 - self.x, self.p)) % self.p


# https://github.com/AndrewQuijano/Homomorphic_Encryption eso ayudo mucho en la implementacion
def gen_elgamal_params() -> ElGamal:
    # We want to generate p and g, where 2 < g < p
    print("  p...")
    q, p = _gen_safe_prime()

    print("  g...")
    g_candidate = _gen_g_candidate(p)
    tested_candidates = [g_candidate]

    while (p - 1) % g_candidate == 0 or (p - 1) % _mod_inverse(g_candidate, p) == 0:
        g_candidate = _get_random_prime(3, p - 1, tested_candidates)
        tested_candidates.append(g_candidate)

    print("  x & y...")
    x = _get_random_prime(2, p - 2)
    y = pow(g_candidate, x, p)

    return ElGamal(p, g_candidate, y, x)


def gen_elgamal_enc_param(p: int) -> int:
    return random.randint(2, p - 1)


def _gen_safe_prime() -> Tuple[int, int]:
    q, p = 0, 0

    while not _is_prime(p):
        q, p = _qp_cycle()
    
    return q, p


def _qp_cycle() -> Tuple[int, int]:
    return (q := _get_random_prime()), 2 * q + 1


def _gen_g_candidate(p: int, prior_candidates: List[int] = None) -> int:
    # we need a random prime between 3 (inclusive) and p - 1 (inclusive)
    if not prior_candidates:
        prior_candidates = list()
    
    g_candidate = (p - 1)
    
    return g_candidate


# https://www.geeksforgeeks.org/multiplicative-inverse-under-modulo-m/ mod inverse for prime mod
def _mod_inverse(g_candidate, p):
    return pow(g_candidate, p - 2, p)


@nb.njit(cache=True)
def _is_coprime(a: int, b: int) -> bool:
    return False if (a == 1 or b == 1) else _gcd(a, b) == 1


# conventional eucledian algorithm is slow -> binary version
@nb.njit(cache=True)
def _gcd(a: int, b: int) -> int:
    return _binary_gcd(a, b)


# Implementation of https://en.wikipedia.org/wiki/Binary_GCD_algorithm
@nb.njit(cache=True)
def _binary_gcd(a: int, b: int) -> int:
    """Same as _gcd(a, b), but in O(n) time complexity."""
    if a == 0:
        return b
    elif b == 0:
        return a
    
    # make a and b odd (by removing trailing zeros)
    i = _trailing_zeros(a)
    a >>= i

    j = _trailing_zeros(b)
    b >>= j

    k = min(i, j)

    while a != 0:
        a >>= _trailing_zeros(a)

        if b > a:
            a, b = b, a
        
        a -= b

    return b << k


# Idea from https://stackoverflow.com/a/63552117/9346708
@nb.njit(cache=True)
def _trailing_zeros(n: int) -> int:
    # Could be more optimized, but should be fast enough
    return _jitted_bit_length(n & -n) - 1


@nb.njit(cache=True)
def _jitted_bit_length(n: int) -> int:
    # based on https://stackoverflow.com/a/9134134/9346708
    if n == 0:
        return 0
    bits = -32
    m = 0
    while n:
        m = n
        n >>= 32
        bits += 32
    while m:
        m >>= 1
        bits += 1
    return bits


# slightly optimized method with 6k+/-1 optimization
@nb.njit(cache=True)
def _is_prime(num: int) -> bool:
    if num <= 3:
        return num > 1

    if not num % 2 or not num % 3:
        return False
    
    limit = num ** 0.5
    for i in range(5, limit+1, 6):
        if num % i == 0 or num % (i+2) == 0:
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
