#include <avr/io.h>
#include <avr/interrupt.h>
#include <string.h>

extern uint8_t isOn;

char receiveChar(void);
void sendChar(char c);
void sendString(char* content);
void sendLine();
void initUART();
void runUART();

void LED_ENABLE();
void LED_MODE();
void LED_SPEED();

void LED_ENABLE_SET(int enabled);
void LED_MODE_SET(int type);
void LED_SPEED_SET(int spd);