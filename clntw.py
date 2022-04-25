import socket
from time import sleep

host = "127.0.0.1"
port = 54321
server_addr = (host, port)

with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
    sock.setblocking(False)
    sock.connect_ex(server_addr)

    sock.sendall(b'REQ')
    recv_data = sock.recv(14)
    roll_T = recv_data[:10]
    key_block_num = recv_data[10:]
    while True:
        recv_data = sock.recv()