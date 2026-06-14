import unittest
import os
import random
from glob import glob
from PIL import Image
from image_convert import convert_images


class ImageConvertTests(unittest.TestCase):

    path: str = "image_convert_testdir"

    # Проверяем конвертацию случайных изображений.
    def test_image_convert(self) -> None:
        test_path: str = os.path.join(self.path, "image_convert")
        # Переходим в тестовый каталог.
        if not os.getcwd().endswith(test_path):
            if os.getcwd().find(self.path) != -1:
                os.chdir("../..")
            os.chdir(test_path)
        # Очищаем каталог.
        for file in os.listdir("."):
            os.remove(file)
        # Создаём файлы для конвертации.
        count: int = 10
        for i in range(count):
            # Случайные размеры и цвет фона.
            width: int = random.randint(100, 500)
            height: int = random.randint(100, 500)
            red: int = random.randint(0, 255)
            grn: int = random.randint(0, 255)
            blu: int = random.randint(0, 255)
            img = Image.new("RGB", (width, height), (red, grn, blu))
            if random.randint(0, 1) == 0:
                ext: str = "png"
            else:
                ext = "jpg"
            img.save(f"img-{i}.{ext}")
        # Конвертируем изображения в JPEG.
        convert_images("png", "jpg")
        # Проверяем, все ли изображения были сконвертированы.
        jpg_images: list[str] = glob(f"*.jpg")
        self.assertEqual(len(jpg_images), count,
                         "Something extra got added to the files.")
        png_images: list[str] = glob(f"*.png")
        self.assertEqual(len(png_images), 0,
                         "Png image was not converted.")

    # Проверяем работу с расширениями изображений.
    def test_filenames(self) -> None:
        test_path: str = os.path.join(self.path, "filenames")
        # Переходим в тестовый каталог.
        if not os.getcwd().endswith(test_path):
            if os.getcwd().find(self.path) != -1:
                os.chdir("../..")
            os.chdir(test_path)
        # Очищаем каталог.
        for file in os.listdir("."):
            os.remove(file)
        # Создаём файлы для конвертации.
        image_names: list[str] = ["normal_name.jpg", "not_jpg.gif",
                                  "double_extension.gif.jpg", "jpg",
                                  ".hidden.jpg"]
        for filename in image_names:
            # Случайные размеры и цвет фона.
            width: int = random.randint(100, 300)
            height: int = random.randint(100, 300)
            red: int = random.randint(0, 255)
            grn: int = random.randint(0, 255)
            blu: int = random.randint(0, 255)
            img = Image.new("RGB", [width, height],
                            f"rgb({red}, {grn}, {blu})")
            img.save(filename, "JPEG")
        # Конвертируем изображения.
        convert_images("jpg", "png")
        # Получаем список файлов в каталоге и сравниваем его с ответом.
        result_images: list[str] = os.listdir()
        answer_images: list[str] = ["normal_name.png", "not_jpg.gif",
                                    "double_extension.gif.png", "jpg",
                                    ".hidden.png"]
        self.assertIn("normal_name.png", result_images,
                      "Image with normal name was not converted.")
        self.assertIn("not_jpg.gif", result_images,
                      "Image with wrong extension got converted.")
        self.assertIn("double_extension.gif.png", result_images,
                      "Image with double extension was not converted.")
        self.assertIn("jpg", result_images,
                      "Image without extension got converted.")
        self.assertIn(".hidden.png", result_images,
                      "Hidden image was not converted.")
        result_images.sort()
        answer_images.sort()
        self.assertEqual(result_images, answer_images,
                         "Extensions aren't handled properly.")


if __name__ == '__main__':
    unittest.main()
