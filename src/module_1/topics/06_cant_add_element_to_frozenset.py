try:
    my_set = {1, 2, 3}
    my_set.add(4)
    print("Correct!")
except Exception as e:
    print(e)

try:
    my_frozenset = frozenset([1, 2, 3])
    my_frozenset.add(4)
    print("Correct!")
except Exception as e:
    print(e)
