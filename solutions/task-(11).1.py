# Код с добавленными assert-ами и логированием

import logging
from typing import List
from typing import Optional
import random
logger = logging.getLogger(__name__)

# Класс частей
class RoboPart:

    def __init__(self, part_cat: str, part_name: str,
                 part_size: int, part_int: int, part_cov: int) -> None:
        logger.debug(f"Creating part \"{part_name}\":"
                     f" cat:\"{part_cat}\", size:{part_size},"
                     f" int:{part_int}, cov:{part_cov}")
        self.__category: str = part_cat  # какой категории принадлежит
        self._name: str = part_name  # игровое название
        self.__slot_size: int = part_size  # занимаемый размер в слотах
        self.__integrity: int = part_int  # сколько урона может выдержать часть
        self.__coverage: int = part_cov  # насколько легко в эту часть попасть

        # Инвариант класса RoboPart
        assert self.__category != ""  # Категория должна быть определена
        assert self._name != ""  # У части должно быть имя
        assert self.__slot_size > 0  # У части должен быть размер
        assert self.__integrity >= 0  # Целостность -- неотрицательная величина
        assert self.__coverage >= 0  # Покрытие -- неотрицательная величина
        logger.info(f"Part {self._name} created")

    def part_take_damage(self, part_dmg: int) -> None:
        logger.debug(f"Part {self._name} receives dmg:{part_dmg}")
        # часть получает урон
        if self.__integrity > 0:
            self.__integrity -= part_dmg
            logger.info(f"Part {self._name} takes {part_dmg} damage")
        logger.debug(f"Part int:{self.__integrity}")

        # если целостность упала меньше нуля, часть ломается
        if self.__integrity <= 0 and self.__category != "BROKEN":
            self.__get_broken()
        assert self.__integrity >= 0

    def __get_broken(self) -> None:
        logger.debug(f"Part {self._name} breaks")
        # сломанная часть теряет свою функциональность
        self.__integrity = 0
        self.__coverage = 0
        self._name = "Broken " + self._name
        self.__category = "BROKEN"
        # Более строгие проверки т.к. сломанное состояние
        # накладывает более строгие ограничения
        assert self.__integrity == 0
        assert self.__coverage == 0
        assert self.__category == "BROKEN"
        logger.info(f"Part is now \"{self._name}\"")

    def part_repair(self, repair_dmg: int) -> None:
        logger.debug(f"Part {self._name} gets int:{repair_dmg} of repairs")
        # чинить можно только функционирующие части
        if self.__integrity > 0:
            self.__integrity += repair_dmg
            logger.info(f"Part {self._name} is repaired for"
                        f" {repair_dmg} integrity")
        logger.debug(f"Part int:{self.__integrity}")
        assert self.__integrity >= 0

    def get_size(self) -> int:
        logger.debug(f"Part {self._name} size:{self.__slot_size}")
        assert self.__slot_size > 0
        return self.__slot_size

    def get_coverage(self) -> int:
        logger.debug(f"Part {self._name} cov:{self.__coverage}")
        assert self.__coverage >= 0
        return self.__coverage

    def get_category(self) -> str:
        logger.debug(f"Part {self._name} cat:{self.__category}")
        assert self.__category != ""
        return self.__category

    def print_info(self) -> None:
        logger.debug(f"Part {self._name} info is printed")
        assert self._name != ""
        assert self.__integrity >= 0
        print(f"{self._name:<26} {self.__integrity:>4}")


class Weapon(RoboPart):

    def __init__(self, part_name: str, weapon_dmg: int) -> None:
        logger.debug(f"Creating weapon \"{part_name}\": dmg:{weapon_dmg}")
        super().__init__("WEAPON", part_name, 1, 100, 100)
        self.__weapon_damage: int = weapon_dmg  # урон, наносимый оружием
        self.__internal_heat: int = 0  # насколько оружие нагрелось

        # Инвариант класса Weapon
        assert self.__weapon_damage >= 0  # Наносимый урон -- неотрицательное значение
        assert self.__internal_heat >= -273  # Температура не меньше абсолютного нуля
        logger.info(f"Weapon {self._name} created")

    def shoot_worker_robot(self, target: WorkerRobot) -> None:
        logger.debug(f"Weapon {self._name} aims at {target.get_name()}")
        # стреляем по роботу
        assert self.__weapon_damage >= 0
        logger.info(f"Weapon {self._name} shoots at {target.get_name()}")
        target.robot_take_damage(self.__weapon_damage)
        # от стрельбы оружие нагревается
        self.__increase_heat(80)

    def __increase_heat(self, heat: int) -> None:
        logger.debug(f"Weapon {self._name} gets heat:{heat}")
        # оружие получает урон от перегрева
        self.__internal_heat += heat
        logger.debug(f"Weapon heat:{self.__internal_heat}")
        if self.__internal_heat > 300:
            logger.info(f"Weapon {self._name} takes heat damage")
            self.part_take_damage(30)
        assert self.__internal_heat >= -273

    def cool(self) -> None:
        logger.info(f"Weapon {self._name} cools")
        # охлаждение оружия
        self.__internal_heat -= 100
        # Пассивное охлаждение не понижает температуру ниже нуля
        self.__internal_heat = max(0, self.__internal_heat)
        logger.debug(f"Weapon heat:{self.__internal_heat}")
        assert self.__internal_heat >= -273


class Utility(RoboPart):

    def __init__(self, part_name: str) -> None:
        logger.debug(f"Creating utility \"{part_name}\"")
        super().__init__("UTILITY", part_name, 1, 15, 20)
        logger.info(f"Utility {self._name} created")

    def scan_wall(self, cell: GridCell) -> None:
        logger.debug(f"Scanning a wall:\"{cell.get_texture()}\"")
        # сканирование клетки на наличие стены
        if cell.is_wall():
            print("Wall")
            return
        print("Not a wall")

    def scan_combat_robot(self, combat_target: CombatRobot) -> None:
        logger.debug(f"Scanning combat robot:\"{combat_target.get_name()}\"")
        # сканирование боевого робота
        print("Combat robot scan results:")
        combat_target.print_info()
        print()

    def scan_worker_robot(self, worker_target: WorkerRobot) -> None:
        logger.debug(f"Scanning worker robot:\"{worker_target.get_name()}\"")
        # сканирование робота-рабочего
        print("Worker robot scan results:")
        worker_target.print_info()
        print()


class Propulsion(RoboPart):

    def __init__(self, part_name: str, knd: int) -> None:
        logger.debug(f"Creating propulsion \"{part_name}\": knd:{knd}")
        # Скорость передвижения в тиках за клетку. (Меньше - быстрее)
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

        # Инвариант класса Propulsion
        assert self.__propulsion_speed > 0  # Передвижение всегда занимает время
        assert self.__propulsion_support >= 0  # Грузоподъёмность -- неотрицательная величина
        logger.info(f"Propulsion {self._name} created")

    # Не делаю логику изменения скорости передвижения робота,
    # поэтому просто создал методы для получения информации
    def get_speed(self) -> int:
        logger.debug(f"Propulsion speed:{self.__propulsion_speed}")
        assert self.__propulsion_speed > 0
        return self.__propulsion_speed

    def get_support(self) -> int:
        logger.debug(f"Propulsion support:{self.__propulsion_support}")
        assert self.__propulsion_support >= 0
        return self.__propulsion_support


# Класс роботов
class Robot:

    def __init__(self, robot_name: str, robot_bhv: str,
                 core_int: int, core_cov: int, robot_slots: int) -> None:
        logger.debug(f"Creating robot \"{robot_name}\": bhv:\"{robot_bhv}\","
                     f" int:{core_int}, cov:{core_cov}, slots:{robot_slots}")
        self._name: str = robot_name  # игровое название
        self.__behavior: str = robot_bhv  # стиль поведения робота
        self.__core_integrity: int = core_int  # сколько урона выдерживает ядро
        self.__core_coverage: int = core_cov  # как легко попасть в ядро
        self.__free_slots: int = robot_slots  # сколько слотов есть у робота
        self._parts: List[RoboPart] = []  # список имеющихся частей

        # Инвариант класса Robot
        assert self._name != ""  # У робота должно быть имя
        assert self.__behavior != ""  # У робота всегда есть поведение
        assert self.__core_integrity >= 0  # Целостность ядра -- величина неотрицательная
        assert self.__core_coverage > 0  # Покрытие ядра -- величина положительная
        assert self.__free_slots >= 0  # Количество слотов -- величина неотрицательная
        logger.info(f"Robot {self._name} created")

    def attach_part(self, attached_part: RoboPart) -> None:
        logger.debug(f"Robot {self._name} tries attaching new part")
        # присоединяем часть только если есть место
        if self.__free_slots >= attached_part.get_size():
            logger.info(f"Robot {self._name} attached new part")
            self._parts.append(attached_part)
            self.__free_slots -= attached_part.get_size()
        logger.debug(f"Robot slots:{self.__free_slots}")
        assert self.__free_slots >= 0

    def robot_take_damage(self, robot_damage: int) -> None:
        logger.debug(f"Robot {self._name} receives dmg:{robot_damage}")
        part_count: int = len(self._parts)

        # считаем общее покрытие у частей и ядра
        total_coverage: int = self.__core_coverage
        for i in range(part_count):
            total_coverage += self._parts[i].get_coverage()
        logger.debug(f"Core cov:{self.__core_coverage}")
        logger.debug(f"Robot total cov:{total_coverage}")
        assert total_coverage > 0  # Мы всегда должны попасть во что-то

        # Вычисляем в какую часть (или ядро) прилетело попадание.
        # Чем больше покрытие у части, тем больше вероятность
        # что в неё прилетит.
        random_hit: int = random.randint(1, total_coverage)
        logger.debug(f"Random rolled: {random_hit} for hit")
        for i in range(part_count):
            random_hit -= self._parts[i].get_coverage()
            logger.debug(f"Check part [{i}] for hit")
            if random_hit <= 0:
                logger.info(f"Robot {self._name} part [{i}] gets hit")
                self._parts[i].part_take_damage(robot_damage)
                return
        self.__core_integrity -= robot_damage
        logger.info(f"Robot {self._name} core takes {robot_damage} damage")
        # ядро не может иметь отрицательную целостность
        self.__core_integrity = max(0, self.__core_integrity)
        logger.debug(f"Robot core int:{self.__core_integrity}")
        assert self.__core_integrity >= 0

    def move(self, current_position: GridCell,
             intended_position: GridCell) -> None:
        logger.debug(f"Robot {self._name} tries to move")
        # получаем урон если врезались в стену
        if intended_position.is_wall():
            logger.info(f"Robot {self._name} crashes into a wall")
            self.robot_take_damage(random.randint(50, 80))
            return
        # получаем урон если врезались в другого робота
        if intended_position.is_occupied():
            logger.info(f"Robot {self._name} crashes into a robot")
            self.robot_take_damage(random.randint(10, 40))
            return
        # если ничего нет, меняем позицию
        current_position.robot_leaves()
        intended_position.robot_arrives(self)
        logger.info(f"Robot {self._name} has moved")

    def get_name(self) -> str:
        logger.debug(f"Robot name:\"{self._name}\"")
        assert self._name != ""
        return self._name

    def _get_core_integrity(self) -> int:
        logger.debug(f"Robot {self._name} core int:{self.__core_integrity}")
        assert self.__core_integrity >= 0
        return self.__core_integrity

    def _set_behavior(self, bhv: str) -> None:
        logger.debug(f"Robot {self._name} bhv is set to:\"{bhv}\"")
        self.__behavior = bhv
        assert self.__behavior != ""

    def print_info(self) -> None:
        logger.debug(f"Robot {self._name} info is printed")
        # Выводим название, поведение, состояние ядра и частей
        print("===", self._name, "===", self.__behavior)
        print(f"{"Core":<26} {self.__core_integrity:>4}")
        for i in range(len(self._parts)):
            self._parts[i].print_info()


class CombatRobot(Robot):

    def __init__(self, name: str) -> None:
        logger.debug(f"Creating combat robot \"{name}\"")
        super().__init__(name, "AGGRESSIVE", 100, 100, 6)
        logger.info(f"Combat robot \"{self._name}\" created")

    def shoot_worker_robot(self, target: WorkerRobot) -> None:
        logger.info(f"Combat robot {self._name} shoots at {target.get_name()}")
        # стреляем по роботу-рабочему из всех пушек
        for i in range(len(self._parts)):
            if self._parts[i].get_category() == "WEAPON":
                # Здесь mypy выдаёт ошибку типов:
                # "RoboPart" has no attribute "shoot_worker_robot"
                # и на данный момент у меня не хватает знаний чтобы
                # от неё избавиться.
                # Программа должна работать корректно т.к. проверка
                # "оружие ли это" была произведена.
                self._parts[i].shoot_worker_robot(target)

    def do_nothing(self) -> None:
        logger.info(f"Combat robot {self._name} does nothing")
        # когда робот не активен, его пушки остывают
        for i in range(len(self._parts)):
            if self._parts[i].get_category() == "WEAPON":
                # Та же самая ошибка типов от mypy, как и выше
                self._parts[i].cool()


class WorkerRobot(Robot):

    def __init__(self, name: str) -> None:
        logger.debug(f"Creating worker robot \"{name}\"")
        super().__init__(name, "WORKING", 50, 50, 4)
        logger.info(f"Worker robot \"{self._name}\" created")

    def become_frightened(self) -> None:
        logger.debug(f"Worker robot {self._name} checks itself")
        # при повреждении ядра рабочий пугается
        if self._get_core_integrity() < 50:
            logger.info(f"Worker robot {self._name} becomes frightened")
            self._set_behavior("FLEEING")

    def scan_combat_robot(self, scan_target: CombatRobot) -> None:
        logger.info(f"Worker robot {self._name} scans {scan_target.get_name()}")
        # сканирование происходит только если есть функционирующий сканер
        has_scanner: bool = False
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
        logger.debug("Creating grid cell")
        self.__robot: Optional[Robot] = None  # Какой робот стоит на клетке
        self.__wall: bool = False  # является ли клетка стеной
        self.__texture: str = " "  # в качестве текстуры используем символ

        # Инвариант класса GridCell
        assert self.__texture != ""  # У клетки всегда есть текстура

    def __update_texture(self) -> None:
        logger.debug("Updating grid cell texture")
        if self.__wall:
            self.__texture = "#"
            assert self.__texture != ""
            return
        if self.__robot == None:
            self.__texture = " "
            assert self.__texture != ""
            return
        # В качестве текстуры робота берём его первую букву названия
        robot_name: str = self.__robot.get_name()
        self.__texture = robot_name[0]
        assert self.__texture != ""

    def set_wall(self) -> None:
        logger.debug("Setting grid cell wall")
        self.__wall = True
        self.__update_texture()
        assert self.__wall == True  # Поставилась ли стена

    def robot_leaves(self) -> None:
        logger.debug("Robot leaves grid cell")
        self.__robot = None
        self.__update_texture()
        assert self.__robot == None  # Ушёл ли робот

    def robot_arrives(self, robot: Robot) -> None:
        logger.debug("Robot arrives at a grid cell")
        self.__robot = robot
        self.__update_texture()
        assert self.__robot != None  # Пришёл ли робот

    def get_texture(self) -> str:
        logger.debug("Getting grid cell texture")
        assert self.__texture != ""
        return self.__texture

    def is_wall(self) -> bool:
        logger.debug("Checking grid cell for a wall")
        return self.__wall

    def is_occupied(self) -> bool:
        logger.debug("Checking grid cell for a robot")
        if self.__robot != None:
            return True
        return False


logging.basicConfig(filename="robots.log", level=logging.DEBUG)
logger.info("==== Run Start ====")

# Создаём части для боевого робота
cmb_weapon = Weapon("Imp. Plasma Rifle", 40)
cmb_prop = Propulsion("Heavy Treads", 1)
cmb_utility = Utility("Targeting Processor")

# Создаём боевого робота
fighter = CombatRobot("Heavy H-12")
fighter.attach_part(cmb_weapon)
fighter.attach_part(cmb_prop)
fighter.attach_part(cmb_utility)
logger.info("Combat robot is set")

# Создаём части для робота-рабочего
wrk_prop1 = Propulsion("Wheel", 2)
wrk_prop2 = Propulsion("Wheel", 2)
wrk_utility = Utility("Scanner")

# Создаём робота-рабочего
worker = WorkerRobot("Worker W-05")
worker.attach_part(wrk_prop1)
worker.attach_part(wrk_prop2)
worker.attach_part(wrk_utility)
logger.info("Worker robot is set")

# Сетка 4х4 со стеной по периметру
grid: List[List[GridCell]] = []
for i in range(4):
    row: List[GridCell] = []
    for j in range(4):
        cell: GridCell = GridCell()
        if i == 0 or i == 3 or j == 0 or j == 3:
            cell.set_wall()
        row.append(cell)
    assert len(row) > 0  # Строка не пустая
    grid.append(row)
assert len(grid) > 0  # Сетка не пустая
logger.info("Grid is formed")

# В левый верхний угол помещаем боевого робота
grid[1][1].robot_arrives(fighter)
# В левый нижний помещаем рабочего
grid[2][1].robot_arrives(worker)

# Вывод стартовой сетки на экран
for i in range(len(grid)):
    for j in range(len(grid[0])):
        print(grid[i][j].get_texture(), end="")
    print()

# Вывод стартового инвентаря роботов
fighter.print_info()
worker.print_info()

# Боевой робот делает несколько передвижений и ударяется в стену
fighter.move(grid[1][1], grid[1][2])  # идёт направо
fighter.move(grid[1][2], grid[2][2])  # идёт вниз
fighter.move(grid[2][2], grid[2][3])  # ударяется в нижнюю стену
fighter.move(grid[2][2], grid[2][3])  # ударяется несколько раз
fighter.move(grid[2][2], grid[2][3])
fighter.move(grid[2][2], grid[2][3])

fighter.shoot_worker_robot(worker)  # Стреляет по рабочему
fighter.shoot_worker_robot(worker)
fighter.shoot_worker_robot(worker)
worker.become_frightened()  # Рабочий пугается

# Вывод итоговой сетки на экран
print()
print()
for i in range(len(grid)):
    for j in range(len(grid[0])):
        print(grid[i][j].get_texture(), end="")
    print()

# Вывод итогового инвентаря роботов
fighter.print_info()
worker.print_info()

# Рабочий сканирует боевого робота
print()
worker.scan_combat_robot(fighter)

# В результате сканирования должно быть выведено имя боевого робота
# Если сканер рабочего сломан, то будет сообщение об этом
logger.info("==== Run Finish ====")
