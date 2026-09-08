.model small

stec segment
db 20 dup (' ')                      ;зарезервировали 20 байт
stec ends

data1 segment
a db 00101100b                       ;44(d) = 2C(h)
data1 ends

data2 segment    
addr dd per2
data2 ends

data3 segment
b db 00110100b                       ;52(d) = 34(h)
data3 ends

;______________________________________________________________

kod1 segment

assume DS: data1, CS: kod1

begin:

jmp far ptr start
per2:

mov ax, data1
mov ds, ax
xor ax, ax

mov bl, a                            ;bl = 2C
ROR bl, 2                            ;bl = B
jmp far ptr per3

kod1 ends

;______________________________________________________________

kod2 segment

assume DS: data3, CS: kod2

per3:

mov ax, data3
mov ds, ax
xor ax, ax

mov bh, b                           ;bh = 34             
ROR bh, 4                           ;bh = 43
jmp far ptr exit
kod2 ends

;_______________________________________________________

kod3 segment

assume CS: kod3

start:

assume DS: data1

mov ax, data1
mov ds, ax
xor ax, ax

mov bl, a                            ;bl = 2C
SHL bl, 1                            ;bl = 58

assume DS: data3
mov ax, data3
mov ds, ax
xor ax, ax 

mov cl, b                            ;cl = 34
SHR cl, 2                            ;cl = D

assume DS: data2
mov ax, data2
mov ds, ax
jmp DS: addr

;_______________________________________________________

exit:

mov ah, 4ch                          ;завершение программы (делаем прерывание)
int 21h
kod3 ends
end begin
end
