import sqlite3
from tkinter import *
import tkinter as tk
from tkinter import messagebox

class Teacher:
    code = None
    surname = None
    firstname = None
    patronymic = None
    gender = None
    birthday = None
    address = None
    phone = None
    subjectTaught = None
    workExperience = None

    def __init__(self, code, surname="Не указано", firstname="Не указано", patronymic="Не указано", gender="Не указано", birthday="Не указано", address="Не указано", phone="Не указано", workExperience="Не указано"):
        self.code = code
        self.surname = surname
        self.firstname = firstname
        self.patronymic = patronymic
        self.gender = gender
        self.birthday = birthday
        self.address = address
        self.phone = phone
        self.workExperience = workExperience


    def __str__(self):
        data = "\n"
        data += "Код: " + str(self.code) + "\n"
        data += "Фамилия: " + self.surname + "\n"
        data += "Имя: " + self.firstname + "\n"
        data += "Отчество: " + self.patronymic + "\n"
        data += "Пол: " + self.gender + "\n"
        data += "День рождения: " + self.birthday + "\n"
        data += "Адрес: " + self.address + "\n"
        data += "Номер телефона: " + self.phone + "\n"
        data += "Опыт работы: " + self.workExperience + "\n"
        return data

def connect_db():
    conn = sqlite3.connect('Teachers.db')
    return conn

def create_tables():
    conn = connect_db()
    cursor = conn.cursor()
    cursor.execute("""CREATE TABLE IF NOT EXISTS Teacher (
        code INTEGER PRIMARY KEY AUTOINCREMENT,
        surname TEXT, 
        firstname TEXT, 
        patronymic TEXT,
        gender TEXT,
        birthday TEXT,
        address TEXT,
        phone TEXT,
        workExperience INTEGER);""")
    cursor.execute("""CREATE TABLE IF NOT EXISTS Subjects (
        idSubjects INTEGER PRIMARY KEY AUTOINCREMENT,
        subjectsTaught TEXT);""")
    cursor.execute("""CREATE TABLE IF NOT EXISTS TeacherSubjects (
        codeTeacher INTEGER,
        idSubjects INTEGER,
        FOREIGN KEY (codeTeacher) REFERENCES Teacher (code),
        FOREIGN KEY (idSubjects) REFERENCES Subjects (idSubjects),
        PRIMARY KEY (codeTeacher, idSubjects));""")
    conn.commit()
    conn.close()

def add_teacher():
    surname = surname_entry.get()
    firstname = firstname_entry.get()
    patronymic = patronymic_entry.get()
    gender = gender_var.get()
    birthday = birthday_entry.get()
    address = address_entry.get()
    phone = phone_entry.get()
    workExperience = int(workExperience_entry.get())
    subjects = subject_entry.get().split(",")

    conn = connect_db()
    cursor = conn.cursor()
    try:
        cursor.execute(
            "INSERT INTO Teacher (surname, firstname, patronymic, gender, birthday, address, phone, workExperience) "
            "VALUES (?, ?, ?, ?, ?, ?, ?, ?);",
            (surname, firstname, patronymic, gender, birthday, address, phone, workExperience))

        teacher_code = cursor.lastrowid
        for subject in subjects:
            subject = subject.strip()
            cursor.execute("INSERT OR IGNORE INTO Subjects (subjectsTaught) VALUES (?);", (subject,))
            cursor.execute("SELECT idSubjects FROM Subjects WHERE subjectsTaught = ?;", (subject,))
            subject_id = cursor.fetchone()[0]
            cursor.execute("INSERT INTO TeacherSubjects (codeTeacher, idSubjects) VALUES (?, ?);",
                           (teacher_code, subject_id))
        messagebox.showinfo("Успех!", f"Преподаватель добавлен")
    except sqlite3.Error as e:
        messagebox.showerror("Ошибка!", f"Ошибка добавления преподавателя: {e}")
    conn.commit()
    conn.close()
    clear_entries()
    update_teacher_codes()

def delete_teacher():
    code = int(selected_teacher_code.get())
    conn = connect_db()
    cursor = conn.cursor()
    cursor.execute("DELETE FROM Teacher WHERE code = ?", (code,))
    cursor.execute("DELETE FROM TeacherSubjects WHERE codeTeacher = ?", (code,))
    conn.commit()
    messagebox.showinfo("Успех!", f"Преподаватель удалён")
    conn.close()
    update_teacher_codes()

def get_teachers():
    conn = connect_db()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM Teacher")
    teachers = cursor.fetchall()
    conn.close()

    if not teachers:
        messagebox.showinfo("Список преподавателей", "Список пуст")
        return

    top = Toplevel()
    top.title("Список преподавателей")
    text_area = Text(top, wrap='word', font=("Helvetica", 16))
    text_area.pack(side='left', fill='both', expand=True)
    scrollbar = Scrollbar(top, orient=VERTICAL, command=text_area.yview)
    scrollbar.pack(side=RIGHT, fill=Y)
    text_area.config(yscrollcommand=scrollbar.set)

    conn = connect_db()
    cursor = conn.cursor()
    teachers_info = ""

    for teacher in teachers:
        cursor.execute("""
                   SELECT subjectsTaught FROM TeacherSubjects 
                   JOIN Subjects ON TeacherSubjects.idSubjects = Subjects.idSubjects 
                   WHERE codeTeacher = ?;
               """, (teacher[0],))
        subjects = cursor.fetchall()
        subjects_list = ', '.join([subject[0] for subject in subjects]) if subjects else "Нет предметов"

        teachers_info += f"ФИО: {teacher[1]} {teacher[2]} {teacher[3]}\nПол: {teacher[4]}\nДень рождения: {teacher[5]}\nАдрес: {teacher[6]}\nТелефон: {teacher[7]}\nОпыт работы: {teacher[8]}\nПредметы: {subjects_list}\n\n"

    conn.close()
    text_area.insert('1.0', teachers_info)
    text_area.config(state='disabled')

def update_teacher_codes():
    selected_teacher_code.set("")
    delete_code_menu['menu'].delete(0, 'end')

    conn = connect_db()
    cursor = conn.cursor()
    cursor.execute("SELECT code, firstname, surname, patronymic FROM Teacher")
    all_teachers = cursor.fetchall()
    conn.close()

    for teacher in all_teachers:
        display_text = f"#{teacher[0]} {teacher[1]} {teacher[2]} {teacher[3]}"
        delete_code_menu['menu'].add_command(label=display_text, command=tk._setit(selected_teacher_code, teacher[0]))


def clear_entries():
    surname_entry.delete(0, tk.END)
    firstname_entry.delete(0, tk.END)
    patronymic_entry.delete(0, tk.END)
    birthday_entry.delete(0, tk.END)
    address_entry.delete(0, tk.END)
    phone_entry.delete(0, tk.END)
    workExperience_entry.delete(0, tk.END)
    subject_entry.delete(0, tk.END)

def show_frame(frame):
    frame1.pack_forget()
    frame2.pack_forget()
    frame3.pack_forget()
    frame4.pack_forget()
    frame.pack(fill=BOTH, expand=True)

def back_to_main():
    show_frame(frame1)

# Создание главного окна
root = tk.Tk()
root.title("Преподаватели")
root.geometry("900x800")

create_tables()

var = IntVar(value=0)
font = ("Helvetica", 16)
button_color = "#744DA9"

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
search_button = Radiobutton(frame1, text="Вывод всех преподавателей", variable=var, value=3, font=font, justify="left", wraplength=430)
search_button.pack(anchor="nw", padx=20, pady=10)
next_button = Button(frame1, text='Далее', padx=40, pady=15, font=font, command=lambda: get_teachers() if var.get() == 3 else show_frame(frame2 if var.get() == 1 else frame3), bg=button_color, activebackground=button_color, fg="white")
next_button.pack(anchor="ne", padx=20, pady=20)

# Элементы frame2
main_screen_button = Button(frame2, text="На главный экран", command=back_to_main, bg=button_color, activebackground=button_color, font=font, fg="white")
main_screen_button.pack(anchor="sw", padx=20, pady=(15, 0))

add_teacher_label = Label(frame2, text="Добавление преподавателя", font=font)
add_teacher_label.pack(anchor="n", padx=20, pady=(0, 10))
surname_label = Label(frame2, text="Фамилия:", font=font)
surname_label.pack(anchor="nw", padx=20, pady=(5, 0))
surname_entry = Entry(frame2, font=font)
surname_entry.pack(anchor="nw", padx=20, pady=(0, 5))
first_name_label = Label(frame2, text="Имя:", font=font)
first_name_label.pack(anchor="nw", padx=20, pady=(5, 0))
firstname_entry = Entry(frame2, font=font)
firstname_entry.pack(anchor="nw", padx=20, pady=(0, 5))
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
workExperience_label = Label(frame2, text="Опыт работы:", font=font)
workExperience_label.pack(anchor="nw", padx=20, pady=(5, 0))
workExperience_entry = Entry(frame2, font=font)
workExperience_entry.pack(anchor="nw", padx=20, pady=(0, 5))
subjects_label = Label(frame2, text="Предметы (через запятую):", font=font)
subjects_label.pack(anchor="nw", padx=20, pady=(5, 0))
subject_entry = Entry(frame2, font=font)
subject_entry.pack(anchor="nw", padx=20, pady=(0, 5))
add_teacher_button = Button(frame2, text="Добавить преподавателя", command=add_teacher, bg=button_color, activebackground=button_color, font=font, fg="white")
add_teacher_button.pack(anchor="nw", padx=20, pady=(5, 0))

# Элементы frame3
main_screen_button2 = Button(frame3, text="На главный экран", command=back_to_main, bg=button_color, activebackground=button_color, font=font, fg="white")
main_screen_button2.pack(anchor="sw", padx=20, pady=20)

delete_label = Label(frame3, text="Удаление преподавателя", font=font)
delete_label.pack(pady=(100, 15))
delete_code_label = Label(frame3, text="Выберите преподавателя для удаления:", font=font)
delete_code_label.pack(anchor="nw", padx=20, pady=(20, 5))
selected_teacher_code = StringVar(frame3)
delete_code_menu = OptionMenu(frame3, selected_teacher_code, "")
delete_code_menu.config(width=50, font=font)
delete_code_menu.pack(anchor="nw", padx=20, pady=(5, 20))
delete_button = Button(frame3, text="Удалить преподавателя", command=delete_teacher, bg=button_color, activebackground=button_color, font=font, fg="white")
delete_button.pack(anchor="nw", pady=(5, 20), padx=20)

# Инициализация
update_teacher_codes()
frame1.pack(fill=BOTH, expand=True)
root.mainloop()