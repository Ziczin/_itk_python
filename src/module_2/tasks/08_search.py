def search(array: list[int], number: int) -> bool:
    """
    Бинарный поиск
    Сложность O(log n) достигается путём уменьшения области поиска вдвое на каждой итерации
    Сложность получения по индексу O(1), можно пренебречь                             ^
    Выход из цикла гарантирован при пересечении указателей, пересечение гарантировано |
    """

    if not array:
        return False

    r_idx = len(array) - 1
    l_idx = 0

    if number > array[-1] or number < array[0]:
        return False

    if number == array[-1] or number == array[0]:
        return True

    while True:
        idx = l_idx + (r_idx - l_idx) // 2

        if l_idx == r_idx or l_idx == idx:
            return False
        elif array[idx] > number:
            r_idx = idx
        elif array[idx] < number:
            l_idx = idx
        else:
            return True


if __name__ == "__main__":
    data_1 = [1, 2, 3, 45, 356, 569, 600, 705, 923]
    data_2 = list(range(0, 1_000_000, 2))
    data_3 = list(range(0, 10_000_000, 2))

    print("TESTS")
    assert not search([], 0)

    assert search(data_1, 1)
    assert search(data_1, 45)
    assert search(data_1, 923)
    assert not search(data_1, 0)
    assert not search(data_1, 64)
    assert not search(data_1, 1024)

    assert search(data_2, 0)
    assert search(data_2, 751_344)
    assert search(data_2, 999_998)
    assert not search(data_2, -10)
    assert not search(data_2, 65_535)
    assert not search(data_2, 1_000_000)

    assert search(data_3, 0)
    assert search(data_3, 3_751_344)
    assert search(data_3, 9_999_998)

    assert not search(data_3, -100)
    assert not search(data_3, 69)
    assert not search(data_3, 1024**3)
