import directory
import notifications
import time


class DuplicateKeyError(RuntimeError):
    def __init__(self, *args):
        self.args = args


class StorageKilledError(RuntimeError):
    def __init__(self, *args):
        self.args = args


class Storage:
    """A service for key-value storage. Any errors are published on its status
    topic.
    """
    def __init__(self, d):
        self._name = d.register("storage", self)
        self._pub_callback = d.lookup_by_requirement(
            directory.require_method("register_publisher"))[
                1].register_publisher("storage_status")
        self._store = {}

    def store(self, key, value):
        """Store a value for the given key. Errors are sent via the notification
        manager.
        """
        if key in self._store:
            self._pub_callback(
                notifications.Event("storage_status", DuplicateKeyError(key)))
        else:
            self._store[key] = value

    def retrieve(self, key):
        """Retrieve a value for a given key. Errors are sent via the
        notification manager.
        """
        try:
            return self._store[key]
        except KeyError as k:
            self._pub_callback(notifications.Event("storage_status", k))

    def modify(self, key, fn):
        """Modify a value at a given key. Errors are sent via the notification
        manager.
        """
        try:
            self._store[key] = fn(self._store[key])
        except KeyError as k:
            self._pub_callback(notifications.Event("storage_status", k))

    def kill(self):
        """Kill the service. A killed notification is sent via the notification
        manager.
        """
        del self._store
        self._pub_callback(
            notifications.Event("storage_status", StorageKilledError("storage killed")))
