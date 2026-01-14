print("Immutable obj copy:")
a = (1, 2, 3)
b = a
print("- a is b:", a is b)


def copy_func():
    import copy

    print("Copy:")

    list1 = [1, 2, [3, 4]]
    list2 = copy.copy(list1)
    list2[2].append(5)

    print("- Orig: ", list1)
    print("- Copy: ", list2)


def deepcopy_func():
    import copy

    print("Deep copy:")

    list1 = [1, 2, [3, 4]]
    list2 = copy.deepcopy(list1)
    list2[2].append(5)

    print("- Orig: ", list1)
    print("- Copy: ", list2)


copy_func()
deepcopy_func()
