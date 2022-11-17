import random
from dataclasses import dataclass
from typing import List

import numba as nb
# because of Deprecation warnings in Numba
import warnings
warnings.filterwarnings("ignore")


# Very big primes -> with optimizations and numba this actually works
LOWER_BOUND: int = 100_000_000_000_000_003 # 1_000_000_007
UPPER_BOUND: int = 1_799_999_999_999_999_999

LOWER_BOUND_COPRIME: int = 100_000_007
UPPER_BOUND_INITIAL_COPRIME: int = 999_999_937

ENDIAN = 'little'

BYTE_COUNT = 16


@dataclass
class RSA:
    n: int
    d: int

    e: int = -1     # -1 means no encryption functionality

    def encrypt(self, msg: str) -> bytes:
        encrypted_list = [None] * len(msg) * BYTE_COUNT

        for index, c in enumerate(msg):
            i = ord(c)
            encrypted_list[index*BYTE_COUNT:index*BYTE_COUNT+BYTE_COUNT] =\
                self.encrypt_num(i).to_bytes(BYTE_COUNT, ENDIAN)
                
        return bytes(encrypted_list)
    
    def encrypt_num(self, i: int) -> int:
        return _modular_power(i, self.e, self.n)
    
    def decrypt(self, msg: bytes) -> str:
        # Note: This implementation only works with the default Python encoding
        decrypted_list = [None] * (len(msg) // BYTE_COUNT)

        for i in range(len(msg) // BYTE_COUNT):
            x = int.from_bytes(msg[i*BYTE_COUNT:i*BYTE_COUNT+BYTE_COUNT], ENDIAN)
            decrypted_list[i] = chr(self.decrypt_num(x))
        
        return ''.join(decrypted_list)

    def decrypt_num(self, i: int) -> int:
        return _modular_power(i, self.d, self.n)

def gen_rsa_params() -> RSA:
    print("  p...")
    p = _get_random_prime()
    print("  q...")
    q = _get_random_prime(black_list=[p])

    print("  n & phi...")
    n = p * q
    phi_n = (p - 1) * (q - 1)

    print("  e...")
    # we don't use even numbers -> more difficult to fit coprime constraint
    e = random.randint(LOWER_BOUND_COPRIME, UPPER_BOUND_INITIAL_COPRIME)
    e = e + 1 if e % 2 == 0 else e

    while not _is_coprime(e, (p - 1)) or not _is_coprime(e, (q - 1)):
        e += 2

    print("  d...")
    d = pow(e, -1, phi_n)

    return RSA(n, d, e)


@nb.njit(cache=True)
def _is_coprime(a: int, b: int) -> bool:
    return False if (a == 1 or b == 1) else _gcd(a, b) == 1


# conventional eucledian algorithm is slow -> binary version
@nb.njit(cache=True)
def _gcd(a: int, b: int) -> int:
    return _binary_gcd(a, b)


# from https://math.stackexchange.com/a/2156132/759013
def _eucledian_gcd(a: int, b: int) -> int:
    while (b):
        a, b = b, a % b
    return a


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


# note that is used only for integers
def _modular_power(base: int, exp: int, mod: int) -> int:
    """
    Returns base ** exp % mod without calculating base ** exp in one step.
    The computational overhead is given with O[log (exp)].

    Why this works can be found here https://en.wikipedia.org/wiki/Modular_exponentiation .
    """
    if mod == 1:
        return 0

    r = 1
    base %= mod

    while exp > 0:
        if exp % 2 == 1:
            r = (r * base) % mod
        
        base = (base * base) % mod
        exp = exp >> 1
    
    return r
