#include "LAB2.h"

struct Node {
	Abitur value;
	Node* next[category_amount];

	Node() {
		for (int i = 0; i < 5; i++) next[i] = nullptr;
	}
};

Abitur::operator string() {
	string result = surname + ": ";
	result += "\n	Экзамены: " + to_string(mark[0]) + " " + to_string(mark[1]) + " " + to_string(mark[2]);
	result += "\n	Аттестат с отличием: ";
	result += attest5 ? "да" : "нет";
	if (university_location == location)
		result += "\n	В пределах населённого пункта университета (" + location + ")";
	else
		result += "\n	За пределами населённого пункта университета (" + location + ")";
	result += "\n	Нуждается в общежитии: ";
	result += need_dormitory ? "да" : "нет";
	return result + "\n";
}

string List::read_all(SearchCategory cat) {
	int sz = desc[(int)cat].size;
	string result = "Список (size = " + to_string(sz) + "):\n";

	Abitur* Abiturs = new Abitur[sz];
	get_all(cat, Abiturs);

	for (int i = 0; i < sz; i++) {
		result += to_string(i + 1) + ". " + string(Abiturs[i]);
	}

	delete[] Abiturs;
	return result;
}

void List::clear() {
	Node* current = desc[0].first;
	while (current) {
		Node* next = current->next[0];
		delete current;
		current = next;
	}

	for (int i = 0; i < category_amount; i++) {
		desc[i].first = nullptr;
		desc[i].last = nullptr;
		desc[i].size = 0;
	}
}

bool List::is_empty() {
	return desc[0].first == nullptr;
}

int List::get_size(SearchCategory cat) {
	return desc[(int)cat].size;
}

bool List::insert(Abitur abitur) {
	//Создаём узел с добавляемым содержимым
	Node* node = new Node();
	node->value = abitur;

	//Берём предшествующий узел из каждой категории и привязываем созданный узел
	for (int i = 0; i < category_amount; i++) {
		if (!match((SearchCategory)i, abitur))
			continue;

		//Нет предшествующего узла для данной категории. Узел - начало списка.
		if (desc[i].last == nullptr) {
			desc[i].first = node;
			desc[i].last = node;
		}

		//Есть предшествующий узел
		else {
			desc[i].last->next[i] = node;
			desc[i].last = node;
		}

		desc[i].size++;
	}

	return true;
}

bool List::remove(int pos) {
	if (pos < 0 || get_size(CAT_ALL) <= pos) return false;
	if (is_empty()) return false;

	Node* prev0 = nullptr;
	Node* node = desc[0].first;
	for (int i = 0; i < pos; i++)
		prev0 = node;
		node = node->next[0];

	int m = 0;
	bool matches[category_amount];
	for (int i = 0; i < category_amount; i++) {
		matches[i] = match((SearchCategory)i, node->value);
		m += matches[i];
	}
	if (m == 1) {
		prev0->next[0] = node->next[0];
		delete node;
		return true;
	}

	//Массив предшествующих узлов
	Node* prev[category_amount];
	for (int i = 0; i < category_amount; i++)
		prev[i] = nullptr;

	if (pos > 0) prev[0] = desc[0].first;
	for (int i = 0; i < pos; i++) {

		for (int j = 1; j < category_amount; j++) {
			if (matches[i] == false) continue;
			if (match((SearchCategory)j, prev[0]->value)) {
				prev[j] = prev[0];
			}
		}

		//Кроме последней итерации идём дальше
		if (i != pos - 1) prev[0] = prev[0]->next[0];
	}

	//Удаляем узел
	for (int i = 0; i < category_amount; i++) {
		if (!match((SearchCategory)i, node->value))
			continue;

		//Узел - конец списка.
		if (node == desc[i].last) {
			desc[i].last = prev[i];
		}
		//Узел - начало списка
		if (node == desc[i].first) {
			desc[i].first = node->next[i];
		}
		//Есть предшествующий узел
		if (prev[i]) {
			prev[i]->next[i] = node->next[i];
		}

		desc[i].size--;
	}
	delete node;
	return true;
}

void List::get_all(SearchCategory cat, Abitur* result_array) {
	int cat_number = (int)cat;
	Node* current = desc[cat_number].first;

	int i = 0;
	while (current) {
		result_array[i++] = current->value;
		current = current->next[cat_number];
	}
}

List::~List() { clear(); }


bool match(SearchCategory cat, Abitur& Abitur) {
	switch (cat) {
	case CAT_ALL:
		return true;
	case CAT_PERFECT_EXAM:
		return Abitur.mark[0] == 5 && Abitur.mark[1] == 5 && Abitur.mark[2] == 5;
	case CAT_ATTEST5:
		return Abitur.attest5;
	case CAT_OUTSIDE_LOCATION:
		return Abitur.location != university_location;
	case CAT_NEED_DORMITORY:
		return Abitur.need_dormitory;
	}
	return false;
}