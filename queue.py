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

