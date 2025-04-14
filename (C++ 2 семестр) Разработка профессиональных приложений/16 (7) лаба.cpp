#include <iostream>
#include <chrono>
#include <windows.h>

#pragma comment(linker, "/STACK:100000000000000")

using namespace std;

void Bubble_Sort(int* massiv, int size, int count_test)
{
    long long time_period = 0;
    for (int j = 0; j < count_test; j++)
    {
        auto begin = chrono::steady_clock::now();

        int variable = 0; // временная переменная для обмена элементов местами
        for (int i = 0; i < size - 1; i++)
        {
            for (int j = 0; j < size - i - 1; j++)
            {
                if (massiv[j] > massiv[j + 1])
                {
                    // меняем элементы местами
                    variable = massiv[j];
                    massiv[j] = massiv[j + 1];
                    massiv[j + 1] = variable;
                }
            }
        }

        auto end = chrono::steady_clock::now();
        auto elapsed_ms = chrono::duration_cast<chrono::nanoseconds>(end - begin);
        time_period += elapsed_ms.count();
    }
    cout << "Сортировка пузырьком: " << time_period / 10 << " nanoseconds\n\n";
}

void Selection_Sort(int* massiv, int size, int count_test)
{
    long long time_period = 0;
    for (int j = 0; j < count_test; j++)
    {
        auto begin = chrono::steady_clock::now();

        int min = 0;
        int variable = 0;
        for (int i = 0; i < size; i++) {
            min = i;
            for (int k = i; k < size; k++) {
                if (massiv[min] > massiv[k]) {
                    min = k;
                }
            }
            variable = massiv[i];
            massiv[i] = massiv[min];
            massiv[min] = variable;
        }

        auto end = chrono::steady_clock::now();
        auto elapsed_ms = chrono::duration_cast<chrono::nanoseconds>(end - begin);
        time_period += elapsed_ms.count();
    }
    cout << "Сортировка выбором: " << time_period / 10 << " nanoseconds\n\n";
}

void Insertion_Sort(int* massiv, int size, int count_test)
{
    long long time_period = 0;
    for (int j = 0; j < count_test; j++)
    {
        auto begin = chrono::steady_clock::now();

        int variable = 0, i = 0;
        for (int j = 1; j < size; j++)
        {
            variable = massiv[j];
            i = j - 1;
            while (i >= 0 && massiv[i] > variable)
            {
                massiv[i + 1] = massiv[i];
                i -= 1;
                massiv[i + 1] = variable;
            }
        }

        auto end = chrono::steady_clock::now();
        auto elapsed_ms = chrono::duration_cast<chrono::nanoseconds>(end - begin);
        time_period += elapsed_ms.count();
    }
    cout << "Сортировка вставками: " << time_period / 10 << " nanoseconds\n\n";
}

void Merge_Sort(int* massiv, int size, int count_test)
{
    long long time_period = 0;
    for (int j = 0; j < count_test; j++)
    {
        auto begin = chrono::steady_clock::now();

        int mid = size / 2; // находим середину сортируемой последовательности
        if (size % 2 == 1)
            mid++;
        int h = 1; // шаг
        // выделяем память под формируемую последовательность
        int* c = (int*)malloc(size * sizeof(int));
        int step;
        while (h < size)
        {
            step = h;
            int i = 0;   // индекс первого пути
            int j = mid; // индекс второго пути
            int element = 0;   // индекс элемента в результирующей последовательности
            while (step <= mid)
            {
                while ((i < step) && (j < size) && (j < (mid + step)))
                { // пока не дошли до конца пути
                  // заполняем следующий элемент формируемой последовательности
                  // меньшим из двух просматриваемых
                    if (massiv[i] < massiv[j])
                    {
                        c[element] = massiv[i];
                        i++; element++;
                    }
                    else {
                        c[element] = massiv[j];
                        j++; element++;
                    }
                }
                while (i < step)
                { // переписываем оставшиеся элементы первого пути (если второй кончился раньше)
                    c[element] = massiv[i];
                    i++; element++;
                }
                while ((j < (mid + step)) && (j < size))
                {  // переписываем оставшиеся элементы второго пути (если первый кончился раньше)
                    c[element] = massiv[j];
                    j++; element++;
                }
                step = step + h; // переходим к следующему этапу
            }
            h = h * 2;
            // Переносим упорядоченную последовательность (промежуточный вариант) в исходный массив
            for (i = 0; i < size; i++)
                massiv[i] = c[i];
        }

        auto end = chrono::steady_clock::now();
        auto elapsed_ms = chrono::duration_cast<chrono::nanoseconds>(end - begin);
        time_period += elapsed_ms.count();
    }
    cout << "Сортировка слиянием: " << time_period / 10 << " nanoseconds\n\n";
}

void quickSort(int* massiv, int left, int right)
{
    int pivot; // разрешающий элемент
    int l_hold = left; //левая граница
    int r_hold = right; // правая граница
    pivot = massiv[left];
    while (left < right) // пока границы не сомкнутся
    {
        while ((massiv[right] >= pivot) && (left < right))
            right--; // сдвигаем правую границу пока элемент [right] больше [pivot]
        if (left != right) // если границы не сомкнулись
        {
            massiv[left] = massiv[right]; // перемещаем элемент [right] на место разрешающего
            left++; // сдвигаем левую границу вправо
        }
        while ((massiv[left] <= pivot) && (left < right))
            left++; // сдвигаем левую границу пока элемент [left] меньше [pivot]
        if (left != right) // если границы не сомкнулись
        {
            massiv[right] = massiv[left]; // перемещаем элемент [left] на место [right]
            right--; // сдвигаем правую границу влево
        }
    }
    massiv[left] = pivot; // ставим разрешающий элемент на место
    pivot = left;
    left = l_hold;
    right = r_hold;
    if (left < pivot) // Рекурсивно вызываем сортировку для левой и правой части массива
        quickSort(massiv, left, pivot - 1);
    if (right > pivot)
        quickSort(massiv, pivot + 1, right);
}

void Quick_Sort(int* massiv, int size, int count_test)
{
    long long time_period = 0;
    for (int j = 0; j < count_test; j++)
    {
        auto begin = chrono::steady_clock::now();

        quickSort(massiv, 0, size-1);

        auto end = chrono::steady_clock::now();
        auto elapsed_ms = chrono::duration_cast<chrono::nanoseconds>(end - begin);
        time_period += elapsed_ms.count();
    }
    cout << "Быстрая сортировка: " << time_period / 10 << " nanoseconds\n\n";
}

// Функция "просеивания" через кучу - формирование кучи
void siftDown(int* massiv, int root, int bottom)
{
    int maxChild; // индекс максимального потомка
    int done = 0; // флаг того, что куча сформирована
    // Пока не дошли до последнего ряда
    while ((root * 2 <= bottom) && (!done))
    {
        if (root * 2 == bottom)    // если мы в последнем ряду,
            maxChild = root * 2;    // запоминаем левый потомок
        // иначе запоминаем больший потомок из двух
        else if (massiv[root * 2] > massiv[root * 2 + 1])
            maxChild = root * 2;
        else
            maxChild = root * 2 + 1;
        // если элемент вершины меньше максимального потомка
        if (massiv[root] < massiv[maxChild])
        {
            int temp = massiv[root]; // меняем их местами
            massiv[root] = massiv[maxChild];
            massiv[maxChild] = temp;
            root = maxChild;
        }
        else // иначе
            done = 1; // пирамида сформирована
    }
}
// Функция сортировки на куче
void heapSort(int* massiv, int size)
{
    // Формируем нижний ряд пирамиды
    for (int i = (size / 2); i >= 0; i--)
        siftDown(massiv, i, size - 1);
    // Просеиваем через пирамиду остальные элементы
    for (int i = size - 1; i >= 1; i--)
    {
        int temp = massiv[0];
        massiv[0] = massiv[i];
        massiv[i] = temp;
        siftDown(massiv, 0, i - 1);
    }
}

void Heap_Sort(int* massiv, int size, int count_test)
{
    long long time_period = 0;
    for (int j = 0; j < count_test; j++)
    {
        auto begin = chrono::steady_clock::now();

        heapSort(massiv, size);

        auto end = chrono::steady_clock::now();
        auto elapsed_ms = chrono::duration_cast<chrono::nanoseconds>(end - begin);
        time_period += elapsed_ms.count();
    }
    cout << "Пирамидальная сортировка: " << time_period / 10 << " nanoseconds\n\n";
}

void Shell_Sort(int* massiv, int size, int count_test)
{
    long long time_period = 0;
    for (int j = 0; j < count_test; j++)
    {
        auto begin = chrono::steady_clock::now();

        int increment = 3;    // начальное приращение сортировки
        while (increment > 0)  // пока существует приращение
        {
            for (int i = 0; i < size; i++)  // для всех элементов массива
            {
                int j = i;          // сохраняем индекс и элемент
                int temp = massiv[i];
                // просматриваем остальные элементы массива, отстоящие от j-ого
                // на величину приращения
                while ((j >= increment) && (massiv[j - increment] > temp))
                {  // пока отстоящий элемент больше текущего
                    massiv[j] = massiv[j - increment]; // перемещаем его на текущую позицию
                    j = j - increment;       // переходим к следующему отстоящему элементу
                }
                massiv[j] = temp; // на выявленное место помещаем сохранённый элемент
            }
            if (increment > 1)      // делим приращение на 2
                increment = increment / 2;
            else if (increment == 1)   // последний проход завершён,
                break;  // выходим из цикла
        }

        auto end = chrono::steady_clock::now();
        auto elapsed_ms = chrono::duration_cast<chrono::nanoseconds>(end - begin);
        time_period += elapsed_ms.count();
    }
    cout << "Шелл - сортировка: " << time_period / 10 << " nanoseconds\n\n";
}

void Shaker_Sort(int* massiv, int size, int count_test)
{
    long long time_period = 0;
    for (int j = 0; j < count_test; j++)
    {
        auto begin = chrono::steady_clock::now();

        int left = 0, right = size - 1; // левая и правая границы сортируемой области массива
        int flag = 1;  // флаг наличия перемещений
        // Выполнение цикла пока левая граница не сомкнётся с правой
        // и пока в массиве имеются перемещения
        while ((left < right) && flag > 0)
        {
            flag = 0;
            for (int i = left; i < right; i++)  //двигаемся слева направо
            {
                if (massiv[i] > massiv[i + 1]) // если следующий элемент меньше текущего,
                {             // меняем их местами
                    double t = massiv[i];
                    massiv[i] = massiv[i + 1];
                    massiv[i + 1] = t;
                    flag = 1;      // перемещения в этом цикле были
                }
            }
            right--; // сдвигаем правую границу на предыдущий элемент
            for (int i = right; i > left; i--)  //двигаемся справа налево
            {
                if (massiv[i - 1] > massiv[i]) // если предыдущий элемент больше текущего,
                {            // меняем их местами
                    double t = massiv[i];
                    massiv[i] = massiv[i - 1];
                    massiv[i - 1] = t;
                    flag = 1;    // перемещения в этом цикле были
                }
            }
            left++; // сдвигаем левую границу на следующий элемент
        }

        auto end = chrono::steady_clock::now();
        auto elapsed_ms = chrono::duration_cast<chrono::nanoseconds>(end - begin);
        time_period += elapsed_ms.count();
    }
    cout << "Шейкер - сортировка: " << time_period / 10 << " nanoseconds\n\n";
}

void random(int massiv[], int size)
{
    for (int i = 0; i < size; i++)
    {
        massiv[i] = rand() % 1000;
    }
}

void reverse(int massiv[], int size) 
{
    reverse(massiv, massiv + size);
}

void Insertion_sort(int* massiv, int size)
{
    int variable = 0, i = 0;
    for (int j = 1; j < size; j++)
    {
        variable = massiv[j];
        i = j - 1;
        while (i >= 0 && massiv[i] > variable)
        {
            massiv[i + 1] = massiv[i];
            i -= 1;
            massiv[i + 1] = variable;
        }
    }
}

int main()
{
    setlocale(LC_ALL, "Russian");

    int count_test = 10;

    const int size_small = 500;
    int* massiv_small = new int[size_small];

    const int size_average = 20000;
    int* massiv_average = new int[size_average];

    random(massiv_small, size_small);
    random(massiv_average, size_average);

    cout << "\n__________________________________________________________\n";
    cout << "\n                 РАНДОМНОЕ ЗАПОЛНЕНИЕ МАССИВОВ\n";
    cout << "__________________________________________________________\n\n";
    Bubble_Sort(massiv_small, size_small, count_test);
    Bubble_Sort(massiv_average, size_average, count_test);
    cout << "---------------------------------------------------------\n\n";

    random(massiv_small, size_small);
    random(massiv_average, size_average);

    Selection_Sort(massiv_small, size_small, count_test);
    Selection_Sort(massiv_average, size_average, count_test);
    cout << "---------------------------------------------------------\n\n";

    random(massiv_small, size_small);
    random(massiv_average, size_average);

    Insertion_Sort(massiv_small, size_small, count_test);
    Insertion_Sort(massiv_average, size_average, count_test);
    cout << "---------------------------------------------------------\n\n";

    random(massiv_small, size_small);
    random(massiv_average, size_average);

    Merge_Sort(massiv_small, size_small, count_test);
    Merge_Sort(massiv_average, size_average, count_test);
    cout << "---------------------------------------------------------\n\n";

    random(massiv_small, size_small);
    random(massiv_average, size_average);

    Quick_Sort(massiv_small, size_small, count_test);
    Quick_Sort(massiv_average, size_average, count_test);
    cout << "---------------------------------------------------------\n\n";

    random(massiv_small, size_small);
    random(massiv_average, size_average);

    Heap_Sort(massiv_small, size_small, count_test);
    Heap_Sort(massiv_average, size_average, count_test);
    cout << "---------------------------------------------------------\n\n";

    random(massiv_small, size_small);
    random(massiv_average, size_average);

    Shell_Sort(massiv_small, size_small, count_test);
    Shell_Sort(massiv_average, size_average, count_test);
    cout << "---------------------------------------------------------\n\n";

    random(massiv_small, size_small);
    random(massiv_average, size_average);

    Shaker_Sort(massiv_small, size_small, count_test);
    Shaker_Sort(massiv_average, size_average, count_test);
    cout << "---------------------------------------------------------\n\n";

    int element = 0;
    Insertion_sort(massiv_small, size_small);
    element = massiv_small[0];
    massiv_small[0] = massiv_small[size_small - 1];
    massiv_small[size_small - 1] = element;

    Insertion_sort(massiv_average, size_average);
    element = massiv_average[0];
    massiv_average[0] = massiv_average[size_average - 1];
    massiv_average[size_average - 1] = element;

    cout << "\n__________________________________________________________\n";
    cout << "\n                 ПОЧТИ УПОРЯДОЧЕННЫЙ МАССИВ\n";
    cout << "__________________________________________________________\n\n";
    Bubble_Sort(massiv_small, size_small, count_test);
    Bubble_Sort(massiv_average, size_average, count_test);
    cout << "---------------------------------------------------------\n\n";

    Insertion_sort(massiv_small, size_small);
    element = massiv_small[0];
    massiv_small[0] = massiv_small[size_small - 1];
    massiv_small[size_small - 1] = element;

    Insertion_sort(massiv_average, size_average);
    element = massiv_average[0];
    massiv_average[0] = massiv_average[size_average - 1];
    massiv_average[size_average - 1] = element;

    Selection_Sort(massiv_small, size_small, count_test);
    Selection_Sort(massiv_average, size_average, count_test);
    cout << "---------------------------------------------------------\n\n";

    Insertion_sort(massiv_small, size_small);
    element = massiv_small[0];
    massiv_small[0] = massiv_small[size_small - 1];
    massiv_small[size_small - 1] = element;

    Insertion_sort(massiv_average, size_average);
    element = massiv_average[0];
    massiv_average[0] = massiv_average[size_average - 1];
    massiv_average[size_average - 1] = element;

    Insertion_Sort(massiv_small, size_small, count_test);
    Insertion_Sort(massiv_average, size_average, count_test);
    cout << "---------------------------------------------------------\n\n";

    Insertion_sort(massiv_small, size_small);
    element = massiv_small[0];
    massiv_small[0] = massiv_small[size_small - 1];
    massiv_small[size_small - 1] = element;

    Insertion_sort(massiv_average, size_average);
    element = massiv_average[0];
    massiv_average[0] = massiv_average[size_average - 1];
    massiv_average[size_average - 1] = element;

    Merge_Sort(massiv_small, size_small, count_test);
    Merge_Sort(massiv_average, size_average, count_test);
    cout << "---------------------------------------------------------\n\n";

    Insertion_sort(massiv_small, size_small);
    element = massiv_small[0];
    massiv_small[0] = massiv_small[size_small - 1];
    massiv_small[size_small - 1] = element;

    Insertion_sort(massiv_average, size_average);
    element = massiv_average[0];
    massiv_average[0] = massiv_average[size_average - 1];
    massiv_average[size_average - 1] = element;

    Quick_Sort(massiv_small, size_small, count_test);
    Quick_Sort(massiv_average, size_average, count_test);
    cout << "---------------------------------------------------------\n\n";

    Insertion_sort(massiv_small, size_small);
    element = massiv_small[0];
    massiv_small[0] = massiv_small[size_small - 1];
    massiv_small[size_small - 1] = element;

    Insertion_sort(massiv_average, size_average);
    element = massiv_average[0];
    massiv_average[0] = massiv_average[size_average - 1];
    massiv_average[size_average - 1] = element;

    Heap_Sort(massiv_small, size_small, count_test);
    Heap_Sort(massiv_average, size_average, count_test);
    cout << "---------------------------------------------------------\n\n";

    Insertion_sort(massiv_small, size_small);
    element = massiv_small[0];
    massiv_small[0] = massiv_small[size_small - 1];
    massiv_small[size_small - 1] = element;

    Insertion_sort(massiv_average, size_average);
    element = massiv_average[0];
    massiv_average[0] = massiv_average[size_average - 1];
    massiv_average[size_average - 1] = element;

    Shell_Sort(massiv_small, size_small, count_test);
    Shell_Sort(massiv_average, size_average, count_test);
    cout << "---------------------------------------------------------\n\n";

    Insertion_sort(massiv_small, size_small);
    element = massiv_small[0];
    massiv_small[0] = massiv_small[size_small - 1];
    massiv_small[size_small - 1] = element;

    Insertion_sort(massiv_average, size_average);
    element = massiv_average[0];
    massiv_average[0] = massiv_average[size_average - 1];
    massiv_average[size_average - 1] = element;

    Shaker_Sort(massiv_small, size_small, count_test);
    Shaker_Sort(massiv_average, size_average, count_test);
    cout << "---------------------------------------------------------\n\n";

    Insertion_sort(massiv_small, size_small);
    reverse(massiv_small, size_small);
    element = massiv_small[0];
    massiv_small[0] = massiv_small[size_small - 1];
    massiv_small[size_small - 1] = element;

    Insertion_sort(massiv_average, size_average);
    reverse(massiv_average, size_average);
    element = massiv_average[0];
    massiv_average[0] = massiv_average[size_average - 1];
    massiv_average[size_average - 1] = element;

    cout << "\n__________________________________________________________\n";
    cout << "\n              ПОЧТИ УПОРЯДОЧЕН В ОБРАТНОМ ПОРЯДКЕ\n";
    cout << "__________________________________________________________\n\n";
    Bubble_Sort(massiv_small, size_small, count_test);
    Bubble_Sort(massiv_average, size_average, count_test);
    cout << "---------------------------------------------------------\n\n";

    Insertion_sort(massiv_small, size_small);
    reverse(massiv_small, size_small);
    element = massiv_small[0];
    massiv_small[0] = massiv_small[size_small - 1];
    massiv_small[size_small - 1] = element;

    Insertion_sort(massiv_average, size_average);
    reverse(massiv_average, size_average);
    element = massiv_average[0];
    massiv_average[0] = massiv_average[size_average - 1];
    massiv_average[size_average - 1] = element;

    Selection_Sort(massiv_small, size_small, count_test);
    Selection_Sort(massiv_average, size_average, count_test);
    cout << "---------------------------------------------------------\n\n";

    Insertion_sort(massiv_small, size_small);
    reverse(massiv_small, size_small);
    element = massiv_small[0];
    massiv_small[0] = massiv_small[size_small - 1];
    massiv_small[size_small - 1] = element;

    Insertion_sort(massiv_average, size_average);
    reverse(massiv_average, size_average);
    element = massiv_average[0];
    massiv_average[0] = massiv_average[size_average - 1];
    massiv_average[size_average - 1] = element;

    Insertion_Sort(massiv_small, size_small, count_test);
    Insertion_Sort(massiv_average, size_average, count_test);
    cout << "---------------------------------------------------------\n\n";

    Insertion_sort(massiv_small, size_small);
    reverse(massiv_small, size_small);
    element = massiv_small[0];
    massiv_small[0] = massiv_small[size_small - 1];
    massiv_small[size_small - 1] = element;

    Insertion_sort(massiv_average, size_average);
    reverse(massiv_average, size_average);
    element = massiv_average[0];
    massiv_average[0] = massiv_average[size_average - 1];
    massiv_average[size_average - 1] = element;

    Merge_Sort(massiv_small, size_small, count_test);
    Merge_Sort(massiv_average, size_average, count_test);
    cout << "---------------------------------------------------------\n\n";

    Insertion_sort(massiv_small, size_small);
    reverse(massiv_small, size_small);
    element = massiv_small[0];
    massiv_small[0] = massiv_small[size_small - 1];
    massiv_small[size_small - 1] = element;

    Insertion_sort(massiv_average, size_average);
    reverse(massiv_average, size_average);
    element = massiv_average[0];
    massiv_average[0] = massiv_average[size_average - 1];
    massiv_average[size_average - 1] = element;

    Quick_Sort(massiv_small, size_small, count_test);
    Quick_Sort(massiv_average, size_average, count_test);
    cout << "---------------------------------------------------------\n\n";

    Insertion_sort(massiv_small, size_small);
    reverse(massiv_small, size_small);
    element = massiv_small[0];
    massiv_small[0] = massiv_small[size_small - 1];
    massiv_small[size_small - 1] = element;

    Insertion_sort(massiv_average, size_average);
    reverse(massiv_average, size_average);
    element = massiv_average[0];
    massiv_average[0] = massiv_average[size_average - 1];
    massiv_average[size_average - 1] = element;

    Heap_Sort(massiv_small, size_small, count_test);
    Heap_Sort(massiv_average, size_average, count_test);
    cout << "---------------------------------------------------------\n\n";

    Insertion_sort(massiv_small, size_small);
    reverse(massiv_small, size_small);
    element = massiv_small[0];
    massiv_small[0] = massiv_small[size_small - 1];
    massiv_small[size_small - 1] = element;

    Insertion_sort(massiv_average, size_average);
    reverse(massiv_average, size_average);
    element = massiv_average[0];
    massiv_average[0] = massiv_average[size_average - 1];
    massiv_average[size_average - 1] = element;

    Shell_Sort(massiv_small, size_small, count_test);
    Shell_Sort(massiv_average, size_average, count_test);
    cout << "---------------------------------------------------------\n\n";

    Insertion_sort(massiv_small, size_small);
    reverse(massiv_small, size_small);
    element = massiv_small[0];
    massiv_small[0] = massiv_small[size_small - 1];
    massiv_small[size_small - 1] = element;

    Insertion_sort(massiv_average, size_average);
    reverse(massiv_average, size_average);
    element = massiv_average[0];
    massiv_average[0] = massiv_average[size_average - 1];
    massiv_average[size_average - 1] = element;

    Shaker_Sort(massiv_small, size_small, count_test);
    Shaker_Sort(massiv_average, size_average, count_test);
    cout << "---------------------------------------------------------\n\n";

    delete[] massiv_small;
    delete[] massiv_average;
    return 0;
}
