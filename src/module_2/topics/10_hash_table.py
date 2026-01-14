class NaiveDict:
    def __init__(self):
        self.table = [None] * 10

    def _hash(self, key):
        """
        Простая хеш-функция для ключа.
        Мы используем встроенную hash() функцию.
        """
        return hash(key) % len(self.table)

    def set(self, key, value):
        """Добавляет пару ключ-значение в словарь."""
        self.table[self._hash(key)] = (key, value)

    def get(self, key):
        """Возвращает значение по ключу, если оно существует."""
        if value := self.table[self._hash(key)][1]:
            return value
        else:
            raise KeyError("key does not exist")


# Пример использования:
naive_dict = NaiveDict()

naive_dict.set("apple", 10)
naive_dict.set("banana", 20)

print(naive_dict.get("apple"))  # 10
print(naive_dict.get("banana"))  # 20
