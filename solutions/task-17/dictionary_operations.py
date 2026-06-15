import random
import string


# Создаём список с ключами.
keys: list[int] = []
i: int = 0
while i < 100:
    num_random: int = random.randint(1, 1000)
    if num_random not in keys:
        keys.append(num_random)
        i += 1

# Заполняем словарь случайными парами.
dictionary: dict[int, str] = {}
ascii_len: int = len(string.ascii_letters)
for key in keys:
    char: str = string.ascii_letters[random.randint(0, ascii_len - 1)]
    dictionary[key] = char + str(random.randint(1, 100))

# Считывание из словаря по ключам.
for key in keys:
    print(f"Ключ: {key:4}  Значение: {dictionary[key]}")

# Удаление пар из словаря.
for key in keys:
    del dictionary[key]
# Вывод пустого словаря.
print("Пустой словарь:", dictionary)
