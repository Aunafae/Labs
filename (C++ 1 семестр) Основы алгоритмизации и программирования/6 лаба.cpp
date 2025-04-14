// Как для одномерного так и для двумерного массива

// СПОСОБЫ ЗАПИСИ МАССИВА В ФУНКЦИЮ В КАЧЕСТВЕ АРГУМЕНТА //

#include <iostream>

using namespace std;

//указатель на массив//

void one_in(int massiv[], const int razmer)
{
	for (int i = 0; i < razmer; i++)
	{
		massiv[i] = rand () % 10;
	}
}
void one_out(int massiv[], const int razmer)
{
	for (int i = 0; i < razmer; i++)
	{
		cout << massiv[i] << " ";
	}
}

void dv_one_in(int dv_massiv[][3], const int lin, const int col)
{
  for (int i = 0; i < lin; i++)
  {
    for (int j = 0; j < col; j++)
    {
      dv_massiv[i][j] = rand() % 10;
    }
  }
}
void dv_one_out(int dv_massiv[][3], const int lin, const int col)
{
  for (int i = 0; i < lin; i++)
  {
    for (int j = 0; j < col; j++)
    {
      cout << dv_massiv[i][j] << "\t";
    }
    cout << endl;
  }
}

//ссылка на массив//

void two_in(int(&massiv)[9], const int razmer)
{
	for (int i = 0; i < razmer; i++)
	{
		massiv[i] = rand () % 10;
	}
}
void two_out(int(&massiv)[9], const int razmer)
{
	for (int i = 0; i < razmer; i++)
	{
		cout << massiv[i] << " ";
	}
}

void dv_two_in(int (&dv_massiv)[3][3], const int lin, const int col)
{
  for (int i = 0; i < lin; i++)
  {
    for (int j = 0; j < col; j++)
    {
      dv_massiv[i][j] = rand() % 10;
    }
  }
}
void dv_two_out(int (&dv_massiv)[3][3], const int lin, const int col)
{
  for (int i = 0; i < lin; i++)
  {
    for (int j = 0; j < col; j++)
    {
      cout << dv_massiv[i][j] << "\t";
    }
    cout << endl;
  }
}

//указатель на ссылку//

void three_in(int massiv[], const int razmer)
{
  int& ykazat = massiv[0];
	int* ssilk = &ykazat;
	for (int i = 0; i < razmer; i++)
	{
		ssilk[i] = rand () % 10;
	}
}
void three_out(int massiv[], const int razmer)
{
  int& ykazat = massiv[0];
	int* ssilk = &ykazat;
	for (int i = 0; i < razmer; i++)
	{
		cout << ssilk[i] << " ";
	}
}

void dv_three_in(int dv_massiv[][3], const int lin, const int col)
{
  for (int i = 0; i < lin; i++)
  {
    for (int j = 0; j < col; j++)
    {
      dv_massiv[i][j] = rand() % 10;
    }
  }
}
void dv_three_out(int dv_massiv[][3], const int lin, const int col)
{
  for (int i = 0; i < lin; i++)
  {
    for (int j = 0; j < col; j++)
    {
      cout << dv_massiv[i][j] << "\t";
    }
    cout << endl;
  }
}

//ссылка на указатель//

void four_in(int& massiv, const int razmer)
{
	int* mass = &massiv;
	for (int i = 0; i < razmer; i++)
	{
		mass[i] = rand () % 10;
	}
}
void four_out(int& massiv, const int razmer)
{
	int* mass = &massiv;
	for (int i = 0; i < razmer; i++)
	{
		cout << mass[i] << " ";
	}
}

void dv_four_in(int (&dv_m)[3], const int lin, const int col)
{
  for (int i = 0; i < lin; i++)
  {
    for (int j = 0; j < col; j++)
    {
      (&dv_m[i])[j] = rand() % 10;
    }
  }
}
void dv_four_out(int (&dv_m)[3], const int lin, const int col)
{
  for (int i = 0; i < lin; i++)
  {
    for (int j = 0; j < col; j++)
    {
      cout << (&dv_m[i])[j] << "\t";
    }
    cout << endl;
  }
}

//указатель на указатель//

void five_in(int massiv[], const int razmer)
{
	for (int i = 0; i < razmer; i++)
	{
		massiv[i] = rand () % 10;
	}
}
void five_out(int massiv[], const int razmer)
{
	for (int i = 0; i < razmer; i++)
	{
		cout << massiv[i] << " ";
	}
}

void dv_five_in(int (*dv_ma)[3], const int lin, const int col)
{
  for (int i = 0; i < lin; i++)
  {
    for (int j = 0; j < col; j++)
    {
      dv_ma[i][j] = rand() % 10;
    }
  }
}
void dv_five_out(int (*dv_ma)[3], const int lin, const int col)
{
  for (int i = 0; i < lin; i++)
  {
    for (int j = 0; j < col; j++)
    {
      cout << dv_ma[i][j] << "\t";
    }
    cout << endl;
  }
}

//ссылка на ссылку//

void six_in(int& massiv, const int razmer)
{
	int& yk1 = massiv;
	int* ms = &yk1;
	for (int i = 0; i < razmer; i++)
	{
    ms[i] = rand () % 10;
	}
}
void six_out(int& massiv, const int razmer)
{
	int& yk1 = massiv;
	int* ms = &yk1;
	for (int i = 0; i < razmer; i++)
	{
		cout << ms[i] << " ";
	}
}

void dv_six_in(int (&dv_ma)[3][3], const int lin, const int col)
{
  for (int i = 0; i < lin; i++)
  {
    for (int j = 0; j < col; j++)
    {
      dv_ma[i][j] = rand() % 10;
    }
  }
}
void dv_six_out(int (&dv_massiv)[3][3], const int lin, const int col)
{
  for (int i = 0; i < lin; i++)
  {
    for (int j = 0; j < col; j++)
    {
      cout << dv_massiv[i][j] << "\t";
    }
    cout << endl;
  }
}

int main()
{
	setlocale(LC_ALL, "Russian");

	const int razmer = 9;
	int massiv[razmer];  

  const int lin = 3;
  const int col = 3;
  int dv_massiv [lin][col];

	cout << endl << "Первый способ - указатель на массив: \n" << endl << "Одномерный массив: " << endl;
  one_in(massiv, razmer);
	one_out(massiv, razmer);

  cout << endl << endl << "Двумерный массив: " << endl;
  dv_one_in(dv_massiv, lin, col);
  dv_one_out(dv_massiv, lin, col);

	cout << endl << endl << endl << "Второй способ - ссылка на массив: \n" << endl << "Одномерный массив: " << endl;
	two_in(massiv, razmer);
  two_out(massiv, razmer);

  cout << endl << endl << "Двумерный массив: " << endl;
  dv_two_in(dv_massiv, lin, col);
  dv_two_out(dv_massiv, lin, col);

	cout << endl << endl << endl << "Третий способ - указатель на ссылку: \n" << endl << "Одномерный массив: " << endl;
  int& ykazat = massiv[0];
	int* ssilk = &ykazat;
	three_in(ssilk, razmer);
  three_out(ssilk, razmer);

  cout << endl << endl << "Двумерный массив: " << endl;
  int (&dv_yk)[3][3] = dv_massiv;
  int (*dv_ss)[3] = dv_yk;
  dv_three_in(dv_ss, lin, col);
  dv_three_out(dv_ss, lin, col);

	cout << endl << endl << endl << "Четвёртый способ - ссылка на указатель: \n" << endl << "Одномерный массив: " << endl;
  int* mas_yk = massiv;
  int& mas_ss = *mas_yk;
	four_in(mas_ss, razmer);
  four_out(mas_ss, razmer);

  cout << endl << endl << "Двумерный массив: " << endl;
  int (*dv_uk)[3] = dv_massiv;
	dv_four_in(*dv_uk, lin, col);
  dv_four_out(*dv_uk, lin, col);

	cout << endl << endl << endl << "Пятый способ - указатель на указатель: \n" << endl << "Одномерный массив: " << endl;
	int* mas_ssilk1 = massiv;
	int* mas_ssilk2 = mas_ssilk1;
	five_in(mas_ssilk2, razmer);
  five_out(mas_ssilk2, razmer);

  cout << endl << endl << "Двумерный массив: " << endl;
  int (*d_m)[3] = dv_massiv;
  dv_five_in(d_m, lin, col);
  dv_five_out(d_m, lin, col);

	cout << endl << endl << endl << "Шестой способ - ссылка на ссылку: \n" << endl << "Одномерный массив: " << endl;
	int& yk1 = massiv[0];
	int& yk2 = yk1;
	six_in(yk2, razmer);
  six_out(yk2, razmer);

  cout << endl << endl << "Двумерный массив: " << endl;
  int (&d_ma)[3][3] = dv_massiv;
  dv_six_in(d_ma, lin, col);
  dv_six_out(d_ma, lin, col);

	cout << endl;
}
