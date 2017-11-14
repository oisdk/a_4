Donnacha Oisín Kidney
115702295

# Assignment 5

## 1
A messaging queue is a first-in first-out queue which allows message producers to asynchronously interact with message consumers, by sending out messages when they are ready, and not waiting for them to be consumed. Message queues are asynchronous, meaning that the time a message is consumed is often not the same time the message is created, and they are non-blocking, meaning a message producer can carry out other work before its last message is consumed.

## 2

queue.py:

```python
import threading

class Queue:
    """A FIFO queue which supports amortized O(1) push and pop."""
    def __init__(self):
        self._front = []
        self._back = []
        # A lock for threadsafe mutation.
        self._lock = threading.Lock()

    def push(self, element):
        """Push an element onto the end of the queue."""
        with self._lock:
            self._back.append(element)

    def pop(self):
        """Pop the next element from the queue."""
        with self._lock:
            if self._front:
                return self._front.pop()
            elif self._back:
                res = self._back[0]
                self._front, self._back = self._back[:0:-1], []
                return res

    def size(self):
        """Return the total number of elements in the queue."""
        with self._lock:
            return len(self._front) + len(self._back)

    def empty(self):
        """Return true iff the queue is empty."""
        with self._lock:
            return not (self._front or self._back)
```

main.py:

```python
import queue

q = queue.Queue()
q.push(1)
q.push(2)
q.push(3)
print(q.size())
print(q.pop())
print(q.pop())
print(q.pop())
print(q.size())
```

output:

```python
3
1
2
3
0
```

## 3

For this task the workers will inefficiently calculate fibonacci numbers from the queue. The locking is managed by the queue structure itself, and the multitasking is handled by the python threading module. The delay is introduced by the time taken to calculate fibonacci numbers.

main.py:

```python
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
```

This is some example output:

```
Worker 1 received message 23
Worker 1 calculated fib for 23: 28657
Worker 1 received message 5
Worker 1 calculated fib for 5: 5
Worker 1 received message 33
Worker 2 received message 4
Worker 2 calculated fib for 4: 3
Worker 2 received message 3
Worker 2 calculated fib for 3: 2
Worker 2 received message 31
Worker 3 received message 12
Worker 3 calculated fib for 12: 144
Worker 3 received message 33
Worker 2 calculated fib for 31: 1346269
Worker 2 received message 27
Worker 2 calculated fib for 27: 196418
Worker 2 received message 30
Worker 2 calculated fib for 30: 832040
Worker 3 calculated fib for 33: 3524578
Worker 1 calculated fib for 33: 3524578
```

As can be seen on the fifth line (`Worker 1 received message 33`), the first worker takes some time to calculate the expensive call to `fib`. In the meantime, the second and third workers can calculate cheaper calls, without blocking the execution of the first call.
