.model large

data segment
nomera db 42 dup(' ')

odin dw ' '
dwa dw ' '
tri dw ' '
chetire dw ' '
pyat dw ' '
shest dw ' '
sem dw ' '

count_even db 0
count_odd db 0

;Просьба ввода
request db 16, "Please, enter 7 two-byte numbers!", 10, '$'
request2 db 16, "Because the numbers are two-byte, please don't write a number more than 65535!", 10, '$'
request3 db 16, "After writing the number, press <space>", 10, '$'

stroka db ' ', "         ", 10, '$'

;Чётные числа
even_nch db ' ', " Even-number elements:  "
even_mass db 50 dup(' ')
even_kz db " ", 10, '$'
	
;Сумма чётых чисел (чётна/нечётна)
Sum_even_nch db '    ', " The sum of the even-numbers: "
Sum_even_mass db 4 dup('/')
Sum_even_kz db " ", 10, '$'

;Произведение чётых чисел (чётно/нечётно)
Pr_even_nch db '    ', " The product of even-numbers: "
Pr_even_mass db 4 dup('/')
Pr_even_kz db " ", 10, '$'

;Нечётные числа
odd_nch db ' ', " Odd-number elements:  "
odd_mass db 50 dup(' ')
odd_kz db " ", 10, '$'
	
;Сумма нечётых чисел (чётна/нечётна)
Sum_odd_nch db '    ', " The sum of the odd-numbers: "
Sum_odd_mass db 4 dup('/')
Sum_odd_kz db " ", 10, '$'

;Произведение нечётых чисел (чётно/нечётно)
Pr_odd_nch db '    ', " The product of odd-numbers: "
Pr_odd_mass db 4 dup('/')
Pr_odd_kz db " ", 10, '$'

;Посимвольный ввод
one db " 1 number   ", 16, " $"
two db " 2 number   ", 16, " $"
three db " 3 number   ", 16, " $"
four db " 4 number   ", 16, " $"
five db " 5 number   ", 16, " $"
six db " 6 number   ", 16, " $"
seven db " 7 number   ", 16, " $"
data ends

kod segment
assume DS: data, CS: kod
begin:
mov ax, data
mov ds, ax
xor ax, ax

lea dx, request 
mov ah, 9
int 21h

lea dx, request2 
mov ah, 9
int 21h

lea dx, request3 
mov ah, 9
int 21h

;__________________________________________________
;Ввод чисел

mov si, 0
lea dx, one
mov ah, 9
int 21h
call inp
mov odin, bx

mov si, 6
lea dx, two
mov ah, 9
int 21h
call inp
mov dwa, bx

mov si, 11
lea dx, three
mov ah, 9
int 21h
call inp
mov tri, bx

mov si, 16
lea dx, four
mov ah, 9
int 21h
call inp
mov chetire, bx

mov si, 21
lea dx, five
mov ah, 9
int 21h
call inp
mov pyat, bx

mov si, 26
lea dx, six
mov ah, 9
int 21h
call inp
mov shest, bx

mov si, 31
lea dx, seven
mov ah, 9
int 21h
call inp
mov sem, bx

;__________________________________________________
;Проверка на чётность/нечётность чисел

xor ax, ax
mov di, 0
mov dx, 0

mov si, 0
mov ax, odin
call proverka 

mov si, 6
mov ax, dwa
call proverka 

mov si, 11
mov ax, tri
call proverka 

mov si, 16
mov ax, chetire
call proverka 

mov si, 21
mov ax, pyat
call proverka 

mov si, 26
mov ax, shest
call proverka 

mov si, 31
mov ax, sem
call proverka 

mov si, 0
mov di, 0

;__________________________________________________
;Проверка на чётность/нечётность суммы и произведения

xor ax, ax
mov al, count_even
mov Sum_even_mass[0], 'e'  ;сумма чётных цифр всегда чётно
mov Sum_even_mass[1], 'v'
mov Sum_even_mass[2], 'e'
mov Sum_even_mass[3], 'n'
mov Pr_even_mass[0], 'e'    ;произведение чётных цифр всегда чётно
mov Pr_even_mass[1], 'v'
mov Pr_even_mass[2], 'e'
mov Pr_even_mass[3], 'n'

xor ax, ax
mov al, count_odd
mov Pr_odd_mass[0], 'o'    ;произведение нечётных цифр всегда нечётно
mov Pr_odd_mass[1], 'd'
mov Pr_odd_mass[2], 'd'
mov Pr_odd_mass[3], ' '
RCR al, 1
JC nechotn
mov Sum_odd_mass[0], 'e'
mov Sum_odd_mass[1], 'v'
mov Sum_odd_mass[2], 'e'
mov Sum_odd_mass[3], 'n'
JMP konezx
nechotn:
mov Sum_odd_mass[0], 'o'
mov Sum_odd_mass[1], 'd'
mov Sum_odd_mass[2], 'd'
mov Sum_odd_mass[3], ' '
konezx:

;__________________________________________________
;Вывод сведений о чётности и нечётности элементов
;И о чётности/нечётности их суммы и произведения

lea dx, stroka 
mov ah, 9
int 21h

lea dx, even_nch 
mov ah, 9
int 21h

lea dx, Sum_even_nch 
mov ah, 9
int 21h

lea dx, Pr_even_nch 
mov ah, 9
int 21h

lea dx, odd_nch 
mov ah, 9
int 21h

lea dx, Sum_odd_nch 
mov ah, 9
int 21h

lea dx, Pr_odd_nch 
mov ah, 9
int 21h

;__________________________________________________
;конец программы

mov ah, 4ch
int 21h

;__________________________________________________
;Процедура ввода числа

inp proc near
mov ah, 1h
int 21h
mov bl, al
mov nomera[si], bl
inc si
sub bl, 30h

mov ah, 1h
int 21h
cmp al, 32
JE ch2
cmp al, 0
JE ch2
mov bh, al
mov nomera[si], bh
inc si
sub bh, 30h
mov al, bl
mov bl, 10
mul bl
add al, bh

mov bx, ax
mov ah, 1h
int 21h
cmp al, 32
JE ch1
cmp al, 0
JE ch1
mov bh, al
mov nomera[si], bh
inc si
sub bh, 30h
mov al, bl
mov bl, 10
mul bl
add al, bh
mov bx, ax
JMP ch3

ch2:
JMP ch1

ch3:
mov cx, ax
mov ah, 1h
int 21h
cmp al, 32
JE ch1
cmp al, 0
JE ch1
xor bx, bx
mov bl, al
mov nomera[si], bl
inc si
sub bl, 30h
mov ax, cx
mov cx, 0010
mul cx
add ax, bx
mov bx, ax

mov cx, ax
mov ah, 1h
int 21h
cmp al, 32
JE ch1
cmp al, 0
JE ch1
xor bx, bx
mov bl, al
mov nomera[si], bl
inc si
sub bl, 30h
mov ax, cx
mov cx, 0010
mul cx
add ax, bx
mov bx, ax

mov cx, ax
mov ah, 1h
int 21h
cmp al, 32
JE ch1
JMP ch1

ch1:

mov ah, ' '
mov nomera[si], ah
mov ah, 2h
mov dl, 0dh
int 21h
mov ah, 2h
mov dl, 0ah
int 21h
              
xor ax,ax   

ret
inp endp

;Конец процедуры ввода числа
;__________________________________________________

;__________________________________________________
;Процедура проверки чётности

proverka proc near

RCR ax, 1
JC nechetn1

mov cx, 5
pomogite:
mov al, nomera[si]
cmp al, 32
JE vixod1
cmp al, 0
JE vixod1
cmp al, 65
JE vixod1
mov even_mass[di], al
inc si
inc di
LOOP pomogite
vixod1:
mov even_mass[di], ' '
inc di
inc count_even 
JMP kz1

nechetn1:
mov bx, di
mov di, dx
mov cx, 5
pamagiti:
mov al, nomera[si]
cmp al, 32
JE vixod2
cmp al, 0
JE vixod2
cmp al, 65
JE vixod2
mov odd_mass[di], al
inc si
inc di
LOOP pamagiti
vixod2:
mov odd_mass[di], ' '
inc di
inc count_odd
mov dx, di
mov di, bx
kz1:

ret
proverka endp

;Конец процедуры проверки чётности
;__________________________________________________

kod ends
end begin
ends