from hashlib import md5
import socket
import numpy as np

def md5_calc(val):
    return md5(val).hexdigest()

host = "127.0.0.1"
port = 54321
server_addr = (host, port)
total_key_bits = 32
block_addr_bits = 10
block_key_bits = total_key_bits - block_addr_bits
block_size = 2**block_key_bits
max_key_digits = len(str(2**total_key_bits))
success_resp = b'SCS'
request_resp = b'REQ'
next_resp = b'NXT'

with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
    sock.connect_ex(server_addr)

    print("Sending REQ")
    sock.sendall(request_resp)

    recv_data = sock.recv(14)
    roll_T = recv_data[:10].decode()
    key_block_num = int(recv_data[10:])
    match_string_S = "00" + roll_T[-3:]

    while True:
        start_val = key_block_num * block_size 
        end_val = (key_block_num + 1) * block_size
        nonce_array = np.arange(start_val, end_val)
        nonce_array = nonce_array.astype(str)
        nonce_array = np.char.zfill(nonce_array, max_key_digits)

        v_array = np.char.add(roll_T, nonce_array)

        v_array = np.char.encode(v_array)
        vectorized_md5_calc = np.vectorize(md5_calc)
        hash_array = vectorized_md5_calc(v_array)

        hash_array_5dig = hash_array.astype('U5')
        matched_pos_mask = np.char.equal(match_string_S, hash_array_5dig)

        result_hash_array = hash_array[matched_pos_mask]

        result_hash_array = np.char.encode(result_hash_array)
        response_hash_packets = np.char.add(success_resp, result_hash_array)

        for pkt in response_hash_packets:
            sock.sendall(pkt)


        # for nonce in np.arange(start_val, end_val):
        #     V = roll_T + str(nonce).zfill(key_space)
        #     M = md5(V.encode()).hexdigest()
        #     if M[:5] == match_string_S:
        #         print(M)
        #         send_data = ("SCS" + M).encode()
        #         sock.sendall(send_data)

        print("Sending NXT")
        sock.sendall(b'NXT')
        recv_data = sock.recv(4)
        if recv_data == b"END":
            print("END packet received. Ending.")
            break
        # recv_data = int(recv_data)
        key_block_num = int(recv_data)

print("Operation ended.")
