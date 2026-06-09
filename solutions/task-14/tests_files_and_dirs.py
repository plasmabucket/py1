import unittest
import os
import shutil
from files_and_dirs import files_and_dirs
from files_and_dirs import append_matches


class FilesAndDirsTests(unittest.TestCase):

    # Путь к каталогу с тестовыми каталогами
    path: str = "./list_testdirs"

    def prepare_matches_dir(self, test_path: str) -> None:
        # Если каталог существует, удаляем его.
        if os.path.exists(test_path):
            shutil.rmtree(test_path)
        # Создаём каталог с 10-ю файлами и 5-ю подкаталогами.
        os.mkdir(test_path)
        for i in range(10):
            with open(os.path.join(test_path, f"{i}.txt"), "wt",
                      encoding="utf-8") as file:
                pass
        for i in range(5):
            os.mkdir(os.path.join(test_path, f"dir{i}"))

    # Проверяем, только ли файлы/каталоги добавляет append_matches().
    def test_append_matches(self) -> None:
        test_path = os.path.join(self.path, "append_matches")
        # Подготавливаем тестовый каталог.
        self.prepare_matches_dir(test_path)
        # Проверяем добавление каталогов.
        # Получаем результат тестируемой функции.
        only_dirs: list[str] = []
        pattern: str = os.path.join(test_path, "*")  # Пытаемся взять всё.
        append_matches(pattern, True, only_dirs)
        # Сравниваем с ответом.
        dir_answer: list[str] = []
        for i in range(5):
            dir_answer.append(f"dir{i}")
        self.assertEqual(len(only_dirs), len(dir_answer),
                         "Dirs aren't properly matched.")
        for i in range(len(only_dirs)):
            self.assertIn(only_dirs[i], dir_answer,
                          "Wrong match got assigned to dirs.")
        # Проверяем добавление файлов.
        # Получаем результат тестируемой функции.
        only_files: list[str] = []
        pattern = os.path.join(test_path, "*")  # Пытаемся взять всё.
        append_matches(pattern, False, only_files)
        # Сравниваем с ответом
        file_answer: list[str] = []
        for i in range(10):
            file_answer.append(f"{i}.txt")
        self.assertEqual(len(only_files), len(file_answer),
                         "Files aren't properly matched.")
        for i in range(len(only_files)):
            self.assertIn(only_files[i], file_answer,
                          "Wrong match got assigned to files.")

    # Проверка результата прохода по тестовой папке.
    def test_list_root(self) -> None:
        test_path = os.path.join(self.path, "root_dir")
        # Результаты
        result: list[list[str]] = files_and_dirs(test_path, "txt", False)
        files_result: list[str] = result[0]
        dirs_result: list[str] = result[1]
        # Ответы
        dir_answer: list[str] = ["dir0_1", "dir0_2", "cursed_dir.txt"]
        file_answer: list[str] = ["root_file.txt", "root_file2.txt",
                                  "кириллица.txt", ".hidden.txt", ".txt"]

        # Проверяем все ли правильные ответы получены.
        for i in range(len(file_answer)):
            self.assertIn(file_answer[i], files_result,
                          "Correct file was not listed.")
        for i in range(len(dir_answer)):
            self.assertIn(dir_answer[i], dirs_result,
                          "Correct dir was not listed.")

        # Проверяем, получили ли мы неправильные ответы.
        self.assertNotIn("backup.txt.bak", files_result,
                         "Double file extension got picked.")
        self.assertNotIn("root_picture.png", files_result,
                         "Wrong file extension got picked.")
        self.assertNotIn("txt", files_result,
                         "Filename got treated as extension.")
        self.assertNotIn("lvl1_file.txt", files_result,
                         "File from subdirectory got picked.")

        self.assertNotIn("dir1_1", dirs_result,
                         "Lvl1 subdirectory got picked.")
        self.assertNotIn("dir1_2", dirs_result,
                         "Lvl1 subdirectory got picked.")
        self.assertNotIn("dir2_1", dirs_result,
                         "Lvl2 subdirectory got picked.")

        # Делаем общую проверку на размер списков.
        self.assertEqual(len(files_result), len(file_answer),
                         "Something wrong got picked as a file.")
        self.assertEqual(len(dirs_result), len(dir_answer),
                         "Something wrong got picked as a directory.")

    # Проход по тестовой папке с погружением на один уровень.
    def test_list_lvl1(self) -> None:
        test_path = os.path.join(self.path, "root_dir")
        # Результаты
        result: list[list[str]] = files_and_dirs(test_path, "txt", True)
        files_result: list[str] = result[0]
        dirs_result: list[str] = result[1]
        # Ответы
        dir_answer: list[str] = ["dir0_1", "dir0_2", "cursed_dir.txt",
                                 "dir1_1", "dir1_2"]
        file_answer: list[str] = ["root_file.txt", "root_file2.txt",
                                  "кириллица.txt", ".hidden.txt", ".txt",
                                  "lvl1_file.txt"]

        # Проверяем все ли правильные ответы получены.
        for i in range(len(file_answer)):
            self.assertIn(file_answer[i], files_result,
                          "Correct file was not listed.")
        for i in range(len(dir_answer)):
            self.assertIn(dir_answer[i], dirs_result,
                          "Correct dir was not listed.")

        # Проверяем, получили ли мы неправильные ответы.
        self.assertNotIn("backup.txt.bak", files_result,
                         "Double file extension got picked.")
        self.assertNotIn("root_picture.png", files_result,
                         "Wrong file extension got picked.")
        self.assertNotIn("txt", files_result,
                         "Filename got treated as extension.")
        self.assertNotIn("lvl1_picture.png", files_result,
                         "Wrong file extension got picked.")
        self.assertNotIn("lvl2_file.txt", files_result,
                         "File from lvl1 subdirectory got picked.")

        self.assertNotIn("dir2_1", dirs_result,
                         "Lvl2 subdirectory got picked.")

        # Делаем общую проверку на размер списков.
        self.assertEqual(len(files_result), len(file_answer),
                         "Something wrong got picked as a file.")
        self.assertEqual(len(dirs_result), len(dir_answer),
                         "Something wrong got picked as a directory.")


if __name__ == '__main__':
    unittest.main()
