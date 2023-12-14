import socket
from hashlib import md5
from comm import send, recive
# TO_FIND = 'EC9C0F7EDCC18A98B1F31853B1813301'
TO_FIND = 'd3d9446802a44259755d38e6d163e820'.upper()

def get_info(info):
    data = info.decode()[:-1].split('~')
    return int(data[1]), int(data[2])

def procces_info(shot, ration):
    for i in range(ration):
        to_hash = str(int(shot)+i).encode()
        res= md5(to_hash).hexdigest().upper()
        if res == TO_FIND:
            return True, to_hash
    return False, -1

def communicate(soc):
    data = recive(soc)
    while data != 'ST#'.encode():
        shot, ration = get_info(data)
        send(soc, b'AK')
        worked, res = procces_info(shot,ration)
        if worked:
            send_back = f"FN~{int(res)}"
            send(soc, send_back)
            soc.close()
            break
        else:
            send(soc, b"CN")
        data = recive(soc)
def main(ip,port):
    client_socket = socket.socket()
    client_socket.connect((ip,port))
    communicate(client_socket)




if __name__ == "__main__":
    main('10.100.102.19',2828)