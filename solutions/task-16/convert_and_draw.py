from files_and_dirs import files_and_dirs
import os
from PIL import Image, ImageDraw


# Функция, конвертирующая формат изображений.
def convert_and_draw(from_ext: str, to_ext: str) -> None:
    # Получаем список изображений на конвертацию.
    r: list[list[str]] = files_and_dirs(".", from_ext, False)
    # Проходим по каждому изображению из списка.
    for filename in r[0]:
        with Image.open(filename) as image:
            draw = ImageDraw.Draw(image)
            # Рисуем в центре квадрат.
            size = image.size
            square_side = max(75, min(size[0], size[1]) * 0.5)
            draw.rectangle([0.5 * size[0] - 0.5 * square_side,
                            0.5 * size[1] - 0.5 * square_side,
                            0.5 * size[0] + 0.5 * square_side,
                            0.5 * size[1] + 0.5 * square_side])
            # Пишем текст.
            draw.multiline_text((0.5 * size[0], 0.5 * size[1]),
                                "Hello,\nWorld!",
                                anchor="mm",
                                font_size=20)
            # Создаём новый файл, удаляем старый.
            image.save(filename.removesuffix(from_ext) + to_ext)
            os.remove(filename)
