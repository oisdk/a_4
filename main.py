import threading
import time
import temperature
import directory
import notifications
import storage

d = directory.Directory()
m = notifications.NotificationManager(d)
t = temperature.Temperature(d, 1)
t.start()
s = storage.Storage(d)


class Client:
    """A basic client which stores temperature readings."""
    def __init__(self, d):
        self._notif_manager = d.lookup_by_requirement(directory.require_method("subscribe"))[1]
        self._notif_manager.subscribe("client", self.handle_event, "storage_status", "temperature")
        self._storage = d.lookup_by_requirement(directory.require_method("store"))[1]
        self._storage.store("temperatures", {})
        self._continue = True

    def handle_event(self, event):
        if event.topic == "temperature":
            threading.Thread(target=self.log_temperature, args=(event,)).start()
        elif event.topic == "storage_status":
            threading.Thread(target=self.handle_storage_error, args=(event,)).start()

    def log_temperature(self, event):
        if self._continue:
            def assgn(d):
                d[time.strftime("%c", event.time)] = event.contents
                return d
            self._storage.modify("temperatures", assgn)
        if self._continue:
            print(self._storage.retrieve("temperatures"))

    def handle_storage_error(self, event):
        self._continue = False
        print(event)
        self._notif_manager.unsubscribe("client", "temperature", "storage_status")


c = Client(d)
time.sleep(5)
s.kill()
