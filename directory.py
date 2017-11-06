from random import randrange

class ServiceNotFoundError(RuntimeError):
    def __init__(self, *args):
        self.args = args


class Directory:
    def __init__(self):
        self._services = {}

    def register(self, name, service):
        if name in self._services:
            newname = name
            while newname in self._services:
                newname = name + str(randrange(2 ** 64))
            name = newname
        self._services[name] = service
        return name

    def lookup_by_name(self, name):
        if name in self._services:
            return self._services[name]
        raise ServiceNotFoundError("service of name %s not registered" % name)

    def lookup_by_requirement(self, requirements):
        for name, service in self._services.items():
            if requirements(service):
                return name, service
        raise ServiceNotFoundError(
            "no service found matching specified requirements")


def require_method(method_name):
    return lambda instance: callable(getattr(instance, method_name, None))
