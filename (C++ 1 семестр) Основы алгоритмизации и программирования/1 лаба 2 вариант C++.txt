#include <iostream>
#include <math.h>
#include <locale.h>

using namespace std;

int main() {
    setlocale (LC_ALL, "Russian");
    while (1) {
        cout << "r - прямоугольник; t - треугольник; c - круг; x - выход.\n";
        switch (cin.get()) {
        case'r':
        {
            cout << "укажите две разные стороны через пробел.\n";
            int a, b;
            cin >> a >> b;
            cout << "S = " << a * b << endl;
            break;
        }
        case 't':
        {
            cout << "укажите высоту и сторону треугольника.\n";
            int a, b;
            cin >> a >> b;
            cout << "S = " << (a * b) / 2.0 << endl;
            break;
        }
        case 'c':
        {
            cout << "укажите радиус круга.\n";
            int a;
            cin >> a;
            cout << "S = " << ((a * a) * 3.14) << endl;
            break;
        }
        case 'x':
            return 0;
        default:
            cout << "не правильно введённое знаечение.\n";
        }
        cin.ignore();
    }
    return 0;
}