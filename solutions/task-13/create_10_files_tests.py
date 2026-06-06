import unittest


class Create10FilesTests(unittest.TestCase):

    # Проверяем, что создано 10 файлов
    def test_10_files(self) -> None:
        path: str = "files/"  # Путь к файлам
        # Имена файлов
        filenames: list[str] = ["1.txt", "2.txt", "3.txt", "4.txt", "5.txt",
                                "6.txt", "7.txt", "8.txt", "9.txt", "10.txt"]
        # Проверяем наличие 10 файлов
        for i in range(10):
            found: bool = True
            try:
                # Открываем и закрываем файл
                with open(path + filenames[i], "rt", encoding="utf-8") as file:
                    pass
            except FileNotFoundError:
                found = False
            # Вынес fail из блока except для более чистого вывода об ошибке
            if not found:
                self.fail(f"File {filenames[i]} not found.")
        # Проверяем, что не было создано лишних файлов
        try:
            with open(path + "11.txt", "rt", encoding="utf-8") as file:
                pass
            self.fail("There are more than 10 files.")
        except FileNotFoundError:
            pass
        # Проверяем лишние файлы с другого конца
        try:
            with open(path + "0.txt", "rt", encoding="utf-8") as file:
                pass
            self.fail("Filenames should start from 1.")
        except FileNotFoundError:
            pass

    # Проверяем, что в файлах по 3 строки
    def test_3_lines(self) -> None:
        path: str = "files/"  # Путь к файлам
        for i in range(10):
            line_count: int = 0
            with open(f"{path}{i+1}.txt", "rt", encoding="utf-8") as file:
                for line in file:
                    line_count += 1
            if line_count < 3:
                self.fail(f"File {i+1}.txt has less than 3 lines.")
            if line_count > 3:
                self.fail(f"File {i+1}.txt has more than 3 lines.")


if __name__ == "__main__":
    unittest.main()
