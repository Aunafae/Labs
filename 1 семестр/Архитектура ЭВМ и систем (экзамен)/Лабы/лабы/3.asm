.model small

data segment
a db 70h            ;112(d)
b db 2Ah            ;42(d)
nod db 0
data ends

kod segment
assume DS: data, CS: kod
begin:

mov ax, data
mov ds, ax
xor ax, ax


mov dl, a           ;dl = 70(h) = 112(d)
mov ah, b           ;ah = 2A(h) = 42(d)

mov cx, 3

delitel:
mov bl, dl
mov dl, ah
mov ax, bx
div dl
LOOP delitel

mov cl, dl          ;cl = 0E(h) = 14(d)
xor ax, ax
xor bx, bx
xor dx, dx

mov bl, cl          ;bl = 0E(h) = 14(d)
mov bh, 2           ;bh = 02(h) = 2(d)

mov cx, 4

start:
mov al, bl
div bh
add dl, ah
SHR bl, 1
LOOP start

mov ah, 4ch
int 21h
kod ends
end begin
end