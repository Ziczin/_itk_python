def repeat(times):
    def decorator(func):
        def wrapper(*args, **kwargs):
            for _ in range(times):
                func(*args, **kwargs)

        return wrapper

    return decorator


@repeat(3)
def say_hello():
    print("Привет!")


@repeat(5)
def say_hello2():
    print("Привет 2!")


say_hello()
say_hello2()
