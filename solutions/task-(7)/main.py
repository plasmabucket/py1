from my_shapes import triangle
from my_shapes import rectangle
from my_shapes.my_circle import circle

print("Площадь треугольника:", triangle.triangle_area(17, 9))
print(triangle.triangle_print(17, 9))
print("Площадь прямоугольника:", rectangle.rectangle_area(11, 11))
print(rectangle.rectangle_print(11, 11))
print("Площадь круга:", circle.circle_area(8))
print(circle.circle_print(8))
