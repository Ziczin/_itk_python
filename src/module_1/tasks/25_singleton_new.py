class SingletonDB:
    def __new__(cls, *args, **kwargs):
        if not hasattr(cls, "instance"):
            cls.instance = super().__new__(cls, *args, **kwargs)
        return cls.instance


if __name__ == "__main__":
    db1 = SingletonDB()
    db2 = SingletonDB()
    assert db1 is db2
