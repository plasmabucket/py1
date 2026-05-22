# Пример побочного эффекта от передачи объектов по ссылке

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


# Хотим дать роботу две одинаковые пушки
# Оружие 1
weapon1: RoboPart = RoboPart()
weapon1.category = "WEAPON"
weapon1.name = "Imp. Plasma Rifle"
weapon1.mass = 3

# Оружие 2
weapon2: RoboPart = weapon1  # вместо копии делаем простое присваивание переменной

# Робот
enemy: Robot = Robot()
enemy.name = "Heavy H-14"
enemy.behavior = "AGGRESSIVE"
enemy.parts.append(weapon1)  # заполняем инвентарь частями
enemy.free_slots -= weapon1.slot_size  # ведём учёт свободных слотов
enemy.parts.append(weapon2)
enemy.free_slots -= weapon2.slot_size


# Вывод инвентаря робота
print("===", enemy.name, "===")
for i in range(len(enemy.parts)):
    print(enemy.parts[i].name, "-", enemy.parts[i].integrity)

# === Heavy H-14 ===
# ... - 100
# ... - 100

# Во время боя одна из пушек получила повреждение
weapon1.integrity -= 30

# Вывод инвентаря робота после боя
print()
print("===", enemy.name, "===")
for i in range(len(enemy.parts)):
    print(enemy.parts[i].name, "-", enemy.parts[i].integrity)

# === Heavy H-14 ===
# ... - 70
# ... - 70

# Ошибка! Повреждёнными оказываются не одна, а обе пушки!
