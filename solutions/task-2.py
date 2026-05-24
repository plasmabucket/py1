# Классы из задания 1.2 дополненные методами

from typing import List
from typing import Optional
import random


# Класс частей
class RoboPart:

    def __init__(self, part_cat: str, part_name: str,
                 part_size: int, part_int: int, part_cov: int) -> None:
        self.category: str = part_cat  # какой категории принадлежит
        self.name: str = part_name  # игровое название
        self.slot_size: int = part_size  # занимаемый размер в слотах
        self.integrity: int = part_int  # сколько урона может выдержать часть
        self.coverage: int = part_cov  # насколько легко в эту часть попасть

    def part_take_damage(self, part_dmg: int) -> None:
        # часть получает урон
        if self.integrity > 0:
            self.integrity -= part_dmg
        # если целостность упала меньше нуля, часть ломается
        if self.integrity <= 0 and self.category != "BROKEN":
            self.get_broken()

    def get_broken(self) -> None:
        # сломанная часть теряет свою функциональность
        self.integrity = 0
        self.coverage = 0
        self.name = "Broken " + self.name
        self.category = "BROKEN"

    def part_repair(self, repair_dmg: int) -> None:
        # чинить можно только функционирующие части
        if self.integrity > 0:
            self.integrity += repair_dmg


# Класс роботов
class Robot:

    def __init__(self, robot_name: str, robot_bhv: str,
                 core_int: int, core_cov: int, robot_slots: int) -> None:
        self.name: str = robot_name  # игровое название
        self.behavior: str = robot_bhv  # стиль поведения робота
        self.core_integrity: int = core_int  # сколько урона выдерживает ядро
        self.core_coverage: int = core_cov  # как легко попасть в ядро
        self.free_slots: int = robot_slots  # сколько слотов есть у робота
        self.parts: List[RoboPart] = []  # список имеющихся частей

    def attach_part(self, attached_part: RoboPart) -> None:
        # присоединяем часть только если есть место
        if self.free_slots >= attached_part.slot_size:
            self.parts.append(attached_part)
            self.free_slots -= attached_part.slot_size

    def robot_take_damage(self, robot_damage: int) -> None:
        part_count: int = len(self.parts)

        # считаем общее покрытие у частей и ядра
        total_coverage: int = self.core_coverage
        for i in range(part_count):
            total_coverage += self.parts[i].coverage

        # Вычисляем в какую часть (или ядро) прилетело попадание.
        # Чем больше покрытие у части, тем больше вероятность
        # что в неё прилетит.
        random_hit: int = random.randint(1, total_coverage)
        for i in range(part_count):
            random_hit -= self.parts[i].coverage
            if random_hit <= 0:
                self.parts[i].part_take_damage(robot_damage)
                return
        self.core_integrity -= robot_damage

    def move(self, current_position: GridCell,
             intended_position: GridCell) -> None:
        # получаем урон если врезались в стену
        if intended_position.wall:
            self.robot_take_damage(random.randint(50, 80))
            return
        # если стены нет, меням позицию
        current_position.robot_leaves()
        intended_position.robot_arrives(self)


# Класс клеток
class GridCell:

    def __init__(self) -> None:
        self.robot: Optional[Robot] = None  # Какой робот стоит на клетке
        self.wall: bool = False  # является ли клетка стеной
        self.texture: str = " "  # в качестве текстуры используем символ

    def update_texture(self) -> None:
        if self.wall:
            self.texture = "#"
            return
        if self.robot == None:
            self.texture = " "
            return
        # В качестве текстуры робота берём его первую букву названия
        self.texture = self.robot.name[0]

    def set_wall(self) -> None:
        self.wall = True
        self.update_texture()

    def robot_leaves(self) -> None:
        self.robot = None
        self.update_texture()

    def robot_arrives(self, rbt: Robot) -> None:
        self.robot = rbt
        self.update_texture()


# Создаём части
weapon = RoboPart("WEAPON", "Imp. Plasma Rifle", 1, 100, 100)
propulsion = RoboPart("PROPULSION", "Heavy Treads", 2, 300, 200)
utility = RoboPart("UTILITY", "Targeting Processor", 1, 15, 20)

# Создаём робота
robot = Robot("Heavy H-12", "AGGRESSIVE", 100, 100, 6)
robot.parts.append(weapon)
robot.parts.append(propulsion)
robot.parts.append(utility)

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
        print(grid[i][j].texture, end="")
    print()

# Вывод инвентаря робота
print("===", robot.name, "===")
print(f"{"Core":<26} {robot.core_integrity:>4}")
for i in range(len(robot.parts)):
    print(f"{robot.parts[i].name:<26} {robot.parts[i].integrity:>4}")

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
print("===", robot.name, "===")
print(f"{"Core":<26} {robot.core_integrity:>4}")
for i in range(len(robot.parts)):
    print(f"{robot.parts[i].name:<26} {robot.parts[i].integrity:>4}")

# Части должны быть повреждены от ударов об стену
# Часть с нулевой целостностью должна иметь приставку "Broken"
