# Классы основанные на описанной в решении 1.1 игре Cogmind

from typing import List


# Класс частей
class RoboPart:
    slot_size: int = 1  # занимаемый размер в слотах
    integrity: int = 100  # сколько урона может выдержать часть
    coverage: int = 100  # насколько легко в эту часть попасть
    mass: int = 1  # вес части
    category: str = "None"  # какой категории принадлежит
    name: str = "None"  # игровое название


# Класс роботов
class Robot:
    core_integrity: int = 100  # сколько урона может выдержать ядро
    energy_generation: int = 5  # генерация энергии ядром
    heat_dissipation: int = 20  # мощность сброса тепла ядром
    free_slots: int = 6  # сколько слотов есть у робота
    parts: List[RoboPart] = []  # список имеющихся частей
    behavior: str = "None"  # стиль поведения робота
    name: str = "None"  # игровое название
    vision_range: int = 12  # дальность обзора в клетках
    speed: int = 100  # количество времени (тиков) для перемещения на 1 клетку


# Класс клеток
class GridCell:
    item: RoboPart  # По умолчанию клетки не содержат ничего
    robot: Robot
    wall: bool = True  # является ли клетка стеной
    wall_integrity: int = 40  # сколько единовременного урона выдерживает стена
    texture: str = "#"  # для примера в качестве текстуры используем символ


# Заполнение полей
# Оружие
weapon: RoboPart = RoboPart()
weapon.category = "WEAPON"
weapon.name = "Imp. Plasma Rifle"
weapon.mass = 3

# Средство передвижения
propulsion: RoboPart = RoboPart()
propulsion.category = "PROPULSION"
propulsion.name = "Heavy Treads"
propulsion.slot_size = 2
propulsion.integrity = 300
propulsion.coverage = 200
propulsion.mass = -20  # средства передвижения увеличивают грузоподъёмность

# Устройство
device: RoboPart = RoboPart()
device.category = "UTILITY"
device.name = "Targeting Processor"
device.integrity = 15
device.coverage = 20
device.mass = 0

# Робот
enemy: Robot = Robot()
enemy.name = "Heavy H-12"
enemy.behavior = "AGGRESSIVE"
enemy.parts.append(weapon)  # заполняем инвентарь частями
enemy.free_slots -= weapon.slot_size  # ведём учёт свободных слотов
enemy.parts.append(propulsion)
enemy.free_slots -= propulsion.slot_size
enemy.parts.append(device)
enemy.free_slots -= device.slot_size

# Сетка 3х3
grid: List[List[GridCell]] = []
for i in range(3):
    row = []
    for j in range(3):
        row.append(GridCell())
    grid.append(row)

# В середину помещаем робота
grid[1][1].wall = False
grid[1][1].wall_integrity = 0
grid[1][1].texture = "H"
grid[1][1].robot = enemy


# Вывод сетки на экран
for i in range(3):
    for j in range(3):
        print(grid[i][j].texture, end="")
    print()

# Вывод инвентаря робота
print("===", enemy.name, "===")
for i in range(3):
    print(enemy.parts[i].name, "-", enemy.parts[i].integrity)
