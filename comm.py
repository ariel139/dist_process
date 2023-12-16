import socket

RECV_SIZE = 1024
DEBUG = True

def send(soc: socket.socket, data):

    if type(data) == str:
        data = data.encode()
    data += b'#'
    soc.send(data)
    if DEBUG: print(f'SENT: {data}')


def recive(soc: socket.socket):
    data = soc.recv(RECV_SIZE)
    # disconnected
    if data == b"":
        return b""
    while data[-1] != 35:
        data += soc.recv(RECV_SIZE)
    if DEBUG: print(f"RECIVED: {data}")
    return data[:-1]

