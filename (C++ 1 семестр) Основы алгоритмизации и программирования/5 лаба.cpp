#include <iostream>

using namespace std;

union worker
{
	struct Tex
	{
		int number, experience, salary, prof, e;
		char FIO[3];
		enum Education
		{
			SecondaryProf,
			Higher
		} education;
	} T;

	struct Ped
	{
		int number, experience, salary, pro, s, z;
		char FIO[3];
		enum Stepen
		{
			Candidate,
			Doctor,
			No
		} stepen;
		enum Zvanie
		{
			Docent,
			Professor,
			Net
		} zvanie;
	} P;
};

int main()
{
	setlocale(LC_ALL, "Russian");
	string c, speciality;
	int rab = -1, zp_tex = 0, count_tex = 0, count_ped = 0, t = 10, p = 20;

	const int razmer = 5;
	worker massiv[razmer];

	while (1)
	{
		cout << endl << "Введите: \nexit - для выхода из программы \nadd - добавить сведения о сотруднике \nall_worker - сведения обо всех сотрудниках ВУЗа \ncount_tex - количество инженерно-технических работников \ncount_ped - количество научно-педогагических работников \nall_doctor - сведения обо всех докторах наук \nsalary_tex - фонд зарплат инженерно-технических работников\n" << endl;
		cin >> c;
		if (c == "exit")
		{
			return 0;
		}

		else if (c == "add")
		{
			rab += 1;
			cout << "Выберите: \ntex - Нучно-технический работник \nped - Научно-педагогический работник\n";
			cin >> speciality;

			if (speciality == "tex")
			{
				massiv[rab].T.prof = t;

				cout << "Введите табельный номер\n";
				cin >> massiv[rab].T.number;

				cout << "Введите ФИО (3 буквы без пробела)\n";
				cin >> massiv[rab].T.FIO;

				cout << "Введите стаж\n";
				cin >> massiv[rab].T.experience;

				cout << "Введите образование (sr - среднее профессиональное / vis - высшее)\n";
				string obrazovanie;
				cin >> obrazovanie;
				if (obrazovanie == "sr")
				{
					massiv[rab].T.e = worker::Tex::Education::SecondaryProf;
				}
				else if (obrazovanie == "vis")
				{
					massiv[rab].T.e = worker::Tex::Education::Higher;
				}

				cout << "Введите оклад\n";
				cin >> massiv[rab].T.salary;

				//для salary_tex (з/п инж-тех работников)
				zp_tex += massiv[rab].T.salary;
				//для count_tex (кол-во инж-тех работников)
				count_tex += 1;
			}

			if (speciality == "ped")
			{
				massiv[rab].P.pro = p;

				cout << "Введите табельный номер\n";
				cin >> massiv[rab].P.number;

				cout << "Введите ФИО (3 буквы без пробела)\n";
				cin >> massiv[rab].P.FIO;

				cout << "Введите стаж\n";
				cin >> massiv[rab].P.experience;

				cout << "Введите учёную степень (kan - кандидат наук / doc - доктор наук / no - отсутствует)\n";
				string st;
				cin >> st;
				if (st == "kan")
				{
					massiv[rab].P.s = worker::Ped::Stepen::Candidate;
				}
				else if (st == "doc")
				{
					massiv[rab].P.s = worker::Ped::Stepen::Doctor;
				}
				else if (st == "no")
				{
					massiv[rab].P.s = worker::Ped::Stepen::No;
				}

				cout << "Введите учёное звание ( doz - доцент / pr - профессор / no - отсутствует )\n";
				string zv;
				cin >> zv;
				if (zv == "doz")
				{
					massiv[rab].P.z = worker::Ped::Zvanie::Docent;
				}
				else if (zv == "pr")
				{
					massiv[rab].P.z = worker::Ped::Zvanie::Professor;
				}
				else if (zv == "no")
				{
					massiv[rab].P.z = worker::Ped::Zvanie::Net;
				}

				cout << "Введите оклад\n";
				cin >> massiv[rab].P.salary;

				//для count_ped (кол-во науч-пед работников)
				count_ped += 1;
			}
		}

		else if (c == "all_worker")
		{
			for (int i = 0; i < rab + 1; i++)
			{
				if (massiv[i].T.prof == t)
				{
					cout << massiv[i].T.number << endl << massiv[i].T.FIO << endl << massiv[i].T.experience << endl << massiv[rab].T.e << endl << massiv[i].T.salary << endl << endl;
				}
				else if (massiv[i].P.pro == p)
				{
					cout << massiv[i].P.number << endl << massiv[i].P.FIO << endl << massiv[i].P.experience << endl << massiv[i].P.s << endl << massiv[i].P.z << endl << massiv[i].P.salary << endl << endl;
				}
			}
		}

		else if (c == "count_tex")
		{
			cout << endl << count_tex << endl;
		}

		else if (c == "count_ped")
		{
			cout << endl << count_ped << endl;
		}

		else if (c == "all_doctor")
		{
			for (int i = 0; i < rab + 1; i++)
			{
				if (massiv[i].P.pro == p)
				{
					if (massiv[i].P.s == worker::Ped::Stepen::Doctor)
					{
						cout << massiv[i].P.number << endl << massiv[i].P.FIO << endl << massiv[i].P.experience << endl << massiv[i].P.s << endl << massiv[i].P.z << endl << massiv[i].P.salary << endl << endl;
					}
				}
			}
		}

		else if (c == "salary_tex")
		{
			cout << endl << zp_tex << endl;
		}

		else
		{
			cout << endl << "Такой команды нет\n";
		}

	}
	return 0;
}
