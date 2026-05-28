# Композиция уже была реализована в решении к предыдущему заданию
# Роботы разных видов могут иметь части разных видов

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

    def get_category(self) -> str:
        return self.__category

    def print_info(self) -> None:
        print(f"{self.__name:<26} {self.__integrity:>4}")


class Weapon(RoboPart):

    def __init__(self, part_name: str, weapon_dmg: int) -> None:
        super().__init__("WEAPON", part_name, 1, 100, 100)
        self.__weapon_damage: int = weapon_dmg  # урон, наносимый оружием
        self.__internal_heat: int = 0  # насколько оружие нагрелось

    def shoot_worker_robot(self, target: WorkerRobot) -> None:
        # стреляем по роботу
        target.robot_take_damage(self.__weapon_damage)
        # от стрельбы оружие нагревается
        self.__increase_heat(80)

    def __increase_heat(self, heat: int) -> None:
        # оружие получает урон от перегрева
        self.__internal_heat += heat
        if self.__internal_heat > 300:
            self.part_take_damage(30)

    def cool(self) -> None:
        # охлаждение оружия
        self.__internal_heat -= 100
        self.__internal_heal = max(0, self.__internal_heat)


class Utility(RoboPart):

    def __init__(self, part_name: str) -> None:
        super().__init__("UTILITY", part_name, 1, 15, 20)

    def scan_wall(self, cell: GridCell) -> None:
        # сканирование клетки на наличие стены
        if cell.is_wall():
            print("Wall")
            return
        print("Not a wall")

    def scan_combat_robot(self, combat_target: CombatRobot) -> None:
        # сканирование боевого робота
        print("Combat robot scan results:")
        combat_target.print_info()
        print()

    def scan_worker_robot(self, worker_target: WorkerRobot) -> None:
        # сканирование робота-рабочего
        print("Worker robot scan results:")
        worker_target.print_info()
        print()


class Propulsion(RoboPart):

    def __init__(self, part_name: str, knd: int) -> None:
        # скорость передвижения в тиках за клетку. (Меньше - быстрее)
        self.__propulsion_speed: int
        self.__propulsion_support: int  # грузоподъёмность
        # инициализация средства передвижения: 1 - гусеницы, 2 - колёса
        if knd == 1:
            super().__init__("PROPULSION", part_name, 2, 300, 200)
            self.__propulsion_speed = 135
            self.__propulsion_support = 25
        elif knd == 2:
            super().__init__("PROPULSION", part_name, 1, 50, 75)
            self.__propulsion_speed = 50
            self.__propulsion_support = 10
        else:  # значение по умолчанию
            super().__init__("PROPULSION", "-unknown-", 1, 100, 100)
            self.__propulsion_speed = 100
            self.__propulsion_support = 15

    # Не делаю логику изменения скорости передвижения робота,
    # поэтому просто создал методы для получения информации
    def get_speed(self) -> int:
        return self.__propulsion_speed

    def get_support(self) -> int:
        return self.__propulsion_support


# Класс роботов
class Robot:

    def __init__(self, robot_name: str, robot_bhv: str,
                 core_int: int, core_cov: int, robot_slots: int) -> None:
        self.__name: str = robot_name  # игровое название
        self.__behavior: str = robot_bhv  # стиль поведения робота
        self.__core_integrity: int = core_int  # сколько урона выдерживает ядро
        self.__core_coverage: int = core_cov  # как легко попасть в ядро
        self.__free_slots: int = robot_slots  # сколько слотов есть у робота
        self._parts: List[RoboPart] = []  # список имеющихся частей

    def attach_part(self, attached_part: RoboPart) -> None:
        # присоединяем часть только если есть место
        if self.__free_slots >= attached_part.get_size():
            self._parts.append(attached_part)
            self.__free_slots -= attached_part.get_size()

    def robot_take_damage(self, robot_damage: int) -> None:
        part_count: int = len(self._parts)

        # считаем общее покрытие у частей и ядра
        total_coverage: int = self.__core_coverage
        for i in range(part_count):
            total_coverage += self._parts[i].get_coverage()

        # Вычисляем в какую часть (или ядро) прилетело попадание.
        # Чем больше покрытие у части, тем больше вероятность
        # что в неё прилетит.
        random_hit: int = random.randint(1, total_coverage)
        for i in range(part_count):
            random_hit -= self._parts[i].get_coverage()
            if random_hit <= 0:
                self._parts[i].part_take_damage(robot_damage)
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
        # получаем урон если врезались в другого робота
        if intended_position.is_occupied():
            self.robot_take_damage(random.randint(10, 40))
            return
        # если ничего нет, меням позицию
        current_position.robot_leaves()
        intended_position.robot_arrives(self)

    def get_name(self) -> str:
        return self.__name

    def _get_core_integrity(self) -> int:
        return self.__core_integrity

    def _set_behavior(self, bhv: str) -> None:
        self.__behavior = bhv

    def print_info(self) -> None:
        # Выводим название, поведение, состояние ядра и частей
        print("===", self.__name, "===", self.__behavior)
        print(f"{"Core":<26} {self.__core_integrity:>4}")
        for i in range(len(self._parts)):
            self._parts[i].print_info()


class CombatRobot(Robot):

    def __init__(self, name: str) -> None:
        super().__init__(name, "AGGRESSIVE", 100, 100, 6)

    def shoot_worker_robot(self, target: WorkerRobot) -> None:
        # стреляем по роботу-рабочему из всех пушек
        for i in range(len(self._parts)):
            if self._parts[i].get_category() == "WEAPON":
                # Здесь mypy выдаёт ошибку типов:
                # "RoboPart" has no attribure "shoot_worker_robot"
                # и на данный момент у меня не хватает знаний чтобы
                # от неё избавиться.
                # Программа должна работать корректно т.к. проверка
                # "оружие ли это" была произведена.
                self._parts[i].shoot_worker_robot(target)

    def do_nothing(self) -> None:
        # когда робот не активен, его пушки остывают
        for i in range(len(self._parts)):
            if self._parts[i].get_category() == "WEAPON":
                # Та же самая ошибка типов от mypy, как и выше
                self._parts[i].cool()


class WorkerRobot(Robot):

    def __init__(self, name: str) -> None:
        super().__init__(name, "WORKING", 50, 50, 4)

    def become_frightened(self) -> None:
        # при повреждении ядра рабочий пугается
        if self._get_core_integrity() < 50:
            self._set_behavior("FLEEING")

    def scan_combat_robot(self, scan_target: CombatRobot) -> None:
        # сканирование происходит только если есть функционирующий сканер
        has_scanner = False
        for i in range(len(self._parts)):
            if self._parts[i].get_category() == "UTILITY":
                has_scanner = True
                break
        if has_scanner:
            print("Scan target:", scan_target.get_name())
            return
        print("! Scanner malfunction !")


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

    def is_occupied(self) -> bool:
        if self.__robot != None:
            return True
        return False


# Создаём части для боевого робота
cmb_weapon = Weapon("Imp. Plasma Rifle", 40)
cmb_prop = Propulsion("Heavy Treads", 1)
cmb_utility = Utility("Targeting Processor")

# Создаём боевого робота
fighter = CombatRobot("Heavy H-12")
fighter.attach_part(cmb_weapon)
fighter.attach_part(cmb_prop)
fighter.attach_part(cmb_utility)

# Создаём части для робота-рабочего
wrk_prop1 = Propulsion("Wheel", 2)
wrk_prop2 = Propulsion("Wheel", 2)
wrk_utility = Utility("Scanner")

# Создаём робота-рабочего
worker = WorkerRobot("Worker W-05")
worker.attach_part(wrk_prop1)
worker.attach_part(wrk_prop2)
worker.attach_part(wrk_utility)

# Вывод стартового инвентаря роботов
fighter.print_info()
worker.print_info()

# метод robot_take_damage распределяет урон по частям вне зависимости
# от их класса
fighter.robot_take_damage(80)
fighter.robot_take_damage(80)
fighter.robot_take_damage(80)
worker.robot_take_damage(40)
worker.robot_take_damage(40)
worker.robot_take_damage(40)

# Вывод итогового инвентаря роботов
print()
fighter.print_info()
worker.print_info()
