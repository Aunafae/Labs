#include <iostream>
#include <string>

using namespace std;

struct Person
{
	string city, surname, organization;
	Person* left = NULL;
	Person* right = NULL;
};

struct Node
{
	string city;
	Person* person = NULL;
	Node* left = NULL;
	Node* right = NULL;
};

void add_person(Person*& n, Person* person)
{
	if (n == NULL)
	{
		n = person;
	}
	else if (person->surname == n->surname)
	{
		return;
	}
	else if (person->surname < n->surname)
	{
		add_person(n->left, person);
	}
	else if (person->surname > n->surname)
	{
		add_person(n->right, person);
	}
}

void add_node(Node*& n, Person* p)
{
	if (n == NULL)
	{
		n = new Node;
		n->person = p;
		n->city = p->city;
		return;
	}

	Node* cnt = n;
	if (p->city == cnt->city)
	{
		add_person(n->person, p);
	}
	else if (p->city <= cnt->city)
	{
		add_node(n->left, p);
	}
	else if (p->city > cnt->city)
	{
		add_node(n->right, p);
	}
}

void print_person(Person* p)
{
	if (p == NULL)
	{
		return;
	}
	print_person(p->left);
	cout << "1. " << p->surname << "  " << p->city << "  " << p->organization << endl;
	print_person(p->right);
}

void print(Node*& n)
{
	if (n == NULL)
	{
		return;
	}
	print(n->left);
	cout << "------------------------------------------------" << endl;
	cout << "Название города:  " << n->city << endl << endl;
	print_person(n->person);
	cout << endl << "------------------------------------------------" << endl << endl;
	print(n->right);
}

void remove_person(Person*& p)
{
	if (p == NULL)
	{
		return;
	}
	remove_person(p->left);
	remove_person(p->right);
	delete p;
	p = NULL;
}

void remove(Node*& n)
{
	if (n == NULL)
	{
		return;
	}
	remove(n->left);
	remove(n->right);
	remove_person(n->person);
	delete n;
	n = NULL;
}

int main()
{
	setlocale(LC_ALL, "ru");

	Node* n = nullptr;

	cout << "Чтобы прекратить ввод, введите '0' в Городе участника" << endl << endl;
	string city, surname, organization;
	while (true)
	{
		Person* person = new Person;
		cout << "Введите Город участника: ";
		getline(cin, person->city, '\n');
		if (person->city == "0")
		{
			break;
		}
		else
		{
			cout << "Введите Фамилию участника: ";
			getline(cin, person->surname, '\n');
			cout << "Введите Организацию участника: ";
			getline(cin, person->organization, '\n');
			add_node(n, person);
		}
		cout << endl;
	}
	cout << endl;
	print(n);
	remove(n);

	return 0;
}
