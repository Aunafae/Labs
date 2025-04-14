#include <iostream>

using namespace std;

int main() {
  setlocale(LC_ALL, "Russian");
  while (1)
  {
    int n = -1, state = 1, proverka;
    string d;
    cout << "Напишите римскую цифру\nИли напишите 0 для выхода из программы\n";
    cin >> d;
    for (int i = 0; i < d.length(); i++)
    {
    proverka = n;
    switch (d[i])
    {
    case ('0'):
      return 0;
    case ('X'):
    {
      switch (state)
      {
        case (1):
          n = 10;
          state = 2;
          break;
        case (2):
          n += 10;
          state = 2;
          break;
        case (6):
          n += 8;
          state = 7;
          break;
        default:
          cout << "Неправильный порядок символов\n";
          break;
      }
      break;
    }
    case ('V'):
    {
      switch (state)
      {
        case (1):
          n = 5;
          state = 3;
          break;
        case (2):
          n += 5;
          state = 3;
          break;
        case (6):
          n += 3;
          state = 7;
          break;
        default:
          cout << "Неправильный порядок символов\n";
          break;
      }
        break;
    }
    case ('I'):
    {
      switch (state)
      {
        case (1):
          n = 1;
          state = 6;
          break;
        case (2):
          n += 1;
          state = 6;
          break;
        case (3):
          n += 1;
          state = 4;
          break;
        case (4):
          n += 1;
          state = 5;
          break;
        case (5):
          n += 1;
          state = 7;
          break;
        case (6):
          n += 1;
          state = 5;
          break;
        default:
          cout << "Неправильный порядок символов\n";
          break;
      }
      break;
    }
    default:
    {
      cout << "Неправильно введённый символ\n";
      proverka = -1;
      n = proverka;
      break;
    }
    }
    if (proverka == n)
    {
      n = -1;
      break;
    }
  }
  if (n > -1 && n <= 39)
  {
    cout << n << endl; 
  }
  else if (n > 39)
    cout << "Неправильный порядок символов\n";
  }
  return 0;
}
