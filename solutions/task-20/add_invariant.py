"""
К решению задания 7.2 добавлен декоратор для поддержки инварианта.
В декоратор передаю набор assert-ов, проверяющих инвариант класса.
Декоратор использую в классе RoboPart.
"""

from typing import List
from typing import Optional
import random
from functools import wraps


# Декоратор для поддержки инварианта.
def invariant(predicate):
    def invariant_decorator(method):
        @wraps(method)
        def wrapper(self, *args, **kwargs):
            result = method(self, *args, **kwargs)
            predicate(self)
            return result
        return wrapper
    return invariant_decorator


# Класс частей
class RoboPart:

    # Инвариант класса RoboPart.
    def __robopart_invar(self) -> None:
        assert len(self.__category) > 0, "Category has to be defined."
        assert len(self.__name) > 0, "Name has to be defined."
        assert self.__slot_size > 0, "Part has to have non-zero size."
        assert self.__integrity >= 0, "Integrity can't be negative."
        assert self.__coverage >= 0, "Coverage can't be negative."

    @invariant(__robopart_invar)
    def __init__(self, part_cat: str, part_name: str,
                 part_size: int, part_int: int, part_cov: int) -> None:
        self.__category: str = part_cat  # какой категории принадлежит
        self.__name: str = part_name  # игровое название
        self.__slot_size: int = part_size  # занимаемый размер в слотах
        self.__integrity: int = part_int  # сколько урона может выдержать часть
        self.__coverage: int = part_cov  # насколько легко в эту часть попасть

    @property
    def size(self) -> int:
        return self.__slot_size

    @property
    def coverage(self) -> int:
        return self.__coverage

    @invariant(__robopart_invar)
    def part_take_damage(self, part_dmg: int) -> None:
        # часть получает урон
        if self.__integrity > 0:
            self.__integrity -= part_dmg
        # если целостность упала меньше нуля, часть ломается
        if self.__integrity <= 0 and self.__category != "BROKEN":
            self.__get_broken()

    @invariant(__robopart_invar)
    def __get_broken(self) -> None:
        # сломанная часть теряет свою функциональность
        self.__integrity = 0
        self.__coverage = 0
        self.__name = "Broken " + self.__name
        self.__category = "BROKEN"

    @invariant(__robopart_invar)
    def part_repair(self, repair_dmg: int) -> None:
        # чинить можно только функционирующие части
        if self.__integrity > 0:
            self.__integrity += repair_dmg

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

    @property
    def name(self) -> str:
        return self.__name

    def attach_part(self, attached_part: RoboPart) -> None:
        # присоединяем часть только если есть место
        if self.__free_slots >= attached_part.size:
            self.__parts.append(attached_part)
            self.__free_slots -= attached_part.size

    def robot_take_damage(self, robot_damage: int) -> None:
        part_count: int = len(self.__parts)

        # считаем общее покрытие у частей и ядра
        total_coverage: int = self.__core_coverage
        for i in range(part_count):
            total_coverage += self.__parts[i].coverage

        # Вычисляем в какую часть (или ядро) прилетело попадание.
        # Чем больше покрытие у части, тем больше вероятность
        # что в неё прилетит.
        random_hit: int = random.randint(1, total_coverage)
        for i in range(part_count):
            random_hit -= self.__parts[i].coverage
            if random_hit <= 0:
                self.__parts[i].part_take_damage(robot_damage)
                return
        self.__core_integrity -= robot_damage
        # ядро не может иметь отрицательную целостность
        self.__core_integrity = max(0, self.__core_integrity)

    def move(self, current_position: GridCell,
             intended_position: GridCell) -> None:
        # получаем урон если врезались в стену
        if intended_position.wall:
            self.robot_take_damage(random.randint(50, 80))
            return
        # если стены нет, меняем позицию
        current_position.robot_leaves()
        intended_position.robot_arrives(self)

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
        if self.__robot is None:
            self.__texture = " "
            return
        # В качестве текстуры робота берём его первую букву названия
        robot_name: str = self.__robot.name
        self.__texture = robot_name[0]

    @property
    def texture(self) -> str:
        return self.__texture

    @property
    def wall(self) -> bool:
        return self.__wall

    @wall.setter
    def wall(self, flag: bool) -> None:
        self.__wall = flag
        self.__update_texture()

    def robot_leaves(self) -> None:
        self.__robot = None
        self.__update_texture()

    def robot_arrives(self, robot: Robot) -> None:
        self.__robot = robot
        self.__update_texture()


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
            cell.wall = True
        row.append(cell)
    grid.append(row)

# В левый верхний угол помещаем робота
grid[1][1].robot_arrives(robot)


# Вывод сетки на экран
for i in range(len(grid)):
    for j in range(len(grid[0])):
        print(grid[i][j].texture, end="")
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
        print(grid[i][j].texture, end="")
    print()

# Вывод инвентаря робота
robot.print_info()

# Части должны быть повреждены от ударов об стену
# Часть с нулевой целостностью должна иметь приставку "Broken"
