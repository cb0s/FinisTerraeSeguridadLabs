import socket
import json
import lib
import hashlib
import base64
import time
from typing import NoReturn


PORT = 52304
BUFFER_SIZE = 65536
KEYEX_ALGO = lib.EncryptionFlags.EDH
ENC_ALGO = lib.EncryptionFlags.AES
PATH_TO_MSG = "lab5/mensajeentrada.txt"


def connect_client(ip: str = "127.0.0.1", port: int = PORT) -> socket.socket:
    client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client.connect((ip, port))
    return client


def key_exchange(client: socket.socket) -> lib.EncryptionMethod:
    if KEYEX_ALGO == lib.EncryptionFlags.NO_ENC:
        return lib.NoEncryption()
    
    header = bytes(0)
    header = lib.apply_flag(ENC_ALGO, header)
    header = lib.apply_flag(KEYEX_ALGO, header)
    header = lib.apply_flag(lib.MessageFlags.KE, header)

    client.send(header)
    # Key exchange also works with relatively small buffer
    response = client.recv(1024).decode('utf8')

    packet_dict = json.loads(response)

    p = packet_dict['p']
    g = packet_dict['g']
    A = packet_dict['A']    

    b = lib.create_random(p)
    B = g ** b % p

    K = A ** b % p
    algo = lib.ENCRYPTION_METHOD_RESOLVER[ENC_ALGO](K.to_bytes(4, 'big'))

    packet = {
        'B': B,
        'nonce-or-iv': base64.b64encode(algo.nonce_or_iv).decode('utf8')
    }

    send_packet = json.dumps(packet)
    client.send(send_packet.encode('utf8'))

    return algo


def send_msg(msg: str, encryptor: lib.EncryptionMethod, client: socket.socket) -> None:
    enc_msg = encryptor.encrypt(msg)
    msg_bytes = lib.apply_flag(lib.MessageFlags.OP, enc_msg)
    client.send(msg_bytes)


def receive_msg(encryptor: lib.EncryptionMethod, client: socket.socket) -> str:
    msg_bytes = client.recv(BUFFER_SIZE)
    return encryptor.decrypt(msg_bytes)


def load_msg(path: str) -> str:
    with open(path, 'r') as f:
        return f.read()


def close(client: socket.socket) -> None:
    msg = bytes(0)
    msg = lib.apply_flag(lib.MessageFlags.EX, msg)
    client.send(msg)
    client.close()


def main() -> NoReturn:
    print("Connecting to server")
    client = connect_client()
    encryptor = key_exchange(client)
    time.sleep(0.2)             # Small delay that the client doesn't exceed the server

    print("Loading and encrypting message")
    msg = load_msg(PATH_TO_MSG)
    msg = json.dumps({'msg': msg})

    print("Sending message")
    send_msg(msg, encryptor, client)
    time.sleep(0.2)             # Small delay that the client doesn't exceed the server
    close(client)
    print("Message successfully transmitted")


if __name__ == '__main__':
    main()
