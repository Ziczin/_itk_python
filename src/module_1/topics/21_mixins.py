import json


class JsonSerializableMixin:
    def to_json(self):
        return json.dumps(self.__dict__)


class Person(JsonSerializableMixin):
    def __init__(self, name, age):
        self.name = name
        self.age = age


person = Person("Alice", 30)
print(person.to_json())
