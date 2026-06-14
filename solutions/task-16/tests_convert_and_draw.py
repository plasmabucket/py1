import unittest
import os
from PIL import Image
from convert_and_draw import convert_and_draw


class ConvertAndDrawTests(unittest.TestCase):

    path: str = "image_convert_testdir"

    # Проверяем рисунок на изображениях разного размера.
    def test_resolutions(self) -> None:
        test_path: str = os.path.join(self.path, "resolutions")
        # Переходим в тестовый каталог.
        if not os.getcwd().endswith(test_path):
            if os.getcwd().find(self.path) != -1:
                os.chdir("../..")
            os.chdir(test_path)
        # Очищаем каталог.
        for filename in os.listdir("."):
            os.remove(filename)
        # Создаём файлы для рисования.
        count: int = 10
        width: int = 40
        height: int = 40
        for i in range(count):
            img = Image.new("RGB", (width, height), (0, 0, 0))
            img.save(f"{i}.jpg")
            width += 50
            height += 50
        # Конвертируем изображения и рисуем квадрат с текстом.
        convert_and_draw("jpg", "png")
        # Проверяем, что все изображения сконвертировались.
        for filename in os.listdir("."):
            self.assertTrue(filename.endswith(".png"))
        # Качество рисунка проверяем вручную.


if __name__ == '__main__':
    unittest.main()
