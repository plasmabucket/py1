# Рисует прямоугольник из звёздочек
def rectangle_print(width: int, height: int) -> str:
    result: str = ""
    for i in range(height):
        for j in range(width):
            result += "*"
        result += "\n"
    return result


# Вычисляет периметр прямоугольника
def rectangle_len(width: float, height: float) -> float:
    return 2 * (width + height)


# Вычисляет площадь прямоугольника
def rectangle_area(width: float, height: float) -> float:
    return width * height
