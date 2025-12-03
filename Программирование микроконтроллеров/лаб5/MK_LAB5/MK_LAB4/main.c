#include "main.h"

int8_t ledState = 0xFF;
uint8_t isOn = 0;
int8_t speed = 0;
int8_t mode = 0;
int countTicks = 0;

// сброс состо€ни€ led
void resetLeds(){
	ledState = 0;
	if (mode == 0) {
		ledState = 0xFF;
	}
	else if (mode == 1) {
		ledState = 0b01101101;
	}
	else if (mode == 2) {
		ledState = 0x01;
	}
	countTicks = 0;
}

// обновление состо€ни€
void updateLeds(){
	if(countTicks > 0) {
		countTicks--;
		return;
	}
	
	switch (speed) {
	case 0:
		countTicks = 5000;
		break;
	case 1:
		countTicks = 3000;
		break;
	case 2:
		countTicks = 1000;
		break;
	}
	
	if (mode == 1) {
		// "бегут" по ленте
		if ((ledState & 0x03) == 3) {
			ledState <<= 1;
		}
		else {
			ledState = (ledState << 1) | 0x01;
		}
	}
	else if (mode == 2) {
		// "зар€жаетс€"
		if (~ledState != 0) {
			ledState =(ledState << 1) + 1;
		}
		else {
			ledState = 0x01;
		}
	}
	PORTA = ledState;
}

// таймерное прерывание
ISR(TIMER0_COMPA_vect) {
	if(!isOn) {
		PORTA = 0;
		return;
	}
	updateLeds();
}

// при вкл - resetLeds(), при выкл - гасит всЄ
ISR(INT0_vect) {
	isOn = ~isOn;
	if (isOn) {
		resetLeds();
	} else {
		PORTA = 0;
	}
}
//переключение mode
ISR(INT1_vect) {
	if (!isOn) return;
	mode = (mode + 1) % 3;
	resetLeds();
}
// переключение speed
ISR(INT2_vect) {
	if (!isOn) return;
	speed = (speed + 1) % 3;
	countTicks = 0;
}
// вкл выкл работы
void LED_ENABLE_SET(int enabled) {
	isOn = enabled;
	if (isOn) {
		resetLeds();
	} else {
		PORTA = 0;
	}
}
// установка режима
void LED_MODE_SET(int type) {
	if (!isOn) return;
	mode = type;
	resetLeds();
}
// установка скорости
void LED_SPEED_SET(int spd) {
	if (!isOn) return;
	speed = spd;
	countTicks = 0;
}

int main(void) {
	DDRD = 0x00;
	PORTD = 0x07;
	DDRA = 0xFF;
	PORTA = 0x00;
	
	// таймер
	TCCR0A = (1 << WGM01); // CTC (сброс после достижени€ значени€)
	TCCR0B = (1 << CS00); // делитель 1 (частота CPU)
	OCR0A = 50; // значение сравнени€ (достижение значени€)
	TIMSK0 = (1 << OCIE0A); // разрешить прерывание по сравнению
	
	// настройка кнопок (прерывани€ по спаду)
	EICRA = (0b10 << ISC00) | (0b10 << ISC10) | (0b10 << ISC20);
	EIMSK = (1 << INT0) | (1 << INT1) | (1 << INT2); //–азрешить прерывани€ INT0 - INT2
	
	initUART();
	
	// глобальные прерывани€
	sei(); 
	
	runUART();
	return 0;
}