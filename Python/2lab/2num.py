import math

square = lambda a: a ** 2
triangle = lambda a, b, c: math.sqrt(((a + b + c) / 2) * (((a + b + c) / 2) - a) * (((a + b + c) / 2) - b) * (((a + b + c) / 2) - c))
rhombus = lambda a, b: (a * b) / 2

L = [['S', 'd', 'S', 'T', 'R'], [7, 5, 3, 6], [3, 5], [5]]

def func(L: list):
    try:
        cm = L[0].pop(0)
    except IndexError:
        exit()
    cm == 'S' and print(square(L[1].pop(0))) or \
    cm == 'T' and print(triangle(L[1].pop(0), L[2].pop(0), L[3].pop(0))) or \
    cm == 'R' and print(rhombus(L[1].pop(0), L[2].pop(0))) or \
    cm != 'S' and cm != 'T' and cm != 'R' and print('Такого варианта нет в меню')
    return func(L)

func(L)