def my_decorator(func):
    def wrapper():
        print("До вызова функции")
        func()
        print("После вызова функции")

    return wrapper


@my_decorator
def say_hello():
    print("Привет!")


say_hello()
