#include <iostream>

using namespace std;

int main()
{
  setlocale(LC_ALL, "Russian");
  int stolbik, stroka, c;
  cout << "Введите букву: \no - одномерный массив; \nd - двумерный массив; \np - перемножение матриц\n";
  c = cin.get();

  if (c == 'o')
  {
    int razmer, sum = 0, ymn = 1;
    cout << "Введите размер массива\n";
    cin >> razmer;
    int* odnomerniy = new int[razmer];
    cout << "Введите элементы массива\n";
    for (int i = 0; i < razmer; i++)
    {
      cin >> odnomerniy[i];
    }
    for (int i = 0; i < razmer; i++)
    {
      sum = sum + odnomerniy[i];
      ymn = ymn * odnomerniy[i];
    }
    cout << "Сумма элементов массива:" << sum << endl;
    cout << "Произведение элементов массива:" << ymn << endl;
    delete[] odnomerniy;
  }

  if (c == 'd')
  {
    cout << "Введите количество строк и количество столбцов массива через пробел\n";
    cin >> stroka >> stolbik;
    int** massiv = new int* [stolbik];

    for (int i = 0; i < stroka; i++)
    {
      massiv[i] = new int[stolbik];
    }

    for (int i = 0; i < stroka; i++)
    {
      for (int j = 0; j < stolbik; j++)
      {
        cout << "Введите [" << i << "][" << j << "] элемент массива\n";
        cin >> massiv[i][j];
      }
    }

    for (int i = 0; i < stroka; i++)
    {
      for (int j = 0; j < stolbik; j++)
      {
        cout << massiv[i][j] << "\t";
      }
      cout << endl;
    }

    int symma = 0;
    for (int i = 0; i < stroka; i++)
    {
      for (int j = 0; j < stolbik; j++)
      {
        if (i == j)
        {
          symma += massiv[i][j];
        }
      }
    }
    cout << "Сумма элементов матрицы, расположенных на главной диагонали:" << symma << endl;

    int symman = 0;
    for (int i = 0; i < stroka; i++)
    {
      for (int j = 0; j < stolbik; j++)
      {
        if (i > j)
        {
          symman += massiv[i][j];
        }
      }
    }
    cout << "Сумма элементов матрицы, расположенных ниже главной диагонали:" << symman << endl;

    int symmav = 0;
    for (int i = 0; i < stroka; i++)
    {
      for (int j = 0; j < stolbik; j++)
      {
        if (i < j)
        {
          symmav += massiv[i][j];
        }
      }
    }
    cout << "Сумма элементов матрицы, расположенных выше главной диагонали:" << symmav << endl;

    int pr = 1;
    for (int i = 0; i < stroka; i++)
    {
      for (int j = 0; j < stolbik; j++)
      {
        if ((j + 1) == stolbik - i)
        {
          pr = pr * massiv[i][j];
        }
      }
    }
    cout << "Произведение элементов матрицы, расположенных на побочной диагонали:" << pr << endl;

    int maxstr;
    for (int i = 0; i < stroka; i++)
    {
      if (i % 2 != 0)
      {
        maxstr = massiv[i][0];
        for (int j = 0; j < stolbik; j++)
        {
          if (massiv[i][j] > maxstr)
          { 
            maxstr = massiv[i][j];
          }
        }
        cout << "Максимумы четных строк матрицы:" << maxstr << endl;
      }
    }

    int minstl;
    for (int i = 0; i < stolbik; i++)
    {
      if ((i == 0) or (i % 2 == 0))
      {
        minstl = massiv[0][i];
        for (int j = 0; j < stroka; j++)
        {
          if (massiv[j][i] < minstl)
          {
            minstl = massiv[j][i];
          }

        }
        cout << "Минимумы нечётных столбцов матрицы:" << minstl << endl;
      }
    }

    for (int i = 0; i < stroka; i++)
    {
      delete massiv[i];
    }
    delete[] massiv;
  }

  if (c == 'p')
  {
    int str1, str2, stl1, stl2;
    cout << "Введите количество строк и количество столбцов первой матрицы\n";
    cin >> str1 >> stl1;
    cout << "Введите количество строк и количество столбцов второй матрицы\n";
    cin >> str2 >> stl2;
    if (stl1 == str2)
    {
      int** matrica1 = new int* [str1];

      for (int i = 0; i < str1; i++)
      {
        matrica1[i] = new int[stl1];
      }

      for (int i = 0; i < str1; i++)
      {
        for (int j = 0; j < stl1; j++)
        {
        cout << "Введите [" << i << "][" << j << "] элемент 1 матрицы\n";
        cin >> matrica1[i][j];
        }
      }

      for (int i = 0; i < str1; i++)
      {
        for (int j = 0; j < stl1; j++)
        {
          cout << matrica1[i][j] << "\t";
        }
        cout << endl;
      }

      int** matrica2 = new int* [str2];

      for (int i = 0; i < str2; i++)
      {
        matrica2[i] = new int[stl2];
      }

      for (int i = 0; i < str2; i++)
      {
        for (int j = 0; j < stl2; j++)
        {
          cout << "Введите [" << i << "][" << j << "] элемент 2 матрицы\n";
          cin >> matrica2[i][j];
        }
      }

      for (int i = 0; i < str2; i++)
      {
        for (int j = 0; j < stl2; j++)
        {
          cout << matrica2[i][j] << "\t";
        }
        cout << endl;
      }

      int** resultat = new int* [str1];
      for (int i = 0; i < str1; i++)
      {
        resultat[i] = new int[stl1];
      }
      cout << "Результат перемножения матриц:\n";
      for (int i = 0; i < str1; i++)
      {
        cout << endl;
        for (int j = 0; j < stl2; j++)
        {
          resultat[i][j] = 0;
          for (int l = 0; l < stl1; l++)
          {
            resultat[i][j] = resultat[i][j] + (matrica1[i][l] * matrica2[l][j]);
          }
          cout << resultat[i][j] << " ";
        }
      }

      for (int i = 0; i < str1; i++)
        delete[] matrica1[i];
      delete[] matrica1;
      
      for (int i = 0; i < str2; i++)
        delete[] matrica2[i];
      delete[] matrica2;
      
      for (int i = 0; i < str1; i++)
        delete[] resultat[i];
      delete[] resultat;
    }
    else
    cout << "Количество столбцов первой матрицы должо быть равно количеству строк второй матрицы\n";
  }

  return 0;
}
