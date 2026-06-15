import unittest
import random
import string
from count_entries import count_entries


class CountEntriesTests(unittest.TestCase):

    # Проверяем работу функции на случайных списках.
    def test_list_of_100_int(self) -> None:
        # Делаем 100 прогонов.
        for i in range(100):
            # Случайно выбираем порог повторов.
            threshold: int = random.randint(0, 20)
            # Подготавливаем список из 100 чисел и считаем повторы.
            list_of_numbers: list[int] = []
            number_repetitions: list[int] = []
            for i in range(10):
                number_repetitions.append(0)
            for i in range(100):
                random_number: int = random.randint(1, 10)
                number_repetitions[random_number - 1] += 1
                list_of_numbers.append(random_number)
            # Создаём список-провильный ответ.
            answer: list[int] = []
            for i in range(len(number_repetitions)):
                if number_repetitions[i] >= threshold:
                    answer.append(i + 1)
            answer.sort()
            # Получаем ответ от функции.
            result: list[int] = count_entries(list_of_numbers, threshold)
            result.sort()
            # Проверяем, что они равны.
            self.assertEqual(answer, result,
                             "Repetitions are not counted properly.")

    # Проверяем, работает ли подсчёт значений-строк.
    def test_strings(self) -> None:
        # Задаём порог повторов.
        threshold: int = 10
        # Создаём список из 100 строк и считаем повторы.
        list_of_strings: list[str] = []
        string_repetitions: list[int] = []
        for i in range(10):
            string_repetitions.append(0)
        for i in range(100):
            random_number: int = random.randint(0, 9)
            random_string: str = string.ascii_letters[random_number]
            string_repetitions[random_number] += 1
            list_of_strings.append(random_string)
        # Создаём список-правильный ответ.
        answer: list[str] = []
        for i in range(len(string_repetitions)):
            if string_repetitions[i] >= threshold:
                answer.append(string.ascii_letters[i])
        answer.sort()
        # Получаем ответ от функции.
        result: list[str] = count_entries(list_of_strings, threshold)
        result.sort()
        # Проверяем, что они равны.
        self.assertEqual(answer, result,
                         "String repetitions are not counted properly.")

    # Проверяем поведение функции на пустом списке.
    def test_empty_list(self) -> None:
        threshold: int = 0
        empty_list: list[None] = []
        answer: list[None] = []

        result: list[None] = count_entries(empty_list, threshold)
        self.assertEqual(answer, result,
                         "Empty list is not handled.")


if __name__ == '__main__':
    unittest.main()
