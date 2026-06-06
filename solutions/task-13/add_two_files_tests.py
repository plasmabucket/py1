import unittest
import random
from add_two_files import add_two_files


class AddTwoFilesTests(unittest.TestCase):

    # Проверяем, что числа из двух файлов складываются
    def test_add_numbers(self) -> None:
        path: str = "test-files/"  # Путь к файлам
        # Создаём два файла с числами
        with open(path + "1.txt", "wt", encoding="utf-8") as file:
            file.write("58\n")
            file.write("28\n")
            file.write("100\n")
        with open(path + "2.txt", "wt", encoding="utf-8") as file:
            file.write("47\n")
            file.write("59\n")
            file.write("52\n")

        sum_two_files = add_two_files(1, 2, path)
        sum_num: int = 58 + 28 + 100 + 47 + 59 + 52
        self.assertEqual(sum_two_files, sum_num,
                         "Numbers from files are not summed.")

    # Проверяем суммирование на случайных данных
    def test_random_files(self) -> None:
        path: str = "test-files/"  # Путь к файлам
        # Делаем 100 прогонов
        for i in range(100):
            sum_num: int = 0
            # Создаём два файла с тремя строками
            f1: int = random.randint(1, 10)
            f2: int = random.randint(1, 10)
            with open(f"{path}{f1}.txt", "wt", encoding="utf-8") as file:
                for i in range(3):
                    num = random.randint(0, 100)
                    file.write(f"{num}\n")
                    sum_num += num
            # Если выпавшие номера файлов совпадают,
            # то пропускаем второе создание файла
            if f1 != f2:
                with open(f"{path}{f2}.txt", "wt", encoding="utf-8") as file:
                    for i in range(3):
                        num = random.randint(0, 100)
                        file.write(f"{num}\n")
                        sum_num += num
            else:
                sum_num *= 2

            sum_two_files = add_two_files(f1, f2, path)
            self.assertEqual(sum_two_files, sum_num,
                             "Error in summing random numbers.")

    # Проверяем поведение при испорченном содержимом файлов
    def test_corrupted_line(self) -> None:
        path: str = "test-files/"
        # Создаём два файла с числами
        with open(f"{path}1.txt", "wt", encoding="utf-8") as file:
            file.write("58\n")
            file.write("28\n")
            file.write("100\n")
        with open(f"{path}2.txt", "wt", encoding="utf-8") as file:
            file.write("47\n")
            file.write("n0t 4 num83r\n")  # Строка с не-числом
            file.write("52\n")

        sum_two_files = add_two_files(1, 2, path)
        self.assertEqual(sum_two_files,
                         "Line 2 in 2.txt could not be cast to integer.",
                         "Corrupted line is unhandled.")

    # Проверяем поведение при избыточном/недостаточном содержимом файлов
    def test_short_long_files(self) -> None:
        path: str = "test-files/"
        # Создаём три файла с разной длиной
        with open(f"{path}1.txt", "wt", encoding="utf-8") as file:
            file.write("58\n")
            file.write("28\n")
            file.write("100\n")
        with open(f"{path}2.txt", "wt", encoding="utf-8") as file:
            pass
        with open(f"{path}3.txt", "wt", encoding="utf-8") as file:
            file.write("47\n")
            file.write("59\n")
            file.write("52\n")
            file.write("34\n")

        sum_short_file = add_two_files(1, 2, path)
        self.assertEqual(sum_short_file,
                         "File 2.txt contains less than 3 lines.",
                         "Short files are unhandled.")
        sum_long_file = add_two_files(3, 1, path)
        self.assertEqual(sum_long_file,
                         "File 3.txt contains more than 3 lines.",
                         "Long files are unhandled.")


if __name__ == '__main__':
    unittest.main()
