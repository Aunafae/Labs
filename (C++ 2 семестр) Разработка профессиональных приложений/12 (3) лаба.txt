#include <iostream>
#include <string>

using namespace std;

struct Student
{
    int number;
    string FIO;
    Student* next = NULL;
};

struct Group
{
    string name, code;
    Student* students = NULL;
    Group* next;
    Group* prev;
};

Group* add_gr()
{
    string name, code;
    cout << "Введите название группы: ";
    getline(cin, name, '\n');
    cout << "Введите код группы: ";
    getline(cin, code, '\n');

    Group* g = new Group();
    g->name = name;
    g->code = code;
    return g;
}

Student* add_st()
{
    string FIO;
    int number;
    cout << "Введите имя студента: ";
    getline(cin, FIO, '\n');
    cout << "Введите номер зачётки: ";
    cin >> number;
    cin.ignore();

    Student* s = new Student();
    s->FIO = FIO;
    s->number = number;
    return s;
}

void add_group(Group*& group)
{
    Group* g = add_gr();

    if (!group)
    {
        group = g;
        group->next = group;
        group->prev = group;
        return;
    }
    Group* new_gr = group;

    while (true)
    {
        if (new_gr->code == g->code)
        {
            cout << "Группа с таким кодом уже существует" << endl << endl;
            delete g;
            return;
        }
        new_gr = new_gr->next;
        if (new_gr == group)
        {
            break;
        }
    }
    g->prev = group->prev;
    g->next = group;
    group->prev->next = g;
    group->prev = g;
}

void add_student(Group*& group, string code)
{
    if (!group)
    {
        cout << "Нет такой группы" << endl << endl;
        return;
    }
    Group* g = group;

    while (g->code != code) {
        g = g->next;
        if (g == group) {
            cout << "Нет группы с таким кодом" << endl << endl;
            return;
        }
    }

    Student* s = add_st();
    if (!g->students)
    {
        g->students = s;
        return;
    }
    Student* last_st = g->students;
    while (last_st->next) {
        last_st = last_st->next;
    }
    last_st->next = s;
}

void remove_group(Group*& group, string code)
{
    if (!group)
    {
        cout << "Нет такой группы" << endl << endl;
        return;
    }
    Group* g = group;

    while (g->code != code)
    {
        g = g->next;
        if (g == group)
        {
            cout << "Нет группы с таким кодом" << endl << endl;
            return;
        }
    }

    Student* s = g->students;
    Student* prev_st;
    while (s)
    {
        prev_st = s;
        s = s->next;
        delete prev_st;
    }

    if (group == group->next)
    {
        delete group;
        group = nullptr;
        return;
    }

    if (group == g)
    {
        group->prev->next = g->next;
        group->next->prev = group->prev;
        group = g->next;
        delete g;
        return;
    }
    g->next->prev = g->prev;
    g->prev->next = g->next;
    delete g;
}

void remove_student(Group* group, int number)
{
    if (!group)
    {
        cout << "Нет групп" << endl << endl;
        return;
    }
    Group* g = group;

    bool found = false;
    Student* s = NULL;
    Student* prev_st = NULL;
    while (true)
    {
        prev_st = NULL;
        s = g->students;
        while (s)
        {
            if (s->number == number)
            {
                found = true;
                break;
            }
            prev_st = s;
            s = s->next;
        }
        if (found)
        {
            break;
        }
        g = g->next;
        if (g == group)
        {
            break;
        }
    }
    if (!found)
    {
        cout << "Нет студента с таким номером зачётки" << endl << endl;
        return;
    }

    if (!prev_st)
    {
        group->students = s->next;
    }
    else
    {
        prev_st->next = s->next;
    }
    delete s;
}

void change_student(Group* group, int number)
{
    if (!group)
    {
        cout << "Нет групп" << endl << endl;
        return;
    }
    Group* g = group;

    bool found = false;
    Student* s = NULL;
    while (true) {
        s = g->students;
        while (s) {
            if (s->number == number) {
                found = true;
                break;
            }
            s = s->next;
        }
        if (found)
        {
            break;
        }
        g = g->next;
        if (g == group)
        {
            break;
        }
    }
    if (!found)
    {
        cout << "Нет студента с таким номером зачётки" << endl;
        return;
    }

    string FIO;
    int new_number;
    cout << "Студент: " << s->FIO << "   " << s->number << endl << endl;
    getchar();
    cout << "Введите новое ФИО студента: ";
    getline(cin, FIO, '\n');
    s->FIO = FIO;
    cout << "Введите новый номер зачётки: ";
    cin >> new_number;
    cin.ignore();
    s->number = new_number;
    cout << endl << "Данные изменены" << endl << endl;
}

void print(Group* group)
{
    if (!group)
    {
        cout << "Нет групп" << endl << endl;
        return;
    }
    Group* g = group;

    while (true)
    {
        cout << "--------------------------------------------------" << endl;
        cout << "имя: " << g->name << "  код: " << g->code << endl << endl;
        Student* s = g->students;
        int counter = 1;
        if (!s)
        {
            cout << "В группе нет студентов" << endl << endl;
        }
        else
        {
            while (s)
            {
                cout << counter++ << ". " << s->FIO << "   " << s->number << endl;
                s = s->next;
            }
        }
        cout << "--------------------------------------------------" << endl << endl;

        g = g->next;
        if (g == group)
        {
            break;
        }
    }
}

void remove(Group*& group)
{
    if (group) group->prev->next = NULL;   //разомкнуть конец кольца
    Group* prev_g;
    while (group) {
        Student* s = group->students;
        Student* prev_s;
        while (s) {
            prev_s = s;
            s = s->next;
            delete prev_s;
        }
        prev_g = group;
        group = group->next;
        delete prev_g;
    }
}

int main()
{
    setlocale(LC_ALL, "Russian");
    int index = 0;
    string c;

    Group* group = NULL;

    while (c[0] != '8')
    {
        cout << "Выберите один из пунктов:\n1) Добавить группу\n2) Добавить студента в группу\n3) Удалить группу\n4) Удалить студента из группы\n5) Вывод данных\n6) Изменение студента в группе\n7) Очистка \n8) Выход" << endl << ": ";
        getline(cin, c);
        cout << endl << endl;

        if (c[0] == '1' && c.length() == 1)
        {
            add_group(group);
            cout << endl;
        }

        else if (c[0] == '2' && c.length() == 1)
        {
            string code;
            if (!group)
            {
                cout << "Ещё нет никаких групп" << endl << endl;
            }
            else
            {
                cout << "Введите код группы студента: ";
                getline(cin, code, '\n');
                add_student(group, code);
                cout << endl << endl;
            }
        }

        else if (c[0] == '3' && c.length() == 1)
        {
            string code;
            if (!group)
            {
                cout << "Ещё нет никаких групп" << endl << endl;
            }
            else
            {
                cout << "Введите код группы: ";
                getline(cin, code, '\n');
                remove_group(group, code);
                cout << endl << endl;
            }
        }

        else if (c[0] == '4' && c.length() == 1)
        {
            int number;
            if (!group)
            {
                cout << "Ещё нет никаких групп" << endl << endl;
            }
            cout << "Введите номер зачётки студента: ";
            cin >> number;
            cin.ignore();
            cout << endl;
            remove_student(group, number);
        }

        else if (c[0] == '5' && c.length() == 1)
        {
            print(group);
        }

        else if (c[0] == '6' && c.length() == 1)
        {
            int number;
            cout << "Введите номер зачётки студента: ";
            cin >> number;
            cin.ignore();
            cout << endl << endl;
            change_student(group, number);
        }

        else if (c[0] == '7' && c.length() == 1)
        {
            remove(group);
            cout << "Список групп и студентов был очищен" << endl << endl;
        }

        else if (c[0] == '8' && c.length() == 1)
        {
            remove(group);
        }

        else if (!c.length())
        {
            cout << "Вы ничего не ввели, попробуйте ещё раз" << endl << endl;
        }

        else
        {
            cout << "Вы ввели неправильное число, попробуйте ещё раз" << endl << endl;
        }
    }

    return 0;
}
