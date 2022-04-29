import socket
import selectors
from time import time
import types

sel = selectors.DefaultSelector()

def accept_wrapper(sock, ind):
    conn, addr = sock.accept()
    name = f"[Client-{ind+1}]"
    print(f"Accepted connection from {name} : {addr}")
    conn.setblocking(False)
    events = selectors.EVENT_READ | selectors.EVENT_WRITE
    data = types.SimpleNamespace(name=name, addr=addr)
    sel.register(conn, events, data=data)
    return 1

def service_connection(key, mask, sent_blocks, file):
    sock = key.fileobj
    data = key.data
    if mask & selectors.EVENT_READ:
        recv_data = sock.recv(35)
        if recv_data[:3] == b'REQ':
            send_data = roll_T + str(sent_blocks).zfill(4).encode()
            sock.sendall(send_data)
            print(f"Data sent for REQ to {data.name}")
            return 1

        if recv_data[:3] == b'SCS':
            write_data = str(key_counter) + ". " + data.name + recv_data[3:].decode() + "\n"
            file.write(write_data)
            return 4
        
        if recv_data[:3] == b'NXT':
            if sent_blocks < num_blocks:
                send_data = str(sent_blocks).zfill(4).encode()
                sock.sendall(send_data)
                print(f"Data sent for NXT to {data.name}")
                return 2
            else:
                sock.sendall(b'END')
                print(f"Closing socket {data.name}")
                sel.unregister(sock)
                sock.close()
                return 3

host = "127.0.0.1"
port = 54321
num_clients = 2
num_blocks = 5
roll_T = b"0421312015"

try:
    lsock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    lsock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    lsock.bind((host, port))
    lsock.listen()
    print("Server started...")
    lsock.setblocking(False)
    sel.register(lsock, selectors.EVENT_READ, data=None)

    client_count = 0
    while client_count < num_clients:
        events = sel.select()
        for key, mask in events:
            if key.data is None:
                ret_val = accept_wrapper(key.fileobj, client_count)
                client_count += ret_val
    print(f"{num_clients} clients have connected. Starting operation...")

    recv_blocks = 0
    sent_blocks = 0
    key_counter = 1
    file = open("/media/yasirl/Data/Programming/MICT/ICT6544_DS_HAM/sockFinal/results.txt", "a")
    write_data = "Number of Clients = " + str(client_count) + "\n"
    file.write(write_data)
    start_time = time()

    while recv_blocks < num_blocks:
        events = sel.select()
        for key, mask in events:
            ret_val = service_connection(key, mask, sent_blocks, file)
            if ret_val == 1:
                sent_blocks += 1
            elif ret_val == 2:
                sent_blocks += 1
                recv_blocks += 1
            elif ret_val == 3:
                recv_blocks += 1
            elif ret_val == 4:
                key_counter += 1
    end_time = time()
    run_time = end_time - start_time
    file.write("Time = " + str(run_time) + "\n")
    print("Operation complete.")

except KeyboardInterrupt:
    print("Keyboard interrupt detected")
finally:
    file.close()
    sel.close()
    lsock.close()