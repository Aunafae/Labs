import math

while(True):
    a0, a1, a2, x = '', '', '', '';
    while (a0 == ''):
        try:
            a0 = float(input("a0 = "))
        except ValueError:
            print("введите числовое значение")
    while (a1 == ''):
        try:
            a1 = float(input("a1 = "))
        except ValueError:
            print("введите числовое значение")
    while (a2 == ''):
        try:
            a2 = float(input("a2 = "))
        except ValueError:
            print("введите числовое значение")
    while (x == ''):
        try:
            x = float(input("x = "))
        except ValueError:
            print("введите числовое значение")

    if (x == 0):
        print("Значение x не может быть равно 0")
        continue
    elif (x < 0) and (int(x)!=x):
        print('Отрицательный Х возводится в дробную степень. Нельзя!')
        continue
    elif (math.e**x**5 == 0):
        print("Крайне малое для вычислений число в знаменателе")
        continue
    elif (a0+a1*x**x+a2*math.pow(abs(math.sin(x)), 1/x))<0:
        print("Подкоренное выражение не может быть меньше 0")
        continue
    else:
        result = math.sqrt(a0+a1*x**x+a2*math.pow(abs(math.sin(x)), 1/x))+((5*a0)/(math.e**x**5))
        print(result)
        break