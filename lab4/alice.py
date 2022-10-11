import socket
import lib
import json


PORT = 52304
# Ecuaciones de Diffie Hellman
# p, a, g -> A = g ** a % p, K = B ** a % p
# b -> B = g ** b % p, K = A ** b % p


def main():
    p = lib.create_random_prime()
    a = lib.create_random(p)
    g = lib.create_random(p)

    print("Calculating A")
    A = g ** a % p

    print("p={}, a={}, g={}, A={}".format(p, a, g, A))

    initial_packet_dict = {
        'p': p,
        'g': g,
        'A': A
    }
    initial_packet = json.dumps(initial_packet_dict)

    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.bind(("127.0.0.1", PORT))
    server.listen(5)

    print(f"Server listening on 127.0.0.1:{PORT}")

    while True:
        (client, address) = server.accept()
        client.send(initial_packet.encode('utf8'))

        receive_packet = client.recv(1024).decode('utf8')
        receive_packet_dict = json.loads(receive_packet)

        B = receive_packet_dict['B']

        K = B ** a % p
        print("Key:", K)


if __name__ == '__main__':
    main()
