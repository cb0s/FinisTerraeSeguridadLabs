import socket
import json
from typing import NoReturn

from lib import RSA


IP: str = "localhost"
PORT: int = 10011
BUFFER_SIZE: int = 65536
OUTPUT_PATH: str = "lab6/mensajerecibido.txt"


def save_msg(msg: str, path: str) -> None:
    with open(path, 'w') as f:
        f.write(msg)


def connect_client(ip: str, port: int) -> socket.socket:
    client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client.connect((ip, port))
    return client


def main() -> NoReturn:
    print(f"Connecting to server on {IP}:{PORT}")
    client = connect_client(ip=IP, port=PORT)
    
    print("Receiving RSA parameters")
    rsa_packet_str = client.recv(BUFFER_SIZE).decode('utf8')
    rsa_packet = json.loads(rsa_packet_str)

    rsa = RSA(rsa_packet['n'], rsa_packet['d'])
    print(rsa)

    print("Receiving encrypted message")
    msg = client.recv(BUFFER_SIZE)

    print("Decrypting...")
    msg = rsa.decrypt(msg)

    print(f"Saving message to {OUTPUT_PATH}")
    save_msg(msg, OUTPUT_PATH)

    print("Closing connection")
    client.close()


if __name__ == '__main__':
    main()
