class RegistryMeta(type):
    registry = {}

    def __new__(meta, name, bases, attrs):
        if name != "Handler":
            if "name" not in attrs:
                raise AttributeError("Class did not contains attribute 'name'")

            if not attrs["name"]:
                raise ValueError("Class name is empty")

            if attrs["name"] in meta.registry:
                raise ValueError("Class with this name already exists (duplicate name)")
            cls = super().__new__(meta, name, bases, attrs)
            meta.registry[attrs["name"]] = cls
            return cls

        attrs["get_by_name"] = lambda name: meta.registry[name]
        return super().__new__(meta, name, bases, attrs)


class Handler(metaclass=RegistryMeta):
    pass


class EmailHandler(Handler):
    name = "email"

    def handle(self, message):
        return f"Email: {message}"


class SMSHandler(Handler):
    name = "sms"

    def handle(self, message):
        return f"SMS: {message}"


handler = Handler.get_by_name("email")()
print(handler.handle("Hello"))

try:

    class DuplicateHandler(Handler):
        name = "email"

except Exception as e:
    print(e)


try:

    class EmptyNameHandler(Handler):
        name = ""

except Exception as e:
    print(e)

try:

    class NoNameHandler(Handler):
        pass

except Exception as e:
    print(e)
