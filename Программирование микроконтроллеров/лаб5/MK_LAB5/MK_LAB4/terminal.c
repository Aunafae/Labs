#include "main.h"

// буфер для хранения команды и её длина
char command[256];
int sizeCommand = 0;

// выполнение
void processCommand() {
	if(strcmp(command, "on") == 0) {
		LED_ENABLE_SET(1);
		return;
	}
	else if(strcmp(command, "off") == 0) {
		LED_ENABLE_SET(0);
		return;
	}
	
	if (isOn) {
		// установка режима
		if (strncmp(command, "type ", 5) == 0) {
			if (sizeCommand == 6) {
				switch (command[5]) {
				case '1':
					LED_MODE_SET(0);
					return;
				case '2':
					LED_MODE_SET(1);
					return;
				case '3':
					LED_MODE_SET(2);
					return;
				}
			}
		}
		// установка скорости
		else if (strncmp(command, "speed ", 6) == 0) {
			if (sizeCommand == 7) {
				switch (command[6]) {
				case '1':
					LED_SPEED_SET(0);
					return;
				case '2':
					LED_SPEED_SET(1);
					return;
				case '3':
					LED_SPEED_SET(2);
					return;
				}
			}
		}
	}
	// если команда не распознана
	sendLine();
	sendString("Invalid command");
}

// получить 1 символ
char receiveChar(void) {
	while(!(UCSR0A & (1<<RXC0)));
	return UDR0;
}

// отправляет 1 символ
void sendChar(char c) {
	while(!( UCSR0A & (1<<UDRE0)));
	UDR0 = c;
}

// отправляет строку
void sendString(char* str) {
	int i = 0;
	while (str[i]) {
        sendChar(str[i++]);
    }
}

// отправляет перевод строки
void sendLine() {
	sendChar((char)13);
	sendChar((char)10);
}


// инициализация UART
void initUART() {
	unsigned int baudRR = (1000000UL)/(8UL*9600UL)-1;
	UBRR0H = baudRR>>8;
	UBRR0L = baudRR;

	UCSR0A |= (1 << U2X0);
	UCSR0B = 1<<RXEN0 | 1<<TXEN0;
	UCSR0C = (1 << UCSZ01) | (1 << UCSZ00);
}

// работа UART
void runUART() {
	sendString("\"on\" - enable LED\r\n\"off\" - disable LED\r\n\"type N\" - change N: 1-3\r\n\"speed N\" - change N: 1-3\r\n");
	while(1) {
		char c = receiveChar();
		if (c == '\r') {
			processCommand();
			sendLine();
			sizeCommand = 0;
		}
		else if (c != 8) { // не backspace
			command[sizeCommand++] = c;
			sendChar(c);
		}
		else if (sizeCommand > 0) { // backspace
			sizeCommand--;
			sendChar(c);
		}
		// завершающий нулевой символ
		command[sizeCommand+1] = '\0';
	}
}