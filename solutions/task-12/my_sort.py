from typing import List


# Функция сортировки списка
def list_sort(lst: List[int]) -> List[int]:
    lst_len: int = len(lst)
    # Проверка на пустой массив
    if lst_len == 0:
        return []
    # Поиск максимума и минимума
    for i in range(lst_len):
        if i == 0:
            min_value: int = lst[0]
            max_value: int = lst[0]
        elif lst[i] < min_value:
            min_value = lst[i]
        elif lst[i] > max_value:
            max_value = lst[i]
    # Массив для размещения отсортированных элементов
    list_copy: List[int] = []
    # Максимальное значение отсортированных элементов
    max_sorted: int = min_value - 1  # Изначально, все элементы несортированные
    while max_sorted < max_value:
        # Поиск минимального неучтённого элемента
        min_unsorted: int = max_value
        for i in range(lst_len):
            if lst[i] < min_unsorted and lst[i] > max_sorted:
                min_unsorted = lst[i]
        # Обрабатываем минимальные неучтённые элементы
        max_sorted = min_unsorted
        for i in range(lst_len):
            if lst[i] == max_sorted:
                list_copy.append(max_sorted)
    # Возвращаем результат
    return list_copy
