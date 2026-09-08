.model small

steck segment
dw 5 dup (' ')
steck ends

data segment
massiv db 5,3,1,8,9,4,2,6 
nyli db 8 dup (0)
data ends

kod segment
assume DS: data, CS: kod
begin:

mov ax, data
mov ds, ax
xor ax, ax

CALL sortirovka

mov ah, massiv[si]              ;вывели элементы массива в регистры по порядку, чтобы проверить
mov al, massiv[si+1]
mov bh, massiv[si+2]
mov bl, massiv[si+3]
mov ch, massiv[si+4]
mov cl, massiv[si+5]
mov dh, massiv[si+6]
mov dl, massiv[si+7]

mov ah, 4ch                     ;конец кода
int 21h

sortirovka proc near

povtor:
mov bx, 7                       ;записываем 7 для проверки сортировки

mov cx, 7                       ;цикл выполнится 7 раз, т.к. сравниваем 8 чисел между собой
nachalo:
mov ah, massiv[si]
cmp ah, massiv[si+1]
JBE konez                       ;если OPR1 <= OPR2, то идём в конец и вычитаем единицу из 7
mov bx, 10                      ;присваиваем 10, чтобы bl != bh
mov al, [si+1]
xchg ah, al                     ;если OPR1 > OPR2, то меняем их местами и записываем в массив
mov massiv[si], ah
mov massiv[si+1], al
konez:
dec bx
inc si
LOOP nachalo

xor si, si
cmp bl, bh                      ;сравниваем регистры для проверки
JNE povtor                      ;если не равны, начинаем сначала

;_______________________________________________________________________________________________________
;Работа счётчика bx: изначально помещаем туда цифру 7, она уменьшается на "1" каждый раз, когда
;OPR1 <= OPR2, т.е. каждый раз, когда нам не приходится менять местами элементы массива, перезаписывая
;их. Если мы 7 раз подряд пройдём проверку (все 7 раз OPR1 <= OPR2), то регистр bx будет равен 0
;это означает конец повторений. 
;Если хотя бы 1 раз из 7 мы не пройдём проверку, то регистру bx будет присвоено значение 10, в таком
;случае мы не сможем за 7 повторений получить в регистре bx "0" и цикл начнётся сначала.
;_______________________________________________________________________________________________________

ret
sortirovka endp

kod ends
end begin
end
