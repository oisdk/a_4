import queue
import threading
import time
import random


class Server(threading.Thread):
    def __init__(self, number, func):
        self._number = number
        self._queue = queue.Queue()
        self._func = func
        threading.Thread.__init__(self)

    def run(self):
        while True:
            for val, client_queue in iter(self._queue.pop, None):
                print("Worker %i received message %i" % (self._number, val))
                client_queue.push(("%s(%s)" % (self._func.__name__, val), self._func(val)))
            time.sleep(1)

    def __call__(self, client_queue, val):
        self._queue.push((val, client_queue))

def fib(n):
    if n == 0:
        return 0
    elif n == 1:
        return 1
    else:
        return fib(n-1) + fib(n-2)

def is_prime(n):
    if n < 2:
        return False
    for i in range(2, n):
        if n % i == 0:
            return False
    return True

def fact(n):
    res = 1
    for i in range(1, n):
        res *= i
    return res


class Client(threading.Thread):
    def __init__(self, number):
        self._queue = queue.Queue()
        self._number = number
        threading.Thread.__init__(self)

    def run(self):
        while True:
            while not self._queue.empty():
                call, val = self._queue.pop()
                print("client %i: %s = %s" % (self._number, call, val))
            time.sleep(1)

    def __call__(self, server, val):
        server(self._queue, val)


fibs = Server(1, fib)
primes = Server(2, is_prime)
facts = Server(3, fact)

c1 = Client(1)
c2 = Client(2)
c3 = Client(3)

c1.start()
c2.start()
c3.start()

fibs.start()
primes.start()
facts.start()

for _ in range(10):
    random.choice([c1, c2, c3])(random.choice([fibs, primes, facts]), random.randrange(35))
