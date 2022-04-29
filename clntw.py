from hashlib import md5
import socket

host = "127.0.0.1"
port = 54321
server_addr = (host, port)
key_space = 32
# key_space = 32
block_size = 2**key_space

with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
    # Blocking is enabled 
    # sock.setblocking(False)

    sock.connect_ex(server_addr)

    print("Sending REQ")
    sock.sendall(b'REQ')

    recv_data = sock.recv(14)
    # print(recv_data)
    roll_T = recv_data[:10].decode()
    # key_block_num = int(recv_data[10:].decode())
    key_block_num = int(recv_data[10:])
    # print(roll_T, key_block_num)
    match_string_S = "00" + roll_T[-3:]

    while True:
        print("New loop")
        start_val = key_block_num * block_size 
        end_val = (key_block_num + 1) * block_size
        for nonce in range(start_val, end_val):
            V = roll_T + str(nonce).zfill(key_space)
            M = md5(V.encode()).hexdigest()
            if M[:5] == match_string_S:
                print(M)
                send_data = ("SCS" + M).encode()
                sock.sendall(send_data)

        print("Sending NXT")
        sock.sendall(b'NXT')
        recv_data = sock.recv(4)
        recv_data = int(recv_data)
        print(recv_data)
        if not recv_data:
            print("No data received.")
            break
        key_block_num = recv_data

print("Operation ended.")
