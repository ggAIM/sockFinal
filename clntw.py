from hashlib import md5
import socket

host = "127.0.0.1"
port = 54321
server_addr = (host, port)
total_key_bits = 32
block_addr_bits = 10
block_key_bits = total_key_bits - block_addr_bits
block_size = 2**block_key_bits

with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
    sock.connect_ex(server_addr)

    print("Sending REQ")
    sock.sendall(b'REQ')

    recv_data = sock.recv(14)
    roll_T = recv_data[:10].decode()
    key_block_num = int(recv_data[10:])
    match_string_S = "00" + roll_T[-3:]

    while True:
        start_val = key_block_num * block_size 
        end_val = (key_block_num + 1) * block_size
        for nonce in range(start_val, end_val):
            V = roll_T + str(nonce).zfill(total_key_bits)
            M = md5(V.encode()).hexdigest()
            if M[:5] == match_string_S:
                print(M)
                send_data = ("SCS" + M).encode()
                sock.sendall(send_data)

        print("Sending NXT")
        sock.sendall(b'NXT')
        recv_data = sock.recv(4)
        if recv_data == b"END":
            print("END packet received. Ending.")
            break
        # recv_data = int(recv_data)
        key_block_num = int(recv_data)

print("Operation ended.")
