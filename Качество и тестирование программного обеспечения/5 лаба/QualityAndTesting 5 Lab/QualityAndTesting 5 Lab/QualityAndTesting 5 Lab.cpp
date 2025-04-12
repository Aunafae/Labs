#include "QualityAndTesting 5 Lab.h"

int compareInts(const void* a, const void* b)
{
    int arg1 = *(const int*)a;
    int arg2 = *(const int*)b;

    if (arg1 < arg2) return -1;
    if (arg1 > arg2) return 1;
    return 0;
}

int countTransmitters(int* arr, int n, int k) {
    if (n <= 0 || k <= 0) {
        throw exception("Неправильные исходные данные");
    }
    qsort(arr, n, sizeof(int), compareInts);

    if (arr[0] <= 0) {
        throw exception("Неправильные исходные данные");
    }

    int count = 0;

    int i = 0;
    while (i < n) {
        count++;
        int coverage = arr[i] + k;
        while (i < n && arr[i] <= coverage)
            i++;
        coverage = arr[i - 1] + k;
        while (i < n && arr[i] <= coverage)
            i++;
    }

    return count;
}

int main() {}