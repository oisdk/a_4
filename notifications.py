from collections import defaultdict
import time
import threading

class DuplicateClientNameError(RuntimeError):
    def __init__(self, *args):
        self.args = args


class NotificationManager:
    def __init__(self, directory):
        self._clients = defaultdict(dict)
        self._topics = set()
        self._name = directory.register("notification_manager", self)
        self._cllock = threading.Lock()
        self._tplock = threading.Lock()

    def register_publisher(self, topic):
        with self._tplock:
            self._topics.add(topic)

        def publish(event):
            with self._cllock:
                for callback in self._clients[topic].values():
                    callback(event)

        return publish

    def subscribe(self, clientname, callback, *topics):
        with self._cllock:
            for topic in topics:
                if clientname in self._clients[topic]:
                    raise DuplicateClientNameError(clientname)
                self._clients[topic][clientname] = callback

    def unsubscribe(self, clientname, *topics):
        with self._cllock:
            for topic in topics:
                del self._clients[topic][clientname]


class Event:
    def __init__(self, time, topic, contents):
        self.time = time
        self.topic = topic
        self.contents = contents

    def __str__(self):
        return "New event\nTopic: %s\nTime: %s\n%s" % (
            self.topic, time.strftime("%c", self.time), self.contents)
