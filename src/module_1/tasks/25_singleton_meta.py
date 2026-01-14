class SingletonMeta(type):
    _instances = {}

    def __call__(cls, *args, **kwargs):
        if cls not in cls._instances:
            cls._instances[cls] = super().__call__(*args, **kwargs)
        return cls._instances[cls]


class DB(metaclass=SingletonMeta):
    pass


if __name__ == "__main__":
    db1 = DB()
    db2 = DB()
    assert db1 is db2
