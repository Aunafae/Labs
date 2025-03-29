#pragma once
#include <iostream>
#include <string>
using namespace std;

//Населённый пункт университета
extern string university_location;

//Перечисление критериев поиска
const int category_amount = 5;
enum SearchCategory {
	CAT_ALL,
	CAT_PERFECT_EXAM,
	CAT_ATTEST5,
	CAT_OUTSIDE_LOCATION,
	CAT_NEED_DORMITORY
};

//Абитуриент
struct Abitur {
	string surname;
	unsigned short mark[3];
	bool attest5;
	string location;
	bool need_dormitory;

	operator string();
};

struct Node;

struct Descriptor {
	Node* first = nullptr;
	Node* last = nullptr;
	int size = 0;
};


class List {
private:
	Descriptor desc[category_amount];
public:
	string read_all(SearchCategory cat);

	void clear();
	bool is_empty();
	int get_size(SearchCategory cat);
	bool insert(Abitur abitur);
	bool remove(int pos);
	void get_all(SearchCategory cat, Abitur* result_array);
	~List();
};

bool match(SearchCategory cat, Abitur& Abitur);