import os


def rm_dir(path: str) -> bool:
    try:
        # Неудача, если каталога не существует
        if not os.path.exists(path):
            return False
        # Неудача, если цель не каталог
        if not os.path.isdir(path):
            return False
        # Получаем список содержимого в каталоге
        entries: list[str] = os.listdir(path)
        # Неудача, если есть подкаталоги
        for i in range(len(entries)):
            if os.path.isdir(os.path.join(path, entries[i])):
                return False
        # Удаляем все файлы в каталоге
        for i in range(len(entries)):
            os.remove(os.path.join(path, entries[i]))
        # Удаляем каталог
        os.rmdir(path)
    # Неудача, если произошла ошибка операций
    except OSError:
        return False
    # Успех, если всё прошло без ошибок.
    return True


# Пример использования.
# Должно удалить каталог вместе с файлом.
if rm_dir("./remove_this_dir"):
    print("success")
else:
    print("fail")
