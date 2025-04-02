#include <iostream>
#include <cmath>
#include <complex>

using namespace std;

const double PI = 3.14159265358979323846; // Определение числа Пи

void solveCubic(double a, double b, double c, double d) {
    // Приведение к приведенной форме
    double p = (3 * a * c - b * b) / (3 * a * a);
    double q = (2 * b * b * b - 9 * a * b * c + 27 * a * a * d) / (27 * a * a * a);

    // Вычисляем дискриминант
    double D = (q / 2) * (q / 2) + (p / 3) * (p / 3) * (p / 3);

    if (D < 0) {
        // Три различных действительных корня
        double r = sqrt(-(p / 3));
        double theta = acos(-q / (2 * r * r * r));

        for (int k = 0; k < 3; ++k) {
            double yk = 2 * r * cos((theta + 2 * PI * k) / 3);
            cout << "Корень " << k + 1 << ": x" << k + 1 << " = " << yk - (b / (3 * a)) << endl;
        }
        cout << "Следствие D: Уравнение имеет три различных действительных корня." << endl;
    }
    else if (D == 0) {
        // Три совпадающих корня
        double y1 = -q / 2;
        cout << "Корни: x1 = x2 = x3 = " << y1 - (b / (3 * a)) << endl;
        cout << "Следствие E: Уравнение имеет три совпадающих корня." << endl;
    }
    else {
        // Один действительный корень и два комплексных
        double u = cbrt(-q / 2 + sqrt(D));
        double v = cbrt(-q / 2 - sqrt(D));
        double y1 = u + v;

        cout << "Корень: x1 = " << y1 - (b / (3 * a)) << endl;
        cout << "Следствие F: Уравнение имеет один действительный корень и два комплексных корня." << endl;
    }
}

int main() {
    setlocale(LC_ALL, "Russian");

    double a, b, c, d;

    cout << "Введите коэффициенты a, b, c, d для уравнения ax^3 + bx^2 + cx + d = 0:" << endl;

    // Проверка ввода для каждого коэффициента
    if (!(cin >> a) || !(cin >> b) || !(cin >> c) || !(cin >> d)) {
        cout << "Коэффициенты не могут быть не числом" << endl;
        return 1;
    }
    if (a == 0) {
        cout << "Коэффициент a не может быть равен нулю." << endl;
        return 1;
    }

    solveCubic(a, b, c, d);

    return 0;
}