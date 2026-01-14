def first():
    from singleton_module import db

    return db


def second():
    from singleton_module import db

    return db


if __name__ == "__main__":
    a = first()
    b = second()
    assert a is b
