.model small

steck segment stack "stack"
db 100 dup('$')
steck ends

data segment
nomber1 dw 3h
nomber2 dw 3h
result1 dw (?)
result2 dw (?)
data ends

kod segment
assume SS: steck, DS: data, CS: kod
begin:

mov ax, data
mov ds, ax
xor ax, ax

mov ax, word ptr nomber1        ;сделать копию значения
push ax                         ;запись в стек аргумента
CALL factorial 
mov result1, ax                 ;помещаем результат в переменную result1
pop ax                          ;очищаем стек, забирая аргумент в регистр ax

mov ax, offset nomber2          ;помещаем относительный адрес переменной в ax
push ax                         ;запись в стек аргумента
CALL factorial 
mov result2, ax                 ;помещаем результат в переменную result1
pop ax                          ;очищаем стек, забирая аргумент в регистр ax


mov ax, result1                 ;выводим result1 и result2 в регистры ax и bx
mov bx, result2

mov ah, 4ch
int 21h




;______________________________________________
;Процедура нахождения факториала

factorial proc near

push bp
mov bp, sp
mov ax, [bp+4]                   ;доступ к аргументу по адресу nomber1 для процедуры

mov cx, [bp+4]
dec cx

mov bx, [bp+4]
povtor:
dec bx
mul bx
LOOP povtor

mov sp, bp                        ;восстановление значения регистра sp
pop bp                            ;восстановление значения старого bp

ret
factorial endp

;Конец процедуры нахождения факториала
;_______________________________________________

kod ends
end begin
ends
