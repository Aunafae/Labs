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

lea si, skobki    ;��������� ����� ������ ������ � ������� si

elements:
mov al, [si]      ;� ������� al �������� ������� ������
inc si

cmp al, '('       ;���������� ������� �� ��������
je open           ;���� �������������, ��������� � open
cmp al, '{'
je open
cmp al, '['
je open

cmp al, ')'
je close          ;���� �������������, ��������� � close
cmp al, '}'
je close
cmp al, ']'
je close

jmp test5

open:
inc cx            ;������� += 1
push ax           ;�������� ������ � ����
jmp elements      ;��������� � ���������� �������� ������

close:
cmp cx, 0         ;��������, ����� �� � �����
jne test1         ;���� ���, �� ������� � test1
mov result, 3     ;����� ������ ������������� ������
jmp elements      ;��������� � ���������� �������� ������

test1:
dec cx            ;���������� �������� �� 1
pop bx            ;���������� ������ �� �����

cmp bl, '('       ;�������� �� ���������� ������������� � ������������� ������
jne test2         ;���� �� ��� ������, ��������� ������
cmp al, ')'       ;���� ������������� ������
je elements       ;��������� ��������� �������

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
mov result, 1     ;�������������� ������
cmp cx, 0         ;���� ���� ����
je check          ;������� � check

test5:
mov result, 2     ;���� ���, �� �� ��� ������ �������

check: 
cmp result, 1     ;���� ������ � �������������� ������
je searching      ;�� ������� � searching   
jmp exit          ;����� �� �����

searching:
cmp bl, '('       ;����, ����� ������ �� �������
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
mov dl, ')'        ;���������� ������ ������ � ������� bl
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