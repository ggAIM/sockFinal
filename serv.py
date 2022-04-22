import socket
import selectors
import types

sel = selectors.DefaultSelector()

def accept_wrapper(sock, ind):
    conn, addr = sock.accept()
    name = f"Client_{ind+1}"
    print(f"Accepted connection from {name} : {addr}")
    conn.setblocking(False)
    events = selectors.EVENT_READ | selectors.EVENT_WRITE
    data = types.SimpleNamespace(name=name, addr=addr)
    # print(name, data)
    # conn.close()
    sel.register(conn, events, data=data)
    return 1

def service_connection():
    pass

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
num_blocks = 2**10


try:
    i = 0
    while i<num_clients:
        events = sel.select()
        for key, mask in events:
            if key.data is None:
                ret_val = accept_wrapper(key.fileobj, i)
                i += ret_val
    print(f"{num_clients} clients have connected. Starting operation...")


except KeyboardInterrupt:
    print("Keyboard interrupt detected")
finally:
    sel.close()