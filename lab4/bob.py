import socket
import json
import lib


PORT = 52304


def main():
    client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client.connect(("127.0.0.1", PORT))
    msg = client.recv(1024).decode('utf8')
    packet_dict = json.loads(msg)

    p = packet_dict['p']
    g = packet_dict['g']
    A = packet_dict['A']

    b = lib.create_random(p)
    B = g ** b % p

    send_packet = json.dumps({'B': B})
    client.send(send_packet.encode('utf8'))
    
    K = A ** b % p
    print("Key:", K)


if __name__ == '__main__':
    main()
