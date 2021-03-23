import socket

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
host = '10.10.10.204'
port = 8080

s.connect((host,port))
s.send("ack".encode())
s_recv = s.recv(100)
print(s_recv.decode())
