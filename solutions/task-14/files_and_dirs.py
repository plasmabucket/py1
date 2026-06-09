import os.path
from glob import glob


# Вспомогательная функция.
# Добавляет в список подходящие по шаблону каталоги или файлы.
def append_matches(pattern: str, dirs: bool, output: list[str]) -> None:
    # Ищем совпадения по шаблону.
    for match in glob(pattern, include_hidden=True):
        # В зависимости от флага добавляем либо только каталоги,
        # либо только файлы.
        if (dirs and os.path.isdir(match) or
                not dirs and os.path.isfile(match)):
            output.append(os.path.basename(match))


def files_and_dirs(path: str, ext: str, list_dirs: bool) -> list[list[str]]:
    # Списки с результатами.
    dir_list: list[str] = []
    file_list: list[str] = []

    # Создаём список каталогов.
    # Берём все каталоги из корневого.
    pattern: str = os.path.join(path, "*")
    append_matches(pattern, True, dir_list)
    # Если нужны каталоги из подкаталогов,
    # повторяем процедуру с одним уровнем глубже.
    if list_dirs:
        pattern = os.path.join(path, "*/*")
        append_matches(pattern, True, dir_list)

    # Создаём список файлов.
    # Берём шаблоном всё с соответствующим окончанием.
    pattern = os.path.join(path, f"*.{ext}")
    append_matches(pattern, False, file_list)
    # Если нужны файлы из подкаталогов,
    # повторяем процедуру с одним уровнем глубже.
    if list_dirs:
        pattern = os.path.join(path, f"*/*.{ext}")
        append_matches(pattern, False, file_list)

    return [file_list, dir_list]


# Пример использования.
result: list[list[str]] = files_and_dirs("./root_dir", "txt", True)
print("Files:")
print(result[0])
print()
print("Directories:")
print(result[1])
