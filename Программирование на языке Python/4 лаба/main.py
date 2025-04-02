from tkinter import *
import tkinter as tk
from tkinter import messagebox


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

    def __init__(self, code, workExperience, surname="Не указано", firstName="Не указано", patronymic="Не указано", gender="Не указано", birthday="Не указано", address="Не указано", phone="Не указано", subjectTaught="Не указано"):
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


teachers = []

def add_teacher():
    code = code_entry.get()
    if not code:
        messagebox.showwarning("Предупреждение", "Код не может быть пустым")
        return
    try:
        code = int(code)
        if any(teacher.code == code for teacher in teachers):
            messagebox.showwarning("Предупреждение", "Преподаватель с таким кодом уже зарегистрирован")
            return
        if (code < 0):
            messagebox.showwarning("Предупреждение", "Код не может быть меньше нуля")
            return
    except ValueError:
        messagebox.showerror("Ошибка ввода", "Код должен быть числом")
        return

    surname = surname_entry.get()
    firstName = firstName_entry.get()
    patronymic = patronymic_entry.get()
    gender = gender_var.get()
    birthday = birthday_entry.get()
    address = address_entry.get()
    phone = phone_entry.get()
    subjectTaught = subjectTaught_entry.get()

    workExperience = workExperience_entry.get()
    if not workExperience:
        messagebox.showwarning("Предупреждение", "Опыт работы не может быть пустым")
        return
    try:
        workExperience = int(workExperience)
        if (workExperience <= 0):
            messagebox.showwarning("Предупреждение", "Опыт работы не может быть меньше или равен нулю")
            return
    except ValueError:
        messagebox.showerror("Ошибка ввода", "Стаж работы должен быть числом")
        return

    script = "Teacher(code=code, workExperience=workExperience"
    if surname != '':
        script += ', surname=surname'
    if firstName != '':
        script += ', firstName=firstName'
    if patronymic != '':
        script += ', patronymic=patronymic'
    if gender != '':
        script += ', gender=gender'
    if birthday != '':
        script += ', birthday=birthday'
    if address != '':
        script += ', address=address'
    if phone != '':
        script += ', phone=phone'
    if subjectTaught != '':
        script += ', subjectTaught=subjectTaught'
    script += ")"

    teacher = eval(script)
    teachers.append(teacher)
    update_teacher_codes()
    messagebox.showinfo("Успех", "Преподаватель добавлен")
    clear_entries()

def update_teacher_codes():
    teacher_codes = [teacher.code for teacher in teachers]
    selected_teacher_code.set("")
    delete_code_menu['menu'].delete(0, 'end')
    for code in teacher_codes:
        delete_code_menu['menu'].add_command(label=code, command=tk._setit(selected_teacher_code, code))

def delete_teacher():
    code = selected_teacher_code.get()
    if not code:
        messagebox.showwarning("Предупреждение", "Код не может быть пустым")
        return
    try:
        code = int(code)
        for teacher in teachers:
            if teacher.code == code:
                teachers.remove(teacher)
                update_teacher_codes()
                messagebox.showinfo("Успех", "Успешное удаление")
                return
        messagebox.showwarning("Предупреждение", "Нет преподавателя с таким кодом")
    except ValueError:
        messagebox.showerror("Ошибка ввода", "Код должен быть числом")

def print_teachers():
    if not teachers:
        messagebox.showinfo("Список преподавателей", "Список пуст")
        return
    # Создаем новое окно
    top = Toplevel()
    top.title("Список преподавателей")
    text_area = Text(top, wrap='word', font=font)
    text_area.pack(side='left', fill='both', expand=True)

    scrollbar = Scrollbar(top, orient=VERTICAL, command=text_area.yview)
    scrollbar.pack(side=RIGHT, fill=Y)
    text_area.config(yscrollcommand=scrollbar.set)

    teachers_info = "\n".join(str(teacher) for teacher in teachers)
    text_area.insert('1.0', teachers_info)
    text_area.config(state='disabled')


def search_teacher():
    try:
        year = int(search_year_entry.get())
        found_teachers = [str(teacher) for teacher in teachers if teacher.workExperience >= year]
        if found_teachers:
            # Создаем новое окно
            top = Toplevel()
            top.title("Список преподавателей")
            text_area = Text(top, wrap='word', font=font)
            text_area.pack(side='left', fill='both', expand=True)

            scrollbar = Scrollbar(top, orient=VERTICAL, command=text_area.yview)
            scrollbar.pack(side=RIGHT, fill=Y)
            text_area.config(yscrollcommand=scrollbar.set)

            teachers_info = "\n".join(found_teachers)
            text_area.insert('1.0', teachers_info)
            text_area.config(state='disabled')
        else:
            messagebox.showinfo("Результаты поиска", "Список пуст")
    except ValueError:
        messagebox.showerror("Ошибка ввода", "Стаж работы должен быть числом")


def clear_entries():
    code_entry.delete(0, tk.END)
    surname_entry.delete(0, tk.END)
    firstName_entry.delete(0, tk.END)
    patronymic_entry.delete(0, tk.END)
    birthday_entry.delete(0, tk.END)
    address_entry.delete(0, tk.END)
    phone_entry.delete(0, tk.END)
    subjectTaught_entry.delete(0, tk.END)
    workExperience_entry.delete(0, tk.END)
    search_year_entry.delete(0, tk.END)

def go_to_menu():
    table(frame1)
def forget_all():  # Скрытие всех фреймов
    frame1.pack_forget()
    frame2.pack_forget()
    frame3.pack_forget()
    frame4.pack_forget()

def table(var):  # Отображение выбранного фрейма
    forget_all()
    var.pack(fill=BOTH, expand=True)

def next_command():
    if var.get() == 1:
        table(frame2)
    elif var.get() == 2:
        table(frame3)
    elif var.get() == 3:
        table(frame4)
    elif var.get() == 0:
        table(frame1)

# Создание главного окна
root = tk.Tk()
root.title("Преподаватели")
root.geometry("600x900")


var = IntVar(value=0)
font = ("Helvetica", 16)
button_color = "#744DA9"

# Создание фреймов для колонок
frame1 = tk.Frame(root)
frame2 = tk.Frame(root)
frame3 = tk.Frame(root)
frame4 = tk.Frame(root)

# Элементы frame1
search_text = Label(frame1, text="Выберите вариант: ", font=font)
search_text.pack(anchor="nw", padx=20, pady=(100, 15))
add_button = Radiobutton(frame1, text="Добавление преподавателя", variable=var, value=1, font=font, justify="left", wraplength=530)
add_button.pack(anchor="nw", padx=20, pady=10)
display_button = Radiobutton(frame1, text="Удаление преподавателя", variable=var, value=2, font=font, justify="left", wraplength=430)
display_button.pack(anchor="nw", padx=20, pady=10)
search_button = Radiobutton(frame1, text="Вывод всех преподавателей или преподавателей с определённым стажем", variable=var, value=3, font=font, justify="left", wraplength=430)
search_button.pack(anchor="nw", padx=20, pady=10)
next_button = Button(frame1, text='Далее', padx=40, pady=15, font=font, command=next_command, bg=button_color, activebackground=button_color, fg="white")
next_button.pack(anchor="ne", padx=20, pady=20)

# Элементы frame2
add_teacher_label = Label(frame2, text="Добавление преподавателя", font=font)
add_teacher_label.pack(anchor="n", padx=20, pady=(20, 10))
code_label = Label(frame2, text="Код:", font=font)
code_label.pack(anchor="nw", padx=20, pady=(5, 0))
code_entry = Entry(frame2, font=font)
code_entry.pack(anchor="nw", padx=20, pady=(0, 5))
surname_label = Label(frame2, text="Фамилия:", font=font)
surname_label.pack(anchor="nw", padx=20, pady=(5, 0))
surname_entry = Entry(frame2, font=font)
surname_entry.pack(anchor="nw", padx=20, pady=(0, 5))
first_name_label = Label(frame2, text="Имя:", font=font)
first_name_label.pack(anchor="nw", padx=20, pady=(5, 0))
firstName_entry = Entry(frame2, font=font)
firstName_entry.pack(anchor="nw", padx=20, pady=(0, 5))
patronymic_label = Label(frame2, text="Отчество:", font=font)
patronymic_label.pack(anchor="nw", padx=20, pady=(5, 0))
patronymic_entry = Entry(frame2, font=font)
patronymic_entry.pack(anchor="nw", padx=20, pady=(0, 5))
gender_label = Label(frame2, text="Пол:", font=font)
gender_label.pack(anchor="nw", padx=20, pady=(5, 0))
gender_var = StringVar(value="м")
male_radio = Radiobutton(frame2, text="Мужской", variable=gender_var, value="м", font=font)
male_radio.pack(anchor="nw", padx=20, pady=(0, 5))
female_radio = Radiobutton(frame2, text="Женский", variable=gender_var, value="ж", font=font)
female_radio.pack(anchor="nw", padx=20, pady=(0, 5))
birthday_label = Label(frame2, text="День рождения:", font=font)
birthday_label.pack(anchor="nw", padx=20, pady=(5, 0))
birthday_entry = Entry(frame2, font=font)
birthday_entry.pack(anchor="nw", padx=20, pady=(0, 5))
address_label = Label(frame2, text="Адрес:", font=font)
address_label.pack(anchor="nw", padx=20, pady=(5, 0))
address_entry = Entry(frame2, font=font)
address_entry.pack(anchor="nw", padx=20, pady=(0, 5))
phone_label = Label(frame2, text="Номер телефона:", font=font)
phone_label.pack(anchor="nw", padx=20, pady=(5, 0))
phone_entry = Entry(frame2, font=font)
phone_entry.pack(anchor="nw", padx=20, pady=(0, 5))
subject_label = Label(frame2, text="Преподаваемый предмет:", font=font)
subject_label.pack(anchor="nw", padx=20, pady=(5, 0))
subjectTaught_entry = Entry(frame2, font=font)
subjectTaught_entry.pack(anchor="nw", padx=20, pady=(0, 5))
work_experience_label = Label(frame2, text="Стаж работы:", font=font)
work_experience_label.pack(anchor="nw", padx=20, pady=(5, 0))
workExperience_entry = Entry(frame2, font=font)
workExperience_entry.pack(anchor="nw", padx=20, pady=(0, 5))
add_teacher_button = Button(frame2, text="Добавить преподавателя", command=add_teacher, bg=button_color, activebackground=button_color, font=font, fg="white")
add_teacher_button.pack(anchor="nw", padx=20, pady=(5, 0))
menu_button = Button(frame2, text="Назад в меню", command=go_to_menu, bg=button_color, activebackground=button_color, font=font, fg="white")
menu_button.pack(anchor="nw", pady=5, padx=20)

# Элементы frame3
delete_label = Label(frame3, text="Удаление преподавателя", font=font)
delete_label.pack(pady=(100, 15))
delete_code_label = Label(frame3, text="Выберите код преподавателя для удаления:", font=font)
delete_code_label.pack(anchor="nw", padx=20, pady=(20, 5))
selected_teacher_code = StringVar(frame3)
selected_teacher_code.set("")
delete_code_menu = OptionMenu(frame3, selected_teacher_code, "")
delete_code_menu.config(width=50, font=font)
delete_code_menu.pack(anchor="nw", padx=20, pady=(5, 20))
delete_button = Button(frame3, text="Удалить преподавателя", command=delete_teacher, bg=button_color, activebackground=button_color, font=font, fg="white")
delete_button.pack(anchor="nw", pady=(5, 20), padx=20)
menu_button = Button(frame3, text="Назад в меню", command=go_to_menu, bg=button_color, activebackground=button_color, font=font, fg="white")
menu_button.pack(anchor="nw", pady=(5, 20), padx=20)

# Элементы frame4
search_label = Label(frame4, text="Поиск преподавателей по стажу", font=font)
search_label.pack(pady=(100, 10))
experience_label = Label(frame4, text="Стаж работы:", font=font)
experience_label.pack(anchor="nw", padx=20)
search_year_entry = Entry(frame4, font=font)
search_year_entry.pack(anchor="nw", pady=(5, 20), padx=20)
search_button = Button(frame4, text="Поиск", command=search_teacher, bg=button_color, activebackground=button_color, font=font, fg="white")
search_button.pack(anchor="nw", pady=(5, 20), padx=20)
menu_button = Button(frame4, text="Назад в меню", command=go_to_menu, bg=button_color, activebackground=button_color, font=font, fg="white")
menu_button.pack(anchor="nw", pady=(5, 20), padx=20)
print_button = Button(frame4, text="Вывести список всех преподавателей", command=print_teachers, bg=button_color, activebackground=button_color, font=font, fg="white")
print_button.pack(pady=100)

update_teacher_codes()
frame1.pack(fill=BOTH, expand=True)
root.mainloop()