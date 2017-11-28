Donnacha Oisín Kidney
115702295

# Assignment 6

## 1
Message queues allow servers and clients to interact asynchronously. By separating the logic of asynchronous communication from the implementation of either the clients or the servers, they allow for better separation of concerns, simplifying client and server code. They also allow users to choose different persistence levels for messages, making them easily adaptable to different priorities.

## 2

Same queue code as from last assignment.


The messages from the clients contain a reference to the client queue, as well as a value to request the function with. The response contains a description of the function carried out, as well as the result of calling that function.

New server/client code:

```python
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
```

## 3

Output:

```
Worker 1 received message 6
Worker 3 received message 18
Worker 2 received message 29
Worker 2 received message 12
Worker 1 received message 8
Worker 2 received message 8
Worker 1 received message 23
Worker 1 received message 9
Worker 1 received message 13
Worker 1 received message 26
client 1: fib(6) = 8
client 2: is_prime(29) = True
client 1: fact(18) = 355687428096000
client 2: is_prime(8) = False
client 1: is_prime(12) = False
client 2: fib(23) = 28657
client 1: fib(8) = 21
client 1: fib(9) = 34
client 2: fib(13) = 233
client 1: fib(26) = 121393
```
