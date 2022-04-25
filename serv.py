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

def service_connection(key, mask):
    sock = key.fileobj
    data = key.data
    # print(data)
    if mask & selectors.EVENT_READ:
        recv_data = sock.recv(35)
        # print(recv_data)
        if recv_data[:3] == b'REQ':
            print("yes")

        # if not recv_data:
        #     print(f"Disconnecting {data.name}")
        #     sel.unregister(sock)
        #     sock.close()

host = "127.0.0.1"
port = 54321
lsock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
lsock.bind((host, port))
lsock.listen()
print("Server started...")
lsock.setblocking(False)
sel.register(lsock, selectors.EVENT_READ, data=None)

num_clients = 2
roll_T = "0421312015"
num_blocks = 5


try:
    i = 0
    while i<num_clients:
        # print(sel.get_map())
        events = sel.select()
        # print(i)
        for key, mask in events:
            # print(key)
            if key.data is None:
                ret_val = accept_wrapper(key.fileobj, i)
                i += ret_val
        # print(sel.get_map())
    print(f"{num_clients} clients have connected. Starting operation...")

    recv_blocks = 0
    sent_blocks = 0
    client_count = 0
    while recv_blocks < num_blocks:
        events = sel.select()
        # print(events)
        for key, mask in events:
            # print(key)
            ret_val = service_connection(key, mask)

except KeyboardInterrupt:
    print("Keyboard interrupt detected")
finally:
    sel.close()