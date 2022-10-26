import random
import sys
import math
import hashlib
import Crypto.Cipher.AES as _AES
import Crypto.Cipher.DES as _DES
import Crypto.Cipher.DES3 as _DES3
from abc import ABC, abstractmethod
from enum import IntFlag
from typing import Union


# Constants used by the classes and methods
LOWER_BOUND = 11#1000003      # PRIME
MAX_BOUND = 97#9999991        # PRIME
DEFAULT_ENCODING = "utf8"


# Classes
class MessageFlags(IntFlag):
    KE = 0      # Key Exchange
    OP = 1      # Operation (after key exchange)
    EX = 2      # Closing the connection in a fair manner


class EncryptionFlags(IntFlag):
    # Key-Exchange methods
    EDH = 0     # Diffie Hellman Exchange

    # Encryption
    DES = 10    # DES
    D3S = 11    # 3DES
    AES = 12    # AES

    NO_ENC = -1 # No encryption is performed



class EncryptionMethod(ABC):
    def __init__(self, key: bytes, length: int):
        self._key = key
        self._key_length = length
        if self._key is not None:
            self._key = hash_key(self._key)[:length]

    @abstractmethod
    def encrypt(self, msg: str, encoding=DEFAULT_ENCODING) -> bytes:
        """Returns encrypted bytes based on the given encoding"""
        ...
    
    @abstractmethod
    def decrypt(self, msg: bytes, encoding=DEFAULT_ENCODING) -> str:
        """Returns decrypted string from the given bytes based on a given encoding"""
        ...
    
    @property
    def nonce_or_iv(self) -> Union[bytes, None]:
        """Returns either the Nonce or the IV byte of the encryptor as an ascii encoded str"""
        if hasattr(self.__class__, 'iv'):
            return self.iv
        elif hasattr(self.__class__, 'nonce'):
            return self.nonce
        else:
            print(vars(self.__class__))
            return None

    def key(self) -> bytes:
        return self._key
    
    def key_length(self) -> int:
        return self._key_length


class NoEncryption(EncryptionMethod):
    def __init__(self, *args):
        super().__init__(None, -1)
    
    def encrypt(self, msg: str, encoding=DEFAULT_ENCODING) -> bytes:
        return msg.encode(encoding)
    
    def decrypt(self, msg: bytes, encoding=DEFAULT_ENCODING) -> str:
        return msg.decode(encoding)


class AES(EncryptionMethod):
    def __init__(self, key: bytes, nonce: bytes = None, *args):
        super().__init__(key, 32)
        self._cipher = _AES.new(self._key, _AES.MODE_EAX, nonce=nonce)
    
    def encrypt(self, msg: str, encoding=DEFAULT_ENCODING) -> bytes:
        enc = self._cipher.encrypt(msg.encode(encoding))
        return enc

    def decrypt(self, msg: bytes, encoding=DEFAULT_ENCODING) -> str:
        return self._cipher.decrypt(msg).decode(encoding)

    @property
    def nonce(self) -> bytes:
        return self._cipher.nonce


class DES(EncryptionMethod):
    def __init__(self, key: bytes, iv: bytes = None, *args):
        super().__init__(key, 8)
        self._cipher = _DES.new(self._key, _DES.MODE_OFB, iv=iv)
    
    def encrypt(self, msg: str, encoding=DEFAULT_ENCODING) -> bytes:
        return self._cipher.encrypt(msg.encode(encoding))

    def decrypt(self, msg: bytes, encoding=DEFAULT_ENCODING) -> str:
        return self._cipher.decrypt(msg).decode(encoding)

    @property
    def iv(self) -> bytes:
        return self._cipher.iv


class D3S(EncryptionMethod):
    def __init__(self, key: bytes, iv: bytes = None, *args):
        super().__init__(key, 24)
        self._key = _DES3.adjust_key_parity(self._key)
        self._cipher = _DES3.new(self._key, _DES3.MODE_CFB, iv=iv)

    def encrypt(self, msg: str, encoding=DEFAULT_ENCODING) -> bytes:
        return self._cipher.encrypt(msg.encode(encoding))

    def decrypt(self, msg: bytes, encoding=DEFAULT_ENCODING) -> str:
        return self._cipher.decrypt(msg).decode(encoding)
    
    @property
    def iv(self) -> bytes:
        return self._cipher.iv


# Functions
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


def apply_flag(flag, bytes_):
    return flag.to_bytes(length=1, byteorder='big') + bytes_


# Hashing keys always gives you the same amount of bytes to work with
def hash_key(key: int) -> bytes:
    return hashlib.sha256(str(key).encode('ascii')).digest()


# Constants which use methods and classes
ENCRYPTION_METHOD_RESOLVER = {
    EncryptionFlags.DES: DES,
    EncryptionFlags.D3S: D3S,
    EncryptionFlags.AES: AES
}
