#pragma once

#include "targetver.h"
// Исключите редко используемые компоненты из заголовков Windows
#define WIN32_LEAN_AND_MEAN
// Файлы заголовков Windows
#include <windows.h>
// Файлы заголовков среды выполнения C
#include <stdlib.h>
#include <malloc.h>
#include <memory.h>
#include <tchar.h>

#include <string>

#define WM_FILLBAR 101010
#define DRAW_PROGRESS 101010
#define GUI_SET_PRIORITY 1
#define GUI_SUSPEND 2
#define GUI_RESUME 3
#define GUI_RADIO_1 4
#define GUI_RADIO_2 5
#define GUI_RADIO_3 6
#define GUI_CREATE_ALL 7
#define GUI_START_ALL 8
#define GUI_STOP_ALL 9
#define GUI_TERMINATE_ALL 10
#define GUI_PRIORITY_LIST 11

class ProgressBar {
private:
    int WIDTH = 300;
    int HEIGHT = 30;
    int x = 0, y = 0;
public:
    HWND hwnd;
    void create(HWND parent, int x, int y);
    void repaint(int amount, int max_amount);
};

int WINAPI WinMain(HINSTANCE hInstance, HINSTANCE hPrevInstance, LPSTR lpCmdLine, int nCmdShow);
LRESULT CALLBACK WndProc(HWND hWnd, UINT message, WPARAM wParam, LPARAM lParam);
LRESULT CALLBACK ProgressBarProc(HWND hWnd, UINT message, WPARAM wParam, LPARAM lParam);
DWORD WINAPI ThreadProc(LPVOID lpParam);
void RegClass(HINSTANCE hInstance);
void setPriorityButton(int index, int threadIndex);
void fillThreadContext(int threadIndex);