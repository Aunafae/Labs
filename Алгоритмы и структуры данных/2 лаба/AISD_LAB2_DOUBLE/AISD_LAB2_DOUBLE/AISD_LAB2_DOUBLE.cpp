#include "LAB2.h"
#include "Windows.h"
#include <chrono>
#include <random>
typedef chrono::steady_clock my_clock;
my_clock::time_point start;
my_clock::time_point finish;

string university_location;

long long timer = 0;

unsigned long long test_count = 10000;
float p = 100;
int to = 100;

Abitur input() {
	Abitur elem;


	cout << "Фамилия >> ";
	cin >> elem.surname;
	cout << "Оценки за три вступительных экзамена >> ";
	cin >> elem.mark[0] >> elem.mark[1] >> elem.mark[2];

	while (true) {
		string answer;
		cout << "Имеется аттестат с отличием? (да/нет) >> ";
		cin >> answer;
		if (answer == "да") elem.attest5 = true;
		else if (answer == "нет") elem.attest5 = false;
		else {
			cout << "Ответ не распознан." << endl;
			continue;
		}
		break;
	}

	cout << "Населённый пункт >> ";
	cin >> elem.location;

	while (true) {
		string answer;
		cout << "Нуждается в общежитии? (да/нет) >> ";
		cin >> answer;
		if (answer == "да") elem.need_dormitory = true;
		else if (answer == "нет") elem.need_dormitory = false;
		else {
			cout << "Ответ не распознан." << endl;
			continue;
		}
		break;
	}

	return elem;
}

int get_rand(int from, int to) {
	random_device dev;
	mt19937 rng(dev());
	uniform_int_distribution<mt19937::result_type> r(from, to);
	return r(rng);
}

int main() {
	setlocale(LC_ALL, "ru");
	SetConsoleCP(1251);
	SetConsoleOutputCP(1251);

	university_location = "УНИВЕРСИТЕТ";
	//cout << "Населённый пункт университета >> ";
	//cin >> university_location;

	List list;

	cout << "Вероятность попадания для подсписка: " << (float)p / to << endl;
	
	//ВСТАВКА
	for (int i = 0; i < 20; i++) cout << ".";
	cout << endl;
	for (int i = 1; i <= test_count; i++) {
		if (i % (test_count / 20) == 0) cout << "|";

		Abitur abit;
		abit.surname = to_string(i) + "-ФАМИЛИЯ";
		abit.attest5 = get_rand(1, to) < p;
		abit.location = (get_rand(1, to) < p) ? "где-то не здесь " + to_string(i) : university_location;
		abit.mark[0] = 5; abit.mark[1] = 4 + (get_rand(1, to) < p); abit.mark[2] = 5;
		abit.need_dormitory = get_rand(1, to) < p;

		start = my_clock::now();
		list.insert(abit);
		finish = my_clock::now();
		timer += chrono::duration_cast<chrono::nanoseconds>(finish - start).count();
	}
	cout << timer * 0.000000001 << "с" << endl;
	
	//УДАЛЕНИЕ
	timer = 0;
	for (int i = 0; i < 20; i++) cout << ".";
	cout << endl;
	for (int i = 1; i <= test_count; i++) {
		if (i % (test_count / 20) == 0) cout << "|";

		int pos = get_rand(0, list.get_size(CAT_ALL)-1);

		start = my_clock::now();
		list.remove(pos);
		finish = my_clock::now();
		timer += chrono::duration_cast<chrono::nanoseconds>(finish - start).count();
	}
	cout << timer * 0.000000001 << "с" << endl;
	system("pause");

	//ПОИСК ПО КАТЕГОРИЯМ
	Abitur* result_array = new Abitur[list.get_size(CAT_ALL)];
	for (int i = 0; i < category_amount; i++) {
		timer = 0;
		start = my_clock::now();
		list.get_all((SearchCategory)i, result_array);
		finish = my_clock::now();
		timer += chrono::duration_cast<chrono::nanoseconds>(finish - start).count();
		cout << i << " категория: " << timer * 0.000000001 << "с" << endl;
	}
	delete[] result_array;
	system("pause");


	int cmd;
	while (true) {
		cout << "\033[0m";//Сделать текст стандартным
		cout <<
			"\
Список команд:\n\
	1. Ввод записи об абитуриенте.\n\
	2. Формирование и вывод списков абитуриентов по критериям:\n\
		1) Все экзамены сданы на «отлично»;\n\
		2) Имеется аттестат с отличием;\n\
		3) Проживает за пределами населенного пункта, в котором расположен университет;\n\
		4) Нуждается в общежитии.\n\
	3. Формирование и вывод полного списка абитуриентов.\n\
	4. Удаление записи об абитуриенте.\n\
	5. Удаление всех записей многосвязного списка.\n\
	0. Выход из программы.\n\
";

		cout << "Введите номер команды >> ";
		cin >> cmd;
		cout << "\033[1m";//Сделать текст жирным
		cout << "\n";

		string answer;

		if (cmd == 1) {
			if (list.insert(input()))
				answer = "Студент добавлен.";
			else
				answer = "Студент не добавлен. Такой позиции ";
		}

		else if (cmd == 2) {
			int cat;
			cout << "Критерий >> ";
			cin >> cat;
			if (1 <= cat && cat <= 4)
				answer = list.read_all((SearchCategory)cat);
			else
				answer = "Нет такого номера.";
		}

		else if (cmd == 3) {
			answer = list.read_all(CAT_ALL);
		}

		else if (cmd == 4) {
			if (list.is_empty()) {
				answer = "Список пуст.";
			}
			else {
				int total_size = list.get_size(CAT_ALL);

				Abitur* Abiturs = new Abitur[total_size];
				list.get_all(CAT_ALL, Abiturs);
				for (int i = 0; i < total_size; i++) {
					cout << to_string(i + 1) + ". " + Abiturs[i].surname + ".\n";
				}
				delete[] Abiturs;

				int num;
				cout << "Номер студента >> ";
				cin >> num;
				if (num < 0 || num > total_size)
					answer = "Указан неверный номер.";
				else {
					list.remove(num - 1);
					answer = "Студент удалён.";
				}
			}
		}

		else if (cmd == 5) {
			list.clear();
			answer = "Список очищен.";
		}

		else if (cmd == 0) {
			list.clear();
			cout << "Программа завершена." << endl;
			exit(0);
		}

		else
			answer = "Нет команды с таким номером";

		cout << answer << endl;
	}
}