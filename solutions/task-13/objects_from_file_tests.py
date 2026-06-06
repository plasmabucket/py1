import unittest
from objects_from_file import objects_from_file


class ObjectsFromFileTests(unittest.TestCase):

    # Тестируем поведение на пустом файле
    def test_empty_file(self) -> None:
        path: str = "test-objectfiles/"
        # Затираем файл, чтобы убедиться что он пустой
        with open(f"{path}empty.txt", "wt", encoding="utf-8") as file:
            pass
        robot_list: list = objects_from_file(f"{path}empty.txt")
        self.assertEqual(len(robot_list), 0,
                         "Empty file returns non-empty list")

    # Тестируем обработку пустых строк
    def test_empty_line(self) -> None:
        path: str = "test-objectfiles/"
        robot_list: list = objects_from_file(f"{path}empty-line.txt")
        none_count: int = 0
        for i in range(len(robot_list)):
            if robot_list[i] == None:
                none_count += 1
        # Должно быть два None из-за двух пустых строку
        self.assertEqual(none_count, 2,
                         "Empty lines are unhandled")

    # Тестируем обработку разделителя в кавычках
    def test_colons_in_quotes(self) -> None:
        path: str = "test-objectfiles/"
        robot_list: list = objects_from_file(f"{path}quotes.txt")
        none_count: int = 0
        for i in range(len(robot_list)):
            if robot_list[i] == None:
                none_count += 1
        self.assertEqual(none_count, 0,
                         "Quotes in strings are unhandled")

    # Тестируем обработку разделителя за управляющими символами
    def test_escape_sequence(self) -> None:
        path: str = "test-objectfiles/"
        robot_list: list = objects_from_file(f"{path}escape.txt")
        none_count: int = 0
        for i in range(len(robot_list)):
            if robot_list[i] == None:
                none_count += 1
        self.assertEqual(none_count, 0,
                         "Escaped colons are unhandled")

    # Проверяем соответствие количества строк и созданных объектов
    def test_line_object_number(self) -> None:
        path: str = "test-objectfiles/"
        # Считаем количество строк в файле
        line_count: int = 0
        with open(f"{path}count-check.txt", "rt", encoding="utf-8") as file:
            for i in file:
                line_count += 1
        robot_list: list = objects_from_file(f"{path}count-check.txt")
        self.assertEqual(len(robot_list), line_count,
                         "Different number of lines and objects")


if __name__ == '__main__':
    unittest.main()
