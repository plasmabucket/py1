# Рисует круг из звёздочек
def circle_print(rad: int) -> str:
    center: int = rad - 1  # поправка для координат сетки
    result: str = ""
    for i in range(rad * 2 - 1):
        for j in range(rad * 2 - 1):
            if (i - center)*(i - center) + (j - center)*(j - center) < rad*rad:
                result += "*"
            else:
                result += " "
        result += "\n"
    return result


# Вычисляет длину окружности
def circle_len(r: float) -> float:
    return 2 * 3.14159 * r  # L = 2 * PI * Rad


# Вычисляет площадь окружности
def circle_area(r: float) -> float:
    return 3.14159 * r * r  # S = PI * Rad^2
