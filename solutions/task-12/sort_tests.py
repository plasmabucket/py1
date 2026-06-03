from typing import List
import unittest
import random
from my_sort import list_sort


class SortTests(unittest.TestCase):

    def test_regression(self) -> None:
        # Проверка, что лист сортируется
        unsorted_list: List = [2, 8, 9, 7, 10, 6, 1, 4, 5, 3]
        self.assertEqual(list_sort(unsorted_list),
                         [1, 2, 3, 4, 5, 6, 7, 8, 9, 10],
                         "list didn't get sorted")
        # Проверка, что переданный лист не был изменён
        self.assertEqual(unsorted_list,
                         [2, 8, 9, 7, 10, 6, 1, 4, 5, 3],
                         "parameter got modified")
        # Проверка, что отсортированный лист остаётся отсортированным
        sorted_list: List = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]
        self.assertEqual(list_sort(sorted_list),
                         [1, 2, 3, 4, 5, 6, 7, 8, 9, 10],
                         "sorted list got unsorted")

    def test_random(self) -> None:
        # Проверяем сортировку на большом количестве случайных списков
        for i in range(1000):
            # Создаём список, заполненный случайными элементами
            unsorted_list: List = []
            for j in range(100):
                unsorted_list.append(random.randint(-100, 100))
            # Сравниваем собственную сортировку с эталонной
            self.assertEqual(list_sort(unsorted_list), sorted(unsorted_list),
                             "random list didn't get sorted")

    def test_empty(self) -> None:
        # Проверяем сортировку пустого списка
        unsorted_list: List = []
        self.assertEqual(list_sort(unsorted_list), [],
                         "empty list is unhandled")

    def test_max(self) -> None:
        # Проверяем сортировку больших значений
        unsorted_list: List = [9223372036854775808, -9223372036854775808, 0]
        self.assertEqual(list_sort(unsorted_list),
                         [-9223372036854775808, 0, 9223372036854775808],
                         "max values aren't sorted")


if __name__ == '__main__':
    unittest.main()
