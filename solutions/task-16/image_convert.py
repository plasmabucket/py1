from files_and_dirs import files_and_dirs
import os
from PIL import Image


# Функция, конвертирующая формат изображений.
def convert_images(from_ext: str, to_ext: str) -> None:
    # Получаем список изображений на конвертацию.
    r: list[list[str]] = files_and_dirs(".", from_ext, False)
    # Проходим по каждому изображению из списка.
    for filename in r[0]:
        with Image.open(filename) as image:
            # Создаём новый файл, удаляем старый.
            image.save(filename.removesuffix(from_ext) + to_ext)
            os.remove(filename)
