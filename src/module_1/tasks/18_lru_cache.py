from collections import OrderedDict
from functools import wraps
from typing import Callable, Any, Tuple, Mapping, Optional
import unittest.mock

KeyType = Tuple[Any, ...]

def make_key(args: Tuple[Any, ...], kwargs: Mapping[str, Any]) -> KeyType:
    if not kwargs:
        return args
    return args + tuple(sorted(kwargs.items()))

def lru_cache(func: Optional[Callable] = None, *, maxsize: int = 128):
    if not isinstance(maxsize, int) or maxsize < 0:
        raise TypeError("'maxsize' must be a non-negative int")

    def decorator(f: Callable):
        cache: "OrderedDict[KeyType, Any]" = OrderedDict()

        @wraps(f)
        def wrapper(*args: Any, **kwargs: Any) -> Any:
            if not maxsize: return f(*args, **kwargs)
            
            key = make_key(args, kwargs)

            if key in cache:
                cache.move_to_end(key)
                return cache[key]
            
            result = f(*args, **kwargs)
            cache[key] = result
            cache.move_to_end(key)

            if len(cache) > maxsize:
                cache.popitem(last=False)

            return result

        return wrapper

    return decorator(func) if func is not None else decorator


@lru_cache
def sum_(a: int, b: int) -> int:
    return a + b

@lru_cache
def sum_many(a: int, b: int, *, c: int, d: int) -> int:
    return a + b + c + d

@lru_cache(maxsize=3)
def multiply(a: int, b: int) -> int:
    return a * b


if __name__ == "__main__":
    assert sum_(1, 2) == 3
    assert sum_(3, 4) == 7

    assert multiply(1, 2) == 2
    assert multiply(3, 4) == 12

    assert sum_many(1, 2, c=3, d=4) == 10

    mocked_func = unittest.mock.Mock()
    mocked_func.side_effect = [1, 2, 3, 4]
    decorated = lru_cache(maxsize=2)(mocked_func)
    assert decorated(1, 2) == 1
    assert decorated(1, 2) == 1
    assert decorated(3, 4) == 2
    assert decorated(3, 4) == 2
    assert decorated(5, 6) == 3
    assert decorated(5, 6) == 3
    assert decorated(1, 2) == 4
    assert mocked_func.call_count == 4

    mocked = unittest.mock.Mock()
    mocked.side_effect = [10, 20, 30, 40]
    dec = lru_cache(maxsize=2)(mocked)

    assert dec(1) == 10
    assert dec(2) == 20
    assert dec(1) == 10
    assert dec(3) == 30
    assert dec(1) == 10
    assert dec(2) == 40
    assert mocked.call_count == 4
