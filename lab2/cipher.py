"""
This is a security toolbox containing an implementation of the Ceaser Rotation,
 the Viginere Encryption/Decryption, and the SHA-256 hashing algorithm.

Note that except for the hash function, only letters matching the [A-Za-z]-pattern are
 fully supported by the different algorithms.

Note: This is a library and is not supposed to run as a standalone application.
"""
import hashlib
from typing import List, Union


def hash_256(s: str) -> str:
    """Hashing a given string with SHA-256, a typical hashing algorithm"""
    return hashlib.sha256(s.encode('utf8')).hexdigest()


def rot_chr(c: str, n: int) -> str:
    """Applying Caeser Rotation encryption for a single letter"""
    alphabet = _get_correct_alphabet(c)
    return alphabet[(ord(c) - ord(alphabet[0]) + n) % 26]


def rot(txt: str, n: int) -> str:
    """Applying Caeser Rotation for a whole string"""
    return ''.join(map(lambda c: rot_chr(c, n), txt))


class Viginere:
    """Class containing both the encryption and decryption methods for the Viginere algorithm with a given password"""
    def __init__(self, pwd: str):
        self._pwd_ords = list(map(ord, pwd))
        self._pwd_len = len(pwd)

    def encrypt(self, txt) -> str:
        return ''.join(map(lambda i: (a:=_get_correct_alphabet(txt[i]))[(ord(txt[i]) + self._pwd_ords[i % self._pwd_len] - 2 * ord(a[0])) % 26],
                            range(len(txt))))
    
    def decrypt(self, txt) -> str:
        return ''.join(map(lambda i: _get_correct_alphabet(txt[i])[(ord(txt[i]) - self._pwd_ords[i % self._pwd_len]) % 26],
                            range(len(txt))))


_major_alphabet = list(map(lambda i: chr(i + 65), range(0, 26)))
_minor_alphabet = list(map(lambda i: chr(i + 97), range(0, 26)))


def _get_correct_alphabet(c: Union[str, chr]) -> List[str]:
    """Internal method -> used for deciding, if a given character is within [A-Z] or [a-z]"""
    return _major_alphabet if ord(c) < 95 else _minor_alphabet
