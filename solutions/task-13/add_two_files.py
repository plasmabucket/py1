from typing import Union


# Функция, возвращающая сумму шести чисел из двух файлов.
# В случае ошибки, возвращает сообщение об ошибке
def add_two_files(f1: int, f2: int, path: str) -> Union[int, str]:
    num_sum: int = 0  # Сумма чисел из файлов
    error_msg: str = ""  # Переменная для сообщений об ошибке
    filenames: list[str] = [f"{f1}.txt", f"{f2}.txt"]
    for i in range(len(filenames)):
        line_count: int = 0  # Счётчик считанных строк
        file = open(f"{path}{filenames[i]}", "rt", encoding="utf-8")
        try:
            # Построчно читаем файл до конца
            for line in file:
                line_count += 1
                num_sum += int(line.rstrip())
        except ValueError:  # Ловим ошибку приведения строки к числу
            assert error_msg == ""  # Не затираем одну ошибку другой
            error_msg = (f"Line {line_count} in {filenames[i]}"
                         f" could not be cast to integer.")
        # Всегда закрываем файл
        finally:
            file.close()
        # Если строки целые, то должно быть считано 3 числа
        if error_msg == "" and line_count < 3:
            error_msg = f"File {filenames[i]} contains less than 3 lines."
        elif error_msg == "" and line_count > 3:
            error_msg = f"File {filenames[i]} contains more than 3 lines."

        if error_msg != "":
            return error_msg
    assert error_msg == ""  # Не возвращаем результат, если есть ошибка
    return num_sum


# Пример использования.
# Перед запуском необходимо сгенерировать файлы
# программой из предыдущего задания.
sum_of_two_files = add_two_files(1, 2, "files/")
if isinstance(sum_of_two_files, str):
    print("Error:")
    print(sum_of_two_files)
else:
    print(sum_of_two_files)
