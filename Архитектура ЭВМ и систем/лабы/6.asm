.model small                    ;создание структуры

Patients STRUC
number dw 0
gender db 0
birth dw 0
admission db 8 dup('/')
discharge db 8 dup('/')
Patients ENDS

data segment
massiv Patients <83,'m',1995,'11.11.22','23.11.22'>,<48,'w',2000,'10.09.22','22.09.22'>,<15,'m',2003,'22.09.22','29.09.22'>
date db '22.09.22'
nomer dw 15
year dw 1995
data ends

kod segment
assume DS: data, CS: kod
begin:

mov ax, data
mov ds, ax
xor ax, ax

mov bx, type Patients            ;перемещение размера структуры в bx
;_________________________________________________________________________________________________________________________
;КОЛИЧЕСТВО ПАЦИЕНТОВ, ПОСТУПИВШИХ НА КОНКРЕТНУЮ ДАТУ

mov cx, 3
lea di, massiv[0].admission     
mov dx, 0                        ;количество пациентов, поступивших 22.09.22

CALL sravnenie

;_________________________________________________________________________________________________________________________
;КОЛИЧЕСТВО ПАЦИЕНТОВ-ЖЕНЩИН, ВЫПИСАННЫХ В КОНКРЕТНУЮ ДАТУ

mov cx, 3  
lea di, massiv[0].gender   
mov dx, 0                        ;количество пациентов, выписавшхся 22.09.22

gender_pr:
mov ah, 'w'
mov al, [di]
cmp ah, al
JNE vix
CALL sravn
vix:
add di, bx                       ;переход к началу даты в следующем сегменте структуры
LOOP gender_pr

;__________________________________________________________________________________________________________________________
;НАЙТИ ГОД РОЖДЕНИЯ ПАЦИЕНТА ПО НОМЕРУ МЕДКАРТЫ

mov cx, 3  
lea di, massiv[0].number   
mov dx, 0                      

medk:
mov ax, nomer
mov dx, [di]
cmp ax, dx
JNE konez
add di, 3
mov dx, [di]                     ;7D3(h) = 2003(d)
mov nomer, dx
sub di, 3
konez:
add di, bx                       ;переход к началу даты в следующем сегменте структуры
LOOP medk

;___________________________________________________________________________________________________________________________
;НАЙТИ КОЛИЧЕСТВО ПАЦИЕНТОВ МУЖСКОГО ПОЛА ПО УКАЗАННОМУ ГОДУ РОЖДЕНИЯ

mov cx, 3  
lea di, massiv[0].birth 
lea si, massiv[0].gender  
mov dx, 0                      

god_r:
mov ax, year
mov dx, [di]
cmp ax, dx
JNE kz

mov al, 'm'
mov ah, [si]
JNE kz
mov dx, 1
push dx

kz:
add di, bx                       ;переход к началу даты в следующем сегменте структуры
add si, bx
LOOP god_r

pop dx

;___________________________________________________________________________________________________________________________

mov ah, 4ch
int 21h

sravnenie proc near
m1:
push cx
mov cx, 8                        ;посимвольное сравнение строк из 8 символов, начала которых расположены в DI и SI
lea si, date                     ;для работы процедуры помещаем адреса начал сравниваемых

pov:
mov ah, [si]
mov al, [di]
cmp ah, al
JNE exit
inc si
inc di
LOOP pov
inc dx
sub di, 8

exit:
pop cx
add di, bx                       ;переход к началу даты в следующем сегменте структуры
LOOP m1
ret
sravnenie endp

sravn proc near
add di, 11
m2:
push cx
mov cx, 8                        ;посимвольное сравнение строк из 8 символов, начала которых расположены в DI и SI
lea si, date                     ;для работы процедуры помещаем адреса начал сравниваемых

pvt:
mov ah, [si]
mov al, [di]
cmp ah, al
JNE vixod
inc si
inc di
LOOP pvt
inc dx
sub di, 8

vixod:
pop cx
sub di, 11
ret
sravn endp

kod ends
end begin