import socket
import json
import time
from typing import NoReturn

from lib import gen_elgamal_params


IP: str = 'localhost'
PORT: int = 10012
# We can receive messages of length 2048 encrypted and 65536 unencrypted
BUFFER_SIZE: int = 65536
OUTPUT_PATH: str = 'lab6/mensajerecibido.txt'


def prepare_server(ip: str, port: int) -> socket.socket:
    # Note that the server only serves one client at a time
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.bind((ip, port))
    server.listen(5)
    return server


def save_msg(msg: str, path: str) -> None:
    with open(path, 'w') as f:
        f.write(msg)


def handle_client(client) -> None:
    print(" Generating ElGamal parameters")
    elgamal = gen_elgamal_params()
    
    print(" Informing client about chosen parameters")
    packet = {
        'g': elgamal.g,
        'p': elgamal.p,
        'y': elgamal.y
    }
    msg = json.dumps(packet).encode('utf8')
    client.send(msg)

    print(" Awaiting securly transmitted document")
    raw_msg = client.recv(BUFFER_SIZE)

    print(" Decrypting message")
    decrypted_msg = elgamal.decrypt(raw_msg)

    print(f" Saving message to {OUTPUT_PATH}")
    save_msg(decrypted_msg, OUTPUT_PATH)


def main() -> NoReturn:
    print(f"Creating server on {IP}:{PORT}")
    server_socket = prepare_server(ip=IP, port=PORT)
    
    try:
        while True:
            (client, address) = server_socket.accept()
            print(f"New client connected ({address})")
            handle_client(client)
            print("Connection closed")
    except Exception as e:
        print(e)
        import traceback
        traceback.print_exc()
        print("Stopping server")


if __name__ == '__main__':
    main()
