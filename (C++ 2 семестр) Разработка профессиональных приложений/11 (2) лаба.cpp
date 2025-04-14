#include <iostream>
#include <string>

using namespace std;

struct Student
{
	int number;
	string FIO;
	string group;
	Student* next;
};

class List
{
private:
	Student* head;
	Student* last;
	int Size = 0;

public:
	List()
	{
		head = NULL;
	}

	bool is_empty()
	{
		return head == NULL;
	}

	void add_beginning(int Inumber, string IFIO, string Igroup)
	{
		Student* p = new Student();
		p->number = Inumber;
		p->FIO = IFIO;
		p->group = Igroup;
		p->next = head;
		head = p;
		Size++;
	}

	void add_end(int Inumber, string IFIO, string Igroup)
	{
		Student* p = new Student();
		p->number = Inumber;
		p->FIO = IFIO;
		p->group = Igroup;
		p->next = NULL;

		if (head == NULL)
			head = p;
		else
		{
			Student* current = head;
			while (current->next != NULL)
			{
				current = current->next;
			}
			current->next = p;
		}
		Size++;
	}

	void add_i(int Inumber, string IFIO, string Igroup, int index)
	{
		if (index == 1)
		{
			add_beginning(Inumber, IFIO, Igroup);
			return;
		}
		else if (index > Size)
		{
			cout << "Введнный элемент был добавлен в конец списка" << endl << endl;
			add_end(Inumber, IFIO, Igroup);
			return;
		}
		else
		{
			Student* slow = head;
			Student* fast = head->next;
			for (int i = 0; i < index - 2; i++)
			{
				fast = fast->next;
				slow = slow->next;
			}
			Student* p = new Student();
			p->number = Inumber;
			p->FIO = IFIO;
			p->group = Igroup;

			slow->next = p;
			p->next = fast;

			Size++;
		}
	}

	void remove_i(int index)
	{
		if (is_empty())
		{
      cout << "Список пуст!" << endl << endl;
			return;
		}
		if (index == 1)
		{
			if (is_empty()) 
      {
        cout << "Список пуст!" << endl << endl;
        return;
      }
			Student* p = head;
			head = p->next;
			delete p;
			Size--;
			return;
		}
		else if (index > Size)
		{
			cout << "В списке нет такого большого элемента!" << endl << endl;
			return;
		}
		else if (index == Size)
		{
			if (is_empty()) return;
			if (Size == 1)
			{
				if (is_empty()) return;
				Student* p = head;
				head = p->next;
				delete p;
				Size--;
				return;
			}
			Student* slow = head;
			for (int i = 0; i < index - 2; i++)
			{
				slow = slow->next;
			}
			slow->next = NULL;
			Size--;
			return;
		}

		Student* slow = head;
		Student* fast = head->next;
		for (int i = 0; i < index - 2; i++)
		{
			fast = fast->next;
			slow = slow->next;
		}
		slow->next = fast->next;
		delete fast;
		Size--;
	}

	void edit_i(int Inumber, string IFIO, string Igroup, int index)
	{
		if (is_empty())
		{
			return;
		}
		if (index == 1)
		{
			Student* p = head;
			head = p->next;
			delete p;
			add_beginning(Inumber, IFIO, Igroup);
			return;
		}
		else if (index > Size)
		{
			cout << "В списке нет такого большого элемента!" << endl << endl;
			return;
		}
		else
		{
			Student* slow = head;
			Student* fast = head->next;
			for (int i = 0; i < index - 2; i++)
			{
				fast = fast->next;
				slow = slow->next;
			}
			Student* p = new Student();
			p->number = Inumber;
			p->FIO = IFIO;
			p->group = Igroup;

			slow->next = p;
			p->next = fast->next;

			delete fast;
		}
	}

	void print()
	{
		if (is_empty())
		{
			cout << "Список пуст!" << endl << endl;
			return;
		}
		Student* current = head;
		while (current)
		{
			cout << current->number << endl << current->FIO << endl << current->group << endl << endl;
			current = current->next;
		}
		cout << endl;
	}

	void remove()
	{
		while (not (is_empty()))
		{
			Student* current = head;
			head = current->next;
			delete current;
		}
		Size = 0;
	}
};

int main()
{
	setlocale(LC_ALL, "Russian");
	int index = 0;
	string c;

	List st;

	while (c[0] != '7')
	{
		cout << "Выберите один из пунктов:\n1) Добавить в начало\n2) Добавить в конец\n3) Добавить в i-ую позицию\n4) Удалить из i-ой позиции\n5) Изменить i-ый элемент\n6) Показать содержимое\n7) Очистка и выход" << endl << endl;
		getline(cin, c);
		cout << endl;

		if (c[0] == '1' && c.length() == 1)
		{
			int num;
			string fio, gr;
			cout << "Введите номер: "; 
			cin >> num;
			cout << "Введите ФИО: ";
			cin.ignore();
      getline(cin, fio, '\n'); 
			cout << "Введите группу: ";
			cin >> gr;
			cin.ignore();
			cout << endl;
			st.add_beginning(num, fio, gr);
		}

		else if (c[0] == '2' && c.length() == 1)
		{
			int num;
			string fio, gr;
			cout << "Введите номер: ";
			cin >> num;
			cout << "Введите ФИО: ";
			cin.ignore();
      getline(cin, fio, '\n'); 
			cout << "Введите группу: ";
			cin >> gr;
			cin.ignore();
			cout << endl;
			st.add_end(num, fio, gr);
		}

		else if (c[0] == '3' && c.length() == 1)
		{
			cout << "Введите индекс (начиная с 1): ";
			cin >> index;
      if (index < 1)
      {
        cout << "Индекс слишком маленький" << endl << endl;
        cin.ignore();
      }
      else
      {
        int num;
  			string fio, gr;
	   	  cout << "Введите номер: ";
  	 		cin >> num;
	  		cout << "Введите ФИО: ";
	 		  cin.ignore();
        getline(cin, fio, '\n'); 
		  	cout << "Введите группу: ";
  			cin >> gr;
	 	   	cin.ignore();
	   		cout << endl;
        
        st.add_i(num, fio, gr, index);
      }
		}

		else if (c[0] == '4' && c.length() == 1)
		{
			cout << "Введите индекс (начиная с 1): ";
			cin >> index;
      if (index < 1)
      {
        cout << "Индекс слишком маленький" << endl << endl;
        cin.ignore();
      }
      else
      {
		  	cin.ignore();
			  cout << endl << endl;
			  st.remove_i(index);
      }
		}

		else if (c[0] == '5' && c.length() == 1)
		{
			cout << "Введите индекс (начиная с 1): ";
			cin >> index;
			if (index < 1)
      {
        cout << "Индекс слишком маленький" << endl << endl;
        cin.ignore();
      }
      else
      {
  			int num;
	 		  string fio, gr;
	 		  cout << "Введите номер: ";
	 		  cin >> num;
		  	cout << "Введите ФИО: ";
			  cin.ignore();
        getline(cin, fio, '\n'); 
	   		cout << "Введите группу: ";
		  	cin >> gr;
			  cin.ignore();
			  cout << endl;
			  st.edit_i(num, fio, gr, index);
      }
		}

		else if (c[0] == '6' && c.length() == 1)
		{
			st.print();
		}

		else if (c[0] == '7' && c.length() == 1)
		{
			st.remove();
		}

		else if (!c.length())
		{
			cout << "Вы ничего не ввели, попробуйте ещё раз" << endl << endl;
		}

		else
		{
			cout << "Вы ввели неправильное число, попробуйте ещё раз" << endl << endl;
		}
	}

	return 0;
}
