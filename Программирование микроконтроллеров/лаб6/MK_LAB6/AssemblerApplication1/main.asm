.include "m1280def.inc"

//r16-r31 часто используемые регистры для временных данных
.def lightmask = r20
.def delayHigh = r21
.def delayLow = r22
.def currDelayHigh = r23
.def currDelayLow = r24
.def flagOn = r25
.def type = r26
.def speed = r27
.cseg

start:
	ldi r16, 0xFF 
	out DDRF, r16
	ldi r16, 0x00 
	out PORTF, r16
	ldi r16, 0x00 
	out DDRD, r16
	ldi r16, 0x07 
	out PORTD, r16
	
	ldi lightmask, 0xFF
	ldi delayHigh, 19
	ldi delayLow, 136

	clr flagOn
	clr type
	clr speed
	clr currDelayHigh 
	clr currDelayLow

	rjmp loop


loop:
	sbis PIND, 0
		rcall switchOn
	sbis PIND, 1
		rcall switchType
	sbis PIND, 2
		rcall changeSpeed

	rcall animateEffect

	mov r16, lightmask 
	and r16, flagOn
	out PORTF, r16

	rcall delay
	rjmp loop

delay:
	ldi r16, 0xFF
	ldi r17, 0x07

	waitLoop:
	dec r16
	cpi r16, 0 
	brne waitLoop
	
	dec r17
	cpi r17, 0 
	brne waitLoop
	ret

initAnimation:
	ldi currDelayHigh, 0 
	ldi currDelayLow, 0

	checkType:
	cpi type, 0 
	brne checkType1
		ldi lightmask, 0xFF
		rjmp checkEnd

	checkType1:
	cpi type, 1 
	brne checkType2
		ldi lightmask, 0b01101101
		rjmp checkEnd

	checkType2:
	cpi type, 2 
	brne checkEnd
		ldi lightmask, 0
		rjmp checkEnd

	checkEnd:
	
	ret

animateEffect:
	mov r16, speed 
	ldi r17, 2
	mul r16, r17
	inc r16

	cp currDelayLow, r16 
	brge skipDelayCheck
		cpi currDelayHigh, 0 
		breq tickUpdate
			dec currDelayHigh
			sub r16, currDelayLow
			clr currDelayLow

	skipDelayCheck:
	sub currDelayLow, r16
	ret

	tickUpdate:
		
	mov currDelayHigh, delayHigh 
	mov currDelayLow, delayLow

	// обработка эффектов
	typeCheck1:
	cpi type, 1 
	brne typeCheck2
		//2 горит, 1 не горит
		mov r16, lightmask
		ldi r17, 0x03
		and r16, r17

		cpi r16, 3 
		breq animate_type1_no_light0
			lsl r16
			inc r16
			lsl lightmask
			or lightmask, r16
			ret
		animate_type1_no_light0:
			lsl r16

			lsl lightmask
			or lightmask, r16
			ret

	typeCheck2:
	cpi type, 2 brne animate_type_end
		//Зарядка шкалы
		cpi lightmask, 0xFF brne animate_type_check2_full_end
			clr lightmask
		animate_type_check2_full_end:

		lsl lightmask
		mov r16, lightmask
		com r16
		ldi r17, 1
		and r16, r17
		or lightmask, r16
	animate_type_end:

	ret

switchOn:
	switch_on_button_release:
		sbis PIND, 0
		rjmp switch_on_button_release
	com flagOn

	rcall initAnimation
	ret


switchType:
	typeButtonRelease:
		sbis PIND, 1
		rjmp typeButtonRelease

	cpi flagOn, 0 brne typeCheck
		ret
	typeCheck:

	inc type
	cpi type, 3 brne typeReset
		clr type
	typeReset:

	rcall initAnimation
	ret

changeSpeed:
	speedButtonReleased:
		sbis PIND, 2
		rjmp speedButtonReleased

	cpi flagOn, 0 
	brne speedCheck
		ret
	speedCheck:

	inc speed
	cpi speed, 3 
	brne speedReset
		clr speed
	speedReset:

	ret