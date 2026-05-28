from typing import List
import random

class Animal:
    def foo(self):
        pass

class Cat(Animal):
    def foo(self):
        print("Кошка мурлычет")

class Bird(Animal):
    def foo(self):
        print("Птица поет")


def list_of_500_animals(animals: List[Animal]) -> List[Animal]:
    animals_copy: List[Animal] = animals.copy()
    # очищаем список
    while len(animals_copy) > 0:
        animals_copy.pop(0)
    # заполняем случайными 500 объектами
    for i in range(500):
        if random.randint(1, 2) == 1:
            animals_copy.append(Cat())
        else:
            animals_copy.append(Bird())
    return animals_copy


# получаем список
random_animals: List[Animal] = [Cat(), Bird()]
random_animals = list_of_500_animals(random_animals)

# вызываем foo по списку
for i in range(len(random_animals)):
    random_animals[i].foo()

# В выводе чередуются мурлыканье кошек и пение птиц.

# Вывод получился таким т.к. происходит полиморфизм подтипов --
# метод foo переопределяется в зависимости от типа объекта, его
# вызывающего.
