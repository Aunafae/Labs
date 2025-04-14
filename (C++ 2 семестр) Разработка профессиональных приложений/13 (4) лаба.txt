#include <iostream>
#include <string>

using namespace std;

struct Node
{
	string word;
	int count = 1;
	Node* left = NULL;
	Node* right = NULL;
};

void add_node(Node*& n, string word)
{
	if (n == NULL)
	{
		n = new Node;
		n->word = word;
		return;
	}

	Node* cnt = n;
	while (true)
	{
		if (word == cnt->word)
		{
			cnt->count++;
			break;
		}
		else if (word < cnt->word)
		{
			return add_node(cnt->left, word);
		}
		else if (word > cnt->word)
		{
			return add_node(cnt->right, word);
		}
	}
}

void print(Node*& n)
{
	if (n == NULL)
	{
		return;
	}
	print(n->left);
	cout << n->word << " - " << n->count << endl;
	print(n->right);
}

void remove(Node*& n)
{
	if (n == NULL)
	{
		return;
	}
	remove(n->left);
	remove(n->right);
	delete n;
	n = NULL;
}

int main()
{
	setlocale(LC_ALL, "ru");

	Node* n = nullptr;

	string word;

	cout << "Вводите слова через enter" << endl;
	cout << "Если ввод окончен, введите '0'" << endl << endl;
	while (true)
	{
		getline(cin, word);
		if (word == "0")
		{
			break;
		}
		else
		{
			add_node(n, word);
		}
	}
	cout << endl;
	print(n);
	remove(n);

	return 0;
}
