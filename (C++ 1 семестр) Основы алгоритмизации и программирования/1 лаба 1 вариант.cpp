#include <iostream>
#include <math.h>
#include <locale.h>

using namespace std;

int main() {
    setlocale(LC_ALL, "Russian");
    char c; 
    while (1) {
        cout << "r - прямоугольник; t - треугольник; c - круг; x - выход.\n";
        c = cin.get();
        if (c == 'r')
        {
            cout << "укажите две разные стороны через пробел.\n";
            int a, b;
            cin >> a >> b;
            cout << "S = " << a * b << endl;
        }
        else if (c == 't')
        {
            cout << "укажите высоту и сторону треугольника.\n";
            int a, b;
            cin >> a >> b;
            cout << "S = " << (a * b) / 2.0 << endl;
        }
        else if (c == 'c')
        {
            cout << "укажите радиус круга.\n";
            int a;
            cin >> a;
            cout << "S = " << ((a * a) * 3.14) << endl;
        }
        else if (c == 'x')
            return 0;
        else
            cout << "не правильно введённое знаечение.\n";
            cin.ignore();
    }
    return 0;
}