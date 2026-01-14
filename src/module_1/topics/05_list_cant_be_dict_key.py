try:
    my_dict = {"name": "Alice", "age": 30, (1, 2): "tuple_key"}
    print("Correct!")
except Exception as e:
    print(e)

try:
    invalid_dict = {["list_key"]: "value"}
    print("Correct!")
except Exception as e:
    print(e)
