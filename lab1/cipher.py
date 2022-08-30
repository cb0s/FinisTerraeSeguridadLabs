"""
Solucion de Lab 1
De Roberto Pineda, Belen Rojas, Cedric Boes
"""
from typing import List


def raise_on_bad_input(c: str) -> None:
    if c is None or not isinstance(c, str) or len(c) != 1:
        raise ValueError("You must enter a char!")


# Depending on the case whether A = 0 (_rot_alphabet_0) or A = 1 (_rot_alphabet_1)
_ascii_constant = 65
_rot_alphabet_0 = list(map(lambda i: chr(i + _ascii_constant), range(0, 26)))
_rot_alphabet_1 = [chr(_ascii_constant + 25)] + list(map(lambda i: chr(i + _ascii_constant), range(0, 25)))
def rot_chr(c: str, n: int, zero_based_a=True) -> str:
    raise_on_bad_input(c)
    _rot_alphabet = _rot_alphabet_0 if zero_based_a else _rot_alphabet_1
    return _rot_alphabet[(ord(c) - _ascii_constant + n) % 26]


def rot(txt: str, n: int, zero_based_a=True) -> str:
    return ''.join(map(lambda c: rot_chr(c, n, zero_based_a), txt))


class Viginere:
    def __init__(self, pwd: str, zero_based_a=True):
        self._pwd_ords = list(map(ord, pwd))
        self._pwd_len = len(pwd)
        self._rot_alphabet = _rot_alphabet_0 if zero_based_a else _rot_alphabet_1
    
    def encrypt(self, txt) -> str:
        print(self._pwd_ords, self._pwd_len)
        return ''.join(map(lambda i: self._rot_alphabet[(ord(txt[i]) + self._pwd_ords[i % self._pwd_len] - 2 * _ascii_constant) % 26],
                            range(len(txt))))
    
    def decrypt(self, txt) -> str:
        return ''.join(map(lambda i: self._rot_alphabet[(ord(txt[i]) - self._pwd_ords[i % self._pwd_len]) % 26],
                            range(len(txt))))


if __name__ == '__main__':
    pwd = "HEROPASSWORD"
    suite = Viginere(pwd)
    txt = ""
    enc_txt = ""
    #enc_txt = rot(txt, 8)
    #enc_txt = suite.encrypt(enc_txt)
    #enc_txt = rot(enc_txt, 12)
    enc_txt = "FQEWNMGZCMYPBHPANWDQJW"
    dec_txt = rot(enc_txt, -12)
    dec_txt = suite.decrypt(dec_txt)
    dec_txt = rot(dec_txt, -8)
    print(txt, enc_txt, dec_txt, f"(encrypted with {pwd})")
