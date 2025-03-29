from kivy.app import App  # Делает приложение (запуск)
from kivy.uix.label import Label  # Вывод текста на экран
from kivy.uix.button import Button  # Кликабельные кнопочки
from kivy.config import Config  # Настройки
from pygments.lexers import HtmlLexer  # Настройки кнопок
from kivy.uix.boxlayout import BoxLayout  # Ориентация текста/кнопочек (горизонтально/вертикально)
from kivy.uix.gridlayout import GridLayout  # Ориентация текста/кнопочек (2х2/3х3)
from kivy.uix.stacklayout import StackLayout  # Ориентация текста/кнопочек (стек/как мешки в машинку)
from kivy.uix.anchorlayout import AnchorLayout  # Ориентация текста/кнопочек (более гибкое расположение на экране)
from kivy.uix.floatlayout import FloatLayout  # Ориентация текста/кнопочек (любое расположение на экране)
from kivy.core.window import Window  # Для масштабирования окна
import time  # Остановка выполнения программы (если понадобится пауза)
from kivy.uix.screenmanager import ScreenManager, Screen  # Для смены экрана
from kivy.config import ConfigParser  # Для настройки перехода и пр
from kivy.uix.recycleview import RecycleView  # Для прокрутки
import random  # Для рандомизации
from kivy.metrics import dp
import os
import ast

Window.size = (590, 680)
Window.clearcolor = (.75, .60, .35, 1)
Window.title = "Андердарк"

HP = 0  # ХП персонажа (начальное рассчитывается по формуле: HP = 100 + n
MAX_HP = 0  # Максимальное HP персонажа
Experience = 0  # Опыт
Trophies = 0  # Трофеи
LVL = 1  # Уровень (Увеличивается по условию: if(Experience >= 50 + 20*LVL):   LVL += 1
Floor = 1  # Этаж подземелья = уровню персонажа

Class = " "  # Класс персонажа, определяющий дальнейшие начальные характеристики:
n = 0  # Число, необходимое для высчитывания начального и максимального HP персонажа
Skill = 0  # Ловкость (зависит от класса)
Luck = 0  # Удача (зависит от класса)
Strenght = 0  # Сила (зависит от класса)
Endurance = 1  # Выносливость (зависит от класса)

Difficulty = " "  # Сложность игры, определяющая дальнейшие характеристики:
k = 2  # Коэфициент удара моба по персонажу (зависит от сложности игры, изменяемой в настройках)

HP_normal_monster = ((random.randint(50, 80)) + (10 * Floor))    # HP обычного монстра
HP_average_monster = ((random.randint(60, 90)) + (10 * Floor))   # HP среднего монстра
HP_elite_monster = ((random.randint(90, 120)) + (10 * Floor))    # HP элитного монсра

damage_from_normal_monster = (random.randint(10, 15) * k + (Floor * 2)) // Endurance   # Урон от обычного монстра
damage_from_average_monster = (random.randint(17, 22) * k + (Floor * 2)) // Endurance  # Урон от среднего монстра
damage_from_elite_monster = (random.randint(27, 33) * k + (Floor * 2)) // Endurance    # Урон от элитного монстра

list = ["Химерий", "Скелет", "Огненная фурия", "Кудуку", "Отверженный", "Скелет лучник", "Некромант", "Теневая мумия"]
list += [ "Каменный голем", "Дроу", "Дуергары", "Иллитид", "Пещерный паук", "Ядовитый паук", "Шипастый шар", "Нежить"]
list += ["Статуя", "Иномирец", "Иглохлыст", "Злая тень", "Стальной скелет", "Загробный иномирец", "Мышь"]
list += ["Красный слизень", "Огромный червь", "Токсичный слизень", "Мёртвый шахтёр", "Летучая мышь", "Мумия"]

mob = " "
HP_mob = 0
Name_Mob = " "
reward = " "

damage_from_monster = 0

# Инвентарь персонажа (сюда будут добавлены все возможные предметы игры, начальное количество которых будет равно 0)

Usual_healing_potion = 0  # Обычное зелье лечения
Powerful_healing_potion = 0  # Сильное зелье лечения
Epic_healing_potion = 0  # Эпическое зелье лечения

# В каждом слоте может быть только 1 предмет
# Старый предмет будет храниться в эфимерном инвентаре, который нельзя просмотреть
helmet = " "  # Шлем - добавляет "X" к выносливости
bib = " "  # Нагрудник - добавляет "X" к HP
pants = " "  # Штаны - добавляет "X" к HP
boots = " "  # Сапоги - добавляет "X" к ловкости
necklace = " "  # Ожерелье - добавляет "X" к удаче
ring = " "  # Кольцо - добавляет "X" к силе
weapon = " "  # Оружие - добавляет "X" к силе

# Список предметов
helmet_leather = 0
helmet_cloth = 0
helmet_epic = 0
helmet_legendary = 0

bib_leather = 0
bib_cloth = 0
bib_epic = 0
bib_legendary = 0

pants_leather = 0
pants_cloth = 0
pants_epic = 0
pants_legendary = 0

boots_leather = 0
boots_cloth = 0
boots_epic = 0
boots_legendary = 0

necklace_leather = 0
necklace_cloth = 0
necklace_epic = 0
necklace_legendary = 0

ring_leather = 0
ring_cloth = 0
ring_epic = 0
ring_legendary = 0

weapon_leather = 0
weapon_cloth = 0
weapon_epic = 0
weapon_legendary = 0

# Конец инвентаря

# Вручную устанавливаемый счётчик слайдов
# (количество возможных вариаций подземелья)
Count_Screen = 27


class Game_Over(Screen):
    def __init__(self, **kw):
        super(Game_Over, self).__init__(**kw)

    def on_enter(self):
        priv = BoxLayout(orientation="vertical")
        priv.add_widget(Label(text="Игра пройдена!", font_size=40,
                              color=[62 / 255, 28 / 255, 0 / 255, 1]))
        priv.add_widget(Button(text="Назад",
                               background_color=[.75, .60, .30, 1],
                               font_size=40,
                               color=[62 / 255, 28 / 255, 0 / 255, 1],
                               background_normal="", on_press=lambda x: set_screen('Мой_персонаж')))
        self.add_widget(priv)
        print("Класс персонажа: ", Class, "\nБонус к ХП: ", n, "\nКоличество ХП: ", HP, "\nЛовкость: ", Skill,
              "\nУдача: ", Luck, "\nСила: ", Strenght, "\nВыносливость: ", Endurance)

    def in_leave(self):
        self.add_widget.clear_widgets()


class Game_Over_Kill(Screen):
    def __init__(self, **kw):
        super(Game_Over_Kill, self).__init__(**kw)

    def on_enter(self):
        priv = BoxLayout(orientation="vertical")
        priv.add_widget(Label(text="Вы умерли!", font_size=40,
                              color=[62 / 255, 28 / 255, 0 / 255, 1]))
        priv.add_widget(Button(text="Назад",
                               background_color=[.75, .60, .30, 1],
                               font_size=40,
                               color=[62 / 255, 28 / 255, 0 / 255, 1],
                               background_normal="", on_press=lambda x: set_screen('Мой_персонаж')))
        self.add_widget(priv)
        print("Класс персонажа: ", Class, "\nБонус к ХП: ", n, "\nКоличество ХП: ", HP, "\nЛовкость: ", Skill,
              "\nУдача: ", Luck, "\nСила: ", Strenght, "\nВыносливость: ", Endurance)

    def in_leave(self):
        self.add_widget.clear_widgets()


class Main_menu(Screen):
    def __init__(self, **kw):
        super(Main_menu, self).__init__(**kw)
        menu = BoxLayout(orientation="vertical")
        menu.add_widget(Button(text="Новая игра",
                               font_size=50,
                               background_color=[.75, .60, .35, 1],
                               color=[62 / 255, 28 / 255, 0 / 255, 1],
                               background_normal="", on_press=self.Новая))
        menu.add_widget(Button(text="Продолжить",
                               font_size=50,
                               background_color=[.75, .60, .30, 1],
                               color=[62 / 255, 28 / 255, 0 / 255, 1],
                               background_normal="", on_press=self.Прода))
        menu.add_widget(Button(text="Мой персонаж",
                               font_size=50,
                               background_color=[.75, .60, .35, 1],
                               color=[62 / 255, 28 / 255, 0 / 255, 1],
                               background_normal="", on_press=self.MyPers))
        menu.add_widget(Button(text="Магазин",
                               font_size=50,
                               background_color=[.75, .60, .30, 1],
                               color=[62 / 255, 28 / 255, 0 / 255, 1],
                               background_normal="", on_press=lambda x: set_screen('Магазин')))
        menu.add_widget(Button(text="Правила",
                               font_size=50,
                               background_color=[.75, .60, .35, 1],
                               color=[62 / 255, 28 / 255, 0 / 255, 1],
                               background_normal="", on_press=lambda x: set_screen('Правила')))
        menu.add_widget(Button(text="История",
                               font_size=50,
                               background_color=[.75, .60, .30, 1],
                               color=[62 / 255, 28 / 255, 0 / 255, 1],
                               background_normal="", on_press=lambda x: set_screen('История')))
        menu.add_widget(Button(text="Настройки",
                               font_size=50,
                               background_color=[.75, .60, .35, 1],
                               color=[62 / 255, 28 / 255, 0 / 255, 1],
                               background_normal="", on_press=lambda x: set_screen('Настройки')))
        menu.add_widget(Button(text="Выход",
                               font_size=50,
                               background_color=[.75, .60, .30, 1],
                               color=[62 / 255, 28 / 255, 0 / 255, 1],
                               background_normal="", on_press=exit))
        self.add_widget(menu)

    def Новая(self, event):
        global HP, MAX_HP, Experience, Trophies, LVL, Floor, Class, n, Skill, Luck, Strenght, Endurance
        global helmet, bib, pants, boots, necklace, ring, weapon, pants_leather, pants_cloth, pants_epic, pants_legendary
        global helmet_leather, helmet_cloth, helmet_epic, helmet_legendary, bib_leather, bib_cloth, bib_epic, bib_legendary
        global boots_leather, boots_cloth, boots_epic, boots_legendary, necklace_leather, necklace_cloth, necklace_epic, necklace_legendary
        global ring_leather, ring_cloth, ring_epic, ring_legendary, weapon_leather, weapon_cloth, weapon_epic, weapon_legendary
        HP = 0  # ХП персонажа (начальное рассчитывается по формуле: HP = 100 + n
        MAX_HP = 0  # Максимальное HP персонажа
        Experience = 0  # Опыт
        Trophies = 0  # Трофеи
        LVL = 1  # Уровень (Увеличивается по условию: if(Experience >= 50 + 20*LVL):   LVL += 1
        Floor = 1  # Этаж

        Class = " "  # Класс персонажа, определяющий дальнейшие начальные характеристики:
        n = 0  # Число, необходимое для высчитывания начального и максимального HP персонажа
        Skill = 0  # Ловкость (зависит от класса)
        Luck = 0  # Удача (зависит от класса)
        Strenght = 0  # Сила (зависит от класса)
        Endurance = 1  # Выносливость (зависит от класса)

        helmet = " "  # Шлем - добавляет "X" к выносливости
        bib = " "  # Нагрудник - добавляет "X" к HP
        pants = " "  # Штаны - добавляет "X" к HP
        boots = " "  # Сапоги - добавляет "X" к ловкости
        necklace = " "  # Ожерелье - добавляет "X" к удаче
        ring = " "  # Кольцо - добавляет "X" к силе
        weapon = " "  # Оружие - добавляет "X" к силе

        helmet_leather = 0
        helmet_cloth = 0
        helmet_epic = 0
        helmet_legendary = 0

        bib_leather = 0
        bib_cloth = 0
        bib_epic = 0
        bib_legendary = 0

        pants_leather = 0
        pants_cloth = 0
        pants_epic = 0
        pants_legendary = 0

        boots_leather = 0
        boots_cloth = 0
        boots_epic = 0
        boots_legendary = 0

        necklace_leather = 0
        necklace_cloth = 0
        necklace_epic = 0
        necklace_legendary = 0

        ring_leather = 0
        ring_cloth = 0
        ring_epic = 0
        ring_legendary = 0

        weapon_leather = 0
        weapon_cloth = 0
        weapon_epic = 0
        weapon_legendary = 0

        set_screen("Выбор_класса")

    def Прода(self, event):
        if Class != " ":
            i = random.randint(1, Count_Screen)
            set_screen(str(i))
        else:
            set_screen("Нет_класса")

    def MyPers(self, event):
        if Class != " ":
            set_screen("Мой_персонаж")
        else:
            set_screen("Нет_класса")


class My_character(Screen):
    def __init__(self, **kw):
        super(My_character, self).__init__(**kw)

    def on_enter(self):
        Сharacter = FloatLayout()
        Сharacter.add_widget(Button(text="<-- В главное меню",
                                    background_color=[185 / 255, 145 / 255, 75 / 255, 1],
                                    font_size=20,
                                    color=[62 / 255, 28 / 255, 0 / 255, 1],
                                    size_hint=(.9, .1), pos=(27, 610),
                                    background_normal="", on_press=self.InMenu))
        Сharacter.add_widget(Button(text="       *тут будет\nэмблема класса*",
                                    background_color=[185 / 255, 145 / 255, 75 / 255, 1],
                                    font_size=15,
                                    color=[62 / 255, 28 / 255, 0 / 255, 1],
                                    size_hint=(.3, .2), pos=(80, 400), background_normal=""))
        Сharacter.add_widget(Label(text="Мой персонаж\n\n\n\n\n\n\n\n\n\n",
                                   font_size=40,
                                   color=[62 / 255, 28 / 255, 0 / 255, 1]))
        Сharacter.add_widget(Label(text="\n\n\n\n\n"
                                        "                                    Класс:        " + str(Class) + "\n"
                                        "                                    Уровень:   " + str(LVL) + "\n"
                                        "                                    Этаж:         " + str(Floor) + "\n"
                                        "                                    Опыт:         " + str(Experience) + "\n"
                                        "                                    Трофеи:     " + str(Trophies) + "\n\n"
                                        "Характеристики:\n\n"
                                        "Ловкость: " + str(Skill) + "\n"
                                        "Сила: " + str(Strenght) + "\n"
                                        "Выносливость: " + str(Endurance) + "\n"
                                        "Удача: " + str(Luck) + "\n\n"
                                        "Инвентарь:\n"
                                        "Простое зелье лечения: " + str(Usual_healing_potion) + "\n"
                                        "Сильное зелье лечения: " + str(Powerful_healing_potion) + "\n"
                                        "Эпическое зелье лечения: " + str(Epic_healing_potion) + "\n",
                                   font_size=25,
                                   color=[62 / 255, 28 / 255, 0 / 255, 1]))
        self.add_widget(Сharacter)

    def InMenu(self, event):
        global HP
        # удаляет все виджеты класса и создает новый виджет этого же класса
        self.clear_widgets()
        self.add_widget(My_character())
        if HP <= 0:
            global MAX_HP, Experience, Trophies, LVL, Floor, Class, n, Skill, Luck, Strenght, Endurance
            global helmet, bib, pants, boots, necklace, ring, weapon, pants_leather, pants_cloth, pants_epic, pants_legendary
            global helmet_leather, helmet_cloth, helmet_epic, helmet_legendary, bib_leather, bib_cloth, bib_epic, bib_legendary
            global boots_leather, boots_cloth, boots_epic, boots_legendary, necklace_leather, necklace_cloth, necklace_epic, necklace_legendary
            global ring_leather, ring_cloth, ring_epic, ring_legendary, weapon_leather, weapon_cloth, weapon_epic, weapon_legendary
            HP = 0  # ХП персонажа (начальное рассчитывается по формуле: HP = 100 + n
            MAX_HP = 0  # Максимальное HP персонажа
            Experience = 0  # Опыт
            Trophies = 0  # Трофеи
            LVL = 1  # Уровень (Увеличивается по условию: if(Experience >= 50 + 20*LVL):   LVL += 1
            Floor = 1  # Этаж

            Class = " "  # Класс персонажа, определяющий дальнейшие начальные характеристики:
            n = 0  # Число, необходимое для высчитывания начального и максимального HP персонажа
            Skill = 0  # Ловкость (зависит от класса)
            Luck = 0  # Удача (зависит от класса)
            Strenght = 0  # Сила (зависит от класса)
            Endurance = 1  # Выносливость (зависит от класса)

            helmet = " "  # Шлем - добавляет "X" к выносливости
            bib = " "  # Нагрудник - добавляет "X" к HP
            pants = " "  # Штаны - добавляет "X" к HP
            boots = " "  # Сапоги - добавляет "X" к ловкости
            necklace = " "  # Ожерелье - добавляет "X" к удаче
            ring = " "  # Кольцо - добавляет "X" к силе
            weapon = " "  # Оружие - добавляет "X" к силе

            helmet_leather = 0
            helmet_cloth = 0
            helmet_epic = 0
            helmet_legendary = 0

            bib_leather = 0
            bib_cloth = 0
            bib_epic = 0
            bib_legendary = 0

            pants_leather = 0
            pants_cloth = 0
            pants_epic = 0
            pants_legendary = 0

            boots_leather = 0
            boots_cloth = 0
            boots_epic = 0
            boots_legendary = 0

            necklace_leather = 0
            necklace_cloth = 0
            necklace_epic = 0
            necklace_legendary = 0

            ring_leather = 0
            ring_cloth = 0
            ring_epic = 0
            ring_legendary = 0

            weapon_leather = 0
            weapon_cloth = 0
            weapon_epic = 0
            weapon_legendary = 0

        set_screen("Главное_меню")

    def in_leave(self):
        self.add_widget.clear_widgets()


class N0_class(Screen):
    def __init__(self, **kw):
        super(N0_class, self).__init__(**kw)

    def on_enter(self):
        No = FloatLayout()
        No.add_widget(Button(text="У Вас нет созданного персонажа!\n\n     (нажмите для продолжения)",
                             font_size=25, color=[62 / 255, 28 / 255, 0 / 255, 1],
                             background_color=[185 / 255, 145 / 255, 75 / 255, 1], size_hint=(.7, .3), pos=(90, 275),
                             background_normal="", on_press=lambda x: set_screen('Главное_меню')))
        self.add_widget(No)

    def in_leave(self):
        self.add_widget.clear_widgets()


class History(Screen):
    def __init__(self, **kw):
        super(History, self).__init__(**kw)

    def on_enter(self):
        self.layout = GridLayout(cols=1, spacing=10, size_hint_y=2.3)
        self.layout.bind(minimum_height=self.layout.setter('height'))
        Istoria = Button(text='<-- В главное меню',
                         background_color=[176 / 255, 136 / 255, 68 / 255, 1],
                         color=[62 / 255, 28 / 255, 0 / 255, 1],
                         font_size=20,
                         background_normal="",
                         on_press=lambda x: set_screen('Главное_меню'),
                         size_hint_y=None, height=dp(40))
        self.layout.add_widget(Istoria)
        root = RecycleView(size_hint=(1, None), size=(Window.width, Window.height))
        root.add_widget(self.layout)
        self.add_widget(root)
        btn = BoxLayout(orientation="vertical")
        btn.add_widget(Button(text="В Андердарке, расположенном под гордом\n"
                                   "Фаэрун, всегда было неспокойно. Там\n"
                                   "обитало множество рас, считающихся\n"
                                   "«тёмными» Жили там тёмные эльфы-дроу,\n"
                                   "иллитиды, наблюдатели,\nтемные дварфы - дуергары.\n\n"
                                   "Андердарк – это огромный лабиринт\n"
                                   "пещер и тоннелей. Здесь нет\n"
                                   "практически никаких источников света,\n"
                                   "за исключением светящихся камней или\n"
                                   "грибов. Сам воздух может содержать\n"
                                   "яды или взрывоопасные газы. Но\n"
                                   "всё это не помешало разумным\n"
                                   "существам жить в Андердарке.\n\n"
                                   "Пусть это и подземный мир, однако,\n"
                                   "растительный и животный мир отличается\n"
                                   "удивительным, для своего климата,\n"
                                   "разнообразием. Растительная жизнь не"
                                   "\nмогла использовать солнечный свет в "
                                   "\nкачестве источника энергии и, таким"
                                   "\nобразом, приняла странные формы,"
                                   "\nприспособленные к жизни под землёй."
                                   "\nБудучи неспособными переваривать"
                                   "\nнормальные питательные вещества,"
                                   "\nбольшую часть времени они полагались"
                                   "\nна поглощение магической энергии, или,"
                                   "\nкак её тут называют, фаэрзресс. Животный\n"
                                   "же мир не менее разнообразен. Здесь есть"
                                   "\nпочти всё: от маленьких насекомых до"
                                   "\nтеневых драконов, создавших свои"
                                   "\nцарства глубоко внутри.\n\n"
                                   "Вам с детства знакомы эти холодные\n"
                                   "туннели, темнота и чувство опасности.\n"
                                   "И пусть со временем у вас развилось\n"
                                   "тёмное зрение, менее опасно здесь не\n"
                                   "стало. Вы привыкли жить среди тьмы,\n"
                                   "с редким вкраплением фосфоресцирующих\n"
                                   "грибов, среди хищников и редко\n"
                                   "встречающихся обитателей Андердарка.\n"
                                   "\nНо ведь всегда было интересно, что там,\n"
                                   "наверху, над многочисленными проходами\n"
                                   "и тоннелями пещер, над подземными\n"
                                   "государствами, над всем этим \n"
                                   "подземным городом.\n\n",
                              font_size=25, color=[62 / 255, 28 / 255, 0 / 255, 1],
                              background_color=[.75, .60, .35, 1],
                              background_normal=""))
        self.layout.add_widget(btn)

    def on_leave(self):
        self.layout.clear_widgets()


class Rules(Screen):
    def __init__(self, **kw):
        super(Rules, self).__init__(**kw)

    def on_enter(self):
        self.layout = GridLayout(cols=1, spacing=10, size_hint_y=2.9)
        self.layout.bind(minimum_height=self.layout.setter('height'))
        Pravila = Button(text='<-- В главное меню',
                         background_color=[176 / 255, 136 / 255, 68 / 255, 1],
                         font_size=20,
                         color=[62 / 255, 28 / 255, 0 / 255, 1],
                         background_normal="",
                         on_press=lambda x: set_screen('Главное_меню'),
                         size_hint_y=None, height=dp(40))
        self.layout.add_widget(Pravila)
        root = RecycleView(size_hint=(1, None), size=(Window.width, Window.height))
        root.add_widget(self.layout)
        self.add_widget(root)
        Pravila2 = BoxLayout(orientation="vertical")
        Pravila2.add_widget(Button(text="На начальном этапе вам предстоит выбрать\n"
                                        "класс персонажа. От этого будут зависеть\n"
                                        "Ваши начальные характеристики, количество\n"
                                        "хп, а также  урон, получаемый от\n"
                                        "ловушек.\n\n"
                                        "Ваши характеристики:\n"
                                        "◊ Сила – отвечает за силу атаки\n"
                                        "◊ Ловкость (ловк) – отвечает за уклонение\n"
                                        "◊ Выносливость (вын) – отвечает за урон\n"
                                        "получаемый от монстров\n"
                                        "◊ Удача – отвечает за ценность и\n"
                                        "количество найденных трофеев, а также за\n"
                                        "частоту встречи ловушек\n\n"
                                        "Классов всего 4:\n\n"
                                        "1. Маг                                 2. Убийца\nКоличество хп – 100     Количество хп – 130\n"
                                        "Ловкость – 2                   Ловкость – 5\nУдача – 3                          Удача – 2\n"
                                        "Сила – 6                            Сила – 5\nВыносливость – 2         Выносливость – 3\n"
                                        "\n3. Воин                               4. Страж\n"
                                        "Количество хп – 170     Количество хп – 210\nЛовкость – 3                   Ловкость – 2\n"
                                        "Удача – 2                          Удача – 1\nСила – 4                            Сила – 3\n"
                                        "Выносливость – 5         Выносливость – 6\n\n"
                                        "После выбора класса начинается\nпрохождение подземелья\n\n                              Опыт и трофеи\n\n"
                                        "Опыт персонажа накапливается при\nпрохождении каждой локации\n(кроме локаций магазина и отдыха)\n\n"
                                        "Опыт необходим для перехода в более\nсложные участки подземелья, этажи\n(всего их 10)\n\n"
                                        "Трофеи персонажа служат валютой, за\nкоторую он может приобретать вещи в\nмагазине.\n\n"
                                        "Трофеи можно получить на локациях\n(«викторина», монстр, сундук)\n\n                      "
                                        "       Бой и механика\n\n"
                                        "Урон, уклонение, количество и качество\nтрофеев не фиксированы, они зависят от\n"
                                        "рандома (с учётом характеристик персонажа,\nкак начальных, так и приобретённых за счёт\n"
                                        "предметов)\nУрон и уклонение (в битве с монстром)\nтакже зависят от рандома, но с учётом не\n"
                                        "только характеристик персонажа, но и\nхарактеристик самого монстра.\n",
                                   font_size=25, color=[62 / 255, 28 / 255, 0 / 255, 1],
                                   background_color=[.75, .60, .35, 1],
                                   background_normal=""))
        self.layout.add_widget(Pravila2)

    def on_leave(self):
        self.layout.clear_widgets()


class Election_class(Screen):
    def __init__(self, **kw):
        super(Election_class, self).__init__(**kw)

    def on_enter(self):
        ViborClass = FloatLayout()
        ViborClass.add_widget(Button(text="<-- В главное меню",
                                     background_color=[185 / 255, 145 / 255, 75 / 255, 1],
                                     font_size=20,
                                     color=[62 / 255, 28 / 255, 0 / 255, 1],
                                     size_hint=(.9, .1), pos=(27, 610),
                                     background_normal="", on_press=lambda x: set_screen('Главное_меню')))
        ViborClass.add_widget(Label(text="\n\n\n\n                               Выбор класса\n\n"
                                         "Вы решили попробовать выбраться из\nПодземного Города, но для этого Вам\n"
                                         "предстоит выбрать свой дальнейший путь…\n"
                                         "Быть может, Вы мечтали стать магом? или\n"
                                         "воином? В любом случае, выбирайте с умом,\n"
                                         "ведь у каждого класса есть как плюсы,\nтак и минусы.\n\n\n\n\n\n\n\n\n\n\n\n",
                                    font_size=25,
                                    color=[62 / 255, 28 / 255, 0 / 255, 1]))
        ViborClass.add_widget(
            Button(text="        Маг\n_____________\n\n  HP - 100\n  Ловк - 2\n  Удача - 2\n  Сила - 6\n"
                        "  Выносл - 2\n",
                   background_color=[180 / 255, 140 / 255, 75 / 255, 1],
                   font_size=20, color=[62 / 255, 28 / 255, 0 / 255, 1], background_normal="",
                   size_hint=(.2, .4), pos=(25, 30),
                   on_press=self.Маг))
        ViborClass.add_widget(
            Button(text="    Убийца\n_____________\n\n  HP - 130\n  Ловк - 5\n  Удача - 2\n  Сила - 5\n"
                        "  Выносл - 3\n",
                   background_color=[176 / 255, 136 / 255, 68 / 255, 1],
                   font_size=20, color=[62 / 255, 28 / 255, 0 / 255, 1], background_normal="",
                   on_press=self.Убийца,
                   size_hint=(.2, .4), pos=(164, 30)))
        ViborClass.add_widget(
            Button(text="       Воин\n_____________\n\n  HP - 170\n  Ловк - 3\n  Удача - 2\n  Сила - 4\n"
                        "  Выносл - 5\n",
                   background_color=[180 / 255, 140 / 255, 75 / 255, 1],
                   font_size=20, color=[62 / 255, 28 / 255, 0 / 255, 1], background_normal="",
                   on_press=self.Воин,
                   size_hint=(.2, .4), pos=(301, 30)))
        ViborClass.add_widget(
            Button(text="      Страж\n_____________\n\n  HP - 210\n  Ловк - 2\n  Удача - 1\n  Сила - 3\n"
                        "  Выносл - 6\n",
                   background_color=[176 / 255, 136 / 255, 68 / 255, 1],
                   font_size=20, color=[62 / 255, 28 / 255, 0 / 255, 1], background_normal="",
                   on_press=self.Страж,
                   size_hint=(.2, .4), pos=(440, 30)))
        self.add_widget(ViborClass)

    def Маг(self, event):
        global Class
        global n
        global Skill
        global Luck
        global Strenght
        global Endurance
        global HP
        global MAX_HP
        Class = "Маг"
        n = 0
        HP = 100 + n
        MAX_HP = HP
        Skill = 2
        Luck = 3
        Strenght = 6
        Endurance = 2
        set_screen('Начало_пути_маг')
        print("Класс персонажа: ", Class, "\nБонус к ХП: ", n, "\nКоличество ХП: ", HP, "\nЛовкость: ", Skill,
              "\nУдача: ", Luck, "\nСила: ", Strenght, "\nВыносливость: ", Endurance)

    def Убийца(self, event):
        global Class
        global n
        global Skill
        global Luck
        global Strenght
        global Endurance
        global HP
        global MAX_HP
        Class = "Убийца"
        n = 30
        HP = 100 + n
        MAX_HP = HP
        Skill = 5
        Luck = 2
        Strenght = 5
        Endurance = 3
        set_screen('Начало_пути_убийца')
        print("Класс персонажа: ", Class, "\nБонус к ХП: ", n, "\nКоличество ХП: ", HP, "\nЛовкость: ", Skill,
              "\nУдача: ", Luck, "\nСила: ", Strenght, "\nВыносливость: ", Endurance)

    def Воин(self, event):
        global Class
        global n
        global Skill
        global Luck
        global Strenght
        global Endurance
        global HP
        global MAX_HP
        Class = "Воин"
        n = 70
        HP = 100 + n
        MAX_HP = HP
        Skill = 3
        Luck = 2
        Strenght = 4
        Endurance = 5
        set_screen('Начало_пути_воин')
        print("Класс персонажа: ", Class, "\nБонус к ХП: ", n, "\nКоличество ХП: ", HP, "\nЛовкость: ", Skill,
              "\nУдача: ", Luck, "\nСила: ", Strenght, "\nВыносливость: ", Endurance)

    def Страж(self, event):
        global Class
        global n
        global Skill
        global Luck
        global Strenght
        global Endurance
        global HP
        global MAX_HP
        Class = "Страж"
        n = 110
        HP = 100 + n
        MAX_HP = HP
        Skill = 2
        Luck = 1
        Strenght = 3
        Endurance = 6
        set_screen('Начало_пути_страж')
        print("Класс персонажа: ", Class, "\nБонус к ХП: ", n, "\nКоличество ХП: ", HP, "\nЛовкость: ", Skill,
              "\nУдача: ", Luck, "\nСила: ", Strenght, "\nВыносливость: ", Endurance)

    def in_leave(self):
        self.add_widget.clear_widgets()


class Beginning_Wizard(Screen):
    def __init__(self, **kw):
        super(Beginning_Wizard, self).__init__(**kw)

    def on_enter(self):
        Class = FloatLayout()
        Class.add_widget(Button(text="Выбрать другой класс",
                                background_color=[185 / 255, 145 / 255, 75 / 255, 1],
                                font_size=20,
                                color=[62 / 255, 28 / 255, 0 / 255, 1],
                                size_hint=(.9, .1), pos=(27, 610),
                                background_normal="", on_press=lambda x: set_screen('Выбор_класса')))
        Class.add_widget(Label(text="\n\nПоздравляем!\nВы выбрали Класс Мага и Ваше\nпутешествие "
                                    "по Андердарку начинается\nс этого момента.\n\n"
                                    "Ваши характеристики:\nКоличество HP - 100\nловкость – 2\nудача – 3\n"
                                    "сила – 6\nвыносливость – 2\n\n"
                                    "На Вашем пути будет множество\nтрудностей "
                                    "и испытаний, но награда\nтого стоит.\n\n"
                                    "Пусть удача сопутствует Вам!\n\n",
                               font_size=25,
                               color=[62 / 255, 28 / 255, 0 / 255, 1]))
        Class.add_widget(Button(text="Продолжить",
                                background_color=[185 / 255, 145 / 255, 75 / 255, 1],
                                font_size=20,
                                color=[62 / 255, 28 / 255, 0 / 255, 1],
                                size_hint=(.9, .1), pos=(27, 1),
                                background_normal="", on_press=self.dalee))
        self.add_widget(Class)

    def dalee(self, event):
        i = random.randint(1, Count_Screen)
        set_screen(str(i))

    def in_leave(self):
        self.add_widget.clear_widgets()


class Beginning_Assassin(Screen):
    def __init__(self, **kw):
        super(Beginning_Assassin, self).__init__(**kw)

    def on_enter(self):
        Class = FloatLayout()
        Class.add_widget(Button(text="Выбрать другой класс",
                                background_color=[185 / 255, 145 / 255, 75 / 255, 1],
                                font_size=20,
                                color=[62 / 255, 28 / 255, 0 / 255, 1],
                                size_hint=(.9, .1), pos=(27, 610),
                                background_normal="", on_press=lambda x: set_screen('Выбор_класса')))
        Class.add_widget(Label(text="\n\nПоздравляем!\nВы выбрали Класс Убийцы и Ваше\nпутешествие "
                                    "по Андердарку начинается\nс этого момента.\n\n"
                                    "Ваши характеристики:\nКоличество HP - 130\nловкость – 5\nудача – 2\n"
                                    "сила – 5\nвыносливость – 3\n\n"
                                    "На Вашем пути будет множество\nтрудностей "
                                    "и испытаний, но награда\nтого стоит.\n\n"
                                    "Пусть удача сопутствует Вам!\n\n",
                               font_size=25,
                               color=[62 / 255, 28 / 255, 0 / 255, 1]))
        Class.add_widget(Button(text="Продолжить",
                                background_color=[185 / 255, 145 / 255, 75 / 255, 1],
                                font_size=20,
                                color=[62 / 255, 28 / 255, 0 / 255, 1],
                                size_hint=(.9, .1), pos=(27, 1),
                                background_normal="", on_press=self.dalee))
        self.add_widget(Class)

    def dalee(self, event):
        i = random.randint(1, Count_Screen)
        set_screen(str(i))

    def in_leave(self):
        self.add_widget.clear_widgets()


class Beginning_Warrior(Screen):
    def __init__(self, **kw):
        super(Beginning_Warrior, self).__init__(**kw)

    def on_enter(self):
        Class = FloatLayout()
        Class.add_widget(Button(text="Выбрать другой класс",
                                background_color=[185 / 255, 145 / 255, 75 / 255, 1],
                                font_size=20,
                                color=[62 / 255, 28 / 255, 0 / 255, 1],
                                size_hint=(.9, .1), pos=(27, 610),
                                background_normal="", on_press=lambda x: set_screen('Выбор_класса')))
        Class.add_widget(Label(text="\n\nПоздравляем!\nВы выбрали Класс Воина и Ваше\nпутешествие "
                                    "по Андердарку начинается\nс этого момента.\n\n"
                                    "Ваши характеристики:\nКоличество HP - 170\nловкость – 3\nудача – 2\n"
                                    "сила – 4\nвыносливость – 5\n\n"
                                    "На Вашем пути будет множество\nтрудностей "
                                    "и испытаний, но награда\nтого стоит.\n\n"
                                    "Пусть удача сопутствует Вам!\n\n",
                               font_size=25,
                               color=[62 / 255, 28 / 255, 0 / 255, 1]))
        Class.add_widget(Button(text="Продолжить",
                                background_color=[185 / 255, 145 / 255, 75 / 255, 1],
                                font_size=20,
                                color=[62 / 255, 28 / 255, 0 / 255, 1],
                                size_hint=(.9, .1), pos=(27, 1),
                                background_normal="", on_press=self.dalee))
        self.add_widget(Class)

    def dalee(self, event):
        i = random.randint(1, Count_Screen)
        set_screen(str(i))

    def in_leave(self):
        self.add_widget.clear_widgets()


class Beginning_Guard(Screen):
    def __init__(self, **kw):
        super(Beginning_Guard, self).__init__(**kw)

    def on_enter(self):
        Class = FloatLayout()
        Class.add_widget(Button(text="Выбрать другой класс",
                                background_color=[185 / 255, 145 / 255, 75 / 255, 1],
                                font_size=20,
                                color=[62 / 255, 28 / 255, 0 / 255, 1],
                                size_hint=(.9, .1), pos=(27, 610),
                                background_normal="", on_press=lambda x: set_screen('Выбор_класса')))
        Class.add_widget(Label(text="\n\nПоздравляем!\nВы выбрали Класс Стража и Ваше\nпутешествие "
                                    "по Андердарку начинается\nс этого момента.\n\n"
                                    "Ваши характеристики:\nКоличество HP - 210\nловкость – 2\nудача – 1\n"
                                    "сила – 3\nвыносливость – 6\n\n"
                                    "На Вашем пути будет множество\nтрудностей "
                                    "и испытаний, но награда\nтого стоит.\n\n"
                                    "Пусть удача сопутствует Вам!\n\n",
                               font_size=25,
                               color=[62 / 255, 28 / 255, 0 / 255, 1]))
        Class.add_widget(Button(text="Продолжить",
                                background_color=[185 / 255, 145 / 255, 75 / 255, 1],
                                font_size=20,
                                color=[62 / 255, 28 / 255, 0 / 255, 1],
                                size_hint=(.9, .1), pos=(27, 1),
                                background_normal="", on_press=self.dalee))
        self.add_widget(Class)

    def dalee(self, event):
        i = random.randint(1, Count_Screen)
        set_screen(str(i))

    def in_leave(self):
        self.add_widget.clear_widgets()


class Settings(Screen):
    def __init__(self, **kw):
        super(Settings, self).__init__(**kw)

    def on_enter(self):
        Class = FloatLayout()
        Class.add_widget(Button(text="Сложность игры \n\n\n\n\n\n\n\n\n\n",
                                font_size=40,
                                color=[62 / 255, 28 / 255, 0 / 255, 1],
                                background_color=[.75, .60, .35, 1],
                                background_normal=""))
        Class.add_widget(Button(text="(Влияет на урон по персонажу и силу монстров)",
                                background_color=[.75, .60, .35, 1], font_size=25,
                                color=[62 / 255, 28 / 255, 0 / 255, 1],
                                size_hint=(.8, .1), pos=(55, 487),
                                background_normal=""))
        Class.add_widget(Button(text="<-- В главное меню",
                                background_color=[185 / 255, 145 / 255, 75 / 255, 1],
                                font_size=20,
                                color=[62 / 255, 28 / 255, 0 / 255, 1],
                                size_hint=(.9, .1), pos=(27, 610),
                                background_normal="", on_press=lambda x: set_screen('Главное_меню')))
        Class.add_widget(Button(text="Лёгкая",
                                background_color=[176 / 255, 136 / 255, 68 / 255, 1],
                                font_size=30,
                                color=[62 / 255, 28 / 255, 0 / 255, 1],
                                size_hint=(.8, .2), pos=(55, 350),
                                background_normal="", on_press=self.easy))
        Class.add_widget(Button(text="Средняя",
                                background_color=[176 / 255, 136 / 255, 68 / 255, 1],
                                font_size=30,
                                color=[62 / 255, 28 / 255, 0 / 255, 1],
                                size_hint=(.8, .2), pos=(55, 195),
                                background_normal="", on_press=self.middle))
        Class.add_widget(Button(text="Сложная",
                                background_color=[176 / 255, 136 / 255, 68 / 255, 1],
                                font_size=30,
                                color=[62 / 255, 28 / 255, 0 / 255, 1],
                                size_hint=(.8, .2), pos=(55, 40),
                                background_normal="", on_press=self.hard))
        self.add_widget(Class)

    def easy(self, event):
        global k
        global Difficulty
        k = 1
        Difficulty = "Лёгкий уровень сложности: "
        print(Difficulty, "  ", k)
        set_screen('Сложность_установлена')

    def middle(self, event):
        global k
        global Difficulty
        k = 2
        Difficulty = "Средний уровень сложности: "
        print(Difficulty, "  ", k)
        set_screen('Сложность_установлена')

    def hard(self, event):
        global k
        global Difficulty
        k = 3
        Difficulty = "Максимальный уровень сложности: "
        print(Difficulty, "  ", k)
        set_screen('Сложность_установлена')

    def in_leave(self):
        self.add_widget.clear_widgets()


class Shop(Screen):
    def __init__(self, **kw):
        super(Shop, self).__init__(**kw)

    def on_enter(self):
        self.layout = GridLayout(cols=1, spacing=10, size_hint_y=1)
        self.layout.bind(minimum_height=self.layout.setter('height'))
        Shop = (Button(text='<-- В главное меню',
                       background_color=[176 / 255, 136 / 255, 68 / 255, 1],
                       font_size=20,
                       color=[62 / 255, 28 / 255, 0 / 255, 1],
                       background_normal="",
                       on_press=lambda x: set_screen('Главное_меню'),
                       size_hint_y=None, height=dp(40)))
        self.layout.add_widget(Shop)
        root = RecycleView(size_hint=(1, None), size=(Window.width, Window.height))
        root.add_widget(self.layout)
        self.add_widget(root)
        Shop2 = FloatLayout()
        Shop2.add_widget(Label(text="                    Предметы                               Купить     \n\n"
                                    "Обычное зелье лечения\n\nСильное зелье лечения\n\nЭпическое зелье лечения\n\n\n\n\n\n\n\n\n\n\n\n",
                               font_size=25, color=[62 / 255, 28 / 255, 0 / 255, 1]))
        Shop2.add_widget(Button(text="5 трофеев",
                                font_size=25, color=[62 / 255, 28 / 255, 0 / 255, 1],
                                background_color=[185 / 255, 145 / 255, 75 / 255, 1], size_hint=(.3, .1),
                                pos=(400, 515),
                                background_normal="", on_press=self.обычное_зелье))
        Shop2.add_widget(Button(text="10 трофеев",
                                font_size=25, color=[62 / 255, 28 / 255, 0 / 255, 1],
                                background_color=[180 / 255, 140 / 255, 75 / 255, 1], size_hint=(.3, .1),
                                pos=(400, 455),
                                background_normal="", on_press=self.сильное_зелье))
        Shop2.add_widget(Button(text="15 трофеев",
                                font_size=25, color=[62 / 255, 28 / 255, 0 / 255, 1],
                                background_color=[185 / 255, 145 / 255, 75 / 255, 1], size_hint=(.3, .1),
                                pos=(400, 395),
                                background_normal="", on_press=self.эпическое_зелье))
        self.add_widget(Shop2)

    def обычное_зелье(self, event):
        global Usual_healing_potion
        global Trophies
        if (Trophies - 5) > 0:
            Usual_healing_potion += 1
            Trophies -= 5
        else:
            set_screen('Нет_средств')

    def сильное_зелье(self, event):
        global Powerful_healing_potion
        global Trophies
        if (Trophies - 10) > 0:
            Powerful_healing_potion += 1
            Trophies -= 10
        else:
            set_screen('Нет_средств')

    def эпическое_зелье(self, event):
        global Epic_healing_potion
        global Trophies
        if (Trophies - 15) > 0:
            Epic_healing_potion += 1
            Trophies -= 15
        else:
            set_screen('Нет_средств')

    def on_leave(self):
        self.layout.clear_widgets()


class N0_money(Screen):
    def __init__(self, **kw):
        super(N0_money, self).__init__(**kw)

    def on_enter(self):
        No = FloatLayout()
        No.add_widget(Button(text="У Вас недостаточно трофеев!\n\n(нажмите для продолжения)",
                             font_size=25, color=[62 / 255, 28 / 255, 0 / 255, 1],
                             background_color=[185 / 255, 145 / 255, 75 / 255, 1], size_hint=(.7, .3), pos=(90, 275),
                             background_normal="", on_press=lambda x: set_screen('Магазин')))
        self.add_widget(No)

    def in_leave(self):
        self.add_widget.clear_widgets()


class Difficulty_is_set(Screen):
    def __init__(self, **kw):
        super(Difficulty_is_set, self).__init__(**kw)

    def on_enter(self):
        No = FloatLayout()
        No.add_widget(Button(text="Сложность игры установлена!\n\n(нажмите для продолжения)",
                             font_size=25, color=[62 / 255, 28 / 255, 0 / 255, 1],
                             background_color=[185 / 255, 145 / 255, 75 / 255, 1], size_hint=(.7, .3), pos=(90, 275),
                             background_normal="", on_press=lambda x: set_screen('Настройки')))
        self.add_widget(No)

    def in_leave(self):
        self.add_widget.clear_widgets()


# _____________________________________________________________________________________
# Викторины
# _____________________________________________________________________________________

class Viktorina1(Screen):
    def __init__(self, **kw):
        super(Viktorina1, self).__init__(**kw)

    def on_enter(self):
        Viktorina = FloatLayout()
        Viktorina.add_widget(Button(text="<-- В главное меню",
                                    background_color=[185 / 255, 145 / 255, 75 / 255, 1],
                                    font_size=20,
                                    color=[62 / 255, 28 / 255, 0 / 255, 1],
                                    size_hint=(.9, .1), pos=(27, 610),
                                    background_normal="", on_press=lambda x: set_screen('Главное_меню')))
        Viktorina.add_widget(Label(text="Вы сосредоточенно передвигаетесь по\nкоридорам, перешагивая опасные места,\n"
                                        "но тут до вашего слуха доносится\nчьё-то мяуканье.\n"
                                        "Добравшись до источника звука вы\nобнаруживаете маленького сфинкса,\n"
                                        "сидящего на большом камне.\n"
                                        "'Кто из 4-х героев ялвяется\nсамым сильным из всех?'\n"
                                        "- спрашивает у вас сфинкс...\n\n\n\n\n",
                                   font_size=25,
                                   color=[62 / 255, 28 / 255, 0 / 255, 1]))
        Viktorina.add_widget(Button(text="Маг",
                                    background_color=[180 / 255, 140 / 255, 75 / 255, 1],
                                    font_size=20, color=[62 / 255, 28 / 255, 0 / 255, 1], background_normal="",
                                    size_hint=(.4, .1), pos=(40, 165),
                                    on_press=self.ПравильныйВыбор))
        Viktorina.add_widget(Button(text="Убийца",
                                    background_color=[180 / 255, 140 / 255, 75 / 255, 1],
                                    font_size=20, color=[62 / 255, 28 / 255, 0 / 255, 1], background_normal="",
                                    size_hint=(.4, .1), pos=(310, 55),
                                    on_press=self.НеправильныйВыбор))
        Viktorina.add_widget(Button(text="Воин",
                                    background_color=[180 / 255, 140 / 255, 75 / 255, 1],
                                    font_size=20, color=[62 / 255, 28 / 255, 0 / 255, 1], background_normal="",
                                    size_hint=(.4, .1), pos=(40, 55),
                                    on_press=self.НеправильныйВыбор))
        Viktorina.add_widget(Button(text="Страж",
                                    background_color=[180 / 255, 140 / 255, 75 / 255, 1],
                                    font_size=20, color=[62 / 255, 28 / 255, 0 / 255, 1], background_normal="",
                                    size_hint=(.4, .1), pos=(310, 165),
                                    on_press=self.НеправильныйВыбор))
        Viktorina.add_widget(Button(text="HP = " + str(HP),
                                    background_color=[150 / 255, 81 / 255, 69 / 255, 1],
                                    font_size=20, color=[64 / 255, 21 / 255, 21 / 255, 1], background_normal="",
                                    size_hint=(.3, .10 / 11), pos=(27, 580)))
        self.add_widget(Viktorina)

    def ПравильныйВыбор(self, event):
        global Experience
        Experience += 10
        global LVL, MAX_HP, Strenght, Skill, Luck, Floor, HP, Endurance, Trophies
        if Experience >= 50 + 20 * LVL:
            LVL += 1
            Experience = 0
            if LVL < 10:
                MAX_HP += MAX_HP // 10
                Floor += 1
                HP += MAX_HP // 2
                if HP > MAX_HP:
                    HP = MAX_HP
                if Class == "Маг":
                    Strenght += 1
                    Luck += 1
                elif Class == "Убийца":
                    Strenght += 1
                    Skill += 1
                elif (Class == "Воин") or (Class == "Страж"):
                    Strenght += 1
                    Endurance += 1
            else:
                set_screen('Конец_Игры')
        else:
            Trophies += 4
            set_screen('2.1')

    def НеправильныйВыбор(self, event):
        global HP, Experience
        HP -= 10
        if HP <= 0:
            set_screen('Конец_Игры_Умер')
        else:
            Experience += 5
            global LVL, MAX_HP, Strenght, Skill, Luck, Floor, Endurance
            if Experience >= 50 + 20 * LVL:
                LVL += 1
                Experience = 0
                if LVL < 10:
                    MAX_HP += MAX_HP // 10
                    Floor += 1
                    HP += MAX_HP // 2
                    if HP > MAX_HP:
                        HP = MAX_HP
                    if Class == "Маг":
                        Strenght += 1
                        Luck += 1
                    elif Class == "Убийца":
                        Strenght += 1
                        Skill += 1
                    elif (Class == "Воин") or (Class == "Страж"):
                        Strenght += 1
                        Endurance += 1
                else:
                    set_screen('Конец_Игры')
            else:
                set_screen('2.2')

    def in_leave(self):
        self.add_widget.clear_widgets()


class Viktorina1T(Screen):
    def __init__(self, **kw):
        super(Viktorina1T, self).__init__(**kw)

    def on_enter(self):
        Viktorina = FloatLayout()
        Viktorina.add_widget(Button(text="<-- В главное меню",
                                    background_color=[185 / 255, 145 / 255, 75 / 255, 1],
                                    font_size=20,
                                    color=[62 / 255, 28 / 255, 0 / 255, 1],
                                    size_hint=(.9, .1), pos=(27, 610),
                                    background_normal="", on_press=lambda x: set_screen('Главное_меню')))
        Viktorina.add_widget(Label(text="Вы правильно ответили на вопрос!\n\n"
                                        "Свинкс благосклонно кивнул вас\nи быстро скрылся за ближайшим проходом.\n"
                                        "На его месте остался неприметный\nдеревянный сундучок!\n\n"
                                        "Вы подходите и обнаруживаете там:\n\n"
                                        "Трофеи + 4 штуки\n\n"
                                        "Опыт + 10\n\n",
                                   font_size=25,
                                   color=[62 / 255, 28 / 255, 0 / 255, 1]))
        Viktorina.add_widget(Button(text="Продолжить",
                                    background_color=[180 / 255, 140 / 255, 75 / 255, 1],
                                    font_size=20, color=[62 / 255, 28 / 255, 0 / 255, 1], background_normal="",
                                    size_hint=(.4, .2), pos=(320, 30),
                                    on_press=self.dalee))
        Viktorina.add_widget(Button(text="HP = " + str(HP),
                                    background_color=[150 / 255, 81 / 255, 69 / 255, 1],
                                    font_size=20, color=[64 / 255, 21 / 255, 21 / 255, 1], background_normal="",
                                    size_hint=(.3, .10 / 11), pos=(27, 580)))
        self.add_widget(Viktorina)

    def dalee(self, event):
        i = random.randint(1, Count_Screen)
        set_screen(str(i))

    def in_leave(self):
        self.add_widget.clear_widgets()


class Viktorina1F(Screen):
    def __init__(self, **kw):
        super(Viktorina1F, self).__init__(**kw)

    def on_enter(self):
        Viktorina = FloatLayout()
        Viktorina.add_widget(Button(text="<-- В главное меню",
                                    background_color=[185 / 255, 145 / 255, 75 / 255, 1],
                                    font_size=20,
                                    color=[62 / 255, 28 / 255, 0 / 255, 1],
                                    size_hint=(.9, .1), pos=(27, 610),
                                    background_normal="", on_press=lambda x: set_screen('Главное_меню')))
        Viktorina.add_widget(Label(text="Кажется, что-то пошло не так...\n"
                                        "Сфинкс зашипил и два огромных\nпрыжка приблизился к вам!\n\n"
                                        "Быстро полоснув острыми когтями\nпо лицу, он скрылся в проходе\n"
                                        "Вам стоит быть аккуратнее, прежде\nчем отвечать на подобные вопросы.\n"
                                        "\nHP - 10\nОпыт + 5\n\n\n",
                                   font_size=25,
                                   color=[62 / 255, 28 / 255, 0 / 255, 1]))
        Viktorina.add_widget(Button(text="Продолжить",
                                    background_color=[180 / 255, 140 / 255, 75 / 255, 1],
                                    font_size=20, color=[62 / 255, 28 / 255, 0 / 255, 1], background_normal="",
                                    size_hint=(.4, .2), pos=(320, 30),
                                    on_press=self.dalee))
        Viktorina.add_widget(Button(text="HP = " + str(HP),
                                    background_color=[150 / 255, 81 / 255, 69 / 255, 1],
                                    font_size=20, color=[64 / 255, 21 / 255, 21 / 255, 1], background_normal="",
                                    size_hint=(.3, .10 / 11), pos=(27, 580)))
        self.add_widget(Viktorina)

    def dalee(self, event):
        i = random.randint(1, Count_Screen)
        set_screen(str(i))

    def in_leave(self):
        self.add_widget.clear_widgets()


class Viktorina2(Screen):
    def __init__(self, **kw):
        super(Viktorina2, self).__init__(**kw)

    def on_enter(self):
        Viktorina = FloatLayout()
        Viktorina.add_widget(Button(text="<-- В главное меню",
                                    background_color=[185 / 255, 145 / 255, 75 / 255, 1],
                                    font_size=20,
                                    color=[62 / 255, 28 / 255, 0 / 255, 1],
                                    size_hint=(.9, .1), pos=(27, 610),
                                    background_normal="", on_press=lambda x: set_screen('Главное_меню')))
        Viktorina.add_widget(Label(text="Вы аккуратно передвигаетесь по\nкоридорам, перешагивая опасные места,\n"
                                        "но тут перед вами словно из ниоткуда\nпоявляется статуя.. Оглядываясь вы\n"
                                        "понимаете, что она 'отсоединилась' от стены..\n"
                                        "И у неё в руках алебарда. Но статуя не\n"
                                        "нападает, лишь внимательно смотрит на вас..\n"
                                        "'Кто из 4-х героев ялвяется\nсамым ловким из всех?'\n"
                                        "- спрашивает у вас она...\n\n\n\n\n",
                                   font_size=25,
                                   color=[62 / 255, 28 / 255, 0 / 255, 1]))
        Viktorina.add_widget(Button(text="Маг",
                                    background_color=[180 / 255, 140 / 255, 75 / 255, 1],
                                    font_size=20, color=[62 / 255, 28 / 255, 0 / 255, 1], background_normal="",
                                    size_hint=(.4, .1), pos=(40, 165),
                                    on_press=self.НеправильныйВыбор))
        Viktorina.add_widget(Button(text="Убийца",
                                    background_color=[180 / 255, 140 / 255, 75 / 255, 1],
                                    font_size=20, color=[62 / 255, 28 / 255, 0 / 255, 1], background_normal="",
                                    size_hint=(.4, .1), pos=(310, 55),
                                    on_press=self.ПравильныйВыбор))
        Viktorina.add_widget(Button(text="Воин",
                                    background_color=[180 / 255, 140 / 255, 75 / 255, 1],
                                    font_size=20, color=[62 / 255, 28 / 255, 0 / 255, 1], background_normal="",
                                    size_hint=(.4, .1), pos=(40, 55),
                                    on_press=self.НеправильныйВыбор))
        Viktorina.add_widget(Button(text="Страж",
                                    background_color=[180 / 255, 140 / 255, 75 / 255, 1],
                                    font_size=20, color=[62 / 255, 28 / 255, 0 / 255, 1], background_normal="",
                                    size_hint=(.4, .1), pos=(310, 165),
                                    on_press=self.НеправильныйВыбор))
        Viktorina.add_widget(Button(text="HP = " + str(HP),
                                    background_color=[150 / 255, 81 / 255, 69 / 255, 1],
                                    font_size=20, color=[64 / 255, 21 / 255, 21 / 255, 1], background_normal="",
                                    size_hint=(.3, .10 / 11), pos=(27, 580)))
        self.add_widget(Viktorina)

    def ПравильныйВыбор(self, event):
        global Experience, Floor
        Experience += 10 + (3 * Floor)
        global LVL, MAX_HP, Strenght, Skill, Luck, HP, Endurance, Trophies
        if Experience >= 50 + 20 * LVL:
            LVL += 1
            Experience = 0
            if LVL < 10:
                MAX_HP += MAX_HP // 10
                Floor += 1
                HP += MAX_HP // 2
                if HP > MAX_HP:
                    HP = MAX_HP
                if Class == "Маг":
                    Strenght += 1
                    Luck += 1
                elif Class == "Убийца":
                    Strenght += 1
                    Skill += 1
                elif (Class == "Воин") or (Class == "Страж"):
                    Strenght += 1
                    Endurance += 1
            else:
                set_screen('Конец_Игры')
        else:
            Trophies += 4 + Floor
            set_screen('12.1')

    def НеправильныйВыбор(self, event):
        global HP, Experience, Floor
        HP -= 10 + (3 * Floor)
        if HP <= 0:
            set_screen('Конец_Игры_Умер')
        else:
            Experience += 5 + (2 * Floor)
            global LVL, MAX_HP, Strenght, Skill, Luck, Endurance
            if Experience >= 50 + 20 * LVL:
                LVL += 1
                Experience = 0
                if LVL < 10:
                    MAX_HP += MAX_HP // 10
                    Floor += 1
                    HP += MAX_HP // 2
                    if HP > MAX_HP:
                        HP = MAX_HP
                    if Class == "Маг":
                        Strenght += 1
                        Luck += 1
                    elif Class == "Убийца":
                        Strenght += 1
                        Skill += 1
                    elif (Class == "Воин") or (Class == "Страж"):
                        Strenght += 1
                        Endurance += 1
                else:
                    set_screen('Конец_Игры')
            else:
                set_screen('12.2')

    def in_leave(self):
        self.add_widget.clear_widgets()


class Viktorina2T(Screen):
    def __init__(self, **kw):
        super(Viktorina2T, self).__init__(**kw)

    def on_enter(self):
        Viktorina = FloatLayout()
        Viktorina.add_widget(Button(text="<-- В главное меню",
                                    background_color=[185 / 255, 145 / 255, 75 / 255, 1],
                                    font_size=20,
                                    color=[62 / 255, 28 / 255, 0 / 255, 1],
                                    size_hint=(.9, .1), pos=(27, 610),
                                    background_normal="", on_press=lambda x: set_screen('Главное_меню')))
        Viktorina.add_widget(Label(text="Вы правильно ответили на вопрос!\n\n"
                                        "Статуя ещё пару секунд смотрела на вас,\n"
                                        "а затем шагнула обратно в стену.\n"
                                        "Вы были так ошеломлены, что не сразу\n"
                                        "заметили сундук, который остался\nоколо стены, в которой скрылась статуя.\n\n"
                                        "Вы подходите и обнаруживаете в сундуке:\n\n"
                                        "Трофеи + " + str(4 + Floor) + " штук\n"
                                                                       "Опыт +" + str(10 + (3 * Floor)),
                                   font_size=25,
                                   color=[62 / 255, 28 / 255, 0 / 255, 1]))
        Viktorina.add_widget(Button(text="Продолжить",
                                    background_color=[180 / 255, 140 / 255, 75 / 255, 1],
                                    font_size=20, color=[62 / 255, 28 / 255, 0 / 255, 1], background_normal="",
                                    size_hint=(.4, .2), pos=(320, 30),
                                    on_press=self.dalee))
        Viktorina.add_widget(Button(text="HP = " + str(HP),
                                    background_color=[150 / 255, 81 / 255, 69 / 255, 1],
                                    font_size=20, color=[64 / 255, 21 / 255, 21 / 255, 1], background_normal="",
                                    size_hint=(.3, .10 / 11), pos=(27, 580)))
        self.add_widget(Viktorina)

    def dalee(self, event):
        # удаляет все виджеты класса и создает новый виджет этого же класса
        self.clear_widgets()
        self.add_widget(Viktorina2T())
        i = random.randint(1, Count_Screen)
        set_screen(str(i))

    def in_leave(self):
        self.add_widget.clear_widgets()


class Viktorina2F(Screen):
    def __init__(self, **kw):
        super(Viktorina2F, self).__init__(**kw)

    def on_enter(self):
        Viktorina = FloatLayout()
        Viktorina.add_widget(Button(text="<-- В главное меню",
                                    background_color=[185 / 255, 145 / 255, 75 / 255, 1],
                                    font_size=20,
                                    color=[62 / 255, 28 / 255, 0 / 255, 1],
                                    size_hint=(.9, .1), pos=(27, 610),
                                    background_normal="", on_press=lambda x: set_screen('Главное_меню')))
        Viktorina.add_widget(Label(text="Кажется, что-то пошло не так...\n"
                                        "Статуя нахмурилась и пришла в движение.\n"
                                        "Вы поняли, что пора бежать, однако вас\n"
                                        "всё равно смогли задеть концом каменной\n"
                                        "алебарды, оставив болезненную рану.\n\n"
                                        "Вам стоит лучше думать, прежде\nчем отвечать на подобные вопросы.\n"
                                        "\nHP - " + str((10 + (3 * Floor))) +
                                        "\nОпыт + " + str((5 + (2 * Floor))),
                                   font_size=25,
                                   color=[62 / 255, 28 / 255, 0 / 255, 1]))
        Viktorina.add_widget(Button(text="Продолжить",
                                    background_color=[180 / 255, 140 / 255, 75 / 255, 1],
                                    font_size=20, color=[62 / 255, 28 / 255, 0 / 255, 1], background_normal="",
                                    size_hint=(.4, .2), pos=(320, 30),
                                    on_press=self.dalee))
        Viktorina.add_widget(Button(text="HP = " + str(HP),
                                    background_color=[150 / 255, 81 / 255, 69 / 255, 1],
                                    font_size=20, color=[64 / 255, 21 / 255, 21 / 255, 1], background_normal="",
                                    size_hint=(.3, .10 / 11), pos=(27, 580)))
        self.add_widget(Viktorina)

    def dalee(self, event):
        # удаляет все виджеты класса и создает новый виджет этого же класса
        self.clear_widgets()
        self.add_widget(Viktorina2F())
        i = random.randint(1, Count_Screen)
        set_screen(str(i))

    def in_leave(self):
        self.add_widget.clear_widgets()


class Viktorina3(Screen):
    def __init__(self, **kw):
        super(Viktorina3, self).__init__(**kw)

    def on_enter(self):
        Viktorina = FloatLayout()
        Viktorina.add_widget(Button(text="<-- В главное меню",
                                    background_color=[185 / 255, 145 / 255, 75 / 255, 1],
                                    font_size=20,
                                    color=[62 / 255, 28 / 255, 0 / 255, 1],
                                    size_hint=(.9, .1), pos=(27, 610),
                                    background_normal="", on_press=lambda x: set_screen('Главное_меню')))
        Viktorina.add_widget(Label(text="Продвигаться по затуманенным коридорам\nдостаточно сложно, вы почти ничего\n"
                                        "не видите и идёте на ощупь.\nПеред вами из клубов тумана вырисовывается\n"
                                        "образ фигуры с длинными белыми волосами.\n"
                                        "Она парит над землёй и смотрит на вас.\n\n"
                                        "'Вам придётся отгадать загадку, иначе\n"
                                        "туман станет ядовитым..\nМагия - удивительная вещь. Как мы\n"
                                        "называем магию здесь, в Андердарке?'\n\n\n",
                                   font_size=25,
                                   color=[62 / 255, 28 / 255, 0 / 255, 1]))
        Viktorina.add_widget(Button(text="Фаэрун",
                                    background_color=[180 / 255, 140 / 255, 75 / 255, 1],
                                    font_size=20, color=[62 / 255, 28 / 255, 0 / 255, 1], background_normal="",
                                    size_hint=(.4, .1), pos=(40, 145),
                                    on_press=self.НеправильныйВыбор))
        Viktorina.add_widget(Button(text="Мана",
                                    background_color=[180 / 255, 140 / 255, 75 / 255, 1],
                                    font_size=20, color=[62 / 255, 28 / 255, 0 / 255, 1], background_normal="",
                                    size_hint=(.4, .1), pos=(310, 55),
                                    on_press=self.НеправильныйВыбор))
        Viktorina.add_widget(Button(text="Фаэрзресс",
                                    background_color=[180 / 255, 140 / 255, 75 / 255, 1],
                                    font_size=20, color=[62 / 255, 28 / 255, 0 / 255, 1], background_normal="",
                                    size_hint=(.4, .1), pos=(40, 55),
                                    on_press=self.ПравильныйВыбор))
        Viktorina.add_widget(Button(text="Ивуилэнс",
                                    background_color=[180 / 255, 140 / 255, 75 / 255, 1],
                                    font_size=20, color=[62 / 255, 28 / 255, 0 / 255, 1], background_normal="",
                                    size_hint=(.4, .1), pos=(310, 145),
                                    on_press=self.НеправильныйВыбор))
        Viktorina.add_widget(Button(text="HP = " + str(HP),
                                    background_color=[150 / 255, 81 / 255, 69 / 255, 1],
                                    font_size=20, color=[64 / 255, 21 / 255, 21 / 255, 1], background_normal="",
                                    size_hint=(.3, .10 / 11), pos=(27, 580)))
        self.add_widget(Viktorina)

    def ПравильныйВыбор(self, event):
        global Experience, Floor, ring_cloth
        Experience += 10 + (3 * Floor) + 3
        global LVL, MAX_HP, Strenght, Skill, Luck, HP, Endurance, Trophies
        if Experience >= 50 + 20 * LVL:
            LVL += 1
            Experience = 0
            if LVL < 10:
                MAX_HP += MAX_HP // 10
                Floor += 1
                HP += MAX_HP // 2
                if HP > MAX_HP:
                    HP = MAX_HP
                if Class == "Маг":
                    Strenght += 1
                    Luck += 1
                elif Class == "Убийца":
                    Strenght += 1
                    Skill += 1
                elif (Class == "Воин") or (Class == "Страж"):
                    Strenght += 1
                    Endurance += 1
            else:
                set_screen('Конец_Игры')
        else:
            ring_cloth += 1
            set_screen('13.1')

    def НеправильныйВыбор(self, event):
        global HP, Experience, Floor
        HP -= 20 + (2 * Floor)
        if HP <= 0:
            set_screen('Конец_Игры_Умер')
        else:
            Experience += 5 + (2 * Floor) + 2
            global LVL, MAX_HP, Strenght, Skill, Luck, Endurance
            if Experience >= 50 + 20 * LVL:
                LVL += 1
                Experience = 0
                if LVL < 10:
                    MAX_HP += MAX_HP // 10
                    Floor += 1
                    HP += MAX_HP // 2
                    if HP > MAX_HP:
                        HP = MAX_HP
                    if Class == "Маг":
                        Strenght += 1
                        Luck += 1
                    elif Class == "Убийца":
                        Strenght += 1
                        Skill += 1
                    elif (Class == "Воин") or (Class == "Страж"):
                        Strenght += 1
                        Endurance += 1
                else:
                    set_screen('Конец_Игры')
            else:
                set_screen('13.2')

    def in_leave(self):
        self.add_widget.clear_widgets()


class Viktorina3T(Screen):
    def __init__(self, **kw):
        super(Viktorina3T, self).__init__(**kw)

    def on_enter(self):
        Viktorina = FloatLayout()
        Viktorina.add_widget(Button(text="<-- В главное меню",
                                    background_color=[185 / 255, 145 / 255, 75 / 255, 1],
                                    font_size=20,
                                    color=[62 / 255, 28 / 255, 0 / 255, 1],
                                    size_hint=(.9, .1), pos=(27, 610),
                                    background_normal="", on_press=lambda x: set_screen('Главное_меню')))
        Viktorina.add_widget(Label(text="Силуэт слегка качнулся, но вы не\nпочувствовали угрозы от него.\n\n"
                                        "'Я уважаю людей, знающих основы\nэтого мира, поэтому я отдам вам\nодно из колец. "
                                        "Оно поможет вам\nстать сильнее, если вы этого\nхотите, конечно.\n\n'"
                                        "Трофеи + 'Кольцо с малым кристаллом' 1шт.\n"
                                        "Опыт +" + str(10 + (3 * Floor) + 3) + "\n\n\n",
                                   font_size=25,
                                   color=[62 / 255, 28 / 255, 0 / 255, 1]))
        Viktorina.add_widget(Button(text="Продолжить\nне надевая",
                                    background_color=[180 / 255, 140 / 255, 75 / 255, 1],
                                    font_size=20, color=[62 / 255, 28 / 255, 0 / 255, 1], background_normal="",
                                    size_hint=(.4, .2), pos=(320, 30),
                                    on_press=self.dalee))
        Viktorina.add_widget(Button(text="Надеть\nкольцо",
                                    background_color=[180 / 255, 140 / 255, 75 / 255, 1],
                                    font_size=20, color=[62 / 255, 28 / 255, 0 / 255, 1], background_normal="",
                                    size_hint=(.4, .2), pos=(40, 30),
                                    on_press=self.equipment))
        Viktorina.add_widget(Button(text="HP = " + str(HP),
                                    background_color=[150 / 255, 81 / 255, 69 / 255, 1],
                                    font_size=20, color=[64 / 255, 21 / 255, 21 / 255, 1], background_normal="",
                                    size_hint=(.3, .10 / 11), pos=(27, 580)))
        self.add_widget(Viktorina)

    def equipment(self, event):
        # удаляет все виджеты класса и создает новый виджет этого же класса
        self.clear_widgets()
        self.add_widget(Viktorina3T())
        set_screen('Экипировка_предмета')

    def dalee(self, event):
        # удаляет все виджеты класса и создает новый виджет этого же класса
        self.clear_widgets()
        self.add_widget(Viktorina3T())
        i = random.randint(1, Count_Screen)
        set_screen(str(i))

    def in_leave(self):
        self.add_widget.clear_widgets()


class Viktorina3F(Screen):
    def __init__(self, **kw):
        super(Viktorina3F, self).__init__(**kw)

    def on_enter(self):
        Viktorina = FloatLayout()
        Viktorina.add_widget(Button(text="<-- В главное меню",
                                    background_color=[185 / 255, 145 / 255, 75 / 255, 1],
                                    font_size=20,
                                    color=[62 / 255, 28 / 255, 0 / 255, 1],
                                    size_hint=(.9, .1), pos=(27, 610),
                                    background_normal="", on_press=lambda x: set_screen('Главное_меню')))
        Viktorina.add_widget(Label(text="'Похоже вы не интересуетесь магией,\nа стоило бы..'\n\n"
                                        "Воздух вокруг вас стал тяжелым,\nвы начинаете задыхаться и стараетесь\n"
                                        "убежать отсюда как можно быстрее.\nЛишь спустя три-четыре поворота вы\n"
                                        "смогли нормально дышать..\n\n"
                                        "Вам стоит быть аккуратнее, прежде\nчем отвечать на подобные вопросы.\n"
                                        "\nHP - " + str((20 + (2 * Floor))) +
                                        "\nОпыт + " + str((5 + (2 * Floor) + 2)),
                                   font_size=25,
                                   color=[62 / 255, 28 / 255, 0 / 255, 1]))
        Viktorina.add_widget(Button(text="Продолжить",
                                    background_color=[180 / 255, 140 / 255, 75 / 255, 1],
                                    font_size=20, color=[62 / 255, 28 / 255, 0 / 255, 1], background_normal="",
                                    size_hint=(.4, .2), pos=(320, 30),
                                    on_press=self.dalee))
        Viktorina.add_widget(Button(text="HP = " + str(HP),
                                    background_color=[150 / 255, 81 / 255, 69 / 255, 1],
                                    font_size=20, color=[64 / 255, 21 / 255, 21 / 255, 1], background_normal="",
                                    size_hint=(.3, .10 / 11), pos=(27, 580)))
        self.add_widget(Viktorina)

    def dalee(self, event):
        # удаляет все виджеты класса и создает новый виджет этого же класса
        self.clear_widgets()
        self.add_widget(Viktorina3F())
        i = random.randint(1, Count_Screen)
        set_screen(str(i))

    def in_leave(self):
        self.add_widget.clear_widgets()


class Viktorina4(Screen):
    def __init__(self, **kw):
        super(Viktorina4, self).__init__(**kw)

    def on_enter(self):
        Viktorina = FloatLayout()
        Viktorina.add_widget(Button(text="<-- В главное меню",
                                    background_color=[185 / 255, 145 / 255, 75 / 255, 1],
                                    font_size=20,
                                    color=[62 / 255, 28 / 255, 0 / 255, 1],
                                    size_hint=(.9, .1), pos=(27, 610),
                                    background_normal="", on_press=lambda x: set_screen('Главное_меню')))
        Viktorina.add_widget(Label(text="Вы проходите мимо коридора с тусклым\nсветом внутри и видите, что там стоят\n"
                                        "два дроу, и общаются между собой.\nВаше любопытство берёт верх и вы подходите\n"
                                        "поближе, чтобы послушать, но задеваете\nголовой сталагмит. Они оборачиваются\n"
                                        "и внезапным движением окружают вас.\n\n"
                                        "Несколько секунд они обсуждают что-то\nна неизвестном вам языке, после чего\n"
                                        "спрашивают: 'Кто не обитает в наших пещерах?'\n\n\n\n",
                                   font_size=25,
                                   color=[62 / 255, 28 / 255, 0 / 255, 1]))
        Viktorina.add_widget(Button(text="Иллитиды",
                                    background_color=[180 / 255, 140 / 255, 75 / 255, 1],
                                    font_size=20, color=[62 / 255, 28 / 255, 0 / 255, 1], background_normal="",
                                    size_hint=(.4, .1), pos=(40, 150),
                                    on_press=self.НеправильныйВыбор))
        Viktorina.add_widget(Button(text="Наги",
                                    background_color=[180 / 255, 140 / 255, 75 / 255, 1],
                                    font_size=20, color=[62 / 255, 28 / 255, 0 / 255, 1], background_normal="",
                                    size_hint=(.4, .1), pos=(310, 55),
                                    on_press=self.ПравильныйВыбор))
        Viktorina.add_widget(Button(text="Дуергары",
                                    background_color=[180 / 255, 140 / 255, 75 / 255, 1],
                                    font_size=20, color=[62 / 255, 28 / 255, 0 / 255, 1], background_normal="",
                                    size_hint=(.4, .1), pos=(40, 55),
                                    on_press=self.НеправильныйВыбор))
        Viktorina.add_widget(Button(text="Наблюдатели",
                                    background_color=[180 / 255, 140 / 255, 75 / 255, 1],
                                    font_size=20, color=[62 / 255, 28 / 255, 0 / 255, 1], background_normal="",
                                    size_hint=(.4, .1), pos=(310, 150),
                                    on_press=self.НеправильныйВыбор))
        Viktorina.add_widget(Button(text="HP = " + str(HP),
                                    background_color=[150 / 255, 81 / 255, 69 / 255, 1],
                                    font_size=20, color=[64 / 255, 21 / 255, 21 / 255, 1], background_normal="",
                                    size_hint=(.3, .10 / 11), pos=(27, 580)))
        self.add_widget(Viktorina)

    def ПравильныйВыбор(self, event):
        global Experience, Floor, bib_leather, bib_cloth, bib_epic
        Experience += 15 + (3 * Floor)
        global LVL, MAX_HP, Strenght, Skill, Luck, HP, Endurance, Trophies
        if Experience >= 50 + 20 * LVL:
            LVL += 1
            Experience = 0
            if LVL < 10:
                MAX_HP += MAX_HP // 10
                Floor += 1
                HP += MAX_HP // 2
                if HP > MAX_HP:
                    HP = MAX_HP
                if Class == "Маг":
                    Strenght += 1
                    Luck += 1
                elif Class == "Убийца":
                    Strenght += 1
                    Skill += 1
                elif (Class == "Воин") or (Class == "Страж"):
                    Strenght += 1
                    Endurance += 1
            else:
                set_screen('Конец_Игры')
        else:
            if Floor < 4:
                bib_leather += 1
            elif (Floor > 3) and (Floor < 8):
                bib_cloth += 1
            elif Floor > 7:
                bib_epic += 1
            set_screen('14.1')

    def НеправильныйВыбор(self, event):
        global HP, Experience, Floor
        HP -= 15 + (3 * Floor)
        if HP <= 0:
            set_screen('Конец_Игры_Умер')
        else:
            Experience += 7 + (2 * Floor)
            global LVL, MAX_HP, Strenght, Skill, Luck, Endurance
            if Experience >= 50 + 20 * LVL:
                LVL += 1
                Experience = 0
                if LVL < 10:
                    MAX_HP += MAX_HP // 10
                    Floor += 1
                    HP += MAX_HP // 2
                    if HP > MAX_HP:
                        HP = MAX_HP
                    if Class == "Маг":
                        Strenght += 1
                        Luck += 1
                    elif Class == "Убийца":
                        Strenght += 1
                        Skill += 1
                    elif (Class == "Воин") or (Class == "Страж"):
                        Strenght += 1
                        Endurance += 1
                else:
                    set_screen('Конец_Игры')
            else:
                set_screen('14.2')

    def in_leave(self):
        self.add_widget.clear_widgets()


class Viktorina4T(Screen):
    def __init__(self, **kw):
        super(Viktorina4T, self).__init__(**kw)

    def on_enter(self):
        if Floor < 4:
            predmet = "Лёгкий нагрудник"
        elif (Floor > 3) and (Floor < 8):
            predmet = "Кожаный нагрудник"
        elif Floor > 7:
            predmet = "Нагрудник из лозы"
        Viktorina = FloatLayout()
        Viktorina.add_widget(Button(text="<-- В главное меню",
                                    background_color=[185 / 255, 145 / 255, 75 / 255, 1],
                                    font_size=20,
                                    color=[62 / 255, 28 / 255, 0 / 255, 1],
                                    size_hint=(.9, .1), pos=(27, 610),
                                    background_normal="", on_press=lambda x: set_screen('Главное_меню')))
        Viktorina.add_widget(Label(text="Они, едва заметно, выдыхают.\n'Свой' - сказал более высокий дроу\n"
                                        "уже на известном вам языке.\n\nНе ходи в этих тоннелях, в этом\n"
                                        "месяце здесь будет очень опасно.\nМы можем дать тебе кое-какую броню,\n"
                                        "чтобы у тебя было больше шансов выжить..\nА теперь уходи.\n\n"
                                        "Предмет: " + str(predmet) +
                                        "\nОпыт +" + str(15 + (3 * Floor)) + "\n\n",
                                   font_size=25,
                                   color=[62 / 255, 28 / 255, 0 / 255, 1]))
        Viktorina.add_widget(Button(text="Продолжить\nне надевая",
                                    background_color=[180 / 255, 140 / 255, 75 / 255, 1],
                                    font_size=20, color=[62 / 255, 28 / 255, 0 / 255, 1], background_normal="",
                                    size_hint=(.4, .2), pos=(320, 30),
                                    on_press=self.dalee))
        Viktorina.add_widget(Button(text="Надеть\nнагрудник",
                                    background_color=[180 / 255, 140 / 255, 75 / 255, 1],
                                    font_size=20, color=[62 / 255, 28 / 255, 0 / 255, 1], background_normal="",
                                    size_hint=(.4, .2), pos=(40, 30),
                                    on_press=self.equipment))
        Viktorina.add_widget(Button(text="HP = " + str(HP),
                                    background_color=[150 / 255, 81 / 255, 69 / 255, 1],
                                    font_size=20, color=[64 / 255, 21 / 255, 21 / 255, 1], background_normal="",
                                    size_hint=(.3, .10 / 11), pos=(27, 580)))
        self.add_widget(Viktorina)

    def equipment(self, event):
        # удаляет все виджеты класса и создает новый виджет этого же класса
        self.clear_widgets()
        self.add_widget(Viktorina4T())
        set_screen('Экипировка_предмета')

    def dalee(self, event):
        # удаляет все виджеты класса и создает новый виджет этого же класса
        self.clear_widgets()
        self.add_widget(Viktorina4T())
        i = random.randint(1, Count_Screen)
        set_screen(str(i))

    def in_leave(self):
        self.add_widget.clear_widgets()


class Viktorina4F(Screen):
    def __init__(self, **kw):
        super(Viktorina4F, self).__init__(**kw)

    def on_enter(self):
        Viktorina = FloatLayout()
        Viktorina.add_widget(Button(text="<-- В главное меню",
                                    background_color=[185 / 255, 145 / 255, 75 / 255, 1],
                                    font_size=20,
                                    color=[62 / 255, 28 / 255, 0 / 255, 1],
                                    size_hint=(.9, .1), pos=(27, 610),
                                    background_normal="", on_press=lambda x: set_screen('Главное_меню')))
        Viktorina.add_widget(Label(text="Внезапно оба дроу исчезают в тенях\nи появляются уже с другой стороны\n"
                                        "от вас. Один из них быстро взмахивает\nклинком и рассекает вам руку, второй\n"
                                        "появляется сзади и едва касается\nножом вашего горла.\n\n"
                                        "'Уходи, чужак'\nОба дроу исчезают, а вы стараетесь\nпоскорее вернуться в известную\n"
                                        "для вас часть пещеры.\n"
                                        "\nHP - " + str((15 + (3 * Floor))) +
                                        "\nОпыт + " + str((7 + (2 * Floor))),
                                   font_size=25,
                                   color=[62 / 255, 28 / 255, 0 / 255, 1]))
        Viktorina.add_widget(Button(text="Продолжить",
                                    background_color=[180 / 255, 140 / 255, 75 / 255, 1],
                                    font_size=20, color=[62 / 255, 28 / 255, 0 / 255, 1], background_normal="",
                                    size_hint=(.4, .2), pos=(320, 30),
                                    on_press=self.dalee))
        Viktorina.add_widget(Button(text="HP = " + str(HP),
                                    background_color=[150 / 255, 81 / 255, 69 / 255, 1],
                                    font_size=20, color=[64 / 255, 21 / 255, 21 / 255, 1], background_normal="",
                                    size_hint=(.3, .10 / 11), pos=(27, 580)))
        self.add_widget(Viktorina)

    def dalee(self, event):
        # удаляет все виджеты класса и создает новый виджет этого же класса
        self.clear_widgets()
        self.add_widget(Viktorina4F())
        i = random.randint(1, Count_Screen)
        set_screen(str(i))

    def in_leave(self):
        self.add_widget.clear_widgets()


class Viktorina5(Screen):
    def __init__(self, **kw):
        super(Viktorina5, self).__init__(**kw)

    def on_enter(self):
        Viktorina = FloatLayout()
        Viktorina.add_widget(Button(text="<-- В главное меню",
                                    background_color=[185 / 255, 145 / 255, 75 / 255, 1],
                                    font_size=20,
                                    color=[62 / 255, 28 / 255, 0 / 255, 1],
                                    size_hint=(.9, .1), pos=(27, 610),
                                    background_normal="", on_press=lambda x: set_screen('Главное_меню')))
        Viktorina.add_widget(Label(text="Вы идёте вперёд, стараясь найти место\nдля ночлега, но дорогу преграждает\n"
                                        "табличка со странными рунами, вместо слов.\nВы рассматриваете её, стараясь понять,\n"
                                        "что на ней изображено, но замечаете на\nсебе чей-то пристальный взгляд..\n"
                                        "'Тебе здесь не место, человек, но я могу\nтебе помочь и дать уйти.. или же посмотреть,\n"
                                        "кто из нас сильнее.\nЯ знаю все эти туннели, а ты знаешь хотя бы,\nпод каким городом "
                                        "расположен Андердарк?\n\n\n",
                                   font_size=25,
                                   color=[62 / 255, 28 / 255, 0 / 255, 1]))
        Viktorina.add_widget(Button(text="Зувелл",
                                    background_color=[180 / 255, 140 / 255, 75 / 255, 1],
                                    font_size=20, color=[62 / 255, 28 / 255, 0 / 255, 1], background_normal="",
                                    size_hint=(.4, .1), pos=(40, 150),
                                    on_press=self.НеправильныйВыбор))
        Viktorina.add_widget(Button(text="Флуарэнс",
                                    background_color=[180 / 255, 140 / 255, 75 / 255, 1],
                                    font_size=20, color=[62 / 255, 28 / 255, 0 / 255, 1], background_normal="",
                                    size_hint=(.4, .1), pos=(310, 55),
                                    on_press=self.НеправильныйВыбор))
        Viktorina.add_widget(Button(text="Евлионис",
                                    background_color=[180 / 255, 140 / 255, 75 / 255, 1],
                                    font_size=20, color=[62 / 255, 28 / 255, 0 / 255, 1], background_normal="",
                                    size_hint=(.4, .1), pos=(40, 55),
                                    on_press=self.НеправильныйВыбор))
        Viktorina.add_widget(Button(text="Фаэрун",
                                    background_color=[180 / 255, 140 / 255, 75 / 255, 1],
                                    font_size=20, color=[62 / 255, 28 / 255, 0 / 255, 1], background_normal="",
                                    size_hint=(.4, .1), pos=(310, 150),
                                    on_press=self.ПравильныйВыбор))
        Viktorina.add_widget(Button(text="HP = " + str(HP),
                                    background_color=[150 / 255, 81 / 255, 69 / 255, 1],
                                    font_size=20, color=[64 / 255, 21 / 255, 21 / 255, 1], background_normal="",
                                    size_hint=(.3, .10 / 11), pos=(27, 580)))
        self.add_widget(Viktorina)

    def ПравильныйВыбор(self, event):
        global Experience, Floor, Luck, pants_leather, pants_epic, pants_cloth
        Experience += 10 + (3 * Floor) + Luck
        global LVL, MAX_HP, Strenght, Skill, HP, Endurance, Trophies
        if Experience >= 50 + 20 * LVL:
            LVL += 1
            Experience = 0
            if LVL < 10:
                MAX_HP += MAX_HP // 10
                Floor += 1
                HP += MAX_HP // 2
                if HP > MAX_HP:
                    HP = MAX_HP
                if Class == "Маг":
                    Strenght += 1
                    Luck += 1
                elif Class == "Убийца":
                    Strenght += 1
                    Skill += 1
                elif (Class == "Воин") or (Class == "Страж"):
                    Strenght += 1
                    Endurance += 1
            else:
                set_screen('Конец_Игры')
        else:
            if Floor < 4:
                pants_leather += 1
            elif (Floor > 3) and (Floor < 8):
                pants_cloth += 1
            elif Floor > 7:
                pants_epic += 1
            Trophies += 4 + Floor * 2
            set_screen('15.1')

    def НеправильныйВыбор(self, event):
        global HP, Experience, Floor, Luck
        HP -= 10 + (4 * Floor) - (2 * Luck)
        if HP <= 0:
            set_screen('Конец_Игры_Умер')
        else:
            Experience += 5 + (2 * Floor) + Luck
            global LVL, MAX_HP, Strenght, Skill, Endurance
            if Experience >= 50 + 20 * LVL:
                LVL += 1
                Experience = 0
                if LVL < 10:
                    MAX_HP += MAX_HP // 10
                    Floor += 1
                    HP += MAX_HP // 2
                    if HP > MAX_HP:
                        HP = MAX_HP
                    if Class == "Маг":
                        Strenght += 1
                        Luck += 1
                    elif Class == "Убийца":
                        Strenght += 1
                        Skill += 1
                    elif (Class == "Воин") or (Class == "Страж"):
                        Strenght += 1
                        Endurance += 1
                else:
                    set_screen('Конец_Игры')
            else:
                set_screen('15.2')

    def in_leave(self):
        self.add_widget.clear_widgets()


class Viktorina5T(Screen):
    def __init__(self, **kw):
        super(Viktorina5T, self).__init__(**kw)

    def on_enter(self):
        if Floor < 4:
            predmet = "Лёгкие штаны"
        elif (Floor > 3) and (Floor < 8):
            predmet = "Кожаные штаны"
        elif Floor > 7:
            predmet = "Штаны из лозы"
        Viktorina = FloatLayout()
        Viktorina.add_widget(Button(text="<-- В главное меню",
                                    background_color=[185 / 255, 145 / 255, 75 / 255, 1],
                                    font_size=20,
                                    color=[62 / 255, 28 / 255, 0 / 255, 1],
                                    size_hint=(.9, .1), pos=(27, 610),
                                    background_normal="", on_press=lambda x: set_screen('Главное_меню')))
        Viktorina.add_widget(Label(text="'Хм, ты правильно ответил.\nВыходит, не я один знаю что-то об\n"
                                        "этом подземном мире.'\nВы смотрите на дуергара, он начинает\n"
                                        "спокойно подходить к вам.\n'Не бойся, я не буду с тобой драться,\n"
                                        "мне нравятся люди, интересующиеся\nэтими шахтами. Я дам тебе экипировку,\n"
                                        "а после уходи отсюда, мне не нужны соседи.'\n\n"
                                        "Предмет: " + str(predmet) +
                                        "\nТрофеи + " + str(4 + Floor * 2) + " штук\n"
                                                                             "Опыт +" + str(
            10 + (3 * Floor) + Luck) + "\n\n",
                                   font_size=25,
                                   color=[62 / 255, 28 / 255, 0 / 255, 1]))
        Viktorina.add_widget(Button(text="Продолжить\nне надевая",
                                    background_color=[180 / 255, 140 / 255, 75 / 255, 1],
                                    font_size=20, color=[62 / 255, 28 / 255, 0 / 255, 1], background_normal="",
                                    size_hint=(.4, .2), pos=(320, 30),
                                    on_press=self.dalee))
        Viktorina.add_widget(Button(text="Надеть\nштаны",
                                    background_color=[180 / 255, 140 / 255, 75 / 255, 1],
                                    font_size=20, color=[62 / 255, 28 / 255, 0 / 255, 1], background_normal="",
                                    size_hint=(.4, .2), pos=(40, 30),
                                    on_press=self.equipment))
        Viktorina.add_widget(Button(text="HP = " + str(HP),
                                    background_color=[150 / 255, 81 / 255, 69 / 255, 1],
                                    font_size=20, color=[64 / 255, 21 / 255, 21 / 255, 1], background_normal="",
                                    size_hint=(.3, .10 / 11), pos=(27, 580)))
        self.add_widget(Viktorina)

    def equipment(self, event):
        # удаляет все виджеты класса и создает новый виджет этого же класса
        self.clear_widgets()
        self.add_widget(Viktorina5T())
        set_screen('Экипировка_предмета')

    def dalee(self, event):
        # удаляет все виджеты класса и создает новый виджет этого же класса
        self.clear_widgets()
        self.add_widget(Viktorina5T())
        i = random.randint(1, Count_Screen)
        set_screen(str(i))

    def in_leave(self):
        self.add_widget.clear_widgets()


class Viktorina5F(Screen):
    def __init__(self, **kw):
        super(Viktorina5F, self).__init__(**kw)

    def on_enter(self):
        Viktorina = FloatLayout()
        Viktorina.add_widget(Button(text="<-- В главное меню",
                                    background_color=[185 / 255, 145 / 255, 75 / 255, 1],
                                    font_size=20,
                                    color=[62 / 255, 28 / 255, 0 / 255, 1],
                                    size_hint=(.4, .1), pos=(27, 610),
                                    background_normal="", on_press=lambda x: set_screen('Главное_меню')))
        Viktorina.add_widget(Button(text="Сохранить",
                                    background_color=[185 / 255, 145 / 255, 75 / 255, 1],
                                    font_size=20,
                                    color=[62 / 255, 28 / 255, 0 / 255, 1],
                                    size_hint=(.4, .1), pos=(320, 610),
                                    background_normal="", on_press=self.piy))
        Viktorina.add_widget(Label(text="Дуергар внимательно смотрит на вас: \n'Это неправильный ответ..'\n\n"
                                        "Вы только успеваете заметить, как он\nнажал что-то на стене возле прохода.\n"
                                        "В этот же момент в вас начинают лететь\n3 стрелы. Вы стараетесь уклониться от\n"
                                        "них, но одна всё-таки попадает вам\nв ногу.. Вам ещё повезло, но стоит\n"
                                        "убиться отсюда.\n\n"
                                        "\nHP - " + str((10 + (4 * Floor) - (2 * Luck))) +
                                        "\nОпыт + " + str((5 + (2 * Floor) + Luck)),
                                   font_size=25,
                                   color=[62 / 255, 28 / 255, 0 / 255, 1]))
        Viktorina.add_widget(Button(text="Продолжить",
                                    background_color=[180 / 255, 140 / 255, 75 / 255, 1],
                                    font_size=20, color=[62 / 255, 28 / 255, 0 / 255, 1], background_normal="",
                                    size_hint=(.4, .2), pos=(320, 30),
                                    on_press=self.dalee))
        Viktorina.add_widget(Button(text="HP = " + str(HP),
                                    background_color=[150 / 255, 81 / 255, 69 / 255, 1],
                                    font_size=20, color=[64 / 255, 21 / 255, 21 / 255, 1], background_normal="",
                                    size_hint=(.3, .10 / 11), pos=(27, 580)))
        self.add_widget(Viktorina)

    def piy(self, event):
        print("Tipo soxranenie")

    def dalee(self, event):
        # удаляет все виджеты класса и создает новый виджет этого же класса
        self.clear_widgets()
        self.add_widget(Viktorina5F())
        i = random.randint(1, Count_Screen)
        set_screen(str(i))

    def in_leave(self):
        self.add_widget.clear_widgets()

# _____________________________________________________________________________________
# Конец викторин
# _____________________________________________________________________________________


# _____________________________________________________________________________________
# Магазины
# _____________________________________________________________________________________

class Magazin1(Screen):
    def __init__(self, **kw):
        super(Magazin1, self).__init__(**kw)

    def on_enter(self):
        Magazin = FloatLayout()
        Magazin.add_widget(Button(text="<-- В главное меню",
                                  background_color=[185 / 255, 145 / 255, 75 / 255, 1],
                                  font_size=20,
                                  color=[62 / 255, 28 / 255, 0 / 255, 1],
                                  size_hint=(.9, .1), pos=(27, 610),
                                  background_normal="", on_press=lambda x: set_screen('Главное_меню')))
        Magazin.add_widget(Label(text="Выйдя на освещённую площадку пещеры,\nвы замечаете старика в неприметных\n"
                                      "одеждах. На его переносной торговочной\nлавке расставленно несколько\n"
                                      "знакомых вам вещей.\n\n"
                                      "Может быть, вам удасться что-то\nкупить у него?\n\n\n\n\n",
                                 font_size=25,
                                 color=[62 / 255, 28 / 255, 0 / 255, 1]))
        Magazin.add_widget(Button(text="Продолжить",
                                  background_color=[180 / 255, 140 / 255, 75 / 255, 1],
                                  font_size=20, color=[62 / 255, 28 / 255, 0 / 255, 1], background_normal="",
                                  size_hint=(.4, .2), pos=(320, 30),
                                  on_press=lambda x: set_screen('5.2')))
        Magazin.add_widget(Button(text="HP = " + str(HP),
                                  background_color=[150 / 255, 81 / 255, 69 / 255, 1],
                                  font_size=20, color=[64 / 255, 21 / 255, 21 / 255, 1], background_normal="",
                                  size_hint=(.3, .10 / 11), pos=(27, 580)))
        self.add_widget(Magazin)

    def in_leave(self):
        self.add_widget.clear_widgets()


class Magazin2(Screen):
    def __init__(self, **kw):
        super(Magazin2, self).__init__(**kw)

    def on_enter(self):
        Magazin = FloatLayout()
        Magazin.add_widget(Button(text="<-- В главное меню",
                                  background_color=[185 / 255, 145 / 255, 75 / 255, 1],
                                  font_size=20,
                                  color=[62 / 255, 28 / 255, 0 / 255, 1],
                                  size_hint=(.9, .1), pos=(27, 610),
                                  background_normal="", on_press=lambda x: set_screen('Главное_меню')))
        Magazin.add_widget(Button(text="Продолжить",
                                  background_color=[180 / 255, 140 / 255, 75 / 255, 1],
                                  font_size=20, color=[62 / 255, 28 / 255, 0 / 255, 1], background_normal="",
                                  size_hint=(.4, .2), pos=(320, 30),
                                  on_press=self.dalee))
        Magazin.add_widget(Label(text="                    Предметы                               Купить     \n\n\n"
                                      "Обычное зелье лечения\n\n\n\nСильное зелье лечения\n\n\n\n"
                                      "Эпическое зелье лечения\n\n\n\n",
                                 font_size=25, color=[62 / 255, 28 / 255, 0 / 255, 1]))
        Magazin.add_widget(Button(text="5 трофеев",
                                  font_size=25, color=[62 / 255, 28 / 255, 0 / 255, 1],
                                  background_color=[185 / 255, 145 / 255, 75 / 255, 1], size_hint=(.3, .1),
                                  pos=(385, 440),
                                  background_normal="", on_press=self.обычное_зелье))
        Magazin.add_widget(Button(text="10 трофеев",
                                  font_size=25, color=[62 / 255, 28 / 255, 0 / 255, 1],
                                  background_color=[180 / 255, 140 / 255, 75 / 255, 1], size_hint=(.3, .1),
                                  pos=(385, 320),
                                  background_normal="", on_press=self.сильное_зелье))
        Magazin.add_widget(Button(text="15 трофеев",
                                  font_size=25, color=[62 / 255, 28 / 255, 0 / 255, 1],
                                  background_color=[185 / 255, 145 / 255, 75 / 255, 1], size_hint=(.3, .1),
                                  pos=(385, 200),
                                  background_normal="", on_press=self.эпическое_зелье))
        self.add_widget(Magazin)

    def dalee(self, event):
        i = random.randint(1, Count_Screen)
        set_screen(str(i))

    def обычное_зелье(self, event):
        global Usual_healing_potion
        global Trophies
        if (Trophies - 5) > 0:
            Usual_healing_potion += 1
            Trophies -= 5
        else:
            set_screen('Нет_средств2')

    def сильное_зелье(self, event):
        global Powerful_healing_potion
        global Trophies
        if (Trophies - 10) > 0:
            Powerful_healing_potion += 1
            Trophies -= 10
        else:
            set_screen('Нет_средств2')

    def эпическое_зелье(self, event):
        global Epic_healing_potion
        global Trophies
        if (Trophies - 15) > 0:
            Epic_healing_potion += 1
            Trophies -= 15
        else:
            set_screen('Нет_средств2')

    def in_leave(self):
        self.add_widget.clear_widgets()


class N0_money2(Screen):
    def __init__(self, **kw):
        super(N0_money2, self).__init__(**kw)

    def on_enter(self):
        No = FloatLayout()
        No.add_widget(Button(text="У Вас недостаточно трофеев!\n\n(нажмите для продолжения)",
                             font_size=25, color=[62 / 255, 28 / 255, 0 / 255, 1],
                             background_color=[185 / 255, 145 / 255, 75 / 255, 1], size_hint=(.7, .3), pos=(90, 275),
                             background_normal="", on_press=lambda x: set_screen('5.2')))
        self.add_widget(No)

    def in_leave(self):
        self.add_widget.clear_widgets()


class Magaz2(Screen):
    def __init__(self, **kw):
        super(Magaz2, self).__init__(**kw)

    def on_enter(self):
        Magazin = FloatLayout()
        Magazin.add_widget(Button(text="<-- В главное меню",
                                  background_color=[185 / 255, 145 / 255, 75 / 255, 1],
                                  font_size=20,
                                  color=[62 / 255, 28 / 255, 0 / 255, 1],
                                  size_hint=(.9, .1), pos=(27, 610),
                                  background_normal="", on_press=lambda x: set_screen('Главное_меню')))
        Magazin.add_widget(Label(text="Вы слоняетесь по коридорам в поисках\nчего-то съестного, ну или хотя бы полезного.\n"
                                      "\nСпустя пару часов вы набредаете на\nнеизвестое существо высокого роста,\n"
                                      "закутанноев плащ.\n\n'Что-то ищите?' - с улыбкой спрашивает оно.\n"
                                      "'У меня есть для вас кое-что, если вам\nэто по карману, конечно же.'\n\n\n",
                                 font_size=25,
                                 color=[62 / 255, 28 / 255, 0 / 255, 1]))
        Magazin.add_widget(Button(text="Продолжить",
                                  background_color=[180 / 255, 140 / 255, 75 / 255, 1],
                                  font_size=20, color=[62 / 255, 28 / 255, 0 / 255, 1], background_normal="",
                                  size_hint=(.4, .2), pos=(320, 30),
                                  on_press=lambda x: set_screen('20.1')))
        Magazin.add_widget(Button(text="HP = " + str(HP),
                                  background_color=[150 / 255, 81 / 255, 69 / 255, 1],
                                  font_size=20, color=[64 / 255, 21 / 255, 21 / 255, 1], background_normal="",
                                  size_hint=(.3, .10 / 11), pos=(27, 580)))
        self.add_widget(Magazin)

    def in_leave(self):
        self.add_widget.clear_widgets()


class Magaz2_1(Screen):
    def __init__(self, **kw):
        super(Magaz2_1, self).__init__(**kw)

    def on_enter(self):
        Magazin = FloatLayout()
        Magazin.add_widget(Button(text="<-- В главное меню",
                                  background_color=[185 / 255, 145 / 255, 75 / 255, 1],
                                  font_size=20,
                                  color=[62 / 255, 28 / 255, 0 / 255, 1],
                                  size_hint=(.9, .1), pos=(27, 610),
                                  background_normal="", on_press=lambda x: set_screen('Главное_меню')))
        Magazin.add_widget(Button(text="Продолжить",
                                  background_color=[180 / 255, 140 / 255, 75 / 255, 1],
                                  font_size=20, color=[62 / 255, 28 / 255, 0 / 255, 1], background_normal="",
                                  size_hint=(.4, .2), pos=(320, 30),
                                  on_press=self.dalee))
        Magazin.add_widget(Label(text="               Предметы                               Купить     \n\n\n"
                                      "Ожерелье из магических\nкамней\n\n\nКольцо с магическим канем"
                                      "\n\n\n\nОружие из зачарованной\nуглеродной стали\n\n\n\n",
                                 font_size=25, color=[62 / 255, 28 / 255, 0 / 255, 1]))
        Magazin.add_widget(Button(text="150 трофеев",
                                  font_size=25, color=[62 / 255, 28 / 255, 0 / 255, 1],
                                  background_color=[185 / 255, 145 / 255, 75 / 255, 1], size_hint=(.3, .1),
                                  pos=(385, 440),
                                  background_normal="", on_press=self.Ожерелье_из_магических_камней))
        Magazin.add_widget(Button(text="150 трофеев",
                                  font_size=25, color=[62 / 255, 28 / 255, 0 / 255, 1],
                                  background_color=[180 / 255, 140 / 255, 75 / 255, 1], size_hint=(.3, .1),
                                  pos=(385, 320),
                                  background_normal="", on_press=self.Кольцо_с_магическим_канем))
        Magazin.add_widget(Button(text="200 трофеев",
                                  font_size=25, color=[62 / 255, 28 / 255, 0 / 255, 1],
                                  background_color=[185 / 255, 145 / 255, 75 / 255, 1], size_hint=(.3, .1),
                                  pos=(385, 200),
                                  background_normal="", on_press=self.Оружие_из_зачарованной_углеродной_стали))
        self.add_widget(Magazin)

    def dalee(self, event):
        i = random.randint(1, Count_Screen)
        set_screen(str(i))

    def Ожерелье_из_магических_камней(self, event):
        global necklace_legendary, Trophies
        if (Trophies - 150) > 0:
            necklace_legendary += 1
            Trophies -= 150
        else:
            set_screen('Нет_средств3')

    def Кольцо_с_магическим_канем(self, event):
        global ring_legendary, Trophies
        if (Trophies - 150) > 0:
            ring_legendary += 1
            Trophies -= 150
        else:
            set_screen('Нет_средств3')

    def Оружие_из_зачарованной_углеродной_стали(self, event):
        global weapon_legendary, Trophies
        if (Trophies - 200) > 0:
            weapon_legendary += 1
            Trophies -= 200
        else:
            set_screen('Нет_средств3')

    def in_leave(self):
        self.add_widget.clear_widgets()


class N0_money3(Screen):
    def __init__(self, **kw):
        super(N0_money3, self).__init__(**kw)

    def on_enter(self):
        No = FloatLayout()
        No.add_widget(Button(text="У Вас недостаточно трофеев!\n\n(нажмите для продолжения)",
                             font_size=25, color=[62 / 255, 28 / 255, 0 / 255, 1],
                             background_color=[185 / 255, 145 / 255, 75 / 255, 1], size_hint=(.7, .3), pos=(90, 275),
                             background_normal="", on_press=lambda x: set_screen('20.1')))
        self.add_widget(No)

    def in_leave(self):
        self.add_widget.clear_widgets()


class Magaz3(Screen):
    def __init__(self, **kw):
        super(Magaz3, self).__init__(**kw)

    def on_enter(self):
        Magazin = FloatLayout()
        Magazin.add_widget(Button(text="<-- В главное меню",
                                  background_color=[185 / 255, 145 / 255, 75 / 255, 1],
                                  font_size=20,
                                  color=[62 / 255, 28 / 255, 0 / 255, 1],
                                  size_hint=(.9, .1), pos=(27, 610),
                                  background_normal="", on_press=lambda x: set_screen('Главное_меню')))
        Magazin.add_widget(Label(text="В поисках пути наверх, вы всё\nчаще начинаете натыкаться на тупики\n"
                                      "или тоннели, ведущие вниз..\nЧто ж, может вам пока рано выбирваться\n"
                                      "и стоит подыскать для себя что-то\nполезное?\n\n"
                                      "Вы помните, что где-то в этой\nместности был дроу, торгующий\n"
                                      "неплохой экипировкой.\n\nЕщё через несколько часов\n"
                                      "вы всё-таки находите его.\n\n",
                                 font_size=25,
                                 color=[62 / 255, 28 / 255, 0 / 255, 1]))
        Magazin.add_widget(Button(text="Продолжить",
                                  background_color=[180 / 255, 140 / 255, 75 / 255, 1],
                                  font_size=20, color=[62 / 255, 28 / 255, 0 / 255, 1], background_normal="",
                                  size_hint=(.4, .2), pos=(320, 30),
                                  on_press=lambda x: set_screen('21.1')))
        Magazin.add_widget(Button(text="HP = " + str(HP),
                                  background_color=[150 / 255, 81 / 255, 69 / 255, 1],
                                  font_size=20, color=[64 / 255, 21 / 255, 21 / 255, 1], background_normal="",
                                  size_hint=(.3, .10 / 11), pos=(27, 580)))
        self.add_widget(Magazin)

    def in_leave(self):
        self.add_widget.clear_widgets()


class Magaz3_2(Screen):
    def __init__(self, **kw):
        super(Magaz3_2, self).__init__(**kw)

    def on_enter(self):
        Magazin = FloatLayout()
        Magazin.add_widget(Button(text="<-- В главное меню",
                                  background_color=[185 / 255, 145 / 255, 75 / 255, 1],
                                  font_size=20,
                                  color=[62 / 255, 28 / 255, 0 / 255, 1],
                                  size_hint=(.9, .1), pos=(27, 610),
                                  background_normal="", on_press=lambda x: set_screen('Главное_меню')))
        Magazin.add_widget(Button(text="Продолжить",
                                  background_color=[180 / 255, 140 / 255, 75 / 255, 1],
                                  font_size=20, color=[62 / 255, 28 / 255, 0 / 255, 1], background_normal="",
                                  size_hint=(.4, .2), pos=(320, 30),
                                  on_press=self.dalee))
        Magazin.add_widget(Label(text="               Предметы                               Купить     \n\n"
                                      "Шлем из\nмагических нитей\n\nНагрудник из\nмагических нитей"
                                      "\n\nШтаны из\nмагических нитей\n\nСапоги из\nмагических нитей\n\n\n\n",
                                 font_size=25, color=[62 / 255, 28 / 255, 0 / 255, 1]))
        Magazin.add_widget(Button(text="175 трофеев",
                                  font_size=25, color=[62 / 255, 28 / 255, 0 / 255, 1],
                                  background_color=[185 / 255, 145 / 255, 75 / 255, 1], size_hint=(.3, .1),
                                  pos=(385, 470),
                                  background_normal="", on_press=self.Шлем_из_магических_нитей))
        Magazin.add_widget(Button(text="200 трофеев",
                                  font_size=25, color=[62 / 255, 28 / 255, 0 / 255, 1],
                                  background_color=[180 / 255, 140 / 255, 75 / 255, 1], size_hint=(.3, .1),
                                  pos=(385, 380),
                                  background_normal="", on_press=self.Нагрудник_из_магических_нитей))
        Magazin.add_widget(Button(text="200 трофеев",
                                  font_size=25, color=[62 / 255, 28 / 255, 0 / 255, 1],
                                  background_color=[185 / 255, 145 / 255, 75 / 255, 1], size_hint=(.3, .1),
                                  pos=(385, 290),
                                  background_normal="", on_press=self.Штаны_из_магических_нитей))
        Magazin.add_widget(Button(text="175 трофеев",
                                  font_size=25, color=[62 / 255, 28 / 255, 0 / 255, 1],
                                  background_color=[185 / 255, 145 / 255, 75 / 255, 1], size_hint=(.3, .1),
                                  pos=(385, 200),
                                  background_normal="", on_press=self.Сапоги_из_магических_нитей))
        self.add_widget(Magazin)

    def dalee(self, event):
        i = random.randint(1, Count_Screen)
        set_screen(str(i))

    def Шлем_из_магических_нитей(self, event):
        global necklace_legendary, Trophies
        if (Trophies - 175) > 0:
            necklace_legendary += 1
            Trophies -= 175
        else:
            set_screen('Нет_средств4')

    def Нагрудник_из_магических_нитей(self, event):
        global ring_legendary, Trophies
        if (Trophies - 200) > 0:
            ring_legendary += 1
            Trophies -= 200
        else:
            set_screen('Нет_средств4')

    def Штаны_из_магических_нитей(self, event):
        global weapon_legendary, Trophies
        if (Trophies - 200) > 0:
            weapon_legendary += 1
            Trophies -= 200
        else:
            set_screen('Нет_средств4')

    def Сапоги_из_магических_нитей(self, event):
        global weapon_legendary, Trophies
        if (Trophies - 175) > 0:
            weapon_legendary += 1
            Trophies -= 175
        else:
            set_screen('Нет_средств4')

    def in_leave(self):
        self.add_widget.clear_widgets()


class N0_money4(Screen):
    def __init__(self, **kw):
        super(N0_money4, self).__init__(**kw)

    def on_enter(self):
        No = FloatLayout()
        No.add_widget(Button(text="У Вас недостаточно трофеев!\n\n(нажмите для продолжения)",
                             font_size=25, color=[62 / 255, 28 / 255, 0 / 255, 1],
                             background_color=[185 / 255, 145 / 255, 75 / 255, 1], size_hint=(.7, .3), pos=(90, 275),
                             background_normal="", on_press=lambda x: set_screen('21.1')))
        self.add_widget(No)

    def in_leave(self):
        self.add_widget.clear_widgets()

# _____________________________________________________________________________________
# Конец магазинов
# _____________________________________________________________________________________


# _____________________________________________________________________________________
# Отдых
# _____________________________________________________________________________________

class Ozero(Screen):
    def __init__(self, **kw):
        super(Ozero, self).__init__(**kw)

    def on_enter(self):
        Ozero = FloatLayout()
        Ozero.add_widget(Button(text="<-- В главное меню",
                                background_color=[185 / 255, 145 / 255, 75 / 255, 1],
                                font_size=20,
                                color=[62 / 255, 28 / 255, 0 / 255, 1],
                                size_hint=(.9, .1), pos=(27, 610),
                                background_normal="", on_press=lambda x: set_screen('Главное_меню')))
        Ozero.add_widget(Label(text="Вы вышли на большую ровную площадку.\nПод потолком пещеры кружат маленькие\n"
                                    "летучие мышки, вроде бы безобидные...\n\n"
                                    "Вы замечаете небольшой костёр,\nоставленный кем-то в этом месте.\n\n"
                                    "Что ж, может и вам стоит передохнуть?\n\n\n\n\n",
                               font_size=25,
                               color=[62 / 255, 28 / 255, 0 / 255, 1]))
        Ozero.add_widget(Button(text="Продолжить",
                                background_color=[180 / 255, 140 / 255, 75 / 255, 1],
                                font_size=20, color=[62 / 255, 28 / 255, 0 / 255, 1], background_normal="",
                                size_hint=(.4, .2), pos=(320, 30),
                                on_press=self.proda))
        Ozero.add_widget(Button(text="HP = " + str(HP),
                                background_color=[150 / 255, 81 / 255, 69 / 255, 1],
                                font_size=20, color=[64 / 255, 21 / 255, 21 / 255, 1], background_normal="",
                                size_hint=(.3, .10 / 11), pos=(27, 580)))
        self.add_widget(Ozero)

    def proda(self, event):
        global HP
        HP = MAX_HP
        set_screen('6.2')

    def in_leave(self):
        self.add_widget.clear_widgets()


class Ozero2(Screen):
    def __init__(self, **kw):
        super(Ozero2, self).__init__(**kw)

    def on_enter(self):
        Ozero = FloatLayout()
        Ozero.add_widget(Button(text="<-- В главное меню",
                                background_color=[185 / 255, 145 / 255, 75 / 255, 1],
                                font_size=20,
                                color=[62 / 255, 28 / 255, 0 / 255, 1],
                                size_hint=(.9, .1), pos=(27, 610),
                                background_normal="", on_press=lambda x: set_screen('Главное_меню')))
        Ozero.add_widget(Label(text="Вам удалось отдохнуть без приключений.\n\n"
                                    "Поев и восстановив силы, вы готовы\nпродолжить путь.\n\n"
                                    "Жаль, но вам всё же придётся\nпокинуть это красивое и тихое место.\n\n"
                                    "Ваше HP полностью восстановлено\n\n\n\n",
                               font_size=25,
                               color=[62 / 255, 28 / 255, 0 / 255, 1]))
        Ozero.add_widget(Button(text="Продолжить",
                                background_color=[180 / 255, 140 / 255, 75 / 255, 1],
                                font_size=20, color=[62 / 255, 28 / 255, 0 / 255, 1], background_normal="",
                                size_hint=(.4, .2), pos=(320, 30),
                                on_press=self.dalee))
        Ozero.add_widget(Button(text="HP = " + str(HP),
                                background_color=[150 / 255, 81 / 255, 69 / 255, 1],
                                font_size=20, color=[64 / 255, 21 / 255, 21 / 255, 1], background_normal="",
                                size_hint=(.3, .10 / 11), pos=(27, 580)))
        self.add_widget(Ozero)

    def dalee(self, event):
        a = random.randint(1, 10)
        if a <= 5:
            set_screen('Моб')
        else:
            i = random.randint(1, Count_Screen)
            set_screen(str(i))

    def in_leave(self):
        self.add_widget.clear_widgets()


class Abandoned_House(Screen):
    def __init__(self, **kw):
        super(Abandoned_House, self).__init__(**kw)

    def on_enter(self):
        Abandoned_House = FloatLayout()
        Abandoned_House.add_widget(Button(text="<-- В главное меню",
                                          background_color=[185 / 255, 145 / 255, 75 / 255, 1],
                                          font_size=20,
                                          color=[62 / 255, 28 / 255, 0 / 255, 1],
                                          size_hint=(.9, .1), pos=(27, 610),
                                          background_normal="", on_press=lambda x: set_screen('Главное_меню')))
        Abandoned_House.add_widget(
            Label(text="Вы долго бродили по коридорам в поисках\nукромного места, однако везде вам"
                       "\nказалось опасно, но вам стоит отдохнуть.\n\nНо и вам должно было повезти."
                       "\nВы нашли небольшой заброшенный дом, или\nбывший склад.. не важно, главное,\n"
                       "что вам очень хочется спать.. Вы решаете\nотдохнуть там.\n\n"
                       "Осмотрев дом вы понимаете, что ничего\nопасного здесь нет, но на всякий\n"
                       "случай садитесь поближе к запасному\nвыходу и засыпаете...",
                  font_size=25,
                  color=[62 / 255, 28 / 255, 0 / 255, 1]))
        Abandoned_House.add_widget(Button(text="Продолжить",
                                          background_color=[180 / 255, 140 / 255, 75 / 255, 1],
                                          font_size=20, color=[62 / 255, 28 / 255, 0 / 255, 1], background_normal="",
                                          size_hint=(.4, .2), pos=(320, 30),
                                          on_press=self.proda))
        Abandoned_House.add_widget(Button(text="HP = " + str(HP),
                                          background_color=[150 / 255, 81 / 255, 69 / 255, 1],
                                          font_size=20, color=[64 / 255, 21 / 255, 21 / 255, 1], background_normal="",
                                          size_hint=(.3, .10 / 11), pos=(27, 580)))
        self.add_widget(Abandoned_House)

    def proda(self, event):
        global HP
        HP = MAX_HP
        set_screen('6.2')

    def in_leave(self):
        self.add_widget.clear_widgets()


class Abandoned_House2(Screen):
    def __init__(self, **kw):
        super(Abandoned_House2, self).__init__(**kw)

    def on_enter(self):
        Abandoned_House = FloatLayout()
        Abandoned_House.add_widget(Button(text="<-- В главное меню",
                                          background_color=[185 / 255, 145 / 255, 75 / 255, 1],
                                          font_size=20,
                                          color=[62 / 255, 28 / 255, 0 / 255, 1],
                                          size_hint=(.9, .1), pos=(27, 610),
                                          background_normal="", on_press=lambda x: set_screen('Главное_меню')))
        Abandoned_House.add_widget(Label(text="Вам удалось отдохнуть без приключений.\n\n"
                                              "Поспав и восстановив силы, вы готовы\nпродолжить путь.\n\n"
                                              "Покидая дом вам кажется, что было бы\nнеплохо запомнить его местоположение\n\n"
                                              "Ваше HP полностью восстановлено\n\n\n\n",
                                         font_size=25,
                                         color=[62 / 255, 28 / 255, 0 / 255, 1]))
        Abandoned_House.add_widget(Button(text="Продолжить",
                                          background_color=[180 / 255, 140 / 255, 75 / 255, 1],
                                          font_size=20, color=[62 / 255, 28 / 255, 0 / 255, 1], background_normal="",
                                          size_hint=(.4, .2), pos=(320, 30),
                                          on_press=self.dalee))
        Abandoned_House.add_widget(Button(text="HP = " + str(HP),
                                          background_color=[150 / 255, 81 / 255, 69 / 255, 1],
                                          font_size=20, color=[64 / 255, 21 / 255, 21 / 255, 1], background_normal="",
                                          size_hint=(.3, .10 / 11), pos=(27, 580)))
        self.add_widget(Abandoned_House)

    def dalee(self, event):
        a = random.randint(1, 10)
        if a <= 3:
            set_screen('Моб')
        else:
            i = random.randint(1, Count_Screen)
            set_screen(str(i))

    def in_leave(self):
        self.add_widget.clear_widgets()


class Hole_in_Wall(Screen):
    def __init__(self, **kw):
        super(Hole_in_Wall, self).__init__(**kw)

    def on_enter(self):
        Hole_in_Wall = FloatLayout()
        Hole_in_Wall.add_widget(Button(text="<-- В главное меню",
                                       background_color=[185 / 255, 145 / 255, 75 / 255, 1],
                                       font_size=20,
                                       color=[62 / 255, 28 / 255, 0 / 255, 1],
                                       size_hint=(.9, .1), pos=(27, 610),
                                       background_normal="", on_press=lambda x: set_screen('Главное_меню')))
        Hole_in_Wall.add_widget(Label(text="Вы бежите по коридору, а за вами\nгонится монстр, похожий на огромный\n"
                                           "шар с шипами! Вы бегло осмотриваете\nмелькающие мимо камни, валуны, стены..\n"
                                           "Вы замечаете темную полосу на стене\nи решаете бежать к ней\n"
                                           "Это оказалось небольшой расщелиной,\nкуда вы с трудом можете пролезть\n"
                                           "Идеально, чтобы спрятаться\n\nПролезая вперёд, вы замечаете небольшое\n"
                                           "свечение впереди. Расщелина вела в\nнебольшую 'комнату' в скале.\n\n",
                                      font_size=25,
                                      color=[62 / 255, 28 / 255, 0 / 255, 1]))
        Hole_in_Wall.add_widget(Button(text="Продолжить",
                                       background_color=[180 / 255, 140 / 255, 75 / 255, 1],
                                       font_size=20, color=[62 / 255, 28 / 255, 0 / 255, 1], background_normal="",
                                       size_hint=(.4, .2), pos=(320, 30),
                                       on_press=self.proda))
        Hole_in_Wall.add_widget(Button(text="HP = " + str(HP),
                                       background_color=[150 / 255, 81 / 255, 69 / 255, 1],
                                       font_size=20, color=[64 / 255, 21 / 255, 21 / 255, 1], background_normal="",
                                       size_hint=(.3, .10 / 11), pos=(27, 580)))
        self.add_widget(Hole_in_Wall)

    def proda(self, event):
        global HP
        HP = MAX_HP
        set_screen('11.2')

    def in_leave(self):
        self.add_widget.clear_widgets()


class Hole_in_Wall2(Screen):
    def __init__(self, **kw):
        super(Hole_in_Wall2, self).__init__(**kw)

    def on_enter(self):
        Hole_in_Wall = FloatLayout()
        Hole_in_Wall.add_widget(Button(text="<-- В главное меню",
                                       background_color=[185 / 255, 145 / 255, 75 / 255, 1],
                                       font_size=20,
                                       color=[62 / 255, 28 / 255, 0 / 255, 1],
                                       size_hint=(.9, .1), pos=(27, 610),
                                       background_normal="", on_press=lambda x: set_screen('Главное_меню')))
        Hole_in_Wall.add_widget(
            Label(text="Осотревшись вокруг вы не видите\nничего: ни монстров, ни воды, ни растений\n"
                       "Может оно и к лучшему..\n\nЧерез какое-то время грохот по другую\n"
                       "сторону расщелины затихает и вы\nпонимаете, что монстр перестал\n"
                       "за вами гнаться\n\nВам тоже стоит отдохнуть и выспаться.\n\n"
                       "Ваше HP полностью восстановлено!\n\n\n",
                  font_size=25,
                  color=[62 / 255, 28 / 255, 0 / 255, 1]))
        Hole_in_Wall.add_widget(Button(text="Продолжить",
                                       background_color=[180 / 255, 140 / 255, 75 / 255, 1],
                                       font_size=20, color=[62 / 255, 28 / 255, 0 / 255, 1], background_normal="",
                                       size_hint=(.4, .2), pos=(320, 30),
                                       on_press=self.dalee))
        Hole_in_Wall.add_widget(Button(text="HP = " + str(HP),
                                       background_color=[150 / 255, 81 / 255, 69 / 255, 1],
                                       font_size=20, color=[64 / 255, 21 / 255, 21 / 255, 1], background_normal="",
                                       size_hint=(.3, .10 / 11), pos=(27, 580)))
        self.add_widget(Hole_in_Wall)

    def dalee(self, event):
        a = random.randint(1, 10)
        if a <= 3:
            set_screen('Моб')
        else:
            i = random.randint(1, Count_Screen)
            set_screen(str(i))

    def in_leave(self):
        self.add_widget.clear_widgets()

# _____________________________________________________________________________________
# Конец локаций отдыха
# _____________________________________________________________________________________


# _____________________________________________________________________________________
# Ловушки
# _____________________________________________________________________________________
class LovyshkaOFF(Screen):
    def __init__(self, **kw):
        super(LovyshkaOFF, self).__init__(**kw)

    def on_enter(self):
        Lovyshka = FloatLayout()
        Lovyshka.add_widget(Button(text="<-- В главное меню",
                                   background_color=[185 / 255, 145 / 255, 75 / 255, 1],
                                   font_size=20,
                                   color=[62 / 255, 28 / 255, 0 / 255, 1],
                                   size_hint=(.9, .1), pos=(27, 610),
                                   background_normal="", on_press=lambda x: set_screen('Главное_меню')))
        Lovyshka.add_widget(Label(text="Проходя по очередному коридору,\nвы в последний момент смогли\n"
                                       "уклониться от пролетающей над\nвашей головой стрелы.\n\n"
                                       "Сегодня вам повезло, но в\nследующий раз стоит внимательнее              \n"
                                       "смотреть под ноги!\n\nОпыт + 10\n\n\n",
                                  font_size=25,
                                  color=[62 / 255, 28 / 255, 0 / 255, 1]))
        Lovyshka.add_widget(Button(text="Продолжить",
                                   background_color=[180 / 255, 140 / 255, 75 / 255, 1],
                                   font_size=20, color=[62 / 255, 28 / 255, 0 / 255, 1], background_normal="",
                                   size_hint=(.4, .2), pos=(320, 30),
                                   on_press=self.proda))
        Lovyshka.add_widget(Button(text="HP = " + str(HP),
                                   background_color=[150 / 255, 81 / 255, 69 / 255, 1],
                                   font_size=20, color=[64 / 255, 21 / 255, 21 / 255, 1], background_normal="",
                                   size_hint=(.3, .10 / 11), pos=(27, 580)))
        self.add_widget(Lovyshka)

    def proda(self, event):
        global Experience
        Experience += 10
        global LVL, MAX_HP, Strenght, Skill, Luck, Floor, HP, Endurance
        if Experience >= 50 + 20 * LVL:
            LVL += 1
            Experience = 0
            if LVL < 10:
                MAX_HP += MAX_HP // 10
                Floor += 1
                HP += MAX_HP // 2
                if HP > MAX_HP:
                    HP = MAX_HP
                if Class == "Маг":
                    Strenght += 1
                    Luck += 1
                elif Class == "Убийца":
                    Strenght += 1
                    Skill += 1
                elif (Class == "Воин") or (Class == "Страж"):
                    Strenght += 1
                    Endurance += 1
            else:
                set_screen('Конец_Игры')
        else:
            a = random.randint(1, 10)
            if a <= 3:
                set_screen('Моб')
            else:
                i = random.randint(1, Count_Screen)
                set_screen(str(i))

    def in_leave(self):
        self.add_widget.clear_widgets()


class LovyshkaON(Screen):
    def __init__(self, **kw):
        super(LovyshkaON, self).__init__(**kw)

    def on_enter(self):
        Lovyshka = FloatLayout()
        Lovyshka.add_widget(Button(text="<-- В главное меню",
                                   background_color=[185 / 255, 145 / 255, 75 / 255, 1],
                                   font_size=20,
                                   color=[62 / 255, 28 / 255, 0 / 255, 1],
                                   size_hint=(.9, .1), pos=(27, 610),
                                   background_normal="", on_press=lambda x: set_screen('Главное_меню')))
        Lovyshka.add_widget(Label(text="Блуждая по коридорам тёмной пещеры,  \nвы не заметили, как наступили на\n"
                                       "исписанный рунами булыжник,\nактивировав ловушку!\n\n"
                                       "Шипы, резко выдвинувшиеся из стены,\nсильно задели вас!\n\n"
                                       "Опыт + 5\nHP - 20\n\n\n\n",
                                  font_size=25,
                                  color=[62 / 255, 28 / 255, 0 / 255, 1]))
        Lovyshka.add_widget(Button(text="Продолжить",
                                   background_color=[180 / 255, 140 / 255, 75 / 255, 1],
                                   font_size=20, color=[62 / 255, 28 / 255, 0 / 255, 1], background_normal="",
                                   size_hint=(.4, .2), pos=(320, 30),
                                   on_press=self.proda))
        Lovyshka.add_widget(Button(text="HP = " + str(HP),
                                   background_color=[150 / 255, 81 / 255, 69 / 255, 1],
                                   font_size=20, color=[64 / 255, 21 / 255, 21 / 255, 1], background_normal="",
                                   size_hint=(.3, .10 / 11), pos=(27, 580)))
        self.add_widget(Lovyshka)

    def proda(self, event):
        global Experience, HP
        HP -= 20
        if HP <= 0:
            set_screen('Конец_Игры_Умер')
        else:
            Experience += 5
            global LVL, MAX_HP, Strenght, Skill, Luck, Floor, Endurance
            if Experience >= 50 + 20 * LVL:
                LVL += 1
                Experience = 0
                if LVL < 10:
                    MAX_HP += MAX_HP // 10
                    Floor += 1
                    HP += MAX_HP // 2
                    if HP > MAX_HP:
                        HP = MAX_HP
                    if Class == "Маг":
                        Strenght += 1
                        Luck += 1
                    elif Class == "Убийца":
                        Strenght += 1
                        Skill += 1
                    elif (Class == "Воин") or (Class == "Страж"):
                        Strenght += 1
                        Endurance += 1
                else:
                    set_screen('Конец_Игры')
            else:
                i = random.randint(1, Count_Screen)
                set_screen(str(i))

    def in_leave(self):
        self.add_widget.clear_widgets()


class Kamnepad(Screen):
    def __init__(self, **kw):
        super(Kamnepad, self).__init__(**kw)

    def on_enter(self):
        Kamnepad = FloatLayout()
        Kamnepad.add_widget(Button(text="<-- В главное меню",
                                   background_color=[185 / 255, 145 / 255, 75 / 255, 1],
                                   font_size=20,
                                   color=[62 / 255, 28 / 255, 0 / 255, 1],
                                   size_hint=(.9, .1), pos=(27, 610),
                                   background_normal="", on_press=lambda x: set_screen('Главное_меню')))
        Kamnepad.add_widget(Label(text="Вы услышали отдалённый грохот\n чем-то похожий на камнепад\n"
                                       "Подняв голову наверх вы поняли,\nчто камни падают прямо на вас!\n\n"
                                       "И теперь лишь от ваших способностей\nзависит ваша жизнь.\n\n"
                                       "Урон от ловушки: " + str((25 - Skill - Endurance)) +
                                       "\nПолученный опыт: " + str((Skill + Endurance)),
                                  font_size=25,
                                  color=[62 / 255, 28 / 255, 0 / 255, 1]))
        Kamnepad.add_widget(Button(text="Продолжить",
                                   background_color=[180 / 255, 140 / 255, 75 / 255, 1],
                                   font_size=20, color=[62 / 255, 28 / 255, 0 / 255, 1], background_normal="",
                                   size_hint=(.4, .2), pos=(320, 30),
                                   on_press=self.dalee))
        Kamnepad.add_widget(Button(text="HP = " + str(HP),
                                   background_color=[150 / 255, 81 / 255, 69 / 255, 1],
                                   font_size=20, color=[64 / 255, 21 / 255, 21 / 255, 1], background_normal="",
                                   size_hint=(.3, .10 / 11), pos=(27, 580)))
        self.add_widget(Kamnepad)

    def dalee(self, event):
        # удаляет все виджеты класса и создает новый виджет этого же класса
        self.clear_widgets()
        self.add_widget(Kamnepad())
        global HP, Experience, LVL, Skill, Endurance
        damage = 25 - Skill - Endurance
        HP -= damage
        if HP <= 0:
            set_screen('Конец_Игры_Умер')
        else:
            Experience += (Skill + Endurance)
            global MAX_HP, Strenght, Luck, Floor
            if Experience >= 50 + 20 * LVL:
                LVL += 1
                Experience = 0
                if LVL < 10:
                    MAX_HP += MAX_HP // 10
                    Floor += 1
                    HP += MAX_HP // 2
                    if HP > MAX_HP:
                        HP = MAX_HP
                    if Class == "Маг":
                        Strenght += 1
                        Luck += 1
                    elif Class == "Убийца":
                        Strenght += 1
                        Skill += 1
                    elif (Class == "Воин") or (Class == "Страж"):
                        Strenght += 1
                        Endurance += 1
                else:
                    set_screen('Конец_Игры')
            else:
                i = random.randint(1, Count_Screen)
                set_screen(str(i))

    def in_leave(self):
        self.add_widget.clear_widgets()


class Molniya(Screen):
    def __init__(self, **kw):
        super(Molniya, self).__init__(**kw)

    def on_enter(self):
        Molniya = FloatLayout()
        Molniya.add_widget(Button(text="<-- В главное меню",
                                  background_color=[185 / 255, 145 / 255, 75 / 255, 1],
                                  font_size=20,
                                  color=[62 / 255, 28 / 255, 0 / 255, 1],
                                  size_hint=(.9, .1), pos=(27, 610),
                                  background_normal="", on_press=lambda x: set_screen('Главное_меню')))
        Molniya.add_widget(Label(text="Вы слышите шипящий звук неподалёку\n от вас, медленно оглядываясь\n"
                                      "вы видите маленький синий шарик...\nКажется это шаровая молния\n\n"
                                      "Стоит затаиться и надеяться на удачу\n\n",
                                 font_size=25,
                                 color=[62 / 255, 28 / 255, 0 / 255, 1]))
        Molniya.add_widget(Button(text="Продолжить",
                                  background_color=[180 / 255, 140 / 255, 75 / 255, 1],
                                  font_size=20, color=[62 / 255, 28 / 255, 0 / 255, 1], background_normal="",
                                  size_hint=(.4, .2), pos=(320, 30),
                                  on_press=self.dalee))
        Molniya.add_widget(Button(text="HP = " + str(HP),
                                  background_color=[150 / 255, 81 / 255, 69 / 255, 1],
                                  font_size=20, color=[64 / 255, 21 / 255, 21 / 255, 1], background_normal="",
                                  size_hint=(.3, .10 / 11), pos=(27, 580)))
        self.add_widget(Molniya)

    def dalee(self, event):
        global HP, Experience, LVL, Skill, Endurance, Luck, Floor, MAX_HP, Strenght
        attempt = random.randint(1, 16) + Luck
        damage = (30 + (Floor * 5))
        if attempt < 12:
            HP -= damage
            if HP <= 0:
                set_screen('Конец_Игры_Умер')
            else:
                Experience += (Luck * 2)
                if Experience >= 50 + 20 * LVL:
                    LVL += 1
                    Experience = 0
                    if LVL < 10:
                        MAX_HP += MAX_HP // 10
                        Floor += 1
                        HP += MAX_HP // 2
                        if HP > MAX_HP:
                            HP = MAX_HP
                        if Class == "Маг":
                            Strenght += 1
                            Luck += 1
                        elif Class == "Убийца":
                            Strenght += 1
                            Skill += 1
                        elif (Class == "Воин") or (Class == "Страж"):
                            Strenght += 1
                            Endurance += 1
                    else:
                        set_screen('Конец_Игры')
                else:
                    set_screen('8.1')
        else:
            Experience += (Luck * 4)
            if Experience >= 50 + 20 * LVL:
                LVL += 1
                Experience = 0
                if LVL < 10:
                    MAX_HP += MAX_HP // 10
                    Floor += 1
                    HP += MAX_HP // 2
                    if HP > MAX_HP:
                        HP = MAX_HP
                    if Class == "Маг":
                        Strenght += 1
                        Luck += 1
                    elif Class == "Убийца":
                        Strenght += 1
                        Skill += 1
                    elif (Class == "Воин") or (Class == "Страж"):
                        Strenght += 1
                        Endurance += 1
                else:
                    set_screen('Конец_Игры')
            else:
                set_screen('8.2')

    def in_leave(self):
        self.add_widget.clear_widgets()


class MolniyaON(Screen):
    def __init__(self, **kw):
        super(MolniyaON, self).__init__(**kw)

    def on_enter(self):
        Molniya = FloatLayout()
        Molniya.add_widget(Button(text="<-- В главное меню",
                                  background_color=[185 / 255, 145 / 255, 75 / 255, 1],
                                  font_size=20,
                                  color=[62 / 255, 28 / 255, 0 / 255, 1],
                                  size_hint=(.9, .1), pos=(27, 610),
                                  background_normal="", on_press=lambda x: set_screen('Главное_меню')))
        Molniya.add_widget(Label(text="К сожалению, вам не удалось скрыться\nот молнии. Впредь вам стоит быть\n"
                                      "осторожнее или.. может стоит задуматься\nоб амулетах на удачу?\n\n"
                                      "Но пора двигаться дальше\n\n"
                                      "Вы получили урон: HP - " + str((30 + (Floor * 5))) +
                                      "\nОпыт: +" + str(Luck * 2),
                                 font_size=25,
                                 color=[62 / 255, 28 / 255, 0 / 255, 1]))
        Molniya.add_widget(Button(text="Продолжить",
                                  background_color=[180 / 255, 140 / 255, 75 / 255, 1],
                                  font_size=20, color=[62 / 255, 28 / 255, 0 / 255, 1], background_normal="",
                                  size_hint=(.4, .2), pos=(320, 30),
                                  on_press=self.dalee))
        Molniya.add_widget(Button(text="HP = " + str(HP),
                                  background_color=[150 / 255, 81 / 255, 69 / 255, 1],
                                  font_size=20, color=[64 / 255, 21 / 255, 21 / 255, 1], background_normal="",
                                  size_hint=(.3, .10 / 11), pos=(27, 580)))
        self.add_widget(Molniya)

    def dalee(self, event):
        # удаляет все виджеты класса и создает новый виджет этого же класса
        self.clear_widgets()
        self.add_widget(MolniyaON())
        i = random.randint(1, Count_Screen)
        set_screen(str(i))

    def in_leave(self):
        self.add_widget.clear_widgets()


class MolniyaOFF(Screen):
    def __init__(self, **kw):
        super(MolniyaOFF, self).__init__(**kw)

    def on_enter(self):
        Molniya = FloatLayout()
        Molniya.add_widget(Button(text="<-- В главное меню",
                                  background_color=[185 / 255, 145 / 255, 75 / 255, 1],
                                  font_size=20,
                                  color=[62 / 255, 28 / 255, 0 / 255, 1],
                                  size_hint=(.9, .1), pos=(27, 610),
                                  background_normal="", on_press=lambda x: set_screen('Главное_меню')))
        Molniya.add_widget(Label(text="К счастью, вам повезло! Вам удалось\nскрыться от молнии. Что ж, и удача\n"
                                      "бывает очень полезна.. Может стоит\nподумать о ей улучшении?\n\n"
                                      "Пора двигаться дальше\n\n"
                                      "Опыт: +" + str(Luck * 4),
                                 font_size=25,
                                 color=[62 / 255, 28 / 255, 0 / 255, 1]))
        Molniya.add_widget(Button(text="Продолжить",
                                  background_color=[180 / 255, 140 / 255, 75 / 255, 1],
                                  font_size=20, color=[62 / 255, 28 / 255, 0 / 255, 1], background_normal="",
                                  size_hint=(.4, .2), pos=(320, 30),
                                  on_press=self.dalee))
        Molniya.add_widget(Button(text="HP = " + str(HP),
                                  background_color=[150 / 255, 81 / 255, 69 / 255, 1],
                                  font_size=20, color=[64 / 255, 21 / 255, 21 / 255, 1], background_normal="",
                                  size_hint=(.3, .10 / 11), pos=(27, 580)))
        self.add_widget(Molniya)

    def dalee(self, event):
        # удаляет все виджеты класса и создает новый виджет этого же класса
        self.clear_widgets()
        self.add_widget(MolniyaOFF())
        i = random.randint(1, Count_Screen)
        set_screen(str(i))

    def in_leave(self):
        self.add_widget.clear_widgets()


class Stretched_Threads(Screen):
    def __init__(self, **kw):
        super(Stretched_Threads, self).__init__(**kw)

    def on_enter(self):
        Stretched_Threads = FloatLayout()
        Stretched_Threads.add_widget(Button(text="<-- В главное меню",
                                            background_color=[185 / 255, 145 / 255, 75 / 255, 1],
                                            font_size=20,
                                            color=[62 / 255, 28 / 255, 0 / 255, 1],
                                            size_hint=(.9, .1), pos=(27, 610),
                                            background_normal="", on_press=lambda x: set_screen('Главное_меню')))
        Stretched_Threads.add_widget(Label(text="Подходя к очередной развилке вы\nостанавливаетесь, чтобы выбрать\n"
                                                "направление, однако ваши мысли прерывает\nтихий лязг, который становится\n"
                                                "всё громче.. Повернув голову напрво\nвы видите скелета, хромающего\n"
                                                "к вам. Больше нет времени думать\nи вы бежите влево..\n"
                                                "Вы добегаете до тупика, \nединственный выход из которого - \n"
                                                "пролезть через растянутые нити,\nкоторые составляют сложную\n"
                                                "паутину. Но попытаться стоит!\n\n",
                                           font_size=25,
                                           color=[62 / 255, 28 / 255, 0 / 255, 1]))
        Stretched_Threads.add_widget(Button(text="Продолжить",
                                            background_color=[180 / 255, 140 / 255, 75 / 255, 1],
                                            font_size=20, color=[62 / 255, 28 / 255, 0 / 255, 1], background_normal="",
                                            size_hint=(.4, .2), pos=(320, 30),
                                            on_press=self.dalee))
        Stretched_Threads.add_widget(Button(text="HP = " + str(HP),
                                            background_color=[150 / 255, 81 / 255, 69 / 255, 1],
                                            font_size=20, color=[64 / 255, 21 / 255, 21 / 255, 1], background_normal="",
                                            size_hint=(.3, .10 / 11), pos=(27, 580)))
        self.add_widget(Stretched_Threads)

    def dalee(self, event):
        global HP, Experience, LVL, Skill, Endurance, Luck, Floor, MAX_HP, Strenght
        attempt = random.randint(1, 30) + Skill
        damage = (35 + (Floor * 5)) - (Luck * 3)
        if attempt < 20:
            HP -= damage
            if HP <= 0:
                set_screen('Конец_Игры_Умер')
            else:
                Experience += (Skill * 1)
                if Experience >= 50 + 20 * LVL:
                    LVL += 1
                    Experience = 0
                    if LVL < 10:
                        MAX_HP += MAX_HP // 10
                        Floor += 1
                        HP += MAX_HP // 2
                        if HP > MAX_HP:
                            HP = MAX_HP
                        if Class == "Маг":
                            Strenght += 1
                            Luck += 1
                        elif Class == "Убийца":
                            Strenght += 1
                            Skill += 1
                        elif (Class == "Воин") or (Class == "Страж"):
                            Strenght += 1
                            Endurance += 1
                    else:
                        set_screen('Конец_Игры')
                else:
                    set_screen('9.1')
        else:
            Experience += (Skill * 2)
            if Experience >= 50 + 20 * LVL:
                LVL += 1
                Experience = 0
                if LVL < 10:
                    MAX_HP += MAX_HP // 10
                    Floor += 1
                    HP += MAX_HP // 2
                    if HP > MAX_HP:
                        HP = MAX_HP
                    if Class == "Маг":
                        Strenght += 1
                        Luck += 1
                    elif Class == "Убийца":
                        Strenght += 1
                        Skill += 1
                    elif (Class == "Воин") or (Class == "Страж"):
                        Strenght += 1
                        Endurance += 1
                else:
                    set_screen('Конец_Игры')
            else:
                set_screen('9.2')

    def in_leave(self):
        self.add_widget.clear_widgets()


class Stretched_ThreadsON(Screen):
    def __init__(self, **kw):
        super(Stretched_ThreadsON, self).__init__(**kw)

    def on_enter(self):
        Stretched_Threads = FloatLayout()
        Stretched_Threads.add_widget(Button(text="<-- В главное меню",
                                            background_color=[185 / 255, 145 / 255, 75 / 255, 1],
                                            font_size=20,
                                            color=[62 / 255, 28 / 255, 0 / 255, 1],
                                            size_hint=(.9, .1), pos=(27, 610),
                                            background_normal="", on_press=lambda x: set_screen('Главное_меню')))
        Stretched_Threads.add_widget(Label(text="Вы остророжно пробираетесь через\n"
                                                "эти нити. Они необычные и имеют странный\n"
                                                "синий цвет, как у тех ядовитых растений что вы\n"
                                                "видели по пути сюда.. Спустя несколько\n"
                                                "секунд, которые показались вам\nвечностью, вы всё же смогли пробраться! Но\n"
                                                "пару раз рукой вы коснулись одной из\nнитей и рука немного почернела Однако\n"
                                                "скелету, что гнался за вами повезло\nменьше. Он запутался в нитях и его\n"
                                                "кости постепенно чернели от соприкосновения.\nВы решаете, что стоит бежать отсюда!\n\n"
                                                "Вы получили урон: HP - " + str((35 + (Floor * 5)) - (Luck * 3)) +
                                                "\nОпыт: +" + str(Skill * 1),
                                           font_size=25,
                                           color=[62 / 255, 28 / 255, 0 / 255, 1]))
        Stretched_Threads.add_widget(Button(text="Продолжить",
                                            background_color=[180 / 255, 140 / 255, 75 / 255, 1],
                                            font_size=20, color=[62 / 255, 28 / 255, 0 / 255, 1], background_normal="",
                                            size_hint=(.4, .2), pos=(320, 30),
                                            on_press=self.dalee))
        Stretched_Threads.add_widget(Button(text="HP = " + str(HP),
                                            background_color=[150 / 255, 81 / 255, 69 / 255, 1],
                                            font_size=20, color=[64 / 255, 21 / 255, 21 / 255, 1], background_normal="",
                                            size_hint=(.3, .10 / 11), pos=(27, 580)))
        self.add_widget(Stretched_Threads)

    def dalee(self, event):
        # удаляет все виджеты класса и создает новый виджет этого же класса
        self.clear_widgets()
        self.add_widget(Stretched_ThreadsON())
        i = random.randint(1, Count_Screen)
        set_screen(str(i))

    def in_leave(self):
        self.add_widget.clear_widgets()


class Stretched_ThreadsOFF(Screen):
    def __init__(self, **kw):
        super(Stretched_ThreadsOFF, self).__init__(**kw)

    def on_enter(self):
        Stretched_Threads = FloatLayout()
        Stretched_Threads.add_widget(Button(text="<-- В главное меню",
                                            background_color=[185 / 255, 145 / 255, 75 / 255, 1],
                                            font_size=20,
                                            color=[62 / 255, 28 / 255, 0 / 255, 1],
                                            size_hint=(.9, .1), pos=(27, 610),
                                            background_normal="", on_press=lambda x: set_screen('Главное_меню')))
        Stretched_Threads.add_widget(Label(text="Вы остророжно пробираетесь через\n"
                                                "эти нити. Они необычные и имеют странный\n"
                                                "синий цвет, как у тех ядовитых растений что вы\n"
                                                "видели по пути сюда.. Спустя несколько\n"
                                                "секунд, которые показались вам\nвечностью, вы всё же смогли пробраться!\n"
                                                "А вот скелету, что гнался\n"
                                                "за вами не повезло.. Кости постепенно\nчернели от соприксновения\n"
                                                "а сами нити оказались достаточно\nпрочными. Но вы всё равно решили,\n"
                                                "что стоит бежать подальше отсюда!\n\n"
                                                "Опыт: +" + str(Skill * 2),
                                           font_size=25,
                                           color=[62 / 255, 28 / 255, 0 / 255, 1]))
        Stretched_Threads.add_widget(Button(text="Продолжить",
                                            background_color=[180 / 255, 140 / 255, 75 / 255, 1],
                                            font_size=20, color=[62 / 255, 28 / 255, 0 / 255, 1], background_normal="",
                                            size_hint=(.4, .2), pos=(320, 30),
                                            on_press=self.dalee))
        Stretched_Threads.add_widget(Button(text="HP = " + str(HP),
                                            background_color=[150 / 255, 81 / 255, 69 / 255, 1],
                                            font_size=20, color=[64 / 255, 21 / 255, 21 / 255, 1], background_normal="",
                                            size_hint=(.3, .10 / 11), pos=(27, 580)))
        self.add_widget(Stretched_Threads)

    def dalee(self, event):
        # удаляет все виджеты класса и создает новый виджет этого же класса
        self.clear_widgets()
        self.add_widget(Stretched_ThreadsOFF())
        i = random.randint(1, Count_Screen)
        set_screen(str(i))

    def in_leave(self):
        self.add_widget.clear_widgets()

# _____________________________________________________________________________________
# Конец ловушек
# _____________________________________________________________________________________


# _____________________________________________________________________________________
# Сундуки
# _____________________________________________________________________________________

class Syndyk1(Screen):
    def __init__(self, **kw):
        super(Syndyk1, self).__init__(**kw)

    def on_enter(self):
        Syndyk = FloatLayout()
        Syndyk.add_widget(Button(text="<-- В главное меню",
                                 background_color=[185 / 255, 145 / 255, 75 / 255, 1],
                                 font_size=20,
                                 color=[62 / 255, 28 / 255, 0 / 255, 1],
                                 size_hint=(.9, .1), pos=(27, 610),
                                 background_normal="", on_press=lambda x: set_screen('Главное_меню')))
        Syndyk.add_widget(Label(text="Переходя из одного коридора в другой,        \nвы замечаете засыпанную пылью и\n"
                                     "камнями нишу в полу. \n\n"
                                     "Подумав, что там может быть что-то\nинтересное, вы принимаетесь\n"
                                     "раскапывать яму.\n\n\n\n\n\n",
                                font_size=25,
                                color=[62 / 255, 28 / 255, 0 / 255, 1]))
        Syndyk.add_widget(Button(text="Продолжить",
                                 background_color=[180 / 255, 140 / 255, 75 / 255, 1],
                                 font_size=20, color=[62 / 255, 28 / 255, 0 / 255, 1], background_normal="",
                                 size_hint=(.4, .2), pos=(320, 30),
                                 on_press=self.proda))
        Syndyk.add_widget(Button(text="HP = " + str(HP),
                                 background_color=[150 / 255, 81 / 255, 69 / 255, 1],
                                 font_size=20, color=[64 / 255, 21 / 255, 21 / 255, 1], background_normal="",
                                 size_hint=(.3, .10 / 11), pos=(27, 580)))
        self.add_widget(Syndyk)

    def proda(self, event):
        global Trophies, Usual_healing_potion, Experience
        Trophies += 6
        Usual_healing_potion += 1
        Experience += 10
        global LVL, MAX_HP, Strenght, Skill, Luck, Floor, HP, Endurance
        if Experience >= 50 + 20 * LVL:
            LVL += 1
            Experience = 0
            if LVL < 10:
                MAX_HP += MAX_HP // 10
                Floor += 1
                HP += MAX_HP // 2
                if HP > MAX_HP:
                    HP = MAX_HP
                if Class == "Маг":
                    Strenght += 1
                    Luck += 1
                elif Class == "Убийца":
                    Strenght += 1
                    Skill += 1
                elif (Class == "Воин") or (Class == "Страж"):
                    Strenght += 1
                    Endurance += 1
            else:
                set_screen('Конец_Игры')
        else:
            set_screen("3.2")

    def in_leave(self):
        self.add_widget.clear_widgets()


class Syndyk2(Screen):
    def __init__(self, **kw):
        super(Syndyk2, self).__init__(**kw)

    def on_enter(self):
        Syndyk = FloatLayout()
        Syndyk.add_widget(Button(text="<-- В главное меню",
                                 background_color=[185 / 255, 145 / 255, 75 / 255, 1],
                                 font_size=20,
                                 color=[62 / 255, 28 / 255, 0 / 255, 1],
                                 size_hint=(.9, .1), pos=(27, 610),
                                 background_normal="", on_press=lambda x: set_screen('Главное_меню')))
        Syndyk.add_widget(Label(text="Заметив железный блеск отделки\nсундука, вы начали копать активнее\n"
                                     "и уже через минуту вы вытаскиваете           \nна поверхность дубовый сундук!\n\n"
                                     "Открыв его, вы обнаруживаете:\n\n"
                                     "Простое зелье лечения - 1 штука\nТрофеи - 6 штук\n\n"
                                     "Опыт + 10\n\n\n",
                                font_size=25,
                                color=[62 / 255, 28 / 255, 0 / 255, 1]))
        Syndyk.add_widget(Button(text="Продолжить",
                                 background_color=[180 / 255, 140 / 255, 75 / 255, 1],
                                 font_size=20, color=[62 / 255, 28 / 255, 0 / 255, 1], background_normal="",
                                 size_hint=(.4, .2), pos=(320, 30),
                                 on_press=self.dalee))
        Syndyk.add_widget(Button(text="HP = " + str(HP),
                                 background_color=[150 / 255, 81 / 255, 69 / 255, 1],
                                 font_size=20, color=[64 / 255, 21 / 255, 21 / 255, 1], background_normal="",
                                 size_hint=(.3, .10 / 11), pos=(27, 580)))
        self.add_widget(Syndyk)

    def dalee(self, event):
        a = random.randint(1, 10)
        if a <= 4:
            set_screen('Моб')
        else:
            i = random.randint(1, Count_Screen)
            set_screen(str(i))

    def in_leave(self):
        self.add_widget.clear_widgets()


class Syndyk3(Screen):
    def __init__(self, **kw):
        super(Syndyk3, self).__init__(**kw)

    def on_enter(self):
        Syndyk = FloatLayout()
        Syndyk.add_widget(Button(text="<-- В главное меню",
                                 background_color=[185 / 255, 145 / 255, 75 / 255, 1],
                                 font_size=20,
                                 color=[62 / 255, 28 / 255, 0 / 255, 1],
                                 size_hint=(.9, .1), pos=(27, 610),
                                 background_normal="", on_press=lambda x: set_screen('Главное_меню')))
        Syndyk.add_widget(Label(text="Вы уже доволно много времени\nбродите в пещерах в поисках материалов\n"
                                     "для вашего оружия и брони, ведь\nпытаться выбраться без оружия - \n"
                                     "заранее обречь себя на смерть.\n\n"
                                     "Вы видите небольшую расщелину в стене,\nкуда с трудом могли бы пролезть.\n"
                                     "Но почему бы не попытаться?\nГлавное, чтобы это не было логовом\n"
                                     "враждебно настроенного существа.\n\n\n\n",
                                font_size=25,
                                color=[62 / 255, 28 / 255, 0 / 255, 1]))
        Syndyk.add_widget(Button(text="Продолжить",
                                 background_color=[180 / 255, 140 / 255, 75 / 255, 1],
                                 font_size=20, color=[62 / 255, 28 / 255, 0 / 255, 1], background_normal="",
                                 size_hint=(.4, .2), pos=(320, 30),
                                 on_press=self.proda))
        Syndyk.add_widget(Button(text="HP = " + str(HP),
                                 background_color=[150 / 255, 81 / 255, 69 / 255, 1],
                                 font_size=20, color=[64 / 255, 21 / 255, 21 / 255, 1], background_normal="",
                                 size_hint=(.3, .10 / 11), pos=(27, 580)))
        self.add_widget(Syndyk)

    def proda(self, event):
        global Trophies, Experience, Floor, boots_leather, boots_cloth, boots_epic
        if Floor < 4:
            boots_leather += 1
        elif (Floor > 3) and (Floor < 8):
            boots_cloth += 1
        elif Floor > 7:
            boots_epic += 1
        Trophies += 6 + Floor
        Experience += 8 + (Floor * 2)
        global LVL, MAX_HP, Strenght, Skill, Luck, HP, Endurance
        if Experience >= 50 + 20 * LVL:
            LVL += 1
            Experience = 0
            if LVL < 10:
                MAX_HP += MAX_HP // 10
                Floor += 1
                HP += MAX_HP // 2
                if HP > MAX_HP:
                    HP = MAX_HP
                if Class == "Маг":
                    Strenght += 1
                    Luck += 1
                elif Class == "Убийца":
                    Strenght += 1
                    Skill += 1
                elif (Class == "Воин") or (Class == "Страж"):
                    Strenght += 1
                    Endurance += 1
            else:
                set_screen('Конец_Игры')
        else:
            set_screen("16.1")

    def in_leave(self):
        self.add_widget.clear_widgets()


class Syndyk3_2(Screen):
    def __init__(self, **kw):
        super(Syndyk3_2, self).__init__(**kw)

    def on_enter(self):
        if Floor < 4:
            predmet = "Лёгкие сапоги"
        elif (Floor > 3) and (Floor < 8):
            predmet = "Кожаные сапоги"
        elif Floor > 7:
            predmet = "Сапоги из лозы"
        Syndyk = FloatLayout()
        Syndyk.add_widget(Button(text="<-- В главное меню",
                                 background_color=[185 / 255, 145 / 255, 75 / 255, 1],
                                 font_size=20,
                                 color=[62 / 255, 28 / 255, 0 / 255, 1],
                                 size_hint=(.9, .1), pos=(27, 610),
                                 background_normal="", on_press=lambda x: set_screen('Главное_меню')))
        Syndyk.add_widget(Label(text="Пройдя сквозь трещину в стене, вы\nвыходите в небольшую комнату двухметровой\n"
                                     "длины. Ближе к дальнему краю в кучке\nсложены вещи."
                                     "\nВы подходите, чтобы получше разглядеть"
                                     "\nих и обнаруживаете:\n\n"
                                     "Предмет: " + str(predmet) +
                                     "\nТрофеи +" + str((6 + Floor)) +
                                     "\nОпыт +" + str((8 + (Floor * 2))) + "\n\n"
                                                                           "Забрав вещи вы спешно покидаете комнату.\n\n",
                                font_size=25,
                                color=[62 / 255, 28 / 255, 0 / 255, 1]))
        Syndyk.add_widget(Button(text="Продолжить\nне надевая",
                                    background_color=[180 / 255, 140 / 255, 75 / 255, 1],
                                    font_size=20, color=[62 / 255, 28 / 255, 0 / 255, 1], background_normal="",
                                    size_hint=(.4, .2), pos=(320, 30),
                                    on_press=self.dalee))
        Syndyk.add_widget(Button(text="Надеть\nсапоги",
                                    background_color=[180 / 255, 140 / 255, 75 / 255, 1],
                                    font_size=20, color=[62 / 255, 28 / 255, 0 / 255, 1], background_normal="",
                                    size_hint=(.4, .2), pos=(40, 30),
                                    on_press=self.equipment))
        Syndyk.add_widget(Button(text="HP = " + str(HP),
                                 background_color=[150 / 255, 81 / 255, 69 / 255, 1],
                                 font_size=20, color=[64 / 255, 21 / 255, 21 / 255, 1], background_normal="",
                                 size_hint=(.3, .10 / 11), pos=(27, 580)))
        self.add_widget(Syndyk)

    def equipment(self, event):
        # удаляет все виджеты класса и создает новый виджет этого же класса
        self.clear_widgets()
        self.add_widget(Syndyk3_2())
        set_screen('Экипировка_предмета')
    def dalee(self, event):
        # удаляет все виджеты класса и создает новый виджет этого же класса
        self.clear_widgets()
        self.add_widget(Syndyk3_2())
        a = random.randint(1, 10)
        if a <= 8:
            set_screen('Моб')
        else:
            i = random.randint(1, Count_Screen)
            set_screen(str(i))

    def in_leave(self):
        self.add_widget.clear_widgets()


class Syndyk4(Screen):
    def __init__(self, **kw):
        super(Syndyk4, self).__init__(**kw)

    def on_enter(self):
        if Floor < 4:
            predmet = "Простое ожерелье"
        elif (Floor > 3) and (Floor < 8):
            predmet = "Ожерелье из малых кристаллов"
        elif Floor > 7:
            predmet = "Ожерелье из драгоценных камней"
        Syndyk = FloatLayout()
        Syndyk.add_widget(Button(text="<-- В главное меню",
                                 background_color=[185 / 255, 145 / 255, 75 / 255, 1],
                                 font_size=20,
                                 color=[62 / 255, 28 / 255, 0 / 255, 1],
                                 size_hint=(.9, .1), pos=(27, 610),
                                 background_normal="", on_press=lambda x: set_screen('Главное_меню')))
        Syndyk.add_widget(Label(text="После очередной погони от монстра\nвы стараетесь найти как можно более\n"
                                     "спокойное место. Но пока что вам\nпопадаются лишь перекрёстки тоннелей,\n"
                                     "в которых не безопасно будет оставаться\nдля отдыха.\n"
                                     "Вдруг от одной из стен вы улавливаете\nотблеск света. Надеясь, что это не\n"
                                     "что-нибудь опасное, вы осторожно\nподходите ближе.\n\n"
                                     "Вы обнаружили: "+str(predmet)+"\nОпыт +"+str((11 + (Floor * 2)))+"\n\n",
                                font_size=25,
                                color=[62 / 255, 28 / 255, 0 / 255, 1]))
        Syndyk.add_widget(Button(text="Продолжить\nне надевая",
                                    background_color=[180 / 255, 140 / 255, 75 / 255, 1],
                                    font_size=20, color=[62 / 255, 28 / 255, 0 / 255, 1], background_normal="",
                                    size_hint=(.4, .2), pos=(320, 30),
                                    on_press=self.proda))
        Syndyk.add_widget(Button(text="Надеть\nожерелье",
                                    background_color=[180 / 255, 140 / 255, 75 / 255, 1],
                                    font_size=20, color=[62 / 255, 28 / 255, 0 / 255, 1], background_normal="",
                                    size_hint=(.4, .2), pos=(40, 30),
                                    on_press=self.equipment))
        Syndyk.add_widget(Button(text="HP = " + str(HP),
                                 background_color=[150 / 255, 81 / 255, 69 / 255, 1],
                                 font_size=20, color=[64 / 255, 21 / 255, 21 / 255, 1], background_normal="",
                                 size_hint=(.3, .10 / 11), pos=(27, 580)))
        self.add_widget(Syndyk)

    def equipment(self, event):
        # удаляет все виджеты класса и создает новый виджет этого же класса
        self.clear_widgets()
        self.add_widget(Syndyk4())
        global Trophies, Experience, Floor, necklace_leather, necklace_cloth, necklace_epic
        if Floor < 4:
            necklace_leather += 1
        elif (Floor > 3) and (Floor < 8):
            necklace_cloth += 1
        elif Floor > 7:
            necklace_epic += 1
        Experience += 11 + (Floor * 2)
        global LVL, MAX_HP, Strenght, Skill, Luck, HP, Endurance
        if Experience >= 50 + 20 * LVL:
            LVL += 1
            Experience = 0
            if LVL < 10:
                MAX_HP += MAX_HP // 10
                Floor += 1
                HP += MAX_HP // 2
                if HP > MAX_HP:
                    HP = MAX_HP
                if Class == "Маг":
                    Strenght += 1
                    Luck += 1
                elif Class == "Убийца":
                    Strenght += 1
                    Skill += 1
                elif (Class == "Воин") or (Class == "Страж"):
                    Strenght += 1
                    Endurance += 1
            else:
                set_screen('Конец_Игры')
        else:
            set_screen('Экипировка_предмета')
    def proda(self, event):
        # удаляет все виджеты класса и создает новый виджет этого же класса
        self.clear_widgets()
        self.add_widget(Syndyk4())
        global Trophies, Experience, Floor, necklace_leather, necklace_cloth, necklace_epic
        if Floor < 4:
            necklace_leather += 1
        elif (Floor > 3) and (Floor < 8):
            necklace_cloth += 1
        elif Floor > 7:
            necklace_epic += 1
        Experience += 11 + (Floor * 2)
        global LVL, MAX_HP, Strenght, Skill, Luck, HP, Endurance
        if Experience >= 50 + 20 * LVL:
            LVL += 1
            Experience = 0
            if LVL < 10:
                MAX_HP += MAX_HP // 10
                Floor += 1
                HP += MAX_HP // 2
                if HP > MAX_HP:
                    HP = MAX_HP
                if Class == "Маг":
                    Strenght += 1
                    Luck += 1
                elif Class == "Убийца":
                    Strenght += 1
                    Skill += 1
                elif (Class == "Воин") or (Class == "Страж"):
                    Strenght += 1
                    Endurance += 1
            else:
                set_screen('Конец_Игры')
        else:
            i = random.randint(1, Count_Screen)
            set_screen(str(i))

    def in_leave(self):
        self.add_widget.clear_widgets()


class Syndyk5(Screen):
    def __init__(self, **kw):
        super(Syndyk5, self).__init__(**kw)

    def on_enter(self):
        if Floor < 4:
            predmet = "Лёгкие шлем"
        elif (Floor > 3) and (Floor < 8):
            predmet = "Кожаный шлем"
        elif Floor > 7:
            predmet = "Шлем из лозы"
        Syndyk = FloatLayout()
        Syndyk.add_widget(Button(text="<-- В главное меню",
                                 background_color=[185 / 255, 145 / 255, 75 / 255, 1],
                                 font_size=20,
                                 color=[62 / 255, 28 / 255, 0 / 255, 1],
                                 size_hint=(.9, .1), pos=(27, 610),
                                 background_normal="", on_press=lambda x: set_screen('Главное_меню')))
        Syndyk.add_widget(Label(text="Сворачивая за угол, вы резко отпрыгнули\nназад, увидев скелета с топором.\n"
                                     "Однако уже спустя секунду поняли, что\nэто не монстр, а труп существа.\n\n"
                                     "Подойдя поближе вы обнаруживаете, что\nкто-то его уже обыскивал и ценных\n"
                                     "вещей у него больше не осталось..\nХотя шлем вам всё же приглянулся.\n\n"
                                     "Получен: "+str(predmet)+"\nОпыт +"+str((8 + Endurance))+
                                     "\nТрофеи +"+str((5 + Floor))+"\n\n",
                                font_size=25,
                                color=[62 / 255, 28 / 255, 0 / 255, 1]))
        Syndyk.add_widget(Button(text="Продолжить\nне надевая",
                                    background_color=[180 / 255, 140 / 255, 75 / 255, 1],
                                    font_size=20, color=[62 / 255, 28 / 255, 0 / 255, 1], background_normal="",
                                    size_hint=(.4, .2), pos=(320, 30),
                                    on_press=self.proda))
        Syndyk.add_widget(Button(text="Надеть\n шлем",
                                    background_color=[180 / 255, 140 / 255, 75 / 255, 1],
                                    font_size=20, color=[62 / 255, 28 / 255, 0 / 255, 1], background_normal="",
                                    size_hint=(.4, .2), pos=(40, 30),
                                    on_press=self.equipment))
        Syndyk.add_widget(Button(text="HP = " + str(HP),
                                 background_color=[150 / 255, 81 / 255, 69 / 255, 1],
                                 font_size=20, color=[64 / 255, 21 / 255, 21 / 255, 1], background_normal="",
                                 size_hint=(.3, .10 / 11), pos=(27, 580)))
        self.add_widget(Syndyk)

    def equipment(self, event):
        # удаляет все виджеты класса и создает новый виджет этого же класса
        self.clear_widgets()
        self.add_widget(Syndyk5())
        global Trophies, Experience, Floor, helmet_leather, helmet_cloth, helmet_epic, Endurance
        if Floor < 4:
            helmet_leather += 1
        elif (Floor > 3) and (Floor < 8):
            helmet_cloth += 1
        elif Floor > 7:
            helmet_epic += 1
        Trophies += 5 + Floor
        Experience += 8 + Endurance
        global LVL, MAX_HP, Strenght, Skill, Luck, HP
        if Experience >= 50 + 20 * LVL:
            LVL += 1
            Experience = 0
            if LVL < 10:
                MAX_HP += MAX_HP // 10
                Floor += 1
                HP += MAX_HP // 2
                if HP > MAX_HP:
                    HP = MAX_HP
                if Class == "Маг":
                    Strenght += 1
                    Luck += 1
                elif Class == "Убийца":
                    Strenght += 1
                    Skill += 1
                elif (Class == "Воин") or (Class == "Страж"):
                    Strenght += 1
                    Endurance += 1
            else:
                set_screen('Конец_Игры')
        else:
            set_screen('Экипировка_предмета')
    def proda(self, event):
        # удаляет все виджеты класса и создает новый виджет этого же класса
        self.clear_widgets()
        self.add_widget(Syndyk5())
        global Trophies, Experience, Floor, helmet_leather, helmet_cloth, helmet_epic, Endurance
        if Floor < 4:
            helmet_leather += 1
        elif (Floor > 3) and (Floor < 8):
            helmet_cloth += 1
        elif Floor > 7:
            helmet_epic += 1
        Trophies += 5 + Floor
        Experience += 8 + Endurance
        global LVL, MAX_HP, Strenght, Skill, Luck, HP
        if Experience >= 50 + 20 * LVL:
            LVL += 1
            Experience = 0
            if LVL < 10:
                MAX_HP += MAX_HP // 10
                Floor += 1
                HP += MAX_HP // 2
                if HP > MAX_HP:
                    HP = MAX_HP
                if Class == "Маг":
                    Strenght += 1
                    Luck += 1
                elif Class == "Убийца":
                    Strenght += 1
                    Skill += 1
                elif (Class == "Воин") or (Class == "Страж"):
                    Strenght += 1
                    Endurance += 1
            else:
                set_screen('Конец_Игры')
        else:
            i = random.randint(1, Count_Screen)
            set_screen(str(i))

    def in_leave(self):
        self.add_widget.clear_widgets()


class Syndyk6(Screen):
    def __init__(self, **kw):
        super(Syndyk6, self).__init__(**kw)

    def on_enter(self):
        Syndyk = FloatLayout()
        Syndyk.add_widget(Button(text="<-- В главное меню",
                                 background_color=[185 / 255, 145 / 255, 75 / 255, 1],
                                 font_size=20,
                                 color=[62 / 255, 28 / 255, 0 / 255, 1],
                                 size_hint=(.9, .1), pos=(27, 610),
                                 background_normal="", on_press=lambda x: set_screen('Главное_меню')))
        Syndyk.add_widget(Label(text="Тихо прокрадываясь вдоль стены,\nвы прислушиваетесь к каждому шороху.\n"
                                     "Однако ваша невнимательность заставила\nсработать одну из нажимных плит, что\n"
                                     "прятались в стене.\n\nВы, стараясь почти не дышать,\nаккуратно оборачиваетесь, чтобы\n"
                                     "посмотреть на неё. Немного разбираясь\nв устройствах ловушек, вы решаете\n"
                                     "резко отпрыгнуть от стены.\n\n\n\n",
                                font_size=25,
                                color=[62 / 255, 28 / 255, 0 / 255, 1]))
        Syndyk.add_widget(Button(text="Продолжить",
                                 background_color=[180 / 255, 140 / 255, 75 / 255, 1],
                                 font_size=20, color=[62 / 255, 28 / 255, 0 / 255, 1], background_normal="",
                                 size_hint=(.4, .2), pos=(320, 30),
                                 on_press=self.proda))
        Syndyk.add_widget(Button(text="HP = " + str(HP),
                                 background_color=[150 / 255, 81 / 255, 69 / 255, 1],
                                 font_size=20, color=[64 / 255, 21 / 255, 21 / 255, 1], background_normal="",
                                 size_hint=(.3, .10 / 11), pos=(27, 580)))
        self.add_widget(Syndyk)

    def proda(self, event):
        global Trophies, Experience, Floor, weapon_leather, weapon_cloth, weapon_epic, Luck
        if Floor < 4:
            weapon_leather += 1
        elif (Floor > 3) and (Floor < 8):
            weapon_cloth += 1
        elif Floor > 7:
            weapon_epic += 1
        Experience += 8 + (Luck * 2)
        global LVL, MAX_HP, Strenght, Skill, HP, Endurance
        if Experience >= 50 + 20 * LVL:
            LVL += 1
            Experience = 0
            if LVL < 10:
                MAX_HP += MAX_HP // 10
                Floor += 1
                HP += MAX_HP // 2
                if HP > MAX_HP:
                    HP = MAX_HP
                if Class == "Маг":
                    Strenght += 1
                    Luck += 1
                elif Class == "Убийца":
                    Strenght += 1
                    Skill += 1
                elif (Class == "Воин") or (Class == "Страж"):
                    Strenght += 1
                    Endurance += 1
            else:
                set_screen('Конец_Игры')
        else:
            set_screen("19.1")

    def in_leave(self):
        self.add_widget.clear_widgets()


class Syndyk6_2(Screen):
    def __init__(self, **kw):
        super(Syndyk6_2, self).__init__(**kw)

    def on_enter(self):
        if Floor < 4:
            predmet = "Обычный клинок"
        elif (Floor > 3) and (Floor < 8):
            predmet = "Оружие из прочного железа"
        elif Floor > 7:
            predmet = "Стальной меч"
        Syndyk = FloatLayout()
        Syndyk.add_widget(Button(text="<-- В главное меню",
                                 background_color=[185 / 255, 145 / 255, 75 / 255, 1],
                                 font_size=20,
                                 color=[62 / 255, 28 / 255, 0 / 255, 1],
                                 size_hint=(.9, .1), pos=(27, 610),
                                 background_normal="", on_press=lambda x: set_screen('Главное_меню')))
        Syndyk.add_widget(Label(text="К вашему удивлению, из противоположной\nстены не вылетела ни одна стрела\n"
                                     "Вы ещё раз смотрите на нажимную плиту\nи видите на её месте небольшую нишу.\n"
                                     "Осторожно подойдя чуть ближе, вы видите\nнебольшое оружие.\n\n"
                                     "Вы получили: " + str(predmet) +
                                     "\nОпыт +" + str((8 + (Luck * 2))) + "\n\n"
                                    "Забрав оружие, вы быстро\nуходите отсюда.\n\n",
                                font_size=25,
                                color=[62 / 255, 28 / 255, 0 / 255, 1]))
        Syndyk.add_widget(Button(text="Продолжить\nне надевая",
                                    background_color=[180 / 255, 140 / 255, 75 / 255, 1],
                                    font_size=20, color=[62 / 255, 28 / 255, 0 / 255, 1], background_normal="",
                                    size_hint=(.4, .2), pos=(320, 30),
                                    on_press=self.dalee))
        Syndyk.add_widget(Button(text="Экипировать\n  оружие",
                                    background_color=[180 / 255, 140 / 255, 75 / 255, 1],
                                    font_size=20, color=[62 / 255, 28 / 255, 0 / 255, 1], background_normal="",
                                    size_hint=(.4, .2), pos=(40, 30),
                                    on_press=self.equipment))
        Syndyk.add_widget(Button(text="HP = " + str(HP),
                                 background_color=[150 / 255, 81 / 255, 69 / 255, 1],
                                 font_size=20, color=[64 / 255, 21 / 255, 21 / 255, 1], background_normal="",
                                 size_hint=(.3, .10 / 11), pos=(27, 580)))
        self.add_widget(Syndyk)

    def equipment(self, event):
        # удаляет все виджеты класса и создает новый виджет этого же класса
        self.clear_widgets()
        self.add_widget(Syndyk6_2())
        set_screen('Экипировка_предмета')
    def dalee(self, event):
        # удаляет все виджеты класса и создает новый виджет этого же класса
        self.clear_widgets()
        self.add_widget(Syndyk6_2())
        a = random.randint(1, 10)
        if a <= 5:
            set_screen('Моб')
        else:
            i = random.randint(1, Count_Screen)
            set_screen(str(i))

    def in_leave(self):
        self.add_widget.clear_widgets()

# _____________________________________________________________________________________
# Конец сундуков
# _____________________________________________________________________________________


# _____________________________________________________________________________________
# Начало блока сражения с монстрами
# _____________________________________________________________________________________


class Predislovie(Screen):
    def __init__(self, **kw):
        super(Predislovie, self).__init__(**kw)

    def on_enter(self):
        Stretched_Threads = FloatLayout()
        Stretched_Threads.add_widget(Button(text="<-- В главное меню",
                                            background_color=[185 / 255, 145 / 255, 75 / 255, 1],
                                            font_size=20,
                                            color=[62 / 255, 28 / 255, 0 / 255, 1],
                                            size_hint=(.9, .1), pos=(27, 610),
                                            background_normal="", on_press=lambda x: set_screen('Главное_меню')))
        Stretched_Threads.add_widget(Label(text="Подходя к очередной развилке вы\nостанавливаетесь, чтобы выбрать\n"
                                                "направление, однако ваши мысли прерывает\nнебольшой шум, который становится\n"
                                                "всё громче.. Повернув голову напрво\nвы видите фигуру, хромающюю\n"
                                                "к вам. Больше нет времени думать\nи вы бежите влево..\n"
                                                "Вы добегаете до тупика, \nединственный выход из которого - \n"
                                                "пролезть через растянутые нити,\nкоторые составляют сложную\n"
                                                "паутину. Пора готовиться к бою.\n\n",
                                           font_size=25,
                                           color=[62 / 255, 28 / 255, 0 / 255, 1]))
        Stretched_Threads.add_widget(Button(text="Продолжить",
                                            background_color=[180 / 255, 140 / 255, 75 / 255, 1],
                                            font_size=20, color=[62 / 255, 28 / 255, 0 / 255, 1], background_normal="",
                                            size_hint=(.4, .2), pos=(320, 30),
                                            on_press=self.dalee))
        Stretched_Threads.add_widget(Button(text="HP = " + str(HP),
                                            background_color=[150 / 255, 81 / 255, 69 / 255, 1],
                                            font_size=20, color=[64 / 255, 21 / 255, 21 / 255, 1], background_normal="",
                                            size_hint=(.3, .10 / 11), pos=(27, 580)))
        self.add_widget(Stretched_Threads)

    def dalee(self, event):
        set_screen('Моб')

    def in_leave(self):
        self.add_widget.clear_widgets()

class Predislovie2(Screen):
    def __init__(self, **kw):
        super(Predislovie2, self).__init__(**kw)

    def on_enter(self):
        Stretched_Threads = FloatLayout()
        Stretched_Threads.add_widget(Button(text="<-- В главное меню",
                                            background_color=[185 / 255, 145 / 255, 75 / 255, 1],
                                            font_size=20,
                                            color=[62 / 255, 28 / 255, 0 / 255, 1],
                                            size_hint=(.9, .1), pos=(27, 610),
                                            background_normal="", on_press=lambda x: set_screen('Главное_меню')))
        Stretched_Threads.add_widget(Label(text="Вы уже несколько часов бродите\nв поисках чего-нибудь съестного,\n"
                                                "но пока что вам не везёт.\nНа новой развилке вы решили пойти\n"
                                                "направо, но это было не лучшим\nрешением.\n\nСпустя пятьсот метров\n"
                                                "вы замечаете странную фигуру..\nА она замечает вас.\n\n"
                                                "Кажется, вам пора бежать!\n\n\n",
                                           font_size=25,
                                           color=[62 / 255, 28 / 255, 0 / 255, 1]))
        Stretched_Threads.add_widget(Button(text="Продолжить",
                                            background_color=[180 / 255, 140 / 255, 75 / 255, 1],
                                            font_size=20, color=[62 / 255, 28 / 255, 0 / 255, 1], background_normal="",
                                            size_hint=(.4, .2), pos=(320, 30),
                                            on_press=self.dalee))
        Stretched_Threads.add_widget(Button(text="HP = " + str(HP),
                                            background_color=[150 / 255, 81 / 255, 69 / 255, 1],
                                            font_size=20, color=[64 / 255, 21 / 255, 21 / 255, 1], background_normal="",
                                            size_hint=(.3, .10 / 11), pos=(27, 580)))
        self.add_widget(Stretched_Threads)

    def dalee(self, event):
        set_screen('Моб')

    def in_leave(self):
        self.add_widget.clear_widgets()

class Predislovie3(Screen):
    def __init__(self, **kw):
        super(Predislovie3, self).__init__(**kw)

    def on_enter(self):
        Stretched_Threads = FloatLayout()
        Stretched_Threads.add_widget(Button(text="<-- В главное меню",
                                            background_color=[185 / 255, 145 / 255, 75 / 255, 1],
                                            font_size=20,
                                            color=[62 / 255, 28 / 255, 0 / 255, 1],
                                            size_hint=(.9, .1), pos=(27, 610),
                                            background_normal="", on_press=lambda x: set_screen('Главное_меню')))
        Stretched_Threads.add_widget(Label(text="Вы вышли к большой пещере,\nв центре которой переливается бликами\n"
                                                "кристально чистое подземное озеро.\nВы уже очень давно не отдыхали\n"
                                                "и вам стоит поспать.\n\nНо не успели вы заснуть, как\n"
                                                "услышали, что кто-то тихонько\nподбирается к вам!\n\n"
                                                "Похоже, отдохнуть не получится.\n\n\n",
                                           font_size=25,
                                           color=[62 / 255, 28 / 255, 0 / 255, 1]))
        Stretched_Threads.add_widget(Button(text="Продолжить",
                                            background_color=[180 / 255, 140 / 255, 75 / 255, 1],
                                            font_size=20, color=[62 / 255, 28 / 255, 0 / 255, 1], background_normal="",
                                            size_hint=(.4, .2), pos=(320, 30),
                                            on_press=self.dalee))
        Stretched_Threads.add_widget(Button(text="HP = " + str(HP),
                                            background_color=[150 / 255, 81 / 255, 69 / 255, 1],
                                            font_size=20, color=[64 / 255, 21 / 255, 21 / 255, 1], background_normal="",
                                            size_hint=(.3, .10 / 11), pos=(27, 580)))
        self.add_widget(Stretched_Threads)

    def dalee(self, event):
        set_screen('Моб')

    def in_leave(self):
        self.add_widget.clear_widgets()


class Mob(Screen):
    def __init__(self, **kw):
        super(Mob, self).__init__(**kw)

    def on_enter(self):
        a = random.randint(1, 30)
        global mob, HP_mob, Name_Mob
        if a < 15:
            mob = "Обычный"
            HP_mob = HP_normal_monster
        elif a < 23:
            mob = "Сильный"
            HP_mob = HP_average_monster
        elif a >=23:
            mob = "Элитный"
            HP_mob = HP_elite_monster
        Name_Mob = random.choice(list)
        Stretched_Threads = FloatLayout()
        Stretched_Threads.add_widget(Label(text="Перед вами "+str(Name_Mob)+"\nРанг монстра: "+str(mob)+"\n"
                                            "HP монстра: "+str(HP_mob)+"\n\n"
                                            "Надеюсь, вам удасться победить монстра\nи не умереть самому..\n\n"
                                            "Ваши характеристики:\nЛовкость - "+str(Skill)+"\nСила - "+str(Strenght)+
                                           "\nВыносливость - "+str(Endurance)+"\nУдача - "+str(Luck)+"\n\n",
                                           font_size=25,
                                           color=[62 / 255, 28 / 255, 0 / 255, 1]))
        Stretched_Threads.add_widget(Button(text="Продолжить",
                                            background_color=[180 / 255, 140 / 255, 75 / 255, 1],
                                            font_size=20, color=[62 / 255, 28 / 255, 0 / 255, 1], background_normal="",
                                            size_hint=(.4, .2), pos=(320, 30),
                                            on_press=self.dalee))
        Stretched_Threads.add_widget(Button(text="HP = " + str(HP),
                                            background_color=[150 / 255, 81 / 255, 69 / 255, 1],
                                            font_size=20, color=[64 / 255, 21 / 255, 21 / 255, 1], background_normal="",
                                            size_hint=(.3, .10 / 11), pos=(40, 600)))
        self.add_widget(Stretched_Threads)

    def dalee(self, event):
        # удаляет все виджеты класса и создает новый виджет этого же класса
        self.clear_widgets()
        self.add_widget(Mob())
        global Class, damage_from_monster
        if mob == "Обычный":
            damage_from_monster = (random.randint(10, 15) * k + (Floor * 2)) // Endurance  # Урон от обычного монстра
        elif mob == "Сильный":
            damage_from_monster = (random.randint(17, 22) * k + (Floor * 2)) // Endurance  # Урон от среднего монстра
        elif mob == "Элитный":
            damage_from_monster = (random.randint(27, 33) * k + (Floor * 2)) // Endurance  # Урон от элитного монстра
        if Class == "Маг":
            set_screen('Бой_мага')
        elif Class == "Убийца":
            set_screen('Бой_убийцы')
        elif Class == "Воин":
            set_screen('Бой_воина')
        elif Class == "Страж":
            set_screen('Бой_стража')

    def in_leave(self):
        self.add_widget.clear_widgets()


class Battle_Assasin(Screen):
    def __init__(self, **kw):
        super(Battle_Assasin, self).__init__(**kw)

    def on_enter(self):
        global mob, HP_mob, Name_Mob
        Battle_Assasin = FloatLayout()
        Battle_Assasin.add_widget(Label(text=str(Name_Mob)+"     ранг: "+str(mob)+"\n\n\n\n\n"
                                            "                    \n\n\n\n\n\n\n\n\n\n\n\n\n",
                                           font_size=25,
                                           color=[62 / 255, 28 / 255, 0 / 255, 1]))
        Battle_Assasin.add_widget(Button(text="Удар в спину",
                                    background_color=[180 / 255, 140 / 255, 75 / 255, 1],
                                    font_size=20, color=[62 / 255, 28 / 255, 0 / 255, 1], background_normal="",
                                    size_hint=(.4, .2), pos=(40, 210),
                                    on_press=self.Удар_в_спину))
        Battle_Assasin.add_widget(Button(text="Сбежать",
                                    background_color=[180 / 255, 140 / 255, 75 / 255, 1],
                                    font_size=20, color=[62 / 255, 28 / 255, 0 / 255, 1], background_normal="",
                                    size_hint=(.4, .2), pos=(310, 55),
                                    on_press=self.Сбежать))
        Battle_Assasin.add_widget(Button(text="Выпить зелье",
                                    background_color=[180 / 255, 140 / 255, 75 / 255, 1],
                                    font_size=20, color=[62 / 255, 28 / 255, 0 / 255, 1], background_normal="",
                                    size_hint=(.4, .2), pos=(40, 55),
                                    on_press=self.Выпить_зелье))
        Battle_Assasin.add_widget(Button(text="Колющий удар",
                                    background_color=[180 / 255, 140 / 255, 75 / 255, 1],
                                    font_size=20, color=[62 / 255, 28 / 255, 0 / 255, 1], background_normal="",
                                    size_hint=(.4, .2), pos=(310, 210),
                                    on_press=self.Колющий_удар))
        Battle_Assasin.add_widget(Button(text="Ваше HP = " + str(HP),
                                            background_color=[150 / 255, 81 / 255, 69 / 255, 1],
                                            font_size=20, color=[64 / 255, 21 / 255, 21 / 255, 1], background_normal="",
                                            size_hint=(.4, .1), pos=(40, 460)))
        Battle_Assasin.add_widget(Button(text="HP монстра = " + str(HP_mob),
                                         background_color=[150 / 255, 81 / 255, 69 / 255, 1],
                                         font_size=20, color=[64 / 255, 21 / 255, 21 / 255, 1], background_normal="",
                                         size_hint=(.4, .1), pos=(40, 380)))
        self.add_widget(Battle_Assasin)

    def Сбежать(self, event):
        # удаляет все виджеты класса и создает новый виджет этого же класса
        self.clear_widgets()
        self.add_widget(Battle_Assasin())
        s = random.randint(1, 35) + Skill + Luck
        if s > 30:
            i = random.randint(1, Count_Screen)
            set_screen(str(i))
        else:
            global HP, damage_from_monster
            HP -= damage_from_monster
            if HP <= 0:
                set_screen('Конец_Игры_Умер')
            else:
                set_screen('Не_сбежал_убийца')
    def Удар_в_спину(self, event):
        # удаляет все виджеты класса и создает новый виджет этого же класса
        self.clear_widgets()
        self.add_widget(Battle_Assasin())
        global HP, damage_from_monster, HP_mob
        HP_mob -= (4 * Skill) + Strenght
        if HP_mob <= 0:
            set_screen('Вы_победили')
        else:
            HP -= damage_from_monster
            if HP <= 0:
                set_screen('Конец_Игры_Умер')
            else:
                set_screen('Вы_нанесли_удар_убийца')
    def Выпить_зелье(self, event):
        # удаляет все виджеты класса и создает новый виджет этого же класса
        self.clear_widgets()
        self.add_widget(Battle_Assasin())
        set_screen('Выпить_зелье_убийца')
    def Колющий_удар(self, event):
        # удаляет все виджеты класса и создает новый виджет этого же класса
        self.clear_widgets()
        self.add_widget(Battle_Assasin())
        global HP, damage_from_monster, HP_mob
        HP_mob -= (4 * Strenght) + Skill
        if HP_mob <= 0:
            set_screen('Вы_победили')
        else:
            HP -= damage_from_monster
            if HP <= 0:
                set_screen('Конец_Игры_Умер')
            else:
                set_screen('Вы_нанесли_удар_убийца')

    def in_leave(self):
        self.add_widget.clear_widgets()

class NoRunAssasin(Screen):
    def __init__(self, **kw):
        super(NoRunAssasin, self).__init__(**kw)

    def on_enter(self):
        No = FloatLayout()
        No.add_widget(Button(text="      Вы не смогли сбежать!\n          Вы получили урон!\n(нажмите для продолжения)",
                             font_size=25, color=[62 / 255, 28 / 255, 0 / 255, 1],
                             background_color=[185 / 255, 145 / 255, 75 / 255, 1], size_hint=(.7, .3), pos=(90, 275),
                             background_normal="", on_press=lambda x: set_screen('Бой_убийцы')))
        self.add_widget(No)

    def in_leave(self):
        self.add_widget.clear_widgets()

class You_struck_blow_Assasin(Screen):
    def __init__(self, **kw):
        super(You_struck_blow_Assasin, self).__init__(**kw)

    def on_enter(self):
        No = FloatLayout()
        No.add_widget(Button(text="          Вы нанесли удар!\n         Вы получили урон!\n(нажмите для продолжения)",
                             font_size=25, color=[62 / 255, 28 / 255, 0 / 255, 1],
                             background_color=[185 / 255, 145 / 255, 75 / 255, 1], size_hint=(.7, .3), pos=(90, 275),
                             background_normal="", on_press=lambda x: set_screen('Бой_убийцы')))
        self.add_widget(No)

    def in_leave(self):
        self.add_widget.clear_widgets()

class Drink_potion_Assasin(Screen):
    def __init__(self, **kw):
        super(Drink_potion_Assasin, self).__init__(**kw)

    def on_enter(self):
        Battle_Assasin = FloatLayout()
        Battle_Assasin.add_widget(Label(text="Выберите, какое зелье выпить\n"
                                             "У вас есть:\n"
                                             "Простое зелье лечения: "+str(Usual_healing_potion)+""
                                            "\nСильное зелье лечения: "+str(Powerful_healing_potion)+"\n"
                                            "Эпическое зелье лечения: "+str(Epic_healing_potion)+"\n\n\n\n\n\n\n\n\n\n\n",
                                        font_size=25,
                                        color=[62 / 255, 28 / 255, 0 / 255, 1]))
        Battle_Assasin.add_widget(Button(text="Простое зелье лечения",
                                         background_color=[180 / 255, 140 / 255, 75 / 255, 1],
                                         font_size=20, color=[62 / 255, 28 / 255, 0 / 255, 1], background_normal="",
                                         size_hint=(.4, .2), pos=(40, 210),
                                         on_press=self.Простое))
        Battle_Assasin.add_widget(Button(text="Сильное зелье лечения",
                                         background_color=[180 / 255, 140 / 255, 75 / 255, 1],
                                         font_size=20, color=[62 / 255, 28 / 255, 0 / 255, 1], background_normal="",
                                         size_hint=(.4, .2), pos=(310, 210),
                                         on_press=self.Сильное))
        Battle_Assasin.add_widget(Button(text="Эпическое зелье лечения",
                                         background_color=[180 / 255, 140 / 255, 75 / 255, 1],
                                         font_size=20, color=[62 / 255, 28 / 255, 0 / 255, 1], background_normal="",
                                         size_hint=(.4, .2), pos=(40, 55),
                                         on_press=self.Эпическое))
        Battle_Assasin.add_widget(Button(text="Продолжить бой",
                                         background_color=[180 / 255, 140 / 255, 75 / 255, 1],
                                         font_size=20, color=[62 / 255, 28 / 255, 0 / 255, 1], background_normal="",
                                         size_hint=(.4, .2), pos=(310, 55),
                                         on_press=self.Никакое))
        self.add_widget(Battle_Assasin)
    def Простое(self, enent):
        # удаляет все виджеты класса и создает новый виджет этого же класса
        self.clear_widgets()
        self.add_widget(Drink_potion_Assasin())
        global Usual_healing_potion, HP, MAX_HP
        if Usual_healing_potion >= 1:
            Usual_healing_potion -= 1
            HP += MAX_HP // 5
            if HP > MAX_HP:
                HP = MAX_HP
        set_screen('Бой_убийцы')
    def Сильное(self, enent):
        # удаляет все виджеты класса и создает новый виджет этого же класса
        self.clear_widgets()
        self.add_widget(Drink_potion_Assasin())
        global Powerful_healing_potion, HP, MAX_HP
        if Powerful_healing_potion >= 1:
            Powerful_healing_potion -= 1
            HP += MAX_HP // 10 * 3
            if HP > MAX_HP:
                HP = MAX_HP
        set_screen('Бой_убийцы')
    def Эпическое(self, enent):
        # удаляет все виджеты класса и создает новый виджет этого же класса
        self.clear_widgets()
        self.add_widget(Drink_potion_Assasin())
        global Epic_healing_potion, HP, MAX_HP
        if Epic_healing_potion >= 1:
            Epic_healing_potion -= 1
            HP += MAX_HP // 10 * 4
            if HP > MAX_HP:
                HP = MAX_HP
        set_screen('Бой_убийцы')
    def Никакое(self, enent):
        # удаляет все виджеты класса и создает новый виджет этого же класса
        self.clear_widgets()
        self.add_widget(Drink_potion_Assasin())
        set_screen('Бой_убийцы')
    def in_leave(self):
        self.add_widget.clear_widgets()


class Battle_Wizard(Screen):
    def __init__(self, **kw):
        super(Battle_Wizard, self).__init__(**kw)

    def on_enter(self):
        global mob, HP_mob, Name_Mob
        Battle_Wizard = FloatLayout()
        Battle_Wizard.add_widget(Label(text=str(Name_Mob)+"     ранг: "+str(mob)+"\n\n\n\n\n"
                                            "                    \n\n\n\n\n\n\n\n\n\n\n\n\n",
                                           font_size=25,
                                           color=[62 / 255, 28 / 255, 0 / 255, 1]))
        Battle_Wizard.add_widget(Button(text="Ледяное копьё",
                                    background_color=[180 / 255, 140 / 255, 75 / 255, 1],
                                    font_size=20, color=[62 / 255, 28 / 255, 0 / 255, 1], background_normal="",
                                    size_hint=(.4, .2), pos=(40, 210),
                                    on_press=self.Ледяное_копьё))
        Battle_Wizard.add_widget(Button(text="Сбежать",
                                    background_color=[180 / 255, 140 / 255, 75 / 255, 1],
                                    font_size=20, color=[62 / 255, 28 / 255, 0 / 255, 1], background_normal="",
                                    size_hint=(.4, .2), pos=(310, 55),
                                    on_press=self.Сбежать))
        Battle_Wizard.add_widget(Button(text="Выпить зелье",
                                    background_color=[180 / 255, 140 / 255, 75 / 255, 1],
                                    font_size=20, color=[62 / 255, 28 / 255, 0 / 255, 1], background_normal="",
                                    size_hint=(.4, .2), pos=(40, 55),
                                    on_press=self.Выпить_зелье))
        Battle_Wizard.add_widget(Button(text="Огненная стрела",
                                    background_color=[180 / 255, 140 / 255, 75 / 255, 1],
                                    font_size=20, color=[62 / 255, 28 / 255, 0 / 255, 1], background_normal="",
                                    size_hint=(.4, .2), pos=(310, 210),
                                    on_press=self.Огненная_стрела))
        Battle_Wizard.add_widget(Button(text="Ваше HP = " + str(HP),
                                            background_color=[150 / 255, 81 / 255, 69 / 255, 1],
                                            font_size=20, color=[64 / 255, 21 / 255, 21 / 255, 1], background_normal="",
                                            size_hint=(.4, .1), pos=(40, 460)))
        Battle_Wizard.add_widget(Button(text="HP монстра = " + str(HP_mob),
                                         background_color=[150 / 255, 81 / 255, 69 / 255, 1],
                                         font_size=20, color=[64 / 255, 21 / 255, 21 / 255, 1], background_normal="",
                                         size_hint=(.4, .1), pos=(40, 380)))
        self.add_widget(Battle_Wizard)

    def Сбежать(self, event):
        # удаляет все виджеты класса и создает новый виджет этого же класса
        self.clear_widgets()
        self.add_widget(Battle_Assasin())
        s = random.randint(1, 35) + Skill + Luck
        if s > 30:
            i = random.randint(1, Count_Screen)
            set_screen(str(i))
        else:
            global HP, damage_from_monster
            HP -= damage_from_monster
            if HP <= 0:
                set_screen('Конец_Игры_Умер')
            else:
                set_screen('Не_сбежал_маг')
    def Ледяное_копьё(self, event):
        # удаляет все виджеты класса и создает новый виджет этого же класса
        self.clear_widgets()
        self.add_widget(Battle_Assasin())
        global HP, damage_from_monster, HP_mob
        HP_mob -= (4 * Luck) + Strenght
        if HP_mob <= 0:
            set_screen('Вы_победили')
        else:
            HP -= damage_from_monster
            if HP <= 0:
                set_screen('Конец_Игры_Умер')
            else:
                set_screen('Вы_нанесли_удар_маг')
    def Выпить_зелье(self, event):
        # удаляет все виджеты класса и создает новый виджет этого же класса
        self.clear_widgets()
        self.add_widget(Battle_Assasin())
        set_screen('Выпить_зелье_маг')
    def Огненная_стрела(self, event):
        # удаляет все виджеты класса и создает новый виджет этого же класса
        self.clear_widgets()
        self.add_widget(Battle_Assasin())
        global HP, damage_from_monster, HP_mob
        HP_mob -= (4 * Strenght) + Luck*2
        if HP_mob <= 0:
            set_screen('Вы_победили')
        else:
            HP -= damage_from_monster
            if HP <= 0:
                set_screen('Конец_Игры_Умер')
            else:
                set_screen('Вы_нанесли_удар_маг')

    def in_leave(self):
        self.add_widget.clear_widgets()

class NoRunWizard(Screen):
    def __init__(self, **kw):
        super(NoRunWizard, self).__init__(**kw)

    def on_enter(self):
        No = FloatLayout()
        No.add_widget(Button(text="      Вы не смогли сбежать!\n          Вы получили урон!\n(нажмите для продолжения)",
                             font_size=25, color=[62 / 255, 28 / 255, 0 / 255, 1],
                             background_color=[185 / 255, 145 / 255, 75 / 255, 1], size_hint=(.7, .3), pos=(90, 275),
                             background_normal="", on_press=lambda x: set_screen('Бой_мага')))
        self.add_widget(No)

    def in_leave(self):
        self.add_widget.clear_widgets()

class You_struck_blow_Wizard(Screen):
    def __init__(self, **kw):
        super(You_struck_blow_Wizard, self).__init__(**kw)

    def on_enter(self):
        No = FloatLayout()
        No.add_widget(Button(text="          Вы нанесли удар!\n         Вы получили урон!\n(нажмите для продолжения)",
                             font_size=25, color=[62 / 255, 28 / 255, 0 / 255, 1],
                             background_color=[185 / 255, 145 / 255, 75 / 255, 1], size_hint=(.7, .3), pos=(90, 275),
                             background_normal="", on_press=lambda x: set_screen('Бой_мага')))
        self.add_widget(No)

    def in_leave(self):
        self.add_widget.clear_widgets()

class Drink_potion_Wizard(Screen):
    def __init__(self, **kw):
        super(Drink_potion_Wizard, self).__init__(**kw)

    def on_enter(self):
        Drink_potion_Wizard = FloatLayout()
        Drink_potion_Wizard.add_widget(Label(text="Выберите, какое зелье выпить\n"
                                             "У вас есть:\n"
                                             "Простое зелье лечения: "+str(Usual_healing_potion)+""
                                            "\nСильное зелье лечения: "+str(Powerful_healing_potion)+"\n"
                                            "Эпическое зелье лечения: "+str(Epic_healing_potion)+"\n\n\n\n\n\n\n\n\n\n\n",
                                        font_size=25,
                                        color=[62 / 255, 28 / 255, 0 / 255, 1]))
        Drink_potion_Wizard.add_widget(Button(text="Простое зелье лечения",
                                         background_color=[180 / 255, 140 / 255, 75 / 255, 1],
                                         font_size=20, color=[62 / 255, 28 / 255, 0 / 255, 1], background_normal="",
                                         size_hint=(.4, .2), pos=(40, 210),
                                         on_press=self.Простое))
        Drink_potion_Wizard.add_widget(Button(text="Сильное зелье лечения",
                                         background_color=[180 / 255, 140 / 255, 75 / 255, 1],
                                         font_size=20, color=[62 / 255, 28 / 255, 0 / 255, 1], background_normal="",
                                         size_hint=(.4, .2), pos=(310, 210),
                                         on_press=self.Сильное))
        Drink_potion_Wizard.add_widget(Button(text="Эпическое зелье лечения",
                                         background_color=[180 / 255, 140 / 255, 75 / 255, 1],
                                         font_size=20, color=[62 / 255, 28 / 255, 0 / 255, 1], background_normal="",
                                         size_hint=(.4, .2), pos=(40, 55),
                                         on_press=self.Эпическое))
        Drink_potion_Wizard.add_widget(Button(text="Продолжить бой",
                                         background_color=[180 / 255, 140 / 255, 75 / 255, 1],
                                         font_size=20, color=[62 / 255, 28 / 255, 0 / 255, 1], background_normal="",
                                         size_hint=(.4, .2), pos=(310, 55),
                                         on_press=self.Никакое))
        self.add_widget(Drink_potion_Wizard)
    def Простое(self, enent):
        # удаляет все виджеты класса и создает новый виджет этого же класса
        self.clear_widgets()
        self.add_widget(Drink_potion_Assasin())
        global Usual_healing_potion, HP, MAX_HP
        if Usual_healing_potion >= 1:
            Usual_healing_potion -= 1
            HP += MAX_HP // 5
            if HP > MAX_HP:
                HP = MAX_HP
        set_screen('Бой_мага')
    def Сильное(self, enent):
        # удаляет все виджеты класса и создает новый виджет этого же класса
        self.clear_widgets()
        self.add_widget(Drink_potion_Assasin())
        global Powerful_healing_potion, HP, MAX_HP
        if Powerful_healing_potion >= 1:
            Powerful_healing_potion -= 1
            HP += MAX_HP // 10 * 3
            if HP > MAX_HP:
                HP = MAX_HP
        set_screen('Бой_мага')
    def Эпическое(self, enent):
        # удаляет все виджеты класса и создает новый виджет этого же класса
        self.clear_widgets()
        self.add_widget(Drink_potion_Assasin())
        global Epic_healing_potion, HP, MAX_HP
        if Epic_healing_potion >= 1:
            Epic_healing_potion -= 1
            HP += MAX_HP // 10 * 4
            if HP > MAX_HP:
                HP = MAX_HP
        set_screen('Бой_мага')
    def Никакое(self, enent):
        # удаляет все виджеты класса и создает новый виджет этого же класса
        self.clear_widgets()
        self.add_widget(Drink_potion_Assasin())
        set_screen('Бой_мага')
    def in_leave(self):
        self.add_widget.clear_widgets()



class Battle_Warrior(Screen):
    def __init__(self, **kw):
        super(Battle_Warrior, self).__init__(**kw)

    def on_enter(self):
        global mob, HP_mob, Name_Mob
        Battle_Warrior = FloatLayout()
        Battle_Warrior.add_widget(Label(text=str(Name_Mob)+"     ранг: "+str(mob)+"\n\n\n\n\n"
                                            "                    \n\n\n\n\n\n\n\n\n\n\n\n\n",
                                           font_size=25,
                                           color=[62 / 255, 28 / 255, 0 / 255, 1]))
        Battle_Warrior.add_widget(Button(text="Рассечение",
                                    background_color=[180 / 255, 140 / 255, 75 / 255, 1],
                                    font_size=20, color=[62 / 255, 28 / 255, 0 / 255, 1], background_normal="",
                                    size_hint=(.4, .2), pos=(40, 210),
                                    on_press=self.Рассечение))
        Battle_Warrior.add_widget(Button(text="Сбежать",
                                    background_color=[180 / 255, 140 / 255, 75 / 255, 1],
                                    font_size=20, color=[62 / 255, 28 / 255, 0 / 255, 1], background_normal="",
                                    size_hint=(.4, .2), pos=(310, 55),
                                    on_press=self.Сбежать))
        Battle_Warrior.add_widget(Button(text="Выпить зелье",
                                    background_color=[180 / 255, 140 / 255, 75 / 255, 1],
                                    font_size=20, color=[62 / 255, 28 / 255, 0 / 255, 1], background_normal="",
                                    size_hint=(.4, .2), pos=(40, 55),
                                    on_press=self.Выпить_зелье))
        Battle_Warrior.add_widget(Button(text="Сильный удар",
                                    background_color=[180 / 255, 140 / 255, 75 / 255, 1],
                                    font_size=20, color=[62 / 255, 28 / 255, 0 / 255, 1], background_normal="",
                                    size_hint=(.4, .2), pos=(310, 210),
                                    on_press=self.Сильный_удар))
        Battle_Warrior.add_widget(Button(text="Ваше HP = " + str(HP),
                                            background_color=[150 / 255, 81 / 255, 69 / 255, 1],
                                            font_size=20, color=[64 / 255, 21 / 255, 21 / 255, 1], background_normal="",
                                            size_hint=(.4, .1), pos=(40, 460)))
        Battle_Warrior.add_widget(Button(text="HP монстра = " + str(HP_mob),
                                         background_color=[150 / 255, 81 / 255, 69 / 255, 1],
                                         font_size=20, color=[64 / 255, 21 / 255, 21 / 255, 1], background_normal="",
                                         size_hint=(.4, .1), pos=(40, 380)))
        self.add_widget(Battle_Warrior)

    def Сбежать(self, event):
        # удаляет все виджеты класса и создает новый виджет этого же класса
        self.clear_widgets()
        self.add_widget(Battle_Assasin())
        s = random.randint(1, 35) + Skill + Luck
        if s > 30:
            i = random.randint(1, Count_Screen)
            set_screen(str(i))
        else:
            global HP, damage_from_monster
            HP -= damage_from_monster
            if HP <= 0:
                set_screen('Конец_Игры_Умер')
            else:
                set_screen('Не_сбежал_воин')
    def Рассечение(self, event):
        # удаляет все виджеты класса и создает новый виджет этого же класса
        self.clear_widgets()
        self.add_widget(Battle_Assasin())
        global HP, damage_from_monster, HP_mob
        HP_mob -= (4 * Skill) + Strenght
        if HP_mob <= 0:
            set_screen('Вы_победили')
        else:
            HP -= damage_from_monster
            if HP <= 0:
                set_screen('Конец_Игры_Умер')
            else:
                set_screen('Вы_нанесли_удар_воин')
    def Выпить_зелье(self, event):
        # удаляет все виджеты класса и создает новый виджет этого же класса
        self.clear_widgets()
        self.add_widget(Battle_Assasin())
        set_screen('Выпить_зелье_воин')
    def Сильный_удар(self, event):
        # удаляет все виджеты класса и создает новый виджет этого же класса
        self.clear_widgets()
        self.add_widget(Battle_Assasin())
        global HP, damage_from_monster, HP_mob
        HP_mob -= (4 * Strenght) + Skill
        if HP_mob <= 0:
            set_screen('Вы_победили')
        else:
            HP -= damage_from_monster
            if HP <= 0:
                set_screen('Конец_Игры_Умер')
            else:
                set_screen('Вы_нанесли_удар_воин')

    def in_leave(self):
        self.add_widget.clear_widgets()

class NoRunWarrior(Screen):
    def __init__(self, **kw):
        super(NoRunWarrior, self).__init__(**kw)

    def on_enter(self):
        No = FloatLayout()
        No.add_widget(Button(text="      Вы не смогли сбежать!\n          Вы получили урон!\n(нажмите для продолжения)",
                             font_size=25, color=[62 / 255, 28 / 255, 0 / 255, 1],
                             background_color=[185 / 255, 145 / 255, 75 / 255, 1], size_hint=(.7, .3), pos=(90, 275),
                             background_normal="", on_press=lambda x: set_screen('Бой_воинв')))
        self.add_widget(No)

    def in_leave(self):
        self.add_widget.clear_widgets()

class You_struck_blow_Warrior(Screen):
    def __init__(self, **kw):
        super(You_struck_blow_Warrior, self).__init__(**kw)

    def on_enter(self):
        No = FloatLayout()
        No.add_widget(Button(text="          Вы нанесли удар!\n         Вы получили урон!\n(нажмите для продолжения)",
                             font_size=25, color=[62 / 255, 28 / 255, 0 / 255, 1],
                             background_color=[185 / 255, 145 / 255, 75 / 255, 1], size_hint=(.7, .3), pos=(90, 275),
                             background_normal="", on_press=lambda x: set_screen('Бой_воина')))
        self.add_widget(No)

    def in_leave(self):
        self.add_widget.clear_widgets()

class Drink_potion_Warrior(Screen):
    def __init__(self, **kw):
        super(Drink_potion_Warrior, self).__init__(**kw)

    def on_enter(self):
        Drink_potion_Warrior = FloatLayout()
        Drink_potion_Warrior.add_widget(Label(text="Выберите, какое зелье выпить\n"
                                             "У вас есть:\n"
                                             "Простое зелье лечения: "+str(Usual_healing_potion)+""
                                            "\nСильное зелье лечения: "+str(Powerful_healing_potion)+"\n"
                                            "Эпическое зелье лечения: "+str(Epic_healing_potion)+"\n\n\n\n\n\n\n\n\n\n\n",
                                        font_size=25,
                                        color=[62 / 255, 28 / 255, 0 / 255, 1]))
        Drink_potion_Warrior.add_widget(Button(text="Простое зелье лечения",
                                         background_color=[180 / 255, 140 / 255, 75 / 255, 1],
                                         font_size=20, color=[62 / 255, 28 / 255, 0 / 255, 1], background_normal="",
                                         size_hint=(.4, .2), pos=(40, 210),
                                         on_press=self.Простое))
        Drink_potion_Warrior.add_widget(Button(text="Сильное зелье лечения",
                                         background_color=[180 / 255, 140 / 255, 75 / 255, 1],
                                         font_size=20, color=[62 / 255, 28 / 255, 0 / 255, 1], background_normal="",
                                         size_hint=(.4, .2), pos=(310, 210),
                                         on_press=self.Сильное))
        Drink_potion_Warrior.add_widget(Button(text="Эпическое зелье лечения",
                                         background_color=[180 / 255, 140 / 255, 75 / 255, 1],
                                         font_size=20, color=[62 / 255, 28 / 255, 0 / 255, 1], background_normal="",
                                         size_hint=(.4, .2), pos=(40, 55),
                                         on_press=self.Эпическое))
        Drink_potion_Warrior.add_widget(Button(text="Продолжить бой",
                                         background_color=[180 / 255, 140 / 255, 75 / 255, 1],
                                         font_size=20, color=[62 / 255, 28 / 255, 0 / 255, 1], background_normal="",
                                         size_hint=(.4, .2), pos=(310, 55),
                                         on_press=self.Никакое))
        self.add_widget(Drink_potion_Warrior)
    def Простое(self, enent):
        # удаляет все виджеты класса и создает новый виджет этого же класса
        self.clear_widgets()
        self.add_widget(Drink_potion_Assasin())
        global Usual_healing_potion, HP, MAX_HP
        if Usual_healing_potion >= 1:
            Usual_healing_potion -= 1
            HP += MAX_HP // 5
            if HP > MAX_HP:
                HP = MAX_HP
        set_screen('Бой_воина')
    def Сильное(self, enent):
        # удаляет все виджеты класса и создает новый виджет этого же класса
        self.clear_widgets()
        self.add_widget(Drink_potion_Assasin())
        global Powerful_healing_potion, HP, MAX_HP
        if Powerful_healing_potion >= 1:
            Powerful_healing_potion -= 1
            HP += MAX_HP // 10 * 3
            if HP > MAX_HP:
                HP = MAX_HP
        set_screen('Бой_воина')
    def Эпическое(self, enent):
        # удаляет все виджеты класса и создает новый виджет этого же класса
        self.clear_widgets()
        self.add_widget(Drink_potion_Assasin())
        global Epic_healing_potion, HP, MAX_HP
        if Epic_healing_potion >= 1:
            Epic_healing_potion -= 1
            HP += MAX_HP // 10 * 4
            if HP > MAX_HP:
                HP = MAX_HP
        set_screen('Бой_воина')
    def Никакое(self, enent):
        # удаляет все виджеты класса и создает новый виджет этого же класса
        self.clear_widgets()
        self.add_widget(Drink_potion_Assasin())
        set_screen('Бой_воина')
    def in_leave(self):
        self.add_widget.clear_widgets()


class Battle_Guard(Screen):
    def __init__(self, **kw):
        super(Battle_Guard, self).__init__(**kw)

    def on_enter(self):
        global mob, HP_mob, Name_Mob
        Battle_Guard = FloatLayout()
        Battle_Guard.add_widget(Label(text=str(Name_Mob)+"     ранг: "+str(mob)+"\n\n\n\n\n"
                                            "                    \n\n\n\n\n\n\n\n\n\n\n\n\n",
                                           font_size=25,
                                           color=[62 / 255, 28 / 255, 0 / 255, 1]))
        Battle_Guard.add_widget(Button(text="Сокрушающий удар",
                                    background_color=[180 / 255, 140 / 255, 75 / 255, 1],
                                    font_size=20, color=[62 / 255, 28 / 255, 0 / 255, 1], background_normal="",
                                    size_hint=(.4, .2), pos=(40, 210),
                                    on_press=self.Сокрушающий_удар))
        Battle_Guard.add_widget(Button(text="Сбежать",
                                    background_color=[180 / 255, 140 / 255, 75 / 255, 1],
                                    font_size=20, color=[62 / 255, 28 / 255, 0 / 255, 1], background_normal="",
                                    size_hint=(.4, .2), pos=(310, 55),
                                    on_press=self.Сбежать))
        Battle_Guard.add_widget(Button(text="Выпить зелье",
                                    background_color=[180 / 255, 140 / 255, 75 / 255, 1],
                                    font_size=20, color=[62 / 255, 28 / 255, 0 / 255, 1], background_normal="",
                                    size_hint=(.4, .2), pos=(40, 55),
                                    on_press=self.Выпить_зелье))
        Battle_Guard.add_widget(Button(text="Рубящий удар",
                                    background_color=[180 / 255, 140 / 255, 75 / 255, 1],
                                    font_size=20, color=[62 / 255, 28 / 255, 0 / 255, 1], background_normal="",
                                    size_hint=(.4, .2), pos=(310, 210),
                                    on_press=self.Рубящий_удар))
        Battle_Guard.add_widget(Button(text="Ваше HP = " + str(HP),
                                            background_color=[150 / 255, 81 / 255, 69 / 255, 1],
                                            font_size=20, color=[64 / 255, 21 / 255, 21 / 255, 1], background_normal="",
                                            size_hint=(.4, .1), pos=(40, 460)))
        Battle_Guard.add_widget(Button(text="HP монстра = " + str(HP_mob),
                                         background_color=[150 / 255, 81 / 255, 69 / 255, 1],
                                         font_size=20, color=[64 / 255, 21 / 255, 21 / 255, 1], background_normal="",
                                         size_hint=(.4, .1), pos=(40, 380)))
        self.add_widget(Battle_Guard)

    def Сбежать(self, event):
        # удаляет все виджеты класса и создает новый виджет этого же класса
        self.clear_widgets()
        self.add_widget(Battle_Assasin())
        s = random.randint(1, 35) + Skill + Luck
        if s > 30:
            i = random.randint(1, Count_Screen)
            set_screen(str(i))
        else:
            global HP, damage_from_monster
            HP -= damage_from_monster
            if HP <= 0:
                set_screen('Конец_Игры_Умер')
            else:
                set_screen('Не_сбежал_страж')
    def Сокрушающий_удар(self, event):
        # удаляет все виджеты класса и создает новый виджет этого же класса
        self.clear_widgets()
        self.add_widget(Battle_Assasin())
        global HP, damage_from_monster, HP_mob
        HP_mob -= (4 * Skill) + Strenght
        if HP_mob <= 0:
            set_screen('Вы_победили')
        else:
            HP -= damage_from_monster
            if HP <= 0:
                set_screen('Конец_Игры_Умер')
            else:
                set_screen('Вы_нанесли_удар_страж')
    def Выпить_зелье(self, event):
        # удаляет все виджеты класса и создает новый виджет этого же класса
        self.clear_widgets()
        self.add_widget(Battle_Assasin())
        set_screen('Выпить_зелье_страж')
    def Рубящий_удар(self, event):
        # удаляет все виджеты класса и создает новый виджет этого же класса
        self.clear_widgets()
        self.add_widget(Battle_Assasin())
        global HP, damage_from_monster, HP_mob
        HP_mob -= (4 * Strenght) + Skill
        if HP_mob <= 0:
            set_screen('Вы_победили')
        else:
            HP -= damage_from_monster
            if HP <= 0:
                set_screen('Конец_Игры_Умер')
            else:
                set_screen('Вы_нанесли_удар_страж')

    def in_leave(self):
        self.add_widget.clear_widgets()

class NoRunGuard(Screen):
    def __init__(self, **kw):
        super(NoRunGuard, self).__init__(**kw)

    def on_enter(self):
        No = FloatLayout()
        No.add_widget(Button(text="      Вы не смогли сбежать!\n          Вы получили урон!\n(нажмите для продолжения)",
                             font_size=25, color=[62 / 255, 28 / 255, 0 / 255, 1],
                             background_color=[185 / 255, 145 / 255, 75 / 255, 1], size_hint=(.7, .3), pos=(90, 275),
                             background_normal="", on_press=lambda x: set_screen('Бой_стража')))
        self.add_widget(No)

    def in_leave(self):
        self.add_widget.clear_widgets()

class You_struck_blow_Guard(Screen):
    def __init__(self, **kw):
        super(You_struck_blow_Guard, self).__init__(**kw)

    def on_enter(self):
        No = FloatLayout()
        No.add_widget(Button(text="          Вы нанесли удар!\n         Вы получили урон!\n(нажмите для продолжения)",
                             font_size=25, color=[62 / 255, 28 / 255, 0 / 255, 1],
                             background_color=[185 / 255, 145 / 255, 75 / 255, 1], size_hint=(.7, .3), pos=(90, 275),
                             background_normal="", on_press=lambda x: set_screen('Бой_стража')))
        self.add_widget(No)

    def in_leave(self):
        self.add_widget.clear_widgets()

class Drink_potion_Guard(Screen):
    def __init__(self, **kw):
        super(Drink_potion_Guard, self).__init__(**kw)

    def on_enter(self):
        Drink_potion_Guard = FloatLayout()
        Drink_potion_Guard.add_widget(Label(text="Выберите, какое зелье выпить\n"
                                             "У вас есть:\n"
                                             "Простое зелье лечения: "+str(Usual_healing_potion)+""
                                            "\nСильное зелье лечения: "+str(Powerful_healing_potion)+"\n"
                                            "Эпическое зелье лечения: "+str(Epic_healing_potion)+"\n\n\n\n\n\n\n\n\n\n\n",
                                        font_size=25,
                                        color=[62 / 255, 28 / 255, 0 / 255, 1]))
        Drink_potion_Guard.add_widget(Button(text="Простое зелье лечения",
                                         background_color=[180 / 255, 140 / 255, 75 / 255, 1],
                                         font_size=20, color=[62 / 255, 28 / 255, 0 / 255, 1], background_normal="",
                                         size_hint=(.4, .2), pos=(40, 210),
                                         on_press=self.Простое))
        Drink_potion_Guard.add_widget(Button(text="Сильное зелье лечения",
                                         background_color=[180 / 255, 140 / 255, 75 / 255, 1],
                                         font_size=20, color=[62 / 255, 28 / 255, 0 / 255, 1], background_normal="",
                                         size_hint=(.4, .2), pos=(310, 210),
                                         on_press=self.Сильное))
        Drink_potion_Guard.add_widget(Button(text="Эпическое зелье лечения",
                                         background_color=[180 / 255, 140 / 255, 75 / 255, 1],
                                         font_size=20, color=[62 / 255, 28 / 255, 0 / 255, 1], background_normal="",
                                         size_hint=(.4, .2), pos=(40, 55),
                                         on_press=self.Эпическое))
        Drink_potion_Guard.add_widget(Button(text="Продолжить бой",
                                         background_color=[180 / 255, 140 / 255, 75 / 255, 1],
                                         font_size=20, color=[62 / 255, 28 / 255, 0 / 255, 1], background_normal="",
                                         size_hint=(.4, .2), pos=(310, 55),
                                         on_press=self.Никакое))
        self.add_widget(Drink_potion_Guard)
    def Простое(self, enent):
        # удаляет все виджеты класса и создает новый виджет этого же класса
        self.clear_widgets()
        self.add_widget(Drink_potion_Assasin())
        global Usual_healing_potion, HP, MAX_HP
        if Usual_healing_potion >= 1:
            Usual_healing_potion -= 1
            HP += MAX_HP // 5
            if HP > MAX_HP:
                HP = MAX_HP
        set_screen('Бой_стража')
    def Сильное(self, enent):
        # удаляет все виджеты класса и создает новый виджет этого же класса
        self.clear_widgets()
        self.add_widget(Drink_potion_Assasin())
        global Powerful_healing_potion, HP, MAX_HP
        if Powerful_healing_potion >= 1:
            Powerful_healing_potion -= 1
            HP += MAX_HP // 10 * 3
            if HP > MAX_HP:
                HP = MAX_HP
        set_screen('Бой_стража')
    def Эпическое(self, enent):
        # удаляет все виджеты класса и создает новый виджет этого же класса
        self.clear_widgets()
        self.add_widget(Drink_potion_Assasin())
        global Epic_healing_potion, HP, MAX_HP
        if Epic_healing_potion >= 1:
            Epic_healing_potion -= 1
            HP += MAX_HP // 10 * 4
            if HP > MAX_HP:
                HP = MAX_HP
        set_screen('Бой_стража')
    def Никакое(self, enent):
        # удаляет все виджеты класса и создает новый виджет этого же класса
        self.clear_widgets()
        self.add_widget(Drink_potion_Assasin())
        set_screen('Бой_стража')
    def in_leave(self):
        self.add_widget.clear_widgets()


class You_win(Screen):
    def __init__(self, **kw):
        super(You_win, self).__init__(**kw)

    def on_enter(self):
        global mob, Floor, reward
        if mob == "Обычный":
            exp = (random.randint(6, 7) * k + Floor)
            tr = random.randint(8, 12)
            reward = " "
        elif mob == "Сильный":
            exp = (random.randint(8, 9) * k + Floor * 2)
            tr = random.randint(12, 17)
            if Floor < 6:
                list = ["Лёгкий шлем", "Лёгкий нагрудник", "Легкие штаны", "Лёгкие сапоги", "Простое ожерелье",
                        "Простое кольцо", "Обычный клинок"]
            else:
                list = ["Кожаный шлем", "Кожаный нагрудник", "Кожаные штаны", "Кожаные сапоги",
                        "Ожерелье из малых кристаллов", "Кольцо с малым кристаллом", "Оружие из прочного железа"]
            reward = random.choice(list)
        elif mob == "Элитный":
            exp = (random.randint(11, 13) * k + Floor * 2)
            tr = random.randint(17, 23)
            if Floor < 6:
                list = ["Шлем из лозы", "Нагрудник из лозы", "Штаны из лозы", "Сапоги из лозы",
                 "Ожерелье из драгоценных камней", "Кольцо с драгоценным камнем", "Стальной меч"]
            else:
                list = ["Шлем из магических нитей", "Нагрудник из магических нитей", "Штаны из магических нитей",
                 "Сапоги из магических нитей", "Ожерелье из магических камней", "Кольцо с магическим камнем",
                 "Оружие из зачарованной углеродной стали"]
            reward = random.choice(list)

        You_win = FloatLayout()
        You_win.add_widget(Label(text="Вы победили "+str(Name_Mob)+"\nс рангом "+str(mob)+"                       "
                                            "                    \n\n"
                                            "Ваша награда:\n"+str(reward)+"\nОпыт + "+str(exp)+
                                           "\nТрофеи + "+str(tr)+"\n\n\n\n\n\n\n",
                                           font_size=25,
                                           color=[62 / 255, 28 / 255, 0 / 255, 1]))
        You_win.add_widget(Button(text="Продолжить\nне экипируя",
                                 background_color=[180 / 255, 140 / 255, 75 / 255, 1],
                                 font_size=20, color=[62 / 255, 28 / 255, 0 / 255, 1], background_normal="",
                                 size_hint=(.4, .2), pos=(320, 30),
                                 on_press=self.dalee))
        You_win.add_widget(Button(text="Экипировать",
                                 background_color=[180 / 255, 140 / 255, 75 / 255, 1],
                                 font_size=20, color=[62 / 255, 28 / 255, 0 / 255, 1], background_normal="",
                                 size_hint=(.4, .2), pos=(40, 30),
                                 on_press=self.equipment))
        You_win.add_widget(Button(text="HP = " + str(HP),
                                 background_color=[150 / 255, 81 / 255, 69 / 255, 1],
                                 font_size=20, color=[64 / 255, 21 / 255, 21 / 255, 1], background_normal="",
                                 size_hint=(.3, .10 / 11), pos=(42, 580)))
        self.add_widget(You_win)

    def equipment(self, event):
        # удаляет все виджеты класса и создает новый виджет этого же класса
        self.clear_widgets()
        self.add_widget(Mob())
        global pants_leather, pants_cloth, pants_epic, pants_legendary
        global helmet_leather, helmet_cloth, helmet_epic, helmet_legendary, bib_leather, bib_cloth, bib_epic, bib_legendary
        global boots_leather, boots_cloth, boots_epic, boots_legendary, necklace_leather, necklace_cloth, necklace_epic, necklace_legendary
        global ring_leather, ring_cloth, ring_epic, ring_legendary, weapon_leather, weapon_cloth, weapon_epic, weapon_legendary
        if reward == "Лёгкий шлем":
            helmet_leather += 1
        elif reward == "Лёгкий нагрудник":
            bib_leather += 1
        elif reward == "Легкие штаны":
            pants_leather += 1
        elif reward == "Лёгкие сапоги":
            boots_leather += 1
        elif reward == "Простое ожерелье":
            necklace_leather += 1
        elif reward == "Простое кольцо":
            ring_leather += 1
        elif reward == "Обычный клинок":
            weapon_leather += 1
        elif reward == "Кожаный шлем":
            helmet_cloth += 1
        elif reward == "Кожаный нагрудник":
            bib_cloth += 1
        elif reward == "Кожаные штаны":
            pants_cloth += 1
        elif reward == "Кожаные сапоги":
            boots_cloth += 1
        elif reward == "Ожерелье из малых кристаллов":
            necklace_cloth += 1
        elif reward == "Кольцо с малым кристаллом":
            ring_cloth += 1
        elif reward == "Оружие из прочного железа":
            weapon_cloth += 1
        elif reward == "Шлем из лозы":
            helmet_epic += 1
        elif reward == "Нагрудник из лозы":
            bib_epic += 1
        elif reward == "Штаны из лозы":
            pants_epic += 1
        elif reward == "Сапоги из лозы":
            boots_epic += 1
        elif reward == "Ожерелье из драгоценных камней":
            necklace_epic += 1
        elif reward == "Кольцо с драгоценным камнем":
            ring_epic += 1
        elif reward == "Стальной меч":
            weapon_epic += 1
        elif reward == "Шлем из магических нитей":
            helmet_legendary += 1
        elif reward == "Нагрудник из магических нитей":
            bib_legendary += 1
        elif reward == "Штаны из магических нитей":
            pants_legendary += 1
        elif reward == "Сапоги из магических нитей":
            boots_legendary += 1
        elif reward == "Ожерелье из магических камней":
            necklace_legendary += 1
        elif reward == "Кольцо с магическим камнем":
            ring_legendary += 1
        elif reward == "Оружие из зачарованной углеродной стали":
            weapon_legendary += 1
        set_screen('Экипировка_предмета')

    def dalee(self, event):
        # удаляет все виджеты класса и создает новый виджет этого же класса
        self.clear_widgets()
        self.add_widget(Mob())
        global pants_leather, pants_cloth, pants_epic, pants_legendary
        global helmet_leather, helmet_cloth, helmet_epic, helmet_legendary, bib_leather, bib_cloth, bib_epic, bib_legendary
        global boots_leather, boots_cloth, boots_epic, boots_legendary, necklace_leather, necklace_cloth, necklace_epic, necklace_legendary
        global ring_leather, ring_cloth, ring_epic, ring_legendary, weapon_leather, weapon_cloth, weapon_epic, weapon_legendary
        if reward == "Лёгкий шлем":
            helmet_leather += 1
        elif reward == "Лёгкий нагрудник":
            bib_leather += 1
        elif reward == "Легкие штаны":
            pants_leather += 1
        elif reward == "Лёгкие сапоги":
            boots_leather += 1
        elif reward == "Простое ожерелье":
            necklace_leather += 1
        elif reward == "Простое кольцо":
            ring_leather += 1
        elif reward == "Обычный клинок":
            weapon_leather += 1
        elif reward == "Кожаный шлем":
            helmet_cloth += 1
        elif reward == "Кожаный нагрудник":
            bib_cloth += 1
        elif reward == "Кожаные штаны":
            pants_cloth += 1
        elif reward == "Кожаные сапоги":
            boots_cloth += 1
        elif reward == "Ожерелье из малых кристаллов":
            necklace_cloth += 1
        elif reward == "Кольцо с малым кристаллом":
            ring_cloth += 1
        elif reward == "Оружие из прочного железа":
            weapon_cloth += 1
        elif reward == "Шлем из лозы":
            helmet_epic += 1
        elif reward == "Нагрудник из лозы":
            bib_epic += 1
        elif reward == "Штаны из лозы":
            pants_epic += 1
        elif reward == "Сапоги из лозы":
            boots_epic += 1
        elif reward == "Ожерелье из драгоценных камней":
            necklace_epic += 1
        elif reward == "Кольцо с драгоценным камнем":
            ring_epic += 1
        elif reward == "Стальной меч":
            weapon_epic += 1
        elif reward == "Шлем из магических нитей":
            helmet_legendary += 1
        elif reward == "Нагрудник из магических нитей":
            bib_legendary += 1
        elif reward == "Штаны из магических нитей":
            pants_legendary += 1
        elif reward == "Сапоги из магических нитей":
            boots_legendary += 1
        elif reward == "Ожерелье из магических камней":
            necklace_legendary += 1
        elif reward == "Кольцо с магическим камнем":
            ring_legendary += 1
        elif reward == "Оружие из зачарованной углеродной стали":
            weapon_legendary += 1
        i = random.randint(1, Count_Screen)
        set_screen(str(i))

    def in_leave(self):
        self.add_widget.clear_widgets()

# _____________________________________________________________________________________
# Конец блока сражения с монстрами
# _____________________________________________________________________________________


# _______________________________________________________________________________________________________
# Начало блока по экипировке предметов (функциональные слоты под предметы с увеличением характеристик)
# _______________________________________________________________________________________________________

class Equipment(Screen):
    def __init__(self, **kw):
        super(Equipment, self).__init__(**kw)

    def on_enter(self):
        Equipment = FloatLayout()
        Equipment.add_widget(Button(text="<-- В главное меню",
                                    background_color=[185 / 255, 145 / 255, 75 / 255, 1],
                                    font_size=20,
                                    color=[62 / 255, 28 / 255, 0 / 255, 1],
                                    size_hint=(.9, .1), pos=(27, 610),
                                    background_normal="", on_press=lambda x: set_screen('Главное_меню')))
        Equipment.add_widget(Label(text="Выберите, что вы хотите экипировать:\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n",
                                   font_size=25,
                                   color=[62 / 255, 28 / 255, 0 / 255, 1]))
        Equipment.add_widget(Button(text="Шлем",
                                    background_color=[180 / 255, 140 / 255, 75 / 255, 1],
                                    font_size=20, color=[62 / 255, 28 / 255, 0 / 255, 1], background_normal="",
                                    size_hint=(.4, .1), pos=(40, 440),
                                    on_press=self.dalee1))
        Equipment.add_widget(Button(text="Нагрудник",
                                    background_color=[180 / 255, 140 / 255, 75 / 255, 1],
                                    font_size=20, color=[62 / 255, 28 / 255, 0 / 255, 1], background_normal="",
                                    size_hint=(.4, .1), pos=(310, 440),
                                    on_press=self.dalee2))
        Equipment.add_widget(Button(text="Штаны",
                                    background_color=[180 / 255, 140 / 255, 75 / 255, 1],
                                    font_size=20, color=[62 / 255, 28 / 255, 0 / 255, 1], background_normal="",
                                    size_hint=(.4, .1), pos=(40, 340),
                                    on_press=self.dalee3))
        Equipment.add_widget(Button(text="Сапоги",
                                    background_color=[180 / 255, 140 / 255, 75 / 255, 1],
                                    font_size=20, color=[62 / 255, 28 / 255, 0 / 255, 1], background_normal="",
                                    size_hint=(.4, .1), pos=(310, 340),
                                    on_press=self.dalee4))
        Equipment.add_widget(Button(text="Ожерелье",
                                    background_color=[180 / 255, 140 / 255, 75 / 255, 1],
                                    font_size=20, color=[62 / 255, 28 / 255, 0 / 255, 1], background_normal="",
                                    size_hint=(.4, .1), pos=(40, 240),
                                    on_press=self.dalee5))
        Equipment.add_widget(Button(text="Кольцо",
                                    background_color=[180 / 255, 140 / 255, 75 / 255, 1],
                                    font_size=20, color=[62 / 255, 28 / 255, 0 / 255, 1], background_normal="",
                                    size_hint=(.4, .1), pos=(310, 240),
                                    on_press=self.dalee6))
        Equipment.add_widget(Button(text="Оружие",
                                    background_color=[180 / 255, 140 / 255, 75 / 255, 1],
                                    font_size=20, color=[62 / 255, 28 / 255, 0 / 255, 1], background_normal="",
                                    size_hint=(.4, .1), pos=(175, 140),
                                    on_press=self.dalee7))
        Equipment.add_widget(Button(text="Продолжить без экипировки",
                                    background_color=[180 / 255, 140 / 255, 75 / 255, 1],
                                    font_size=20, color=[62 / 255, 28 / 255, 0 / 255, 1], background_normal="",
                                    size_hint=(.9, .1), pos=(27, 40),
                                    on_press=self.dalee8))
        self.add_widget(Equipment)

    def dalee1(self, event):
        global helmet_epic, helmet_legendary, helmet_cloth, helmet_leather
        if helmet_leather >= 1 or helmet_cloth >= 1 or helmet_epic >= 1 or helmet_legendary >= 1:
            set_screen('Экипировка_шлема')
        else:
            set_screen('Экипировка_предметаNO')

    def dalee2(self, event):
        global bib_leather, bib_cloth, bib_epic, bib_legendary
        if bib_leather >= 1 or bib_cloth >= 1 or bib_epic >= 1 or bib_legendary >= 1:
            set_screen('Экипировка_нагрудника')
        else:
            set_screen('Экипировка_предметаNO')

    def dalee3(self, event):
        global pants_leather, pants_cloth, pants_epic, pants_legendary
        if pants_leather >= 1 or pants_cloth >= 1 or pants_epic >= 1 or pants_legendary >= 1:
            set_screen('Экипировка_штанов')
        else:
            set_screen('Экипировка_предметаNO')

    def dalee4(self, event):
        global boots_leather, boots_cloth, boots_epic, boots_legendary
        if boots_leather >= 1 or boots_cloth >= 1 or boots_epic >= 1 or boots_legendary >= 1:
            set_screen('Экипировка_сапог')
        else:
            set_screen('Экипировка_предметаNO')

    def dalee5(self, event):
        global necklace_leather, necklace_cloth, necklace_epic, necklace_legendary
        if necklace_leather >= 1 or necklace_cloth >= 1 or necklace_epic >= 1 or necklace_legendary >= 1:
            set_screen('Экипировка_ожерелья')
        else:
            set_screen('Экипировка_предметаNO')

    def dalee6(self, event):
        global ring_leather, ring_cloth, ring_epic, ring_legendary
        if ring_leather >= 1 or ring_cloth >= 1 or ring_epic >= 1 or ring_legendary >= 1:
            set_screen('Экипировка_кольца')
        else:
            set_screen('Экипировка_предметаNO')

    def dalee7(self, event):
        global weapon_leather, weapon_cloth, weapon_epic, weapon_legendary
        if weapon_leather >= 1 or weapon_cloth >= 1 or weapon_epic >= 1 or weapon_legendary >= 1:
            set_screen('Экипировка_оружия')
        else:
            set_screen('Экипировка_предметаNO')

    def dalee8(self, event):
        i = random.randint(1, Count_Screen)
        set_screen(str(i))

    def in_leave(self):
        self.add_widget.clear_widgets()


class EquipmentOK(Screen):
    def __init__(self, **kw):
        super(EquipmentOK, self).__init__(**kw)

    def on_enter(self):
        EquipmentOK = FloatLayout()
        EquipmentOK.add_widget(Button(text="<-- В главное меню",
                                      background_color=[185 / 255, 145 / 255, 75 / 255, 1],
                                      font_size=20,
                                      color=[62 / 255, 28 / 255, 0 / 255, 1],
                                      size_hint=(.9, .1), pos=(27, 610),
                                      background_normal="", on_press=lambda x: set_screen('Главное_меню')))
        EquipmentOK.add_widget(Label(text="            Вы экипировали предмет\n\n"
                                          "Если предмет был заменён на другой,\n"
                                          " то вы сможете переэкипировать его\n"
                                          "                    в следующий раз\n\n\n\n\n\n\n\n\n\n\n\n",
                                     font_size=25,
                                     color=[62 / 255, 28 / 255, 0 / 255, 1]))
        EquipmentOK.add_widget(Button(text="Продолжить игру",
                                      background_color=[180 / 255, 140 / 255, 75 / 255, 1],
                                      font_size=20, color=[62 / 255, 28 / 255, 0 / 255, 1], background_normal="",
                                      size_hint=(.6, .2), pos=(115, 95),
                                      on_press=self.dalee))
        EquipmentOK.add_widget(Button(text="   Экипировать\nдругой предмет",
                                      background_color=[180 / 255, 140 / 255, 75 / 255, 1],
                                      font_size=20, color=[62 / 255, 28 / 255, 0 / 255, 1], background_normal="",
                                      size_hint=(.6, .2), pos=(115, 270),
                                      on_press=self.ekipa))
        self.add_widget(EquipmentOK)

    def dalee(self, event):
        i = random.randint(1, Count_Screen)
        set_screen(str(i))

    def ekipa(self, event):
        set_screen('Экипировка_предмета')

    def in_leave(self):
        self.add_widget.clear_widgets()


class EquipmentNO(Screen):
    def __init__(self, **kw):
        super(EquipmentNO, self).__init__(**kw)

    def on_enter(self):
        EquipmentNO = FloatLayout()
        EquipmentNO.add_widget(Button(text="<-- В главное меню",
                                      background_color=[185 / 255, 145 / 255, 75 / 255, 1],
                                      font_size=20,
                                      color=[62 / 255, 28 / 255, 0 / 255, 1],
                                      size_hint=(.9, .1), pos=(27, 610),
                                      background_normal="", on_press=lambda x: set_screen('Главное_меню')))
        EquipmentNO.add_widget(Label(text="                  Вы не экипировали предмет\n\n"
                                          "Скорее всего, вы выбрали не тот тип предмета\n"
                                          "          или же у вас нет такого предмета\n\n\n\n\n\n\n\n\n\n\n\n",
                                     font_size=25,
                                     color=[62 / 255, 28 / 255, 0 / 255, 1]))
        EquipmentNO.add_widget(Button(text="Попробовать снова",
                                      background_color=[180 / 255, 140 / 255, 75 / 255, 1],
                                      font_size=20, color=[62 / 255, 28 / 255, 0 / 255, 1], background_normal="",
                                      size_hint=(.6, .2), pos=(115, 270),
                                      on_press=self.dalee))
        EquipmentNO.add_widget(Button(text="Продолжить игру\nбез экипировки",
                                      background_color=[180 / 255, 140 / 255, 75 / 255, 1],
                                      font_size=20, color=[62 / 255, 28 / 255, 0 / 255, 1], background_normal="",
                                      size_hint=(.6, .2), pos=(115, 90),
                                      on_press=self.dalee1))
        self.add_widget(EquipmentNO)

    def dalee(self, event):
        set_screen('Экипировка_предмета')

    def dalee1(self, event):
        i = random.randint(1, Count_Screen)
        set_screen(str(i))

    def in_leave(self):
        self.add_widget.clear_widgets()


class EquipmentHelmet(Screen):
    def __init__(self, **kw):
        super(EquipmentHelmet, self).__init__(**kw)

    def on_enter(self):
        Equipment = FloatLayout()
        Equipment.add_widget(Button(text="<-- В главное меню",
                                    background_color=[185 / 255, 145 / 255, 75 / 255, 1],
                                    font_size=20,
                                    color=[62 / 255, 28 / 255, 0 / 255, 1],
                                    size_hint=(.9, .1), pos=(27, 610),
                                    background_normal="", on_press=lambda x: set_screen('Главное_меню')))
        Equipment.add_widget(Label(text="Выберите, что вы хотите экипировать:\n\n\n\n\n\n\n\n\n\n\n\n\n\n",
                                   font_size=25,
                                   color=[62 / 255, 28 / 255, 0 / 255, 1]))
        Equipment.add_widget(Button(text="Лёгкий шлем",
                                    background_color=[180 / 255, 140 / 255, 75 / 255, 1],
                                    font_size=20, color=[62 / 255, 28 / 255, 0 / 255, 1], background_normal="",
                                    size_hint=(.8, .1), pos=(60, 400),
                                    on_press=self.dalee1))
        Equipment.add_widget(Button(text="Кожаный шлем",
                                    background_color=[180 / 255, 140 / 255, 75 / 255, 1],
                                    font_size=20, color=[62 / 255, 28 / 255, 0 / 255, 1], background_normal="",
                                    size_hint=(.8, .1), pos=(60, 300),
                                    on_press=self.dalee2))
        Equipment.add_widget(Button(text="Шлем из лозы",
                                    background_color=[180 / 255, 140 / 255, 75 / 255, 1],
                                    font_size=20, color=[62 / 255, 28 / 255, 0 / 255, 1], background_normal="",
                                    size_hint=(.8, .1), pos=(60, 200),
                                    on_press=self.dalee3))
        Equipment.add_widget(Button(text="Шлем из магических нитей",
                                    background_color=[180 / 255, 140 / 255, 75 / 255, 1],
                                    font_size=20, color=[62 / 255, 28 / 255, 0 / 255, 1], background_normal="",
                                    size_hint=(.8, .1), pos=(60, 100),
                                    on_press=self.dalee4))
        self.add_widget(Equipment)

    def dalee1(self, event):
        global helmet_leather, helmet, Endurance
        if helmet_leather >= 1:
            if helmet == " ":
                helmet = "helmet_leather"
                Endurance += 1
            elif helmet == "helmet_cloth":
                helmet = "helmet_leather"
                Endurance -= 1
            elif helmet == "helmet_epic":
                helmet = "helmet_leather"
                Endurance -= 2
            elif helmet == "helmet_legendary":
                helmet = "helmet_leather"
                Endurance -= 4
            set_screen('Экипировка_предметаOK')
        else:
            set_screen('Экипировка_предметаNO')

    def dalee2(self, event):
        global helmet_cloth, helmet, Endurance
        if helmet_cloth >= 1:
            if helmet == " ":
                helmet = "helmet_cloth"
                Endurance += 2
            elif helmet == "helmet_leather":
                helmet = "helmet_cloth"
                Endurance += 1
            elif helmet == "helmet_epic":
                helmet = "helmet_cloth"
                Endurance -= 1
            elif helmet == "helmet_legendary":
                helmet = "helmet_cloth"
                Endurance -= 3
            set_screen('Экипировка_предметаOK')
        else:
            set_screen('Экипировка_предметаNO')

    def dalee3(self, event):
        global helmet_epic, helmet, Endurance
        if helmet_epic >= 1:
            if helmet == " ":
                helmet = "helmet_epic"
                Endurance += 3
            elif helmet == "helmet_leather":
                helmet = "helmet_epic"
                Endurance += 2
            elif helmet == "helmet_cloth":
                helmet = "helmet_epic"
                Endurance += 1
            elif helmet == "helmet_legendary":
                helmet = "helmet_epic"
                Endurance -= 2
            set_screen('Экипировка_предметаOK')
        else:
            set_screen('Экипировка_предметаNO')

    def dalee4(self, event):
        global helmet_legendary, helmet, Endurance
        if helmet_legendary >= 1:
            if helmet == " ":
                helmet = "helmet_legendary"
                Endurance += 5
            elif helmet == "helmet_leather":
                helmet = "helmet_legendary"
                Endurance += 4
            elif helmet == "helmet_cloth":
                helmet = "helmet_legendary"
                Endurance += 3
            elif helmet == "helmet_epic":
                helmet = "helmet_legendary"
                Endurance += 2
            set_screen('Экипировка_предметаOK')
        else:
            set_screen('Экипировка_предметаNO')

    def in_leave(self):
        self.add_widget.clear_widgets()


class EquipmentBib(Screen):
    def __init__(self, **kw):
        super(EquipmentBib, self).__init__(**kw)

    def on_enter(self):
        Equipment = FloatLayout()
        Equipment.add_widget(Button(text="<-- В главное меню",
                                    background_color=[185 / 255, 145 / 255, 75 / 255, 1],
                                    font_size=20,
                                    color=[62 / 255, 28 / 255, 0 / 255, 1],
                                    size_hint=(.9, .1), pos=(27, 610),
                                    background_normal="", on_press=lambda x: set_screen('Главное_меню')))
        Equipment.add_widget(Label(text="Выберите, что вы хотите экипировать:\n\n\n\n\n\n\n\n\n\n\n\n\n\n",
                                   font_size=25,
                                   color=[62 / 255, 28 / 255, 0 / 255, 1]))
        Equipment.add_widget(Button(text="Лёгкий нагрудник",
                                    background_color=[180 / 255, 140 / 255, 75 / 255, 1],
                                    font_size=20, color=[62 / 255, 28 / 255, 0 / 255, 1], background_normal="",
                                    size_hint=(.8, .1), pos=(60, 400),
                                    on_press=self.dalee1))
        Equipment.add_widget(Button(text="Кожаный нагрудник",
                                    background_color=[180 / 255, 140 / 255, 75 / 255, 1],
                                    font_size=20, color=[62 / 255, 28 / 255, 0 / 255, 1], background_normal="",
                                    size_hint=(.8, .1), pos=(60, 300),
                                    on_press=self.dalee2))
        Equipment.add_widget(Button(text="Нагрудник из лозы",
                                    background_color=[180 / 255, 140 / 255, 75 / 255, 1],
                                    font_size=20, color=[62 / 255, 28 / 255, 0 / 255, 1], background_normal="",
                                    size_hint=(.8, .1), pos=(60, 200),
                                    on_press=self.dalee3))
        Equipment.add_widget(Button(text="Нагрудник из магических нитей",
                                    background_color=[180 / 255, 140 / 255, 75 / 255, 1],
                                    font_size=20, color=[62 / 255, 28 / 255, 0 / 255, 1], background_normal="",
                                    size_hint=(.8, .1), pos=(60, 100),
                                    on_press=self.dalee4))
        self.add_widget(Equipment)

    def dalee1(self, event):
        global bib_leather, bib, MAX_HP
        if bib_leather >= 1:
            if bib == " ":
                bib = "bib_leather"
                MAX_HP += 10
            elif bib == "bib_cloth":
                bib = "bib_leather"
                MAX_HP -= 10
            elif bib == "bib_epic":
                bib = "bib_leather"
                MAX_HP -= 20
            elif bib == "bib_legendary":
                bib = "bib_leather"
                MAX_HP -= 40
            set_screen('Экипировка_предметаOK')
        else:
            set_screen('Экипировка_предметаNO')

    def dalee2(self, event):
        global bib_cloth, bib, MAX_HP
        if bib_cloth >= 1:
            if bib == " ":
                bib = "bib_cloth"
                MAX_HP += 20
            elif bib == "bib_leather":
                bib = "bib_cloth"
                MAX_HP += 10
            elif bib == "bib_epic":
                bib = "bib_cloth"
                MAX_HP -= 10
            elif bib == "bib_legendary":
                bib = "bib_cloth"
                MAX_HP -= 30
            set_screen('Экипировка_предметаOK')
        else:
            set_screen('Экипировка_предметаNO')

    def dalee3(self, event):
        global bib_epic, bib, MAX_HP
        if bib_epic >= 1:
            if bib == " ":
                bib = "bib_epic"
                MAX_HP += 30
            elif bib == "bib_leather":
                bib = "bib_epic"
                MAX_HP += 20
            elif bib == "bib_cloth":
                bib = "bib_epic"
                MAX_HP += 10
            elif bib == "bib_legendary":
                bib = "bib_epic"
                MAX_HP -= 20
            set_screen('Экипировка_предметаOK')
        else:
            set_screen('Экипировка_предметаNO')

    def dalee4(self, event):
        global bib_legendary, bib, MAX_HP
        if bib_legendary >= 1:
            if bib == " ":
                bib = "bib_legendary"
                MAX_HP += 50
            elif bib == "bib_leather":
                bib = "bib_legendary"
                MAX_HP += 40
            elif bib == "bib_cloth":
                bib = "bib_legendary"
                MAX_HP += 30
            elif bib == "bib_epic":
                bib = "bib_legendary"
                MAX_HP += 20
            set_screen('Экипировка_предметаOK')
        else:
            set_screen('Экипировка_предметаNO')

    def in_leave(self):
        self.add_widget.clear_widgets()


class EquipmentPants(Screen):
    def __init__(self, **kw):
        super(EquipmentPants, self).__init__(**kw)

    def on_enter(self):
        Equipment = FloatLayout()
        Equipment.add_widget(Button(text="<-- В главное меню",
                                    background_color=[185 / 255, 145 / 255, 75 / 255, 1],
                                    font_size=20,
                                    color=[62 / 255, 28 / 255, 0 / 255, 1],
                                    size_hint=(.9, .1), pos=(27, 610),
                                    background_normal="", on_press=lambda x: set_screen('Главное_меню')))
        Equipment.add_widget(Label(text="Выберите, что вы хотите экипировать:\n\n\n\n\n\n\n\n\n\n\n\n\n\n",
                                   font_size=25,
                                   color=[62 / 255, 28 / 255, 0 / 255, 1]))
        Equipment.add_widget(Button(text="Лёгкие штаны",
                                    background_color=[180 / 255, 140 / 255, 75 / 255, 1],
                                    font_size=20, color=[62 / 255, 28 / 255, 0 / 255, 1], background_normal="",
                                    size_hint=(.8, .1), pos=(60, 400),
                                    on_press=self.dalee1))
        Equipment.add_widget(Button(text="Кожаные штаны",
                                    background_color=[180 / 255, 140 / 255, 75 / 255, 1],
                                    font_size=20, color=[62 / 255, 28 / 255, 0 / 255, 1], background_normal="",
                                    size_hint=(.8, .1), pos=(60, 300),
                                    on_press=self.dalee2))
        Equipment.add_widget(Button(text="Штаны из лозы",
                                    background_color=[180 / 255, 140 / 255, 75 / 255, 1],
                                    font_size=20, color=[62 / 255, 28 / 255, 0 / 255, 1], background_normal="",
                                    size_hint=(.8, .1), pos=(60, 200),
                                    on_press=self.dalee3))
        Equipment.add_widget(Button(text="Штаны из магических нитей",
                                    background_color=[180 / 255, 140 / 255, 75 / 255, 1],
                                    font_size=20, color=[62 / 255, 28 / 255, 0 / 255, 1], background_normal="",
                                    size_hint=(.8, .1), pos=(60, 100),
                                    on_press=self.dalee4))
        self.add_widget(Equipment)

    def dalee1(self, event):
        global pants_leather, pants, MAX_HP
        if pants_leather >= 1:
            if pants == " ":
                pants = "pants_leather"
                MAX_HP += 10
            elif pants == "pants_cloth":
                pants = "pants_leather"
                MAX_HP -= 10
            elif pants == "pants_epic":
                pants = "pants_leather"
                MAX_HP -= 20
            elif pants == "pants_legendary":
                pants = "pants_leather"
                MAX_HP -= 40
            print(pants)
            set_screen('Экипировка_предметаOK')
        else:
            set_screen('Экипировка_предметаNO')

    def dalee2(self, event):
        global pants_cloth, pants, MAX_HP
        if pants_cloth >= 1:
            if pants == " ":
                pants = "pants_cloth"
                MAX_HP += 20
            elif pants == "pants_leather":
                pants = "pants_cloth"
                MAX_HP += 10
            elif pants == "pants_epic":
                pants = "pants_cloth"
                MAX_HP -= 10
            elif pants == "pants_legendary":
                pants = "pants_cloth"
                MAX_HP -= 30
            print(pants)
            set_screen('Экипировка_предметаOK')
        else:
            set_screen('Экипировка_предметаNO')

    def dalee3(self, event):
        global pants_epic, pants, MAX_HP
        if pants_epic >= 1:
            if pants == " ":
                pants = "pants_epic"
                MAX_HP += 30
            elif pants == "pants_leather":
                pants = "pants_epic"
                MAX_HP += 20
            elif pants == "pants_cloth":
                pants = "pants_epic"
                MAX_HP += 10
            elif pants == "pants_legendary":
                pants = "pants_epic"
                MAX_HP -= 20
            set_screen('Экипировка_предметаOK')
        else:
            set_screen('Экипировка_предметаNO')

    def dalee4(self, event):
        global pants_legendary, pants, MAX_HP
        if pants_legendary >= 1:
            if pants == " ":
                pants = "pants_legendary"
                MAX_HP += 50
            elif pants == "pants_leather":
                pants = "pants_legendary"
                MAX_HP += 40
            elif pants == "pants_cloth":
                pants = "pants_legendary"
                MAX_HP += 30
            elif pants == "pants_epic":
                pants = "pants_legendary"
                MAX_HP += 20
            set_screen('Экипировка_предметаOK')
        else:
            set_screen('Экипировка_предметаNO')

    def in_leave(self):
        self.add_widget.clear_widgets()


class EquipmentBoots(Screen):
    def __init__(self, **kw):
        super(EquipmentBoots, self).__init__(**kw)

    def on_enter(self):
        Equipment = FloatLayout()
        Equipment.add_widget(Button(text="<-- В главное меню",
                                    background_color=[185 / 255, 145 / 255, 75 / 255, 1],
                                    font_size=20,
                                    color=[62 / 255, 28 / 255, 0 / 255, 1],
                                    size_hint=(.9, .1), pos=(27, 610),
                                    background_normal="", on_press=lambda x: set_screen('Главное_меню')))
        Equipment.add_widget(Label(text="Выберите, что вы хотите экипировать:\n\n\n\n\n\n\n\n\n\n\n\n\n\n",
                                   font_size=25,
                                   color=[62 / 255, 28 / 255, 0 / 255, 1]))
        Equipment.add_widget(Button(text="Лёгкие сапоги",
                                    background_color=[180 / 255, 140 / 255, 75 / 255, 1],
                                    font_size=20, color=[62 / 255, 28 / 255, 0 / 255, 1], background_normal="",
                                    size_hint=(.8, .1), pos=(60, 400),
                                    on_press=self.dalee1))
        Equipment.add_widget(Button(text="Кожаные сапоги",
                                    background_color=[180 / 255, 140 / 255, 75 / 255, 1],
                                    font_size=20, color=[62 / 255, 28 / 255, 0 / 255, 1], background_normal="",
                                    size_hint=(.8, .1), pos=(60, 300),
                                    on_press=self.dalee2))
        Equipment.add_widget(Button(text="Сапоги из лозы",
                                    background_color=[180 / 255, 140 / 255, 75 / 255, 1],
                                    font_size=20, color=[62 / 255, 28 / 255, 0 / 255, 1], background_normal="",
                                    size_hint=(.8, .1), pos=(60, 200),
                                    on_press=self.dalee3))
        Equipment.add_widget(Button(text="Сапоги из магических нитей",
                                    background_color=[180 / 255, 140 / 255, 75 / 255, 1],
                                    font_size=20, color=[62 / 255, 28 / 255, 0 / 255, 1], background_normal="",
                                    size_hint=(.8, .1), pos=(60, 100),
                                    on_press=self.dalee4))
        self.add_widget(Equipment)

    def dalee1(self, event):
        global boots_leather, boots, Skill
        if boots_leather >= 1:
            if boots == " ":
                boots = "boots_leather"
                Skill += 1
            elif boots == "boots_cloth":
                boots = "boots_leather"
                Skill -= 1
            elif boots == "boots_epic":
                boots = "boots_leather"
                Skill -= 2
            elif boots == "boots_legendary":
                boots = "boots_leather"
                Skill -= 4
            set_screen('Экипировка_предметаOK')
        else:
            set_screen('Экипировка_предметаNO')

    def dalee2(self, event):
        global boots_cloth, boots, Skill
        if boots_cloth >= 1:
            if boots == " ":
                boots = "boots_cloth"
                Skill += 2
            elif boots == "boots_leather":
                boots = "boots_cloth"
                Skill += 1
            elif boots == "boots_epic":
                boots = "boots_cloth"
                Skill -= 1
            elif boots == "boots_legendary":
                boots = "boots_cloth"
                Skill -= 3
            set_screen('Экипировка_предметаOK')
        else:
            set_screen('Экипировка_предметаNO')

    def dalee3(self, event):
        global boots_epic, boots, Skill
        if boots_epic >= 1:
            if boots == " ":
                boots = "boots_epic"
                Skill += 3
            elif boots == "boots_leather":
                boots = "boots_epic"
                Skill += 2
            elif boots == "boots_cloth":
                boots = "boots_epic"
                Skill += 1
            elif boots == "boots_legendary":
                boots = "boots_epic"
                Skill -= 2
            set_screen('Экипировка_предметаOK')
        else:
            set_screen('Экипировка_предметаNO')

    def dalee4(self, event):
        global boots_legendary, boots, Skill
        if boots_legendary >= 1:
            if boots == " ":
                boots = "boots_legendary"
                Skill += 5
            elif boots == "boots_leather":
                boots = "boots_legendary"
                Skill += 4
            elif boots == "boots_cloth":
                boots = "boots_legendary"
                Skill += 3
            elif boots == "boots_epic":
                boots = "boots_legendary"
                Skill += 2
            set_screen('Экипировка_предметаOK')
        else:
            set_screen('Экипировка_предметаNO')

    def in_leave(self):
        self.add_widget.clear_widgets()


class EquipmentNecklace(Screen):
    def __init__(self, **kw):
        super(EquipmentNecklace, self).__init__(**kw)

    def on_enter(self):
        Equipment = FloatLayout()
        Equipment.add_widget(Button(text="<-- В главное меню",
                                    background_color=[185 / 255, 145 / 255, 75 / 255, 1],
                                    font_size=20,
                                    color=[62 / 255, 28 / 255, 0 / 255, 1],
                                    size_hint=(.9, .1), pos=(27, 610),
                                    background_normal="", on_press=lambda x: set_screen('Главное_меню')))
        Equipment.add_widget(Label(text="Выберите, что вы хотите экипировать:\n\n\n\n\n\n\n\n\n\n\n\n\n\n",
                                   font_size=25,
                                   color=[62 / 255, 28 / 255, 0 / 255, 1]))
        Equipment.add_widget(Button(text="Простое ожерелье",
                                    background_color=[180 / 255, 140 / 255, 75 / 255, 1],
                                    font_size=20, color=[62 / 255, 28 / 255, 0 / 255, 1], background_normal="",
                                    size_hint=(.8, .1), pos=(60, 400),
                                    on_press=self.dalee1))
        Equipment.add_widget(Button(text="Ожерелье из малых кристаллов",
                                    background_color=[180 / 255, 140 / 255, 75 / 255, 1],
                                    font_size=20, color=[62 / 255, 28 / 255, 0 / 255, 1], background_normal="",
                                    size_hint=(.8, .1), pos=(60, 300),
                                    on_press=self.dalee2))
        Equipment.add_widget(Button(text="Ожерелье из драгоценных камней",
                                    background_color=[180 / 255, 140 / 255, 75 / 255, 1],
                                    font_size=20, color=[62 / 255, 28 / 255, 0 / 255, 1], background_normal="",
                                    size_hint=(.8, .1), pos=(60, 200),
                                    on_press=self.dalee3))
        Equipment.add_widget(Button(text="Ожерелье из магических камней",
                                    background_color=[180 / 255, 140 / 255, 75 / 255, 1],
                                    font_size=20, color=[62 / 255, 28 / 255, 0 / 255, 1], background_normal="",
                                    size_hint=(.8, .1), pos=(60, 100),
                                    on_press=self.dalee4))
        self.add_widget(Equipment)

    def dalee1(self, event):
        global necklace_leather, necklace, Luck
        if necklace_leather >= 1:
            if necklace == " ":
                necklace = "necklace_leather"
                Luck += 1
            elif necklace == "necklace_cloth":
                necklace = "necklace_leather"
                Luck -= 1
            elif necklace == "necklace_epic":
                necklace = "necklace_leather"
                Luck -= 2
            elif necklace == "necklace_legendary":
                necklace = "necklace_leather"
                Luck -= 4
            set_screen('Экипировка_предметаOK')
        else:
            set_screen('Экипировка_предметаNO')

    def dalee2(self, event):
        global necklace_cloth, necklace, Luck
        if necklace_cloth >= 1:
            if necklace == " ":
                necklace = "necklace_cloth"
                Luck += 2
            elif necklace == "necklace_leather":
                necklace = "necklace_cloth"
                Luck += 1
            elif necklace == "necklace_epic":
                necklace = "necklace_cloth"
                Luck -= 1
            elif necklace == "necklace_legendary":
                necklace = "necklace_cloth"
                Luck -= 3
            set_screen('Экипировка_предметаOK')
        else:
            set_screen('Экипировка_предметаNO')

    def dalee3(self, event):
        global necklace_epic, necklace, Luck
        if necklace_epic >= 1:
            if necklace == " ":
                necklace = "necklace_epic"
                Luck += 3
            elif necklace == "necklace_leather":
                necklace = "necklace_epic"
                Luck += 2
            elif necklace == "necklace_cloth":
                necklace = "necklace_epic"
                Luck += 1
            elif necklace == "necklace_legendary":
                necklace = "necklace_epic"
                Luck -= 2
            set_screen('Экипировка_предметаOK')
        else:
            set_screen('Экипировка_предметаNO')

    def dalee4(self, event):
        global necklace_legendary, necklace, Luck
        if necklace_legendary >= 1:
            if necklace == " ":
                necklace = "necklace_legendary"
                Luck += 5
            elif necklace == "necklace_leather":
                necklace = "necklace_legendary"
                Luck += 4
            elif necklace == "necklace_cloth":
                necklace = "necklace_legendary"
                Luck += 3
            elif necklace == "necklace_epic":
                necklace = "necklace_legendary"
                Luck += 2
            set_screen('Экипировка_предметаOK')
        else:
            set_screen('Экипировка_предметаNO')

    def in_leave(self):
        self.add_widget.clear_widgets()


class EquipmentRing(Screen):
    def __init__(self, **kw):
        super(EquipmentRing, self).__init__(**kw)

    def on_enter(self):
        Equipment = FloatLayout()
        Equipment.add_widget(Button(text="<-- В главное меню",
                                    background_color=[185 / 255, 145 / 255, 75 / 255, 1],
                                    font_size=20,
                                    color=[62 / 255, 28 / 255, 0 / 255, 1],
                                    size_hint=(.9, .1), pos=(27, 610),
                                    background_normal="", on_press=lambda x: set_screen('Главное_меню')))
        Equipment.add_widget(Label(text="Выберите, что вы хотите экипировать:\n\n\n\n\n\n\n\n\n\n\n\n\n\n",
                                   font_size=25,
                                   color=[62 / 255, 28 / 255, 0 / 255, 1]))
        Equipment.add_widget(Button(text="Простое кольцо",
                                    background_color=[180 / 255, 140 / 255, 75 / 255, 1],
                                    font_size=20, color=[62 / 255, 28 / 255, 0 / 255, 1], background_normal="",
                                    size_hint=(.8, .1), pos=(60, 400),
                                    on_press=self.dalee1))
        Equipment.add_widget(Button(text="Кольцо с малым кристаллом",
                                    background_color=[180 / 255, 140 / 255, 75 / 255, 1],
                                    font_size=20, color=[62 / 255, 28 / 255, 0 / 255, 1], background_normal="",
                                    size_hint=(.8, .1), pos=(60, 300),
                                    on_press=self.dalee2))
        Equipment.add_widget(Button(text="Кольцо с драгоценным камнем",
                                    background_color=[180 / 255, 140 / 255, 75 / 255, 1],
                                    font_size=20, color=[62 / 255, 28 / 255, 0 / 255, 1], background_normal="",
                                    size_hint=(.8, .1), pos=(60, 200),
                                    on_press=self.dalee3))
        Equipment.add_widget(Button(text="Кольцо с магическим камнем",
                                    background_color=[180 / 255, 140 / 255, 75 / 255, 1],
                                    font_size=20, color=[62 / 255, 28 / 255, 0 / 255, 1], background_normal="",
                                    size_hint=(.8, .1), pos=(60, 100),
                                    on_press=self.dalee4))
        self.add_widget(Equipment)

    def dalee1(self, event):
        global ring_leather, ring, Strenght
        if ring_leather >= 1:
            if ring == " ":
                ring = "ring_leather"
                Strenght += 1
            elif ring == "ring_cloth":
                ring = "ring_leather"
                Strenght -= 1
            elif ring == "ring_epic":
                ring = "ring_leather"
                Strenght -= 2
            elif ring == "ring_legendary":
                ring = "ring_leather"
                Strenght -= 4
            set_screen('Экипировка_предметаOK')
        else:
            set_screen('Экипировка_предметаNO')

    def dalee2(self, event):
        global ring_cloth, ring, Strenght
        if ring_cloth >= 1:
            if ring == " ":
                ring = "ring_cloth"
                Strenght += 2
            elif ring == "ring_leather":
                ring = "ring_cloth"
                Strenght += 1
            elif ring == "ring_epic":
                ring = "ring_cloth"
                Strenght -= 1
            elif ring == "ring_legendary":
                ring = "ring_cloth"
                Strenght -= 3
            set_screen('Экипировка_предметаOK')
        else:
            set_screen('Экипировка_предметаNO')

    def dalee3(self, event):
        global ring_epic, ring, Strenght
        if ring_epic >= 1:
            if ring == " ":
                ring = "ring_epic"
                Strenght += 3
            elif ring == "ring_leather":
                ring = "ring_epic"
                Strenght += 2
            elif ring == "ring_cloth":
                ring = "ring_epic"
                Strenght += 1
            elif ring == "ring_legendary":
                ring = "ring_epic"
                Strenght -= 2
            set_screen('Экипировка_предметаOK')
        else:
            set_screen('Экипировка_предметаNO')

    def dalee4(self, event):
        global ring_legendary, ring, Strenght
        if ring_legendary >= 1:
            if ring == " ":
                ring = "ring_legendary"
                Strenght += 5
            elif ring == "ring_leather":
                ring = "ring_legendary"
                Strenght += 4
            elif ring == "ring_cloth":
                ring = "ring_legendary"
                Strenght += 3
            elif ring == "ring_epic":
                ring = "ring_legendary"
                Strenght += 2
            set_screen('Экипировка_предметаOK')
        else:
            set_screen('Экипировка_предметаNO')

    def in_leave(self):
        self.add_widget.clear_widgets()


class EquipmentWeapon(Screen):
    def __init__(self, **kw):
        super(EquipmentWeapon, self).__init__(**kw)

    def on_enter(self):
        Equipment = FloatLayout()
        Equipment.add_widget(Button(text="<-- В главное меню",
                                    background_color=[185 / 255, 145 / 255, 75 / 255, 1],
                                    font_size=20,
                                    color=[62 / 255, 28 / 255, 0 / 255, 1],
                                    size_hint=(.9, .1), pos=(27, 610),
                                    background_normal="", on_press=lambda x: set_screen('Главное_меню')))
        Equipment.add_widget(Label(text="Выберите, что вы хотите экипировать:\n\n\n\n\n\n\n\n\n\n\n\n\n\n",
                                   font_size=25,
                                   color=[62 / 255, 28 / 255, 0 / 255, 1]))
        Equipment.add_widget(Button(text="Обычный клинок",
                                    background_color=[180 / 255, 140 / 255, 75 / 255, 1],
                                    font_size=20, color=[62 / 255, 28 / 255, 0 / 255, 1], background_normal="",
                                    size_hint=(.8, .1), pos=(60, 400),
                                    on_press=self.dalee1))
        Equipment.add_widget(Button(text="Оружие из прочного железа",
                                    background_color=[180 / 255, 140 / 255, 75 / 255, 1],
                                    font_size=20, color=[62 / 255, 28 / 255, 0 / 255, 1], background_normal="",
                                    size_hint=(.8, .1), pos=(60, 300),
                                    on_press=self.dalee2))
        Equipment.add_widget(Button(text="Стальной меч",
                                    background_color=[180 / 255, 140 / 255, 75 / 255, 1],
                                    font_size=20, color=[62 / 255, 28 / 255, 0 / 255, 1], background_normal="",
                                    size_hint=(.8, .1), pos=(60, 200),
                                    on_press=self.dalee3))
        Equipment.add_widget(Button(text="Оружие из зачарованной углеродной стали",
                                    background_color=[180 / 255, 140 / 255, 75 / 255, 1],
                                    font_size=20, color=[62 / 255, 28 / 255, 0 / 255, 1], background_normal="",
                                    size_hint=(.8, .1), pos=(60, 100),
                                    on_press=self.dalee4))
        self.add_widget(Equipment)

    def dalee1(self, event):
        global weapon_epic, weapon, Strenght
        if weapon_leather >= 1:
            if weapon == " ":
                weapon = "weapon_leather"
                Strenght += 1
            elif weapon == "weapon_cloth":
                weapon = "weapon_leather"
                Strenght -= 1
            elif weapon == "weapon_epic":
                weapon = "weapon_leather"
                Strenght -= 2
            elif weapon == "weapon_legendary":
                weapon = "weapon_leather"
                Strenght -= 4
            set_screen('Экипировка_предметаOK')
        else:
            set_screen('Экипировка_предметаNO')

    def dalee2(self, event):
        global weapon_cloth, weapon, Strenght
        if weapon_cloth >= 1:
            if weapon == " ":
                weapon = "weapon_cloth"
                Strenght += 2
            elif weapon == "weapon_leather":
                weapon = "weapon_cloth"
                Strenght += 1
            elif weapon == "weapon_epic":
                weapon = "weapon_cloth"
                Strenght -= 1
            elif weapon == "weapon_legendary":
                weapon = "weapon_cloth"
                Strenght -= 3
            set_screen('Экипировка_предметаOK')
        else:
            set_screen('Экипировка_предметаNO')

    def dalee3(self, event):
        global weapon_epic, weapon, Strenght
        if weapon_epic >= 1:
            if weapon == " ":
                weapon = "weapon_epic"
                Strenght += 3
            elif weapon == "weapon_leather":
                weapon = "weapon_epic"
                Strenght += 2
            elif weapon == "weapon_cloth":
                weapon = "weapon_epic"
                Strenght += 1
            elif weapon == "weapon_legendary":
                weapon = "weapon_epic"
                Strenght -= 2
            set_screen('Экипировка_предметаOK')
        else:
            set_screen('Экипировка_предметаNO')

    def dalee4(self, event):
        global weapon_legendary, weapon, Strenght
        if weapon_legendary >= 1:
            if weapon == " ":
                weapon = "weapon_legendary"
                Strenght += 5
            elif weapon == "weapon_leather":
                weapon = "weapon_legendary"
                Strenght += 4
            elif weapon == "weapon_cloth":
                weapon = "weapon_legendary"
                Strenght += 3
            elif weapon == "weapon_epic":
                weapon = "weapon_legendary"
                Strenght += 2
            set_screen('Экипировка_предметаOK')
        else:
            set_screen('Экипировка_предметаNO')

    def in_leave(self):
        self.add_widget.clear_widgets()


# _______________________________________________________________________________________________________
# Конец блока по экипировке предметов
# _______________________________________________________________________________________________________


def set_screen(name_screen):
    sm.current = name_screen


sm = ScreenManager()
sm.add_widget(Main_menu(name='Главное_меню'))
sm.add_widget(History(name="История"))
sm.add_widget(Rules(name="Правила"))
sm.add_widget(My_character(name="Мой_персонаж"))
sm.add_widget(N0_class(name="Нет_класса"))
sm.add_widget(Election_class(name="Выбор_класса"))
sm.add_widget(Beginning_Wizard(name="Начало_пути_маг"))
sm.add_widget(Beginning_Assassin(name="Начало_пути_убийца"))
sm.add_widget(Beginning_Warrior(name="Начало_пути_воин"))
sm.add_widget(Beginning_Guard(name="Начало_пути_страж"))
sm.add_widget(Settings(name="Настройки"))
sm.add_widget(Shop(name="Магазин"))
sm.add_widget(N0_money(name="Нет_средств"))
sm.add_widget(Difficulty_is_set(name="Сложность_установлена"))
sm.add_widget(LovyshkaOFF(name="1"))
sm.add_widget(Viktorina1(name="2"))
sm.add_widget(Viktorina1T(name="2.1"))
sm.add_widget(Viktorina1F(name="2.2"))
sm.add_widget(Syndyk1(name="3"))
sm.add_widget(Syndyk2(name="3.2"))
sm.add_widget(LovyshkaON(name="4"))
sm.add_widget(Magazin1(name="5"))
sm.add_widget(Magazin2(name="5.2"))
sm.add_widget(N0_money2(name="Нет_средств2"))
sm.add_widget(Ozero(name="6"))
sm.add_widget(Ozero2(name="6.2"))
sm.add_widget(Kamnepad(name="7"))
sm.add_widget(Molniya(name="8"))
sm.add_widget(MolniyaON(name="8.1"))
sm.add_widget(MolniyaOFF(name="8.2"))
sm.add_widget(Stretched_Threads(name="9"))
sm.add_widget(Stretched_ThreadsON(name="9.1"))
sm.add_widget(Stretched_ThreadsOFF(name="9.2"))
sm.add_widget(Abandoned_House(name="10"))
sm.add_widget(Abandoned_House2(name="10.2"))
sm.add_widget(Hole_in_Wall(name="11"))
sm.add_widget(Hole_in_Wall2(name="11.2"))
sm.add_widget(Viktorina2(name="12"))
sm.add_widget(Viktorina2T(name="12.1"))
sm.add_widget(Viktorina2F(name="12.2"))
sm.add_widget(Viktorina3(name="13"))
sm.add_widget(Viktorina3T(name="13.1"))
sm.add_widget(Viktorina3F(name="13.2"))
sm.add_widget(Viktorina4(name="14"))
sm.add_widget(Viktorina4T(name="14.1"))
sm.add_widget(Viktorina4F(name="14.2"))
sm.add_widget(Viktorina5(name="15"))
sm.add_widget(Viktorina5T(name="15.1"))
sm.add_widget(Viktorina5F(name="15.2"))
sm.add_widget(Syndyk3(name="16"))
sm.add_widget(Syndyk3_2(name="16.1"))
sm.add_widget(Syndyk4(name="17"))
sm.add_widget(Syndyk5(name="18"))
sm.add_widget(Syndyk6(name="19"))
sm.add_widget(Syndyk6_2(name="19.1"))
sm.add_widget(Magaz2(name="20"))
sm.add_widget(Magaz2_1(name="20.1"))
sm.add_widget(N0_money3(name="Нет_средств3"))
sm.add_widget(Magaz3(name="21"))
sm.add_widget(Magaz3_2(name="21.1"))
sm.add_widget(N0_money4(name="Нет_средств4"))
sm.add_widget(Predislovie(name="22"))
sm.add_widget(Predislovie2(name="23"))
sm.add_widget(Predislovie3(name="24"))
sm.add_widget(Predislovie(name="25"))
sm.add_widget(Predislovie2(name="26"))
sm.add_widget(Predislovie3(name="27"))
sm.add_widget(Mob(name="Моб"))
sm.add_widget(Battle_Assasin(name="Бой_убийцы"))
sm.add_widget(NoRunAssasin(name="Не_сбежал_убийца"))
sm.add_widget(You_struck_blow_Assasin(name="Вы_нанесли_удар_убийца"))
sm.add_widget(Drink_potion_Assasin(name="Выпить_зелье_убийца"))
sm.add_widget(Battle_Wizard(name="Бой_мага"))
sm.add_widget(NoRunWizard(name="Не_сбежал_маг"))
sm.add_widget(You_struck_blow_Wizard(name="Вы_нанесли_удар_маг"))
sm.add_widget(Drink_potion_Wizard(name="Выпить_зелье_маг"))
sm.add_widget(Battle_Warrior(name="Бой_воина"))
sm.add_widget(NoRunWarrior(name="Не_сбежал_воин"))
sm.add_widget(You_struck_blow_Warrior(name="Вы_нанесли_удар_воин"))
sm.add_widget(Drink_potion_Warrior(name="Выпить_зелье_воин"))
sm.add_widget(Battle_Guard(name="Бой_стража"))
sm.add_widget(NoRunGuard(name="Не_сбежал_страж"))
sm.add_widget(You_struck_blow_Guard(name="Вы_нанесли_удар_страж"))
sm.add_widget(Drink_potion_Guard(name="Выпить_зелье_страж"))
sm.add_widget(You_win(name="Вы_победили"))
sm.add_widget(Game_Over(name="Конец_Игры"))
sm.add_widget(Game_Over_Kill(name="Конец_Игры_Умер"))
sm.add_widget(Equipment(name="Экипировка_предмета"))
sm.add_widget(EquipmentNO(name="Экипировка_предметаNO"))
sm.add_widget(EquipmentOK(name="Экипировка_предметаOK"))
sm.add_widget(EquipmentHelmet(name="Экипировка_шлема"))
sm.add_widget(EquipmentBib(name="Экипировка_нагрудника"))
sm.add_widget(EquipmentPants(name="Экипировка_штанов"))
sm.add_widget(EquipmentBoots(name="Экипировка_сапог"))
sm.add_widget(EquipmentNecklace(name="Экипировка_ожерелья"))
sm.add_widget(EquipmentRing(name="Экипировка_кольца"))
sm.add_widget(EquipmentWeapon(name="Экипировка_оружия"))



class Андердарк(App):
    def __init__(self, **kwargs):
        super(Андердарк, self).__init__(**kwargs)
        self.config = ConfigParser()

    def build_config(self, config):
        config.adddefaultsection('General')
        config.setdefault('General', 'user_data', '{}')

    def set_value_from_config(self):
        self.config.read(os.path.join(self.directory, '%(appname)s.ini'))
        self.user_data = ast.literal_eval(self.config.get(
            'General', 'user_data'))

    def get_application_config(self):
        self.config.read(os.path.join(self.directory, '%(appname)s.ini'))
        self.user_data = ast.literal_eval(self.config.get('General', 'user_data'))

    def build(self):
        return sm


if __name__ == '__main__':
    Андердарк().run()