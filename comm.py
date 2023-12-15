import socket

RECV_SIZE = 1024


def send(soc: socket.socket, data):

    if type(data) == str:
        data = data.encode()
    data += b'#'
    soc.send(data)


def recive(soc: socket.socket):
    data = soc.recv(RECV_SIZE)
    # disconnected
<<<<<<< HEAD
    if data == b"":
        return b""
=======
    if data == b'':
        return b''
>>>>>>> 24e99213344558adc28ea17f59168572fb9a6a8f
    while data[-1] != 35:
        data += soc.recv(RECV_SIZE)

    return data[:-1]

