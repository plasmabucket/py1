from my_shapes import triangle
from my_shapes.my_circle import circle

import datetime


base_len: int = 17  # основание треугольника
height: int = 9  # высота треугольника
rad: int = 8  # радиус окружности
today: datetime.datetime = datetime.datetime.now()
later: datetime.datetime = today + datetime.timedelta(hours=1)

print(f"Сегодня уже {today:%d %b}, на часах {today:%H:%M},")
print(f"а у треугольника с основанием {base_len} и высотой {height}"
      f" площадь всё ещё {triangle.triangle_area(base_len, height):.2f}!")
print("Посмотрите на него!")
print(triangle.triangle_print(base_len, height))
print(f"В {later:%H:%M} у окружности радиусом {rad} длина"
      f" будет {circle.circle_len(rad):.2f}")
