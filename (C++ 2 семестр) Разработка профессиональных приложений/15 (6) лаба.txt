#include <iostream>
#include <chrono>

using namespace std;

void linear_search(int* massiv, int size, int number, int count_test)
{
    long long time_period = 0;
    int element = 0;
    for (int j = 0; j < count_test; j++)
    {
        auto begin = chrono::steady_clock::now();

        for (int i = 0; i < size; i++)
        {
            if (massiv[i] == number)
            {
                element = i;
                break;
            }
        }

        auto end = chrono::steady_clock::now();
        auto elapsed_ms = chrono::duration_cast<chrono::nanoseconds>(end - begin);
        time_period += elapsed_ms.count();
    }
    cout << "Линейный алгоритм: " << time_period / 1000 << " nanoseconds\n\n";
}

void binary_search(int* massiv, int size, int number, int count_test)
{
    long long time_period = 0;
    int element = 0;
    for (int j = 0; j < count_test; j++)
    {
        auto begin = chrono::steady_clock::now();

        bool flag = false;
        int left = 0;       // левая граница
        int right = size - 1; // правая граница
        int mid;

        while ((left <= right) && (flag != true)) {
            mid = (left + right) / 2; // срединный индекс отрезка [left, right]

            if (massiv[mid] == number)
            {
                element = mid;
                flag = true; //проверяем ключ со серединным элементом
            }
            if (massiv[mid] > number)
            {
                right = mid - 1; // проверяем, какую часть нужно отбросить
            }
            else
            {
                left = mid + 1;
            }
        }

        auto end = chrono::steady_clock::now();
        auto elapsed_ms = chrono::duration_cast<chrono::nanoseconds>(end - begin);
        time_period += elapsed_ms.count();
    }
    cout << "Бинарный алгоритм: " << time_period / 1000 << " nanoseconds\n\n";
}

void linear_with_barrier(int* massiv, int size, int number, int count_test)
{
    long long time_period = 0;
    int element = 0;
    for (int j = 0; j < count_test; j++)
    {
        auto begin = chrono::steady_clock::now();

        massiv = (int*)realloc(massiv, (size + 1) * sizeof(int));
        massiv[size] = number;
        int i = 0;
        while (massiv[i] != number)
        {
            i++;
        }
        element = i < size ? i : -1;

        auto end = chrono::steady_clock::now();
        auto elapsed_ms = chrono::duration_cast<chrono::nanoseconds>(end - begin);
        time_period += elapsed_ms.count();
    }
    cout << "Линейный алгоритм с барьером: " << time_period / 1000 << " nanoseconds\n\n";
}

int main()
{
    setlocale(LC_ALL, "Russian");

    int count_test = 1000;
    const int size = 1000000;
    int* massiv = new int[size];
    for (int i = 0; i < size; i++)
    {
        massiv[i] = i;
    }

    int number1 = 1, number2 = 500000, number3 = 999999;

    cout << endl << "---------------------------------------------------------" << endl << endl;
    linear_search(massiv, size, number1, count_test);
    linear_search(massiv, size, number2, count_test);
    linear_search(massiv, size, number3, count_test);
    cout << "---------------------------------------------------------" << endl;

    cout << endl << "---------------------------------------------------------" << endl << endl;
    binary_search(massiv, size, number1, count_test);
    binary_search(massiv, size, number2, count_test);
    binary_search(massiv, size, number3, count_test);
    cout << "---------------------------------------------------------" << endl;

    cout << endl << "---------------------------------------------------------" << endl << endl;
    linear_with_barrier(massiv, size, number1, count_test);
    linear_with_barrier(massiv, size, number2, count_test);
    linear_with_barrier(massiv, size, number3, count_test);
    cout << "---------------------------------------------------------" << endl;

    delete[] massiv;
    return 0;
}
