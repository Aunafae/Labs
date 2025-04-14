#include <iostream>

using namespace std;

struct lexeme
{
	string signals;
	string title;
};

int main()
{
	setlocale(LC_ALL, "Russian");
	int d = 0;              //первый пустой элемент массива лексем
	const int razmer = 256; //размер массива
	char symbol[razmer];    //массив символов
	lexeme massiv[256];     //массив лексем
	cout << "Введите строку:\n";
	cin.getline(symbol, razmer, '\n');
	string symbols = symbol;
	int i = -1;
	while (++i < symbols.length())
	{
		//Пробелики
		if (symbols[i] == ' ')
		{
			continue;
		}
		//Цифры
		if ((symbols[i] >= 48) && (symbols[i] <= 57))
		{
			while (i < symbols.length() && (48 <= symbols[i] && symbols[i] <= 57))
			{
				massiv[d].signals += symbols[i++];
			}
			i--;//Чтобы цикл в дальнейшем обработал не вошедший в лексему символ
			massiv[d++].title = "Число                ";
		}
		//Идентификатор
		else if ((symbols[i] >= 65 && symbols[i] <= 90) || (symbols[i] >= 97 && symbols[i] <= 122))
		{
			while ((i < symbols.length()) && ((symbols[i] >= 48 && symbols[i] <= 57) || (symbols[i] >= 65 && symbols[i] <= 90) || (symbols[i] >= 97 && symbols[i] <= 122)))
			{
				massiv[d].signals += symbols[i++];
			}
			i--;
			massiv[d++].title = "Идентификатор        ";
		}
		//Сравнение и присваивание
		else if (i < symbols.length())
		{
			if (symbols[i] == 62 && symbols[i + 1] == 61)
			{
				int a = 0;
				while (a < 2)
				{
					a += 1;
					massiv[d].signals += symbols[i++];
				}
				i--;
				massiv[d++].title = "Больше или равно     ";
			}
			else if (symbols[i] == 60 && symbols[i + 1] == 61)
			{
				int a = 0;
				while (a < 2)
				{
					a += 1;
					massiv[d].signals += symbols[i++];
				}
				i--;
				massiv[d++].title = "Меньше или равно     ";
			}
			else if (symbols[i] == 61)
			{
				while ((i < symbols.length()) && (symbols[i] == 61))
				{
					massiv[d].signals += symbols[i++];
				}
				i--;
				massiv[d++].title = "Оператор присваивания";
			}
			else
		    {
    			while (i < symbols.length())
	    		{
		    		massiv[d].signals += symbols[i++];
			    }
    			i--;
	    		massiv[d++].title = "\nНеправильные символы ";
		    }
		}
	}
	cout << endl;
	for (int i = 0; i < d; i++)
	{
		cout << massiv[i].title << "   " << massiv[i].signals << endl;
	}
	return 0;
}
