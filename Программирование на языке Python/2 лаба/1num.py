import math

a0, a1, a2, x = '', '', '', ''
try:
    a0 = float(input("a0 = "))
    a1 = float(input("a1 = "))
    a2 = float(input("a2 = "))
    x = float(input("x = "))
except ValueError:
    print("все значения должны быть целыми или вещественными числами")
    exit(-1)

result = lambda: ((x == 0 and "Значение x не может быть равно 0") or
                  (lambda: (((x < 0) and (int(x) != x)) and 'Отрицательный Х возводится в дробную степень. Нельзя') or
                           (lambda: (math.e**x**5 == 0 and 'Крайне малое для вычислений число в знаменателе') or
                                    (lambda: (((a0+a1*x**x+a2*math.pow(abs(math.sin(x)), 1/x))<0) and 'Подкоренное выражение не может быть меньше 0') or
                                             (math.sqrt(a0+a1*x**x+a2*math.pow(abs(math.sin(x)), 1/x))+((5*a0)/(math.e**x**5))))())())())
print(result())