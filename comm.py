import socket

RECV_SIZE = 1024


def send(soc: socket.socket, data):

    if type(data) == str:
        data = data.encode()
    data += b'#'
    soc.send(data)


def recive(soc: socket.socket):
    data = soc.recv(RECV_SIZE)
    while data[-1] == 35:
        data += soc.recv(RECV_SIZE)

    return data[:-1]

