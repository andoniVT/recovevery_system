'''
Created on 16/11/2014

@author: andoni
'''

import threading 
import time

exitFlag = 0

class myThread(threading.Thread):
    
    def __init__(self, threadID, name, counter):
        threading.Thread.__init__(self)
        self.threadID = threadID
        self.name = name
        self.counter = counter
    
    def run(self):
        print "Starting " + self.name
        print_time(self.name, self.counter, 5)
        print "Exiting " + self.name

def print_time(threadName, delay, counter):
    while counter:
        if exitFlag:
            thread.exit()
        time.sleep(delay)
        print "%s: %s" %(threadName , time.ctime(time.time()))
        counter-=1

def worker(count):
    print "Esta es la prueba %s" %count 
    return

if __name__ == '__main__':
    
    threads = list()
    for i in range(3):
        t = threading.Thread(target=worker , args=(i,))
        threads.append(t)
        t.start()
    
    '''
    thread1 = myThread(1, "Thread-1" , 1)
    thread2 = myThread(2, "Thread-2" , 2)    
    thread1.start()
    thread2.start()    
    print "Exiting Main Thread"
    '''
