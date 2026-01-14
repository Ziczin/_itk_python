from datetime import datetime


class CreatedAtMeta(type):
    def __call__(cls, *args, **kwargs):
        instance = super().__call__(*args, **kwargs)
        instance.created_at = datetime.now()
        return instance


class A(metaclass=CreatedAtMeta):
    pass


a = A()
print(a.created_at)
