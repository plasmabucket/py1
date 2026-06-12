from glob import glob
from zipfile import ZipFile


def mkarchive(archive_name: str, ext: str) -> None:
    # Создаём новый архив
    with ZipFile(archive_name, "w") as archive:
        # Добавляем в него только файлы с подходящим расширением
        for file in glob(f"*.{ext}"):
            # Не включаем в создаваемый архив сам архив.
            if file != archive_name:
                archive.write(file)
