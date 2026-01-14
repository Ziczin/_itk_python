class MyMeta(type):
    def __new__(cls, name, bases, attrs):
        # Модификации класса перед его созданием
        attrs["greeting"] = "Hello"
        return super().__new__(cls, name, bases, attrs)


class MyClass(metaclass=MyMeta):
    pass


print(MyClass.greeting)


class MethodAddingMeta(type):
    def __new__(cls, name, bases, attrs):
        attrs["say_hello"] = lambda self: "Hello from {}".format(
            self.__class__.__name__
        )
        return super().__new__(cls, name, bases, attrs)


class MyClass2(metaclass=MethodAddingMeta):
    pass


obj = MyClass2()
print(obj.say_hello())
