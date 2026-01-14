try:
    my_dict = {}
    my_list = [1, 2, 3]
    my_dict[my_list] = "value"
    print("Correct!")
except Exception as e:
    print(e)

try:
    my_dict = {}
    my_tuple = (1, 2, 3)
    my_dict[my_tuple] = "value"
    print("Correct!")
except Exception as e:
    print(e)


class Some:
    def __init__(self):
        self.publ = "publ"
        self._prot = "prot"
        self.__priv = "priv"


try:
    my_dict = {}
    my_obj = Some()
    my_dict[my_obj] = "value"
    print("Correct!")
except Exception as e:
    print(e)
