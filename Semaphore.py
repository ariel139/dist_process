import win32event
import win32security
import win32


class Semaphore:
    def __init__(self, semaphore_name: str, initial_value: int, maximum_value: int, semaphore_attributes=None ):
        if semaphore_attributes is not None:
            if not isinstance(semaphore_attributes, win32security.PyCredHandleType):
                raise Exception('Unsupported type of security attributes')
        self.semaphore_handle = win32event.CreateSemaphore(semaphore_attributes, initial_value,maximum_value, semaphore_name)

    @classmethod
    def open_semaphore(cls, semaphore_name: str, desired_access=win32event.EVENT_ALL_ACCESS, inherit_flag=True):
        cls.semaphore = win32event.OpenSemaphore(desired_access, inherit_flag, semaphore_name)

    def acquire(self, maximum_waiting=win32event.INFINITE):
        response = win32event.WaitForSingleObject(self.semaphore_handle,maximum_waiting)
        if response != win32event.WAIT_OBJECT_0:
            raise Exception(f'Error in semaphore acquiring: {response}')

    def release(self, semaphore_handle=None, release_amount=1):
        if semaphore_handle is None:
            semaphore_handle = self.semaphore_handle
        else:
            if type(semaphore_handle) != int:
                raise Exception('The semaphore handle type is not correct')
        if release_amount != 1:
            print('WARNING: a none 1 release amount can cause problems')

        win32event.CreateSemaphore(semaphore_handle, release_amount)






