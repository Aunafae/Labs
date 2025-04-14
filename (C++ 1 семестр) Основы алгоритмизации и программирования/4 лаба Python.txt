number = []
oklad = []
last_name = []
first_name = []
patronymic = []
post = []
gender = []
zpfirm = 0
countw = 0
countm = 0
zpw = 0
zpm = 0
print ("Введите количество работников")
c = int(input())
while c > 0:
  c -= 1
  print ("Введите номер")
  number.append (int(input()))
  print ("Введите оклад")
  oklad.append (int(input()))
  print ("Введите фамилию")
  last_name.append (input())
  print ("Введите имя")
  first_name.append (input())
  print ("Введите отчество")
  patronymic.append (input())
  print ("Введите должность")
  post.append (input())
  print ("Введите пол")
  gender.append (input())
for i in range (0, len(oklad)):
  zpfirm += oklad[i]
for i in range (0, len(gender)):
  if gender[i] == "m":
    countm += 1
  elif gender[i] == "w":
    countw += 1
for i in range (0, len(gender)):
  if gender[i] == "m":
    zpm += oklad[i]
  else:
    zpw += oklad[i]
print ("Фонд зарплаты фирмы: ", zpfirm, "Количество мужчин: ", countm, "Количество женщин: ", countw, "Фонд зарплаты мужчин: ", zpm , "Фонд зарплаты женщин: ", zpw)
