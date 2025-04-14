#include <iostream>
#include <string>

using namespace std;

void odd(int size);

void even(int size)
{
    if (size & 1)
    {
        odd(size);
    }
    else
    {
        cout << "Чётна" << endl;
    }
}

void odd(int size)
{
    if (size & 1)
    {
        cout << "Нечётна" << endl;
    }
    else
    {
        even(size);
    }
}

bool check(string str, int i, int result = 0)
{
    if (str[i + 1] == '\0')
    {
        return result;
    }
    else
    {
        return check(str, ++i, not(result));
    }
}

void check2(string str, int beginning, int end, int size)
{
    if (str[beginning] == str[end])
    {
        if (beginning == (size - 1))
        {
            cout << "Палиндром" << endl;
            return;
        }
        beginning++;
        end--;
        check2(str, beginning, end, size);
    }
    else
    {
        cout << "Не палиндром" << endl;
    }
}

int main()
{
    setlocale(LC_ALL, "Russian");
    cout << "Введите строку:" << endl;
    string str;
    cin >> str;
    int size = str.size();
    cout << endl << size << " симв. - ";
    even(size);

    cout << check(str, 0) << endl << "(0 - нечётно; 1 - чётно)" << endl << endl;

    int beginning = 0, end = (size - 1);
    check2(str, beginning, end, size);

    return 0;
}
