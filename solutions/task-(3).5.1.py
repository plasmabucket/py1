# Модификация программы для разделения видимости полей
# Все поля объектов сделаны приватными

from typing import List
from typing import Optional
import random


# Класс частей
class RoboPart:

    def __init__(self, part_cat: str, part_name: str,
                 part_size: int, part_int: int, part_cov: int) -> None:
        self.__category: str = part_cat  # какой категории принадлежит
        self.__name: str = part_name  # игровое название
        self.__slot_size: int = part_size  # занимаемый размер в слотах
        self.__integrity: int = part_int  # сколько урона может выдержать часть
        self.__coverage: int = part_cov  # насколько легко в эту часть попасть

    def part_take_damage(self, part_dmg: int) -> None:
        # часть получает урон
        if self.__integrity > 0:
            self.__integrity -= part_dmg
        # если целостность упала меньше нуля, часть ломается
        if self.__integrity <= 0 and self.__category != "BROKEN":
            self.__get_broken()

    def __get_broken(self) -> None:
        # сломанная часть теряет свою функциональность
        self.__integrity = 0
        self.__coverage = 0
        self.__name = "Broken " + self.__name
        self.__category = "BROKEN"

    def part_repair(self, repair_dmg: int) -> None:
        # чинить можно только функционирующие части
        if self.__integrity > 0:
            self.__integrity += repair_dmg

    def get_size(self) -> int:
        return self.__slot_size

    def get_coverage(self) -> int:
        return self.__coverage

    def print_info(self) -> None:
        print(f"{self.__name:<26} {self.__integrity:>4}")


# Класс роботов
class Robot:

    def __init__(self, robot_name: str, robot_bhv: str,
                 core_int: int, core_cov: int, robot_slots: int) -> None:
        self.__name: str = robot_name  # игровое название
        self.__behavior: str = robot_bhv  # стиль поведения робота
        self.__core_integrity: int = core_int  # сколько урона выдерживает ядро
        self.__core_coverage: int = core_cov  # как легко попасть в ядро
        self.__free_slots: int = robot_slots  # сколько слотов есть у робота
        self.__parts: List[RoboPart] = []  # список имеющихся частей

    def attach_part(self, attached_part: RoboPart) -> None:
        # присоединяем часть только если есть место
        if self.__free_slots >= attached_part.get_size():
            self.__parts.append(attached_part)
            self.__free_slots -= attached_part.get_size()

    def robot_take_damage(self, robot_damage: int) -> None:
        part_count: int = len(self.__parts)

        # считаем общее покрытие у частей и ядра
        total_coverage: int = self.__core_coverage
        for i in range(part_count):
            total_coverage += self.__parts[i].get_coverage()

        # Вычисляем в какую часть (или ядро) прилетело попадание.
        # Чем больше покрытие у части, тем больше вероятность
        # что в неё прилетит.
        random_hit: int = random.randint(1, total_coverage)
        for i in range(part_count):
            random_hit -= self.__parts[i].get_coverage()
            if random_hit <= 0:
                self.__parts[i].part_take_damage(robot_damage)
                return
        self.__core_integrity -= robot_damage
        # ядро не может иметь отрицательную целостность
        self.__core_integrity = max(0, self.__core_integrity)

    def move(self, current_position: GridCell,
             intended_position: GridCell) -> None:
        # получаем урон если врезались в стену
        if intended_position.is_wall():
            self.robot_take_damage(random.randint(50, 80))
            return
        # если стены нет, меням позицию
        current_position.robot_leaves()
        intended_position.robot_arrives(self)

    def get_name(self) -> str:
        return self.__name

    def print_info(self) -> None:
        print("===", self.__name, "===")
        print(f"{"Core":<26} {self.__core_integrity:>4}")
        for i in range(len(self.__parts)):
            self.__parts[i].print_info()


# Класс клеток
class GridCell:

    def __init__(self) -> None:
        self.__robot: Optional[Robot] = None  # Какой робот стоит на клетке
        self.__wall: bool = False  # является ли клетка стеной
        self.__texture: str = " "  # в качестве текстуры используем символ

    def __update_texture(self) -> None:
        if self.__wall:
            self.__texture = "#"
            return
        if self.__robot == None:
            self.__texture = " "
            return
        # В качестве текстуры робота берём его первую букву названия
        robot_name: str = self.__robot.get_name()
        self.__texture = robot_name[0]

    def set_wall(self) -> None:
        self.__wall = True
        self.__update_texture()

    def robot_leaves(self) -> None:
        self.__robot = None
        self.__update_texture()

    def robot_arrives(self, robot: Robot) -> None:
        self.__robot = robot
        self.__update_texture()

    def get_texture(self) -> str:
        return self.__texture

    def is_wall(self) -> bool:
        return self.__wall


# Создаём части
weapon = RoboPart("WEAPON", "Imp. Plasma Rifle", 1, 100, 100)
propulsion = RoboPart("PROPULSION", "Heavy Treads", 2, 300, 200)
utility = RoboPart("UTILITY", "Targeting Processor", 1, 15, 20)

# Создаём робота
robot = Robot("Heavy H-12", "AGGRESSIVE", 100, 100, 6)
robot.attach_part(weapon)
robot.attach_part(propulsion)
robot.attach_part(utility)

# Сетка 4х4 со стеной по периметру
grid: List[List[GridCell]] = []
for i in range(4):
    row: List[GridCell] = []
    for j in range(4):
        cell: GridCell = GridCell()
        if i == 0 or i == 3 or j == 0 or j == 3:
            cell.set_wall()
        row.append(cell)
    grid.append(row)

# В левый верхний угол помещаем робота
grid[1][1].robot_arrives(robot)


# Вывод сетки на экран
for i in range(len(grid)):
    for j in range(len(grid[0])):
        print(grid[i][j].get_texture(), end="")
    print()

# Вывод инвентаря робота
robot.print_info()

# Робот делает несколько передвижений и ударяется в стену
robot.move(grid[1][1], grid[1][2])  # идёт направо
robot.move(grid[1][2], grid[2][2])  # идёт вниз
robot.move(grid[2][2], grid[2][3])  # ударяется в нижнюю стену
robot.move(grid[2][2], grid[2][3])  # ударяется несколько раз
robot.move(grid[2][2], grid[2][3])
robot.move(grid[2][2], grid[2][3])

# Вывод сетки на экран
print()
for i in range(len(grid)):
    for j in range(len(grid[0])):
        print(grid[i][j].get_texture(), end="")
    print()

# Вывод инвентаря робота
robot.print_info()

# Части должны быть повреждены от ударов об стену
# Часть с нулевой целостностью должна иметь приставку "Broken"
