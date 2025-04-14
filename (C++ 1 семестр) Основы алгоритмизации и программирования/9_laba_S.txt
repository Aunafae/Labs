#include <iostream>
#include <fstream>
#include <string>

using namespace std;

struct workers
{
	int number, salary;
	char name[10], surname[10], patronymic[15], post[15], gender;
};

int main()
{
	setlocale(LC_ALL, "Russian");
	int choice;
	while (1)
	{
		cout << "1 - Запись данных о сотрудниках в файл\n2 - Чтение данных о сотрудниках из файла и вывод статистики\n3 - Выход" << endl;
		cin >> choice;
		if (choice == 1)
		{
			cout << endl << "Введите путь до файла: ";
			string path;
			cin >> path;
			int count;
			cout << "\nСколько сотрудников хотите ввести?" << endl << endl;
			cin >> count;
			workers* massiv = new workers[count];
			for (int i = 0; i < count; i++)
			{
				cout << endl << "Введите табельный номер: ";
				cin >> massiv[i].number;
				cout << endl << "Введите ФИО: ";
				cin >> massiv[i].name >> massiv[i].surname >> massiv[i].patronymic;
				cout << endl << "Введите оклад: ";
				cin >> massiv[i].salary;
				cout << endl << "Введите должность: ";
				cin >> massiv[i].post;
				cout << endl << "Введите пол ( m / w ): ";
				cin >> massiv[i].gender;
				cout << endl;
			}
			ofstream file(path, ios_base::app);
			file.ostream::write((char*)massiv, count * sizeof(workers));
			file.close();
			delete[] massiv;
		}
		if (choice == 2)
		{
			cout << endl << "Введите путь до файла: ";
			string path2;
			cin >> path2;
			ifstream file2(path2);
			file2.seekg(0, ios::end);
			int size_fail = file2.tellg();
			file2.close();
			file2.open(path2, ios_base::in);
			int correctness = (size_fail % sizeof(workers));
			if (correctness == 0)
			{
				cout << endl << "Данные в файле записаны корректно" << endl << endl;
				int count2;
				count2 = (size_fail) / (sizeof(workers));
				workers* massiv2 = new workers[count2];
				file2.istream::read((char*)massiv2, count2 * sizeof(workers));
				int count_m = 0, count_w = 0, salary_m = 0, salary_w = 0, salary_mw = 0;
				for (int i = 0; i < count2; i++)
				{
					if (massiv2[i].gender == 'm')
					{
						count_m += 1;
						salary_m += massiv2[i].salary;
					}
					else if (massiv2[i].gender == 'w')
					{
						count_w += 1;
						salary_w += massiv2[i].salary;
					}
				}
				salary_mw = salary_m + salary_w;
				cout << endl << "Количество мужчин: " << count_m << endl << "Количество женщин: " << count_w << endl << "Фонд зарплат мужчин: " << salary_m << endl << "Фонд зарплат женщин: " << salary_w << endl << "Фонд зарплат работников " << salary_mw << endl << endl;
				file2.close();
				delete[] massiv2;
			}
			else if (correctness != 0)
			{
				cout << endl << "Данные в файле записаны некорректно!" << endl << endl;
				return 1;
			}
		}
		if (choice == 3)
		{
			return 0;
		}
	}
	return 0;
}
