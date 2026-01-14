from datetime import datetime


class CreatedAt(type):
    def __new__(cls, name, bases, attrs):
        now = datetime.now()
        attrs["created_at"] = now.strftime("%d.%m.%Y %H:%M:%S")
        return super().__new__(cls, name, bases, attrs)


class Base(metaclass=CreatedAt):
    pass


a = Base()

print(a.created_at)
