import timeit

print(timeit.timeit("x = [1, 2, 3, 4, 5]", number=1000000))  # ~0.082
print(timeit.timeit("x = (1, 2, 3, 4, 5)", number=1000000))  # ~0.016
