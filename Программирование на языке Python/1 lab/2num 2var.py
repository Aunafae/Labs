list = [1, 5.5, 'sun', 3, 'moon', 8.2]

while(True):
    choice = input("\n1 - Показать значения списка на экране\n"
                   "2 - Добавить новый элемент (любого типа) в конец списка\n"
                   "3 - Удалить указанный Вами элемент\n"
                   "4 - Сформировать кортеж, состоящий из элементов, стоящих на нечетных позициях списка; вывести содержимое кортежа на экран\n"
                   "5 - Найти произведение всех вещественных элементов списка\n"
                   "6 - Сформировать строку из значений элементов списка и посчитать количество знаков препинания в строке\n"
                   "7 - Задать с клавиатуры множество M1, сформировать множество M2 из списка; вывести на экран множество, полученное путем пересечения множеств M1 и M2\n"
                   "8 - Получить из списка словарь, ключом каждого элемента сделать позицию элемента в словаре; построчно отобразить на экране элементы словаря с ключом меньше 5\n"
                   "0 - ВЫХОД\n\n"
                   "Введите число от 1 до 8 :   ")
    if choice == '1':
        print(list)
    elif choice == '2':
        element = input("Введите добавляемый элемент: ")
        try:
            list.append(int(element))
        except:
            try:
                list.append(float(element))
            except:
                list.append((element))
    elif choice == '3':
        try:
            list.pop(int(input("Введите индекс удаляемого элемента:")))
        except ValueError:
            print("Введите числовое значение")
        except IndexError:
            print("Такого индекса в списке нет")
    if choice == '4':
        tuple = ()
        for i in range(len(list)):
            if i % 2 != 0:
                tuple += (list[i],)
        print("Кортеж: ", tuple)
    elif choice == '5':
        mul = 1
        for i in range(len(list)):
            if type(list[i]) is float:
                mul *= list[i]
        print("Произведение всех вещественных чисел списка: ", mul)
    elif choice == '6':
        text = ""
        symbols = ['.', ',', ';', ':', '!', '?', '-', '(', ')', '"', "'"]
        count = 0
        for i in range(len(list)):
            text += str(list[i])
        for i in range(len(text)):
            if symbols.__contains__(text[i]) is True:
                count += 1
        print(count)
    elif choice == '7':
        your_list = []
        while True:
            word = input("Для выхода введите 'exit'\nВведите элемент множества: ")
            your_list.append(word)
            if word == 'exit':
                break
        set1 = set(your_list)
        set2 = set(list)
        set3 = set1.union(set2)
        print(set3)
    elif choice == '8':
        dictionary = {}
        for i in range(len(list)):
            dictionary[i] = str(list[i])
        if len(list) >= 5:
            for i in range(5):
                print("{0}: {1}".format(i, dictionary[i]))
        else:
            for key, value in dictionary.items():
                print("{0}: {1}".format(key, value))
    elif choice == '0':
        print("Выход...")
        break