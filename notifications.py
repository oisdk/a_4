import threading
import time
from collections import defaultdict


class DuplicateClientNameError(RuntimeError):
    def __init__(self, *args):
        self.args = args


class NotificationManager:
    """A notification manager. Instances of this class will manage publishers
    and subscribers, and send messages from the former to the latter.
    """

    def __init__(self, directory):
        """Initialize a NotificationManager with the directory service.
        """
        self._clients = defaultdict(dict)
        self._topics = set()
        self._name = directory.register("notification_manager", self)
        self._cllock = threading.Lock()
        self._tplock = threading.Lock()

    def register_publisher(self, topic):
        """This method registers a new publisher on the given topic, and
        returns the callback to send out a new event.
        """
        with self._tplock:
            self._topics.add(topic)

        def publish(event):
            with self._cllock:
                for callback in self._clients[topic].values():
                    callback(event)

        return publish

    def subscribe(self, clientname, callback, *topics):
        """This method takes a client name and callback, and several topics, and
        subscribes that client to those topics. The client name must be unique.
        """
        with self._cllock:
            for topic in topics:
                if clientname in self._clients[topic]:
                    raise DuplicateClientNameError(clientname)
                self._clients[topic][clientname] = callback

    def unsubscribe(self, clientname, *topics):
        """This method unsubscribes the specified client name from the given
        topics.
        """
        with self._cllock:
            for topic in topics:
                del self._clients[topic][clientname]


class Event:
    """An event is what is sent by the notification manager."""

    def __init__(self, topic, contents, time_created=None):
        self.time = time.gmtime() if time_created is None else time_created
        self.topic = topic
        self.contents = contents

    def __str__(self):
        return "New event\nTopic: %s\nTime: %s\n%s" % (
            self.topic, time.strftime("%c", self.time), self.contents)
