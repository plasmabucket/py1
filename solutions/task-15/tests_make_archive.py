import unittest
import os
import random
from zipfile import ZipFile
from make_archive import mkarchive


class MakeArchiveTests(unittest.TestCase):

    path: str = "archive_testdir"

    def test_make_archive(self) -> None:
        # Переходим в тестовый каталог.
        if not os.getcwd().endswith(self.path):
            os.chdir(self.path)
        # Создаём файлы для архивации.
        files_answer: list[str] = []
        for i in range(10):
            if random.randint(0, 1) == 0:
                ext: str = "txt"
                files_answer.append(f"{i}.{ext}")
            else:
                ext = "png"
            with open(f"{i}.{ext}", "wt", encoding="utf-8") as file:
                pass
        # Создаём архив из текстовых файлов.
        archive_name = "text_files.zip"
        mkarchive(archive_name, "txt")
        # Очищаем тестовый каталог от созданных файлов.
        for entry in os.listdir():
            if entry.endswith(".txt") or entry.endswith(".png"):
                os.remove(entry)
        # Читаем созданный архив.
        files_result: list[str] = []
        with ZipFile(archive_name, "r") as archive:
            files_result = archive.namelist()
        # Проверяем результат с эталоном.
        for entry in files_answer:
            self.assertIn(entry, files_result,
                          f"{entry} was not included in the archive.")
        self.assertEqual(len(files_answer), len(files_result),
                         "Something extra got included in the archive.")

    def test_empty_archive(self) -> None:
        # Переходим в тестовый каталог.
        if not os.getcwd().endswith(self.path):
            os.chdir(self.path)
        # Создаём пустой архив.
        archive_name = "empty_archive.zip"
        mkarchive(archive_name, "txt")
        # Читаем созданный архив.
        files_result: list[str] = []
        with ZipFile(archive_name, "r") as archive:
            files_result = archive.namelist()
        # Проверяем, что архив пустой.
        self.assertEqual(files_result, [],
                         "Empty archive is not empty.")

    # Проверка, попытается ли программа во время исполнения
    # заархивировать собственный архив.
    def test_recursive_archiving(self) -> None:
        # Переходим в тестовый каталог.
        if not os.getcwd().endswith(self.path):
            os.chdir(self.path)
        # Указываем расширение, совпадающее с расширением архива.
        archive_name = "recursive_archive.testzip"
        mkarchive(archive_name, "testzip")
        # Проверяем, что архив пустой.
        files_result: list[str] = []
        with ZipFile(archive_name, "r") as archive:
            files_result = archive.namelist()
        self.assertEqual(files_result, [],
                         "Recursive archive is not empty.")


if __name__ == '__main__':
    unittest.main()
