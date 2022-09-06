import hashlib
from typing import List


def hash_256(s: str) -> str:
    return hashlib.sha256(s.encode('utf8')).hexdigest()


def rot_chr(c: str, n: int) -> str:
    alphabet = _get_correct_alphabet(c)
    return alphabet[(ord(c) - ord(alphabet[0]) + n) % 26]


def rot(txt: str, n: int, zero_based_a=True) -> str:
    return ''.join(map(lambda c: rot_chr(c, n), txt))


class Viginere:
    def __init__(self, pwd: str, zero_based_a=True):
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


def _get_correct_alphabet(c: str) -> List[str]:
    return _major_alphabet if ord(c) < 95 else _minor_alphabet
