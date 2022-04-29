# import socket
# from time import sleep

# host = "127.0.0.1"
# port = 54321
# server_addr = (host, port)

# sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
# sock.setblocking(False)
# sock.connect_ex(server_addr)

# sock.close()

# def tfun(a):
#     a += 1
#     return a

# a = 5
# print(a)

# print(tfun(a))
# print(a)

from hashlib import md5


roll_T = "0421312015"
# match_string_S = concat("00", roll_T[-3:])
match_string_S = "00" + roll_T[-3:]
# match_string_S = "00" + roll_T(-3:)
print(match_string_S)
hsh = md5(match_string_S.encode()).hexdigest()
print(hsh[:5])
print(hsh)

b1 = b"123"
b2 = int(b1)
b3 = int(b1.decode())
print(b2)
print(b3)
print(type(b2))
print(type(b3))