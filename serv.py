import socket
import selectors
import types

sel = selectors.DefaultSelector()

def accept_wrapper(sock, ind):
    conn, addr = sock.accept()
    name = f"[Client-{ind+1}]"
    print(f"Accepted connection from {name} : {addr}")
    conn.setblocking(False)
    events = selectors.EVENT_READ | selectors.EVENT_WRITE
    data = types.SimpleNamespace(name=name, addr=addr)
    # print(name, data)
    # conn.close()
    sel.register(conn, events, data=data)
    return 1

def service_connection(key, mask, sent_blocks):
    sock = key.fileobj
    data = key.data
    # print(data)
    if mask & selectors.EVENT_READ:
        recv_data = sock.recv(35)
        # print(recv_data)
        if recv_data[:3] == b'REQ':
            # print(recv_data[3:])
            send_data = roll_T + str(sent_blocks).zfill(4).encode()
            sock.sendall(send_data)
            print(f"Data sent for REQ to {data.name}")
            return 1

        if recv_data[:3] == b'SCS':
            write_data = data.name + recv_data[3:].decode()
            print(write_data)
        
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
# lsock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
# lsock.bind((host, port))
# lsock.listen()
# print("Server started...")
# lsock.setblocking(False)
# sel.register(lsock, selectors.EVENT_READ, data=None)

num_clients = 2
roll_T = b"0421312015"
num_blocks = 5


try:
    lsock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    lsock.bind((host, port))
    lsock.listen()
    print("Server started...")
    lsock.setblocking(False)
    sel.register(lsock, selectors.EVENT_READ, data=None)

    client_count = 0
    while client_count < num_clients:
        # print(sel.get_map())
        events = sel.select()
        for key, mask in events:
            # print(key)
            if key.data is None:
                ret_val = accept_wrapper(key.fileobj, client_count)
                client_count += ret_val
        # print(sel.get_map())
    print(f"{num_clients} clients have connected. Starting operation...")

    recv_blocks = 0
    sent_blocks = 0
    while recv_blocks < num_blocks:
        # print(sent_blocks, recv_blocks)
        events = sel.select()
        # print(events)
        for key, mask in events:
            # print(key)
            ret_val = service_connection(key, mask, sent_blocks)
            if ret_val == 1:
                sent_blocks += 1
            elif ret_val == 2:
                sent_blocks += 1
                recv_blocks += 1
            elif ret_val == 3:
                recv_blocks += 1
        # print(sent_blocks, recv_blocks)
    print("Operation complete.")
    sel.close()
    lsock.close()

except KeyboardInterrupt:
    print("Keyboard interrupt detected")
finally:
    sel.close()