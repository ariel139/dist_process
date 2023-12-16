__author__ = 'Yossi'
import win32event
import time,random

MUTEX_ALL_ACCESS = 0x1F0001
SEMAPHORE_ALL_ACCESS = 0x1F0003
SEMAPHORE_MODIFY_STATE = 0x0002
SYNCHRONIZE = 0x00100000L

MAX_USER_READ = 2
MAX_USER_WRITE = 1
INFINITE = 0xffffffff



SEMAPHORE_NAME = "Semaphore_2"
MUTEX_NAME = "Mutex_1"


def main():


    try:
        update_readers_count_lock = win32event.OpenMutex(MUTEX_ALL_ACCESS,False,MUTEX_NAME)
        print MUTEX_NAME, "Opened"
    except:

        update_readers_count_lock = win32event.CreateMutex(None, False, MUTEX_NAME)
        print MUTEX_NAME, "Created"


    try:
        write_db_semaphore = win32event.OpenSemaphore(SEMAPHORE_ALL_ACCESS,True,SEMAPHORE_NAME)
        print "\n" +  SEMAPHORE_NAME, " Opened"
    except:
        #if not self.update_readers_count_lock:
        write_db_semaphore = win32event.CreateSemaphore(None, MAX_USER_READ,MAX_USER_READ, SEMAPHORE_NAME)
        print "\n" + SEMAPHORE_NAME, " Created"



    print "\nBefore Critical"
    # try gain the write access
    win32event.WaitForSingleObject(update_readers_count_lock,INFINITE)
    print "\nIn Critical A\n"

    # Critical Section
    i = random.randint(3,10)
    print "\nA Now will sleep in critical A %d seconds\n" %i
    while i:
        time.sleep(1)
        print".",
        i -= 1

    win32event.ReleaseMutex(update_readers_count_lock)
    print "\nOut of n Critical A\n"



    # ------------------------------------------------------


    print "\nBefore Critical B\n"
    # try gain the write access
    win32event.WaitForSingleObject(write_db_semaphore,INFINITE)
    print "\nIn Critical B\n"

    # Critical Section
    i = random.randint(3,10)
    print "\nB Now will sleep in critical B %d seconds\n" %i
    while i:
        time.sleep(1)
        print"#",
        i -= 1

    win32event.ReleaseSemaphore(write_db_semaphore, 1)
    print "\nOut of n Critical B\n"




if __name__ == '__main__':
    from sys import argv

    main()
