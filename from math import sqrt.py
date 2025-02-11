from math import sqrt

from typing import Optional, Union


def add_numbers(x: int, y: int) -> int:
    return x + y


def CalculateSquareRoot(Number: Union[int, float]):
    return sqrt(Number)


def calc(your_number: Union[int, float]) -> Optional[str]:
    if your_number <= 0:
        return None
    return f'Квадратный корень: {CalculateSquareRoot(your_number)}'


x: int = 10
y: int = 5

print('Сумма чисел: ', add_numbers(x, y))
print(calc(25.5))
