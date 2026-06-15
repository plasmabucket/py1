import random
from typing import Any


def count_entries(lst: list[Any], threshold: int) -> list[Any]:
    # Ведём подсчёт повторов значений.
    dictionary: dict[Any, int] = {}
    for entry in lst:
        if dictionary.get(entry) != None:
            dictionary[entry] += 1
        else:
            dictionary[entry] = 1
    # Выводим в результат значения с нужным количеством повторов.
    result: list[Any] = []
    for key in dictionary.keys():
        if dictionary[key] >= threshold:
            result.append(key)
    return result


# Пример использования.
# Составляем список из 100 элементов с повторами значений.
list_of_numbers: list[int] = []
for i in range(100):
    list_of_numbers.append(random.randint(1, 10))
# Выводим значения, повторяющиеся больше 10 раз.
entry_count: list[int] = count_entries(list_of_numbers, 10)
print(sorted(entry_count))
