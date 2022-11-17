import socket
import json
from typing import NoReturn

from lib import ElGamal, gen_elgamal_enc_param


IP: str = "localhost"
PORT: int = 10012
# We can receive messages of length 2048 encrypted and 65536 unencrypted
BUFFER_SIZE: int = 65536
INPUT_PATH: str = "lab6/mensajeentrada.txt"


def load_msg(path: str) -> str:
    with open(path, 'r') as file:
        return file.read()


def connect_client(ip: str, port: int) -> socket.socket:
    client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client.connect((ip, port))
    return client


def main() -> NoReturn:
    print(f"Connecting to server on {IP}:{PORT}")
    client = connect_client(ip=IP, port=PORT)
    
    print("Receiving ElGamal parameters")
    elgamal_packet_str = client.recv(BUFFER_SIZE).decode('utf8')
    elgamal_packet = json.loads(elgamal_packet_str)

    print("Generating missing encryption parameter")
    r = gen_elgamal_enc_param(elgamal_packet['p'])
    elgamal = ElGamal(elgamal_packet['p'],
                      elgamal_packet['g'],
                      elgamal_packet['y'],
                      r=r)
    print(elgamal)

    print("Loading message")
    msg = load_msg(INPUT_PATH)
    
    print("Encrypting message")
    enc_msg = elgamal.encrypt(msg)

    print("Sending encrypted message")
    client.send(enc_msg)

    print("Closing connection")
    client.close()


if __name__ == '__main__':
    main()
