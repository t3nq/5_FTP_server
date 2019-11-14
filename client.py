import socket
import os

port = 1234
host = '25.49.254.121'

while True:
    request = input('\n> ')
    sock = socket.socket()
    sock.connect((host, port))
    if request.split()[0] == 'toServer':
        filename = request.split()[1]
        size = int(os.path.getsize(filename) / 1024) + 1 if os.path.getsize(filename) % 1024 != 0 else os.path.getsize(filename) / 1024
        sock.send((request + ' ' + str(size)).encode())
        with open(filename, 'rb') as f:
            toSendFile = f.read()
        sock.send(toSendFile)
    else:
        sock.send(request.encode())
    response = sock.recv(1024).decode()
    print(response)
    sock.close()
