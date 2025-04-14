#include <iostream>
#include <fstream>
#include <stdio.h>

using namespace std;

int main()
{
	setlocale(LC_ALL, "Russian");
	char stroka[500];
	char symbol;
	ofstream file1("laba8.txt");
	if (!file1.is_open())
	{
		cout << "Ошибка открытия файла!" << endl;
    file1.close();
    return 1;
	}
	else
	{
		cout << "Введите строку:\n" << endl;
		while (true)
		{
			string linia;
			cin.getline(stroka, 500, '\n');
			if (int(stroka[0]) == 0)
			{
				break;
			}
			linia = stroka;
			file1 << stroka << endl;
			file1.close();
			ifstream file2("laba8.txt");
			if (!file2.is_open())
			{
				cout << endl << "Ошибка открытия файла!" << endl;
        file2.close();
        return 1;
			}
			ofstream file3("8.txt", ofstream::app);
			if (!file3.is_open())
			{
				cout << endl << "Ошибка открытия файла!" << endl;
        file3.close();
        return 1;
			}
			else
			{
				string strochka = "";
				char simv;
				int razmer = 0;
				razmer = linia.length();
				int i = 0;
				if (stroka[0] == ',')
				{
					i += 1;
					while (stroka[i] == ',')
					{
						i += 1;
					}
				}
				int f = i;
				int count_bug = ' ';
				while (count_bug != 0)
				{
					count_bug = 0;
					for (i; i < razmer; i++)
					{
						while (stroka[i] == ',' and stroka[i + 1] == ',')
						{
							//Две запятые подряд
							strochka += stroka[i];
							i += 1;
							i += 1;
							count_bug += 1;
						}
						while (stroka[i] == ',' and stroka[i + 1] != ' ')
						{
							//Нет пробела после запятой
							strochka += stroka[i];
							strochka += ' ';
							i += 1;
              razmer += 1;
							count_bug += 1;
						}
						while (stroka[i] == ' ' and stroka[i + 1] == ',')
						{
							//Пробел перед запятой!
							strochka += stroka[i + 1];
							i += 1;
							count_bug += 1;
						}
						//Всё ок
						strochka += stroka[i];
					}
					if (count_bug != 0)
					{
						for (int j = 0; j < 100; j++)
						{
							stroka[j] = ' ';
						}
						for (int k = 0; k < strochka.length(); k++)
						{
							stroka[k] = strochka[k];
						}
						strochka = "";
						i = 0;
					}
					else
					{
						file3 << '\n' << strochka;
					}
				}
			}

			file2.close();
			file3.close();
		}
	}

	remove("laba8.txt");
	rename("8.txt", "laba8.txt");

	cout << endl << endl;
	ifstream file4("laba8.txt");
	if (!file4.is_open())
	{
		cout << endl << "Ошибка открытия файла!" << endl;
    file4.close();
    return 1;
	}
	else
	{
		char simv;
		while (file4.get(simv))
		{
			cout << simv;
		}
		cout << endl;
	}
	file4.close();

	return 0;
}
