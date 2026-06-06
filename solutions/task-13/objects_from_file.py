from typing import Union
from typing import Optional


# В качестве примера взял созданный в предыдущих решениях класс роботов
class Robot:
    def __init__(self, robot_name: str, robot_bhv: str,
                 core_int: int, core_cov: int, robot_slots: int) -> None:
        self._name: str = robot_name  # игровое название
        self.__behavior: str = robot_bhv  # стиль поведения робота
        self.__core_integrity: int = core_int  # сколько урона выдерживает ядро
        self.__core_coverage: int = core_cov  # как легко попасть в ядро
        self.__free_slots: int = robot_slots  # сколько слотов есть у робота

        # Инвариант класса Robot
        assert self._name != ""  # У робота должно быть имя
        assert self.__behavior != ""  # У робота всегда есть поведение
        assert self.__core_integrity >= 0  # Целостность ядра -- величина неотрицательная
        assert self.__core_coverage > 0  # Покрытие ядра -- величина положительная
        assert self.__free_slots >= 0  # Количество слотов -- величина неотрицательная

    def print_info(self) -> None:
        print(f"'{self._name}' - '{self.__behavior}' -"
              f" int:{self.__core_integrity} - cov:{self.__core_coverage} -"
              f" slots:{self.__free_slots}")


# Считывание полей объектов из файла
# В случае некорректной строки, в список добавляется None
def objects_from_file(filepath: str) -> list[Optional[Robot]]:
    field_count: int = 5
    list_of_objects: list[Optional[Robot]] = []
    with open(filepath, "rt", encoding="utf-8") as file:
        line: str
        for line in file:
            line = line.strip()
            raw_fields: list[str] = line.split(":")
            object_fields: list[Union[str, int]] = []
            # Обрабатываем строки с некорректным числом полей
            if len(raw_fields) != field_count:
                list_of_objects.append(None)
                continue
            # Добавляем имя и поведение
            # Имя и поведение не могут быть пустыми
            if raw_fields[0] == "" or raw_fields[1] == "":
                list_of_objects.append(None)
                continue
            object_fields.append(raw_fields[0])  # Имя
            object_fields.append(raw_fields[1])  # Поведение
            # Ловим ошибки преобразования str в int
            try:
                core_int = int(raw_fields[2])
                core_cov = int(raw_fields[3])
                robot_slots = int(raw_fields[4])
            except ValueError:
                list_of_objects.append(None)
                continue
            # Добавляем целостность, покрытие и количество слотов
            # Целостность -- неотрицательная величина
            # Покрытие -- положительная величина
            # Количество слотов -- неотрицательная величина
            if core_int < 0 or core_cov <= 0 or robot_slots < 0:
                list_of_objects.append(None)
                continue
            object_fields.append(core_int)  # Целостность
            object_fields.append(core_cov)  # Покрытие
            object_fields.append(robot_slots)  # Количество слотов

            assert len(object_fields) == len(raw_fields)  # Все поля должны быть обработаны
            assert len(object_fields) == field_count  # Обработанных полей должно быть нужное количество
            # Если все проверки пройдены, создаём объект класса
            list_of_objects.append(Robot(object_fields[0], object_fields[1],
                                         object_fields[2], object_fields[3],
                                         object_fields[4]))
    return list_of_objects


robot_list: list[Optional[Robot]] = objects_from_file("objectfiles/objects.txt")
# Вывод получившегося списка
for i in range(len(robot_list)):
    if robot_list[i] != None:
        robot_list[i].print_info()
    else:
        print("None")
