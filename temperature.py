import random
import threading
import time

import directory
import notifications


class Temperature(threading.Thread):
    """A class for temperature readings, which sends out the temperature via
    the notification manager.
    """
    def __init__(self, d, timeout):
        self._pub_callback = d.lookup_by_requirement(
            directory.require_method("register_publisher"))[
                1].register_publisher("temperature")
        threading.Thread.__init__(self)
        self._timeout = timeout

    def run(self):
        temp = random.randrange(100) - 50
        while True:
            newtemp = random.randrange(100) - 50
            if abs(temp - newtemp) > 5:
                self._pub_callback(
                    notifications.Event("temperature",
                                        "the temperature is %i℃" % newtemp))
            temp = newtemp
            time.sleep(self._timeout)
