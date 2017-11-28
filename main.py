import queue
import threading
import time
import random

def fib(n):
    if n == 0:
        return 0
    elif n == 1:
        return 1
    else:
        return fib(n-1) + fib(n-2)

class Worker(threading.Thread):
    def __init__(self, queue, number):
        self._number = number
        self._queue = queue
        threading.Thread.__init__(self)

    def run(self):
        while True:
            val = self._queue.pop()
            if val is None:
                break
            print("Worker %i received message %i" % (self._number, val))
            print("Worker %i calculated fib for %i: %i" % (self._number, val, fib(val)))

q = queue.Queue()
for i in range(10):
    q.push(random.randrange(35))

w1 = Worker(q, 1)
w2 = Worker(q, 2)
w3 = Worker(q, 3)
w1.start()
w2.start()
w3.start()
