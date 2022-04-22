import socket

host = "127.0.0.1"
port = 54321
server_addr = (host, port)

sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
sock.setblocking(False)
sock.connect_ex(server_addr)
sock.close()