import threading as thread
import time

global x                #Shared Data
x = True
lock = thread.Lock()    #Lock for synchronising access

def Reader():
    global x
    while x:
        print('Reader is Reading!')
        lock.acquire()      #Acquire the lock before Reading (mutex approach)
        print('Shared Data:', x)
        lock.release()      #Release the lock after Reading
        print()
        time.sleep(1)

def Writer():
    global x
    print('Writer is Writing!')
    lock.acquire()      #Acquire the lock before Writing
    x = False             #Write on the shared memory
    print('Writer is Releasing the lock!')
    lock.release()      #Release the lock after Writing
    print()

if __name__ == '__main__':
    
        
    Thread1 = thread.Thread(target = Reader)
    Thread1.start()
    time.sleep(5)
    Thread2 = thread.Thread(target = Writer)
    Thread2.start()

Thread1.join()
Thread2.join()