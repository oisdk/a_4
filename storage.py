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
    def __init__(self, d):
        self._name = d.register("storage", self)
        self._pub_callback = d.lookup_by_requirement(
            directory.require_method("register_publisher"))[
                1].register_publisher("storage_status")
        self._store = {}

    def store(self, key, value):
        if key in self._store:
            self._pub_callback(
                notifications.Event(time.gmtime(), "storage_status", DuplicateKeyError(key)))
        else:
            self._store[key] = value

    def retrieve(self, key):
        try:
            return self._store[key]
        except KeyError as k:
            self._pub_callback(notifications.Event(time.gmtime(), "storage_status", k))

    def modify(self, key, fn):
        try:
            self._store[key] = fn(self._store[key])
        except KeyError as k:
            self._pub_callback(notifications.Event(time.gmtime(), "storage_status", k))

    def kill(self):
        self._pub_callback(
            notifications.Event(time.gmtime(), "storage_status", StorageKilledError("storage killed")))
