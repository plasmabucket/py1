import unittest
import os
import shutil
from rm_dir import rm_dir


class RmDirTests(unittest.TestCase):

    # Путь к каталогу с тестовыми каталогами.
    path = "./rm_testdirs"

    # Проверка успешного удаления каталога.
    def test_success(self) -> None:
        test_path = os.path.join(self.path, "should_be_removed")
        # Подготавливаем каталог для удаления.
        # Если каталог существует, удаляем его.
        if os.path.exists(test_path):
            shutil.rmtree(test_path)
        # Создаём каталог с 10-ю файлами.
        os.mkdir(test_path)
        for i in range(10):
            with open(os.path.join(test_path, f"{i}.txt"), "wt",
                      encoding="utf-8") as file:
                pass
        # Удаляем его нашей функцией.
        result: bool = rm_dir(test_path)
        self.assertFalse(os.path.exists(os.path.join(test_path, "0.txt")),
                         "Files are not removed.")
        self.assertFalse(os.path.exists(test_path),
                         "Dir didn't get removed.")
        self.assertTrue(result,
                        "Didn't return True after success.")

    # Проверка попытки удалить несуществующий каталог
    def test_does_not_exist(self) -> None:
        test_path: str = os.path.join(self.path, "does_not_exist")
        self.assertFalse(rm_dir(test_path),
                         "Doesn't fail on non-existent path.")

    # Проверка попытки удалить файл
    def test_rm_file(self) -> None:
        test_path: str = os.path.join(self.path, "this_is_a_file")
        # Создаём файл если его нет
        if not os.path.exists(test_path):
            with open(test_path, "wt", encoding="utf-8") as file:
                pass
        # Пытаемся его удалить
        result: bool = rm_dir(test_path)
        self.assertTrue(os.path.exists(test_path),
                        "File got removed.")
        self.assertFalse(result,
                         "Doesn't fail on removing a file.")

    # Проверка поведения на каталогах с подкаталогами
    def test_rm_dir_with_subdirs(self) -> None:
        test_path: str = os.path.join(self.path, "remove_me")
        subdir_path: str = os.path.join(test_path, "nuh-uh")
        file_path: str = os.path.join(test_path, "file")
        # Создаём каталог, подкаталог и файл если их нет
        if not os.path.exists(test_path):
            os.mkdir(test_path)
        if not os.path.exists(subdir_path):
            os.mkdir(subdir_path)
        if not os.path.exists(file_path):
            with open(file_path, "wt", encoding="utf-8") as file:
                pass
        # Пытаемся их удалить
        result: bool = rm_dir(test_path)
        self.assertTrue(os.path.exists(test_path),
                        "Directory with subdir got removed.")
        self.assertTrue(os.path.exists(subdir_path),
                        "Subdir got removed.")
        self.assertTrue(os.path.exists(file_path),
                        "File got removed in a dir with subdir.")
        self.assertFalse(result,
                         "Doesn't fail on removing a dir with subdir.")


if __name__ == '__main__':
    unittest.main()
