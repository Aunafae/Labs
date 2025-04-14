#include <iostream>

using namespace std;

struct Human
{
	int number, oklad;
	string last_name, first_name, patronymic, post, gender;
};

int main()
{
	setlocale(LC_ALL, "Russian");

	int razmer, zpfirm = 0, countw = 0, countm = 0, zpw = 0, zpm = 0;
	cout << "Введите количество работников фирмы:";
	cin >> razmer;

	Human* svedenia = new Human[razmer];

	for (int i = 0; i < razmer; i++)
	{
		cout << "Введите табельный номер\n";
		cin >> svedenia[i].number;

		cout << "Введите Фамилию\n";
		cin >> svedenia[i].last_name;

		cout << "Введите Имя\n";
		cin >> svedenia[i].first_name;

		cout << "Введите Отчество\n";
		cin >> svedenia[i].patronymic;

		cout << "Введите Оклад\n";
		cin >> svedenia[i].oklad;

		cout << "Введите Должность\n";
		cin >> svedenia[i].post;

		cout << "Введите Пол работника ( man / woman )\n";
		cin >> svedenia[i].gender;
	}

	for (int i = 0; i < razmer; i++)
	{
		zpfirm = zpfirm + svedenia[i].oklad;
	}
	cout << "Фонд зарплаты фирмы: " << zpfirm << endl;

	for (int i = 0; i < razmer; i++)
  {
		if (svedenia[i].gender == "woman")
		{
			countw += 1;
		}
		else
		{
			countm += 1;
		}
	}
	cout << "Количество мужчин: " << countm << endl;
	cout << "Количество женщин: " << countw << endl;

  for (int i = 0; i < razmer; i++)
  {
		if (svedenia[i].gender == "woman")
		{
			zpw += svedenia[i].oklad;
		}
		else
		{
			zpm += svedenia[i].oklad;
		}
	}
	cout << "Фонд зарплаты мужчин: " << zpm << endl;
	cout << "Фонд зарплаты женщин: " << zpw << endl;

	delete[] svedenia;

	return 0;
}
