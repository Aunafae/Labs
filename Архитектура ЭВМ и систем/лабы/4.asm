.model small

data segment
mass dw 18 dup (0, 1)
maxc dw 0
minc dw 1000
data ends

kod segment
assume DS: data, CS: kod
begin:

mov ax, data
mov ds, ax
xor ax, ax

mov cx, 16               ;нам нужно только 16 повторений (т.к. 0 и 1 уже есть в массиве)
povtor:
mov ax, mass[si+2]       ;в регистр ax поместить значение следующего элемента массива
add ax, mass[si]         ;сложить следующий элемент с текущим
mov mass[si+4], ax       ;в элемент после следующего поместить значение регистра ax
inc si
inc si                   ;увеличили индекс массива на 2
LOOP povtor

; 0  1  1   2   3   5  
; 8  D  15  22  37  59 
; 90 E9 179 262 3DB 63D

xor si, si
mov bx, minc

mov cx, 6                ;6 повторений, т.к. в строке 6 элементов массива
minimymi:
inc si
inc si
mov dx, mass[si+10]      ;записываем в регистр dx элемент массива
mov ch, 2
mov ax, dx
div ch                   ;проверяем его на чётность
xor ch, ch
cmp ah, ch
JE nachalo               ;если чётный, то идём в начало
cmp dx, bx               ;если нечётный, то сравниваем элемент массива со значением минимума
JGE nachalo              ;если больше или равно, то идём в начало
mov bx, dx               ;если меньше, то присваиваем переменной minc значение регистра dx
nachalo:
LOOP minimymi

xor si, si
mov bx, maxc

mov cx, 3                ;3 повторения, т.к. имеется только 3 столбца
maksimymi:
mov ax, mass[si+6]       ;записываем в регистр ax элемент массива
ROR ax, 1                ;сдвигаем вправо для проверки чётности
JC konez                 ;если нечётный, то идём в конец
mov dx, mass[si+6]       ;если чётный, то записываем в регистр dx элемент массива
cmp dx, bx               ;сравниваем его со значением максимума
JLE konez                ;если меньше, то идём в конец
mov bx, dx               ;если больше, то присваиваем переменной minc значение регистра dx
konez:
mov dx, cx
mov cx, 12
sm:
inc si
LOOP sm
mov cx, dx
LOOP maksimymi

mov ah, 4ch
int 21h
kod ends
end begin
end