import socket
import lib
import json
import base64
from typing import Tuple, NoReturn, Type


PORT = 52304
BUFFER_SIZE = 65536
PATH_TO_SAVE = "lab5/mensajerecibido.txt"
# Ecuaciones de Diffie Hellman
# p, a, g -> A = g ** a % p, K = B ** a % p
# b -> B = g ** b % p, K = A ** b % p


def prepare_key_exchange() -> Tuple[int, int, int, int]:
    p = lib.create_random_prime()
    a = lib.create_random(p)
    g = lib.create_random(p)
    A = g ** a % p
    return p, a, g, A


def create_initial_packet(p, g, A) -> bytes:
    initial_packet_dict = {
        'p': p,
        'g': g,
        'A': A
    }
    initial_packet = json.dumps(initial_packet_dict)
    return initial_packet


def prepare_server(ip: str, port: int) -> socket.socket:
    # Note that the server only serves one client at a time
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.bind((ip, port))
    server.listen(5)
    return server


def key_exchange(client: socket.socket,
                initial_packet: bytes,
                encryptor_class: Type[lib.EncryptionMethod],
                p: int,
                a: int) -> lib.EncryptionMethod:
    client.send(initial_packet.encode('utf8'))

    receive_packet = client.recv(1024).decode('utf8')
    receive_packet_dict = json.loads(receive_packet)

    B = receive_packet_dict['B']
    nonce_or_iv = base64.b64decode(receive_packet_dict['nonce-or-iv'].encode('utf8'))

    K = B ** a % p

    return encryptor_class(K.to_bytes(4, 'big'), nonce_or_iv)


def save_msg(msg: str, path: str):
    with open(path, 'w') as f:
        f.write(msg)


def handle_client(client: socket.socket, initial_packet: bytes, p: int, a: int) -> None:
    client.settimeout(1)
    encryptor = lib.NoEncryption()
    try:
        while True:
            raw_msg = client.recv(BUFFER_SIZE)
            if len(raw_msg) == 0:
                raise Exception("Client disconnected unexpectedly")

            flag = int(raw_msg[0])
            if flag == lib.MessageFlags.KE:
                encryptor_class = lib.ENCRYPTION_METHOD_RESOLVER[int(raw_msg[2])]
                encryptor = key_exchange(client, initial_packet, encryptor_class, p, a)
            elif flag == lib.MessageFlags.OP:
                decrypted_json = encryptor.decrypt(raw_msg[1:])
                msg = json.loads(decrypted_json)['msg']
                save_msg(msg, PATH_TO_SAVE)
            elif flag == lib.MessageFlags.EX:
                print("Client handled successfully")
                client.close()
                break
            else:
                raise Exception(f"Message Flag {flag} cannot be interpreted")
    except Exception as e:
        print("Stopping client connection. Cause:", e)
        client.close()


def main() -> NoReturn:
    print("Calculating key exchange parameters")
    p, a, g, A = prepare_key_exchange()
    print("p={}, a={}, g={}, A={}".format(p, a, g, A))

    initial_packet = create_initial_packet(p, g, A)

    server = prepare_server("127.0.0.1", PORT)
    print(f"Server listening on 127.0.0.1:{PORT}")

    while True:
        (client, address) = server.accept()
        print(f"New client connected ({address})")
        handle_client(client, initial_packet, p, a)


if __name__ == '__main__':
    main()
