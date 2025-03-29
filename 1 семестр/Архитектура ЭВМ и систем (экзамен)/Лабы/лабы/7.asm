.model small

steck segment stack "stack"
dw 20 dup('$')
steck ends

data segment
skobki db "(()){}[][](){}[]()(("
result db (?)
data ends

kod segment
assume SS: steck, DS: data, CS: kod
begin:

mov ax, data
mov ds, ax
xor ax, ax

lea si, skobki    ;загружаем адрес начала строки в регистр si

elements:
mov al, [si]      ;в регистр al помещаем элемент строки
inc si

cmp al, '('       ;сравниваем элемент со скобками
je open           ;если открывающаяся, переходим в open
cmp al, '{'
je open
cmp al, '['
je open

cmp al, ')'
je close          ;если закрывающаяся, переходим в close
cmp al, '}'
je close
cmp al, ']'
je close

jmp test5

open:
inc cx            ;счётчик += 1
push ax           ;помещаем скобку в стек
jmp elements      ;переходим к следующему элементу строки

close:
cmp cx, 0         ;проверка, пусто ли в стеке
jne test1         ;если нет, то переход в test1
mov result, 3     ;иначе лишние закрывающиеся скобки
jmp elements      ;переходим к следующему элементу строки

test1:
dec cx            ;уменьшение счётчика на 1
pop bx            ;извлечение скобки из стека

cmp bl, '('       ;проверка на совпадение открывающейся и закрывающейся скобок
jne test2         ;если не эта скобка, проверяем другие
cmp al, ')'       ;если закрывающаяся скобка
je elements       ;проверяем следующий элемент

test2:
cmp bl, '{'
jne test3
cmp al, '}'
je elements

test3:
cmp bl, '['
jne test4
cmp al, ']'
je elements

test4:
mov result, 1     ;несоответствие скобок
cmp cx, 0         ;если стек пуст
je check          ;переход в check

test5:
mov result, 2     ;если нет, то не все скобки закрыты

check: 
cmp result, 1     ;если ошибка в несоответствии скобок
je searching      ;то переход в searching   
jmp exit          ;иначе на выход

searching:
cmp bl, '('       ;ищем, какой скобки не хватает
je locate1
cmp bl, '{'
je locate2
cmp bl, '['
je locate3
cmp bl, ')'
je locate4
cmp bl, '}'
je locate5
cmp bl, ']'
je locate6
jmp exit

locate1:
mov dl, ')'        ;записываем нужную скобку в регистр bl
jmp exit
locate2:
mov dl, '}'
jmp exit
locate3:
mov dl, ']'
jmp exit
locate4:
mov dl, '('
jmp exit
locate5:
mov dl, '{'
jmp exit
locate6:
mov dl, '['

exit:
xor ax, ax
mov al, result

mov ah, 4ch
int 21h
kod ends
end begin
ends