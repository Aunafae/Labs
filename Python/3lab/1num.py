class Teacher:
    code = None
    surname = None
    firstName = None
    patronymic = None
    gender = None
    birthday = None
    address = None
    phone = None
    subjectTaught = None
    workExperience = None

    def __init__(self, code, surname, firstName, patronymic, gender, birthday, address, phone, subjectTaught, workExperience):
        self.code = code
        self.surname = surname
        self.firstName = firstName
        self.patronymic = patronymic
        self.gender = gender
        self.birthday = birthday
        self.address = address
        self.phone = phone
        self.subjectTaught = subjectTaught
        self.workExperience = workExperience

    def __str__(self):
        data = "\n"
        data += "Код: " + str(self.code) + "\n"
        data += "Фамилия: " + self.surname + "\n"
        data += "Имя: " + self.firstName + "\n"
        data += "Отчество: " + self.patronymic + "\n"
        data += "Пол: " + self.gender + "\n"
        data += "День рождения: " + self.birthday + "\n"
        data += "Адрес: " + self.address + "\n"
        data += "Номер телефона: " + self.phone + "\n"
        data += "Преподаваемый предмет: " + self.subjectTaught + "\n"
        data += "Стаж работы: " + str(self.workExperience) + "\n"
        return data
def add_teacher():
    print("\nЗаполняем данные о преподавателе")
    try:
        code = int(input('Код: '))
    except ValueError:
        print("код и стаж работы должны быть представлены числовыми данными")
        return
    for teacher in teachers:
        if code == teacher.code:
            print("Преподаватель с таким кодом уже зарегестрирован")
            return
    surname = input('Фамилия: ')
    firstName = input('Имя: ')
    patronymic = input('Отчество: ')
    gender = input('Пол (м/ж): ')
    birthday = input('День рождения: ')
    address = input('Адрес: ')
    phone = input('Номер телефона: ')
    subjectTaught = input('Преподаваемый предмет: ')
    try:
        workExperience = int(input('Стаж работы: '))
    except ValueError:
        print("код и стаж работы должны быть представлены числовыми данными")
        return
    teachers.append(Teacher(code, surname, firstName, patronymic, gender, birthday, address, phone, subjectTaught, workExperience))
def delete_teacher(code):
    for teacher in teachers:
        if teacher.code == code:
            teachers.remove(teacher)
            print("\nУспешное удаление\n")
            return
    print("\nНет преподавателя с таким номером\n")
def print_teachers():
    for teacher in teachers:
        print(teacher)
def search_teacher(year):
    for teacher in teachers:
        if teacher.workExperience >= year:
            print(teacher)

teachers = []
while(True):
    choice = input("\n0 - выход\n\
1 - добавить преподавателя\n\
2 - удалить данные о преподавателе\n\
3 - вывести список преподавателей\n\
4 - поиск преподавателей со стажем работы больше введённого\n\
Введите пункт меню: ")
    if choice == '0':
        print('Выход...')
        exit()
    elif choice == '1':
        add_teacher()
    elif choice == '2':
        try:
            code = int(input("Введите код удаляемого учителя: "))
        except ValueError:
            print("Код должен быть задан числовым значением")
            continue
        delete_teacher(code)
    elif choice == '3':
        print_teachers()
    elif choice == '4':
        try:
            year = int(input("Введите жалаемый стаж работы: "))
        except ValueError:
            print("Год должен быть задан числовым значением")
            continue
        search_teacher(year)
    else:
        print('Нет такого варианта в меню')