def outer():
    x = 5

    def inner():
        nonlocal x
        x = 10

    inner()
    print(x)


outer()
