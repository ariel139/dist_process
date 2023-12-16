
print(f'try {__name__}')
import socket
from Semaphore import Semaphore
from multiprocessing import Process
import concurrent.futures
from comm import send, recive
from atexit import register
from threading import Thread

sem = Semaphore("shot semaphore", 1, 4)
TO_FIND = 'EC9C0F7EDCC18A98B1F31853B1813301'
# TO_FIND = '8155bc545f84d9652f1012ef2bdfb6eb'.upper()
SERVER_IP = '10.100.102.19'
SERVER_PORT = 2828
RUNNIG = True
RATION = 100000000
shot = 0

def client_process(client_soc):
    global RUNNIG, shot
    while RUNNIG: 
        send(client_soc, f"SR~{shot}~{RATION}~{TO_FIND}".encode())
        add_to_shot()
        client_soc.settimeout(5)
        res = recive(client_soc).decode()
        print(res)
        if res == "":
            print('client dissconnected')
            return
        res = res.split('~')
        if res[0] == 'AK':
            while True:
                try:
                    res = recive(client_soc).decode()
                    break
                except socket.error:
                    continue
        if res[0] == 'CN':
            add_to_shot()
        if res[0] == 'FN':
            print(f'found {res[1]}')
            RUNNIG = False



def add_to_shot():
    global shot
    sem.acquire()
    shot += RATION
    sem.release()




def main():
    register(sem.delete)
    server_socket = socket.socket()
    server_socket.bind((SERVER_IP,SERVER_PORT))
    print('server running...')
    process = []
    while RUNNIG:
        server_socket.listen(5)
        client_soc, addr = server_socket.accept()
        print(f'new client from {addr} connected')
        prc = Thread(target=client_process, args = (client_soc,))
        prc.start()
        # client_prc = Process(target=client_process, args= (client_soc,))
        # client_prc.start()
        process.append(prc)
    for prc in process:
        prc.join()



if __name__ == "__main__":
    main()