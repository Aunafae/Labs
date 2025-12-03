#include <avr/io.h>
//#include <util/delay.h>
#include <avr/interrupt.h>

int8_t pressed = 0;
int8_t led = 0xFF;
int8_t turn_on = 0;
int8_t speed = 0;
int8_t mode = 0;
int ticks = 0;

void reset(){
	led = 0;
	if (mode == 0) {
		led = 0xFF;
	}
	if (mode == 1) {
		led = 0b01101101;
	}
	if (mode == 2) {
		led = 0x01;
	}
	ticks = 0;
}

void play(){
	if(ticks > 0) {
		ticks--;
		return;
	}
	
	if (speed == 0) {
		ticks = 5000;
	}
	else if (speed == 1) {
		ticks = 3000;
	}
	else if (speed == 2) {
		ticks = 1000;
	}
	
	if (mode == 1) {
		//2 горит, 1 не горит (смещаясь по ленте)
		if ((led & 0x03) == 3) {
			led <<= 1;
		}
		else {
			led = (led << 1) | 0x01;
		}
	}
	else if (mode == 2) {
		//Зарядка шкалы
		if (~led != 0) {
			led =(led << 1) + 1;
		}
		else {
			led = 0x01;
		}
	}
	
	PORTF = led;
}

ISR(TIMER0_COMPA_vect) {
	if(!turn_on) {
		PORTF = 0;
		return;
	}
	play();
}

ISR(INT0_vect) {
	turn_on = ~turn_on;
	if (turn_on) reset();
	else PORTF = 0;
}
ISR(INT1_vect) {
	if (!turn_on) return;
	mode = (mode + 1) % 3;
	reset();
}

ISR(INT2_vect) {
	if (!turn_on) return;
	speed = (speed + 1) % 3;
	ticks = 0;
}


int main(void) {
	DDRD = 0x00;
	PORTD = 0x07;
	DDRF = 0xFF;
	PORTF = 0x00;
	
	//ТАЙМЕР
	// CTC (сброс после достижения значения)
	TCCR0A = (1 << WGM01);

	//Делитель 1 => 001 = CS2=0 | CS1=0 | CS0=1 (=частота CPU)
	TCCR0B = (1 << CS00);
		
	//Достижение этого значения
	OCR0A = 50;
		
	//Разрешить прерывание (как с кнопками)
	TIMSK0 = (1 << OCIE0A);
	
	//КНОПКИ
	//По спадающему фронту
	EICRA = (0b10 << ISC00) |
	(0b10 << ISC10) |
	(0b10 << ISC20);

	//Разрешить прерывания INT0 - INT2
	EIMSK = (1 << INT0) |
	(1 << INT1) |
	(1 << INT2);
	
	sei();
	
	while(1);
	return 0;
}