#include <iostream>
#include <fstream>
#include <stdio.h>

using namespace std;

int main()
{
	setlocale(LC_ALL, "Russian");
	char stroka[100];
	char symbol;
	ofstream file1("laba8.txt");
	if (!file1.is_open())
	{
		cout << "Ошибка открытия файла!" << endl;
	}
	else
	{
		cout << "Введите строку:\n" << endl;
		cin.getline(stroka, 100);
		file1 << stroka << endl;
	}
	file1.close();
	ifstream file2("laba8.txt");
	if (!file2.is_open())
	{
		cout << endl << "Ошибка открытия файла!" << endl;
	}

	ofstream file3("8.txt");
	if (!file3.is_open())
	{
		cout << endl << "Ошибка открытия файла!" << endl;
	}
	else
	{
		string strochka = "";
		char simv;
		int razmer = 0;
		while (file2.get(simv))
		{
			razmer += 1;
		}
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
				file3 << strochka;
			}
		}
	}
	
	file2.close();
	file3.close();

	remove("laba8.txt");
	char oldfilename[] = "8.txt";        // старое имя файла
	char newfilename[] = "laba8.txt";    // новое имя файла
	rename(oldfilename, newfilename);

	cout << endl << endl;
	ifstream file4("laba8.txt");
	if (!file4.is_open())
	{
		cout << endl << "Ошибка открытия файла!" << endl;
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
