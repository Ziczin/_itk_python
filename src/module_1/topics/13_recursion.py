def factorial(n):
    if n == 1:
        return 1
    else:
        return n * factorial(n - 1)


try:
    print(factorial(5))
except Exception as e:
    print(e)

try:
    print(factorial(1000))
except Exception as e:
    print(e)
