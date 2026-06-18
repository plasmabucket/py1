# Повторяет вызов функции указанное количество раз.
def repeat(count: int):
    def repeat_decorator(func):
        def wrapper(arg: int) -> int:
            result: int = func(arg)
            for i in range(count - 1):
                result = func(result)
            return result
        return wrapper
    return repeat_decorator

# Ловит ошибку деления на ноль при вызове функции.
def none_on_zero_div_error(func):
    def wrapper(*args, **kwargs):
        try:
            result = func(*args, **kwargs)
        except ZeroDivisionError as ex:
            print(ex)  # Сообщает об ошибке
            return None
        return result
    return wrapper


# Трижды прибавляем 2 к числу.
@repeat(3)
def add_two(a: int) -> int:
    return a + 2

# Делим числа, но ловим деление на ноль.
@none_on_zero_div_error
def divide(a: int, b: int) -> int:
    return a // b


# Использование функций.
x: int = 2
y: int = 0
print(f"{x=}, {y=}")
x = add_two(x)  # Из-за декоратора прибавляется 6, а не 2
print(f"{x=}, {y=}")
print(f"x // y = {divide(x, y)}")  # Декоратор ловит ошибку
