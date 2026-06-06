# Программа, создающая 10 файлов.
# Каждый файл содержит 3 случайных числа
import random

n_files: int = 10  # Количество файлов.
n_lines: int = 3  # Количество строк в файле
path: str = "files/"  # Путь к файлам
for i in range(n_files):
    with open(f"{path}{i + 1}.txt", "wt", encoding="utf-8") as file:
        for i in range(n_lines):
            # Пишем случайное число в каждую строку
            number: str = f"{random.randint(0, 100)}\n"
            file.write(number)
