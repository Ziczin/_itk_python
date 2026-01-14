def append_to_list(value, my_list=[]):
    my_list.append(value)
    return my_list


res1 = append_to_list(1)
print(res1)

res2 = append_to_list(2)
print(res2)


def append_to_list2(value, my_list=None):
    my_list = my_list or []

    my_list.append(value)
    return my_list


res3 = append_to_list2(1)
print(res3)

res4 = append_to_list2(2)
print(res4)
