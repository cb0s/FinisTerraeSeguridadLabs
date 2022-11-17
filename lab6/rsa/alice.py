import socket
import json
import time
from typing import NoReturn

from lib import gen_rsa_params


IP: str = 'localhost'
PORT: int = 10011
INPUT_PATH: str = 'lab6/mensajeentrada.txt'


def prepare_server(ip: str, port: int) -> socket.socket:
    # Note that the server only serves one client at a time
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.bind((ip, port))
    server.listen(5)
    return server


def load_msg(path: str) -> str:
    with open(path, 'r') as file:
        return file.read()


def handle_client(client) -> None:
    print(" Generating RSA parameters")
    rsa = gen_rsa_params()

    packet = {
        'n':    rsa.n,
        'd':    rsa.d
    }
    print(f"  {rsa}")

    print(" Sending RSA information")
    client.send(json.dumps(packet).encode('utf8'))

    print(" Loading and encrypting message")
    msg = load_msg(INPUT_PATH)
    msg = rsa.encrypt(msg)
    time.sleep(.25)     # to ensure client is ready

    print(" Sending encrypted message")
    client.send(msg)


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
