# Рисует треугольник из звёздочек
def triangle_print(base_len: int, height: int) -> str:
    result: str = ""
    # коэффициент наклона сторон с поправкой на координаты сетки
    k: float = 2 * (height - 1) / (base_len - 1)
    for i in range(height):
        for j in range(base_len):
            if (k * j - i - height + 1 < 0.1
                    and -k * j - i + height - 1 < 0.1):
                result += "*"
            else:
                result += " "
        result += "\n"
    return result


# Вычисляет периметр треугольника
def triangle_len(side_a: float, side_b: float, side_c: float) -> float:
    return side_a + side_b + side_c


# Вычисляет площадь треугольника по высоте и основанию
def triangle_area(base_len: float, height: float) -> float:
    return 0.5 * height * base_len
