from random import randrange

class ServiceNotFoundError(RuntimeError):
    def __init__(self, *args):
        self.args = args


class Directory:
    """A directory service."""
    def __init__(self):
        self._services = {}

    def register(self, name, service):
        """Registers a new service, and returns its unique name."""
        if name in self._services:
            newname = name
            while newname in self._services:
                newname = name + str(randrange(2 ** 64))
            name = newname
        self._services[name] = service
        return name

    def lookup_by_name(self, name):
        """Looks up a service given its name. Raises an error if it is not
        found.
        """
        if name in self._services:
            return self._services[name]
        raise ServiceNotFoundError("service of name %s not registered" % name)

    def lookup_by_requirement(self, requirements):
        """Takes a predicate and returns a service which satisfies that
        predicate.
        """
        for name, service in self._services.items():
            if requirements(service):
                return name, service
        raise ServiceNotFoundError(
            "no service found matching specified requirements")


def require_method(method_name):
    """Generate a predicate for requiring a method with a particular name."""
    return lambda instance: callable(getattr(instance, method_name, None))
