import socket
from threading import Semaphore
from multiprocessing import Process
from comm import send, recive
sem = Semaphore()
TO_FIND = 'EC9C0F7EDCC18A98B1F31853B1813301'
TO_FIND = '8155bc545f84d9652f1012ef2bdfb6eb'.upper()
SERVER_IP = '10.100.102.19'
SERVER_PORT = 2828
RUNNIG = True
RATION = 100000
shot = 0

def client_process(client_soc):
    global RUNNIG, shot
    while RUNNIG: 
        send(client_soc, f"SR~{shot}~{RATION}~{TO_FIND}".encode())
        shot+=RATION
        ack = recive(client_soc).decode()
        if ack == 'AK':
            client_soc.settimeout(5)
            while True:
                try: 
                    res = recive(client_soc).decode()
                    res = res.split('~')
                    if res[0] == 'FN':
                        print(f'found {res[1]}')
                        RUNNIG = False
                        break
                    if res == "":
                        raise Exception("Client error")
                    else:
                        sem.acquire()
                        shot += RATION
                        sem.release()
                        break
                except socket.error:
                    continue


    


def main():
    server_socket = socket.socket()
    server_socket.bind((SERVER_IP,SERVER_PORT))
    print('server running...')
    process = []
    while RUNNIG:
        server_socket.listen(5)
        client_soc, addr = server_socket.accept()
        print(f'new client from {addr} connected')
        client_prc = Process(target=client_process, args= (client_soc,))
        client_prc.start()
        process.append(client_prc)
    for prc in process:
        prc.join()



if __name__ == "__main__":
    main()