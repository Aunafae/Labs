#include "framework.h"
#include "algorithm"

HWND threadWindow;
HWND mainWindow;
HWND contextWindow;
HANDLE hThread[3];
ProgressBar progressbar[3];
int amount[3] = { 0, 0, 0 };
DWORD dwThreadId[3] = { -1, -1, -1 };
int thread_nums[3] = { 0, 1, 2 };
unsigned long long thread_work[3] = { 0, 0, 0 };

HWND hComboBox;
int selectedThread = 0;

void ProgressBar::create(HWND parent, int x, int y) {
    hwnd = CreateWindowEx(0, TEXT("ProgressBar"), NULL, WS_CHILD | WS_VISIBLE, x, y, WIDTH, HEIGHT, parent, NULL, (HINSTANCE)GetWindowLong(parent, GWLP_HINSTANCE), NULL);
    this->x = x;
    this->y = y;
}

void ProgressBar::repaint(int amount, int max_amount) {
    float step = WIDTH / (float)max_amount;

    PAINTSTRUCT ps;
    HBRUSH hBrush = CreateSolidBrush(RGB(0, 0, 255));
    HDC hdc = BeginPaint(hwnd, &ps);

    SelectObject(hdc, hBrush);
    Rectangle(hdc, 0, 0, step * amount, HEIGHT);

    EndPaint(hwnd, &ps);
    DeleteObject(hBrush);
}


int WINAPI WinMain(HINSTANCE hInstance, HINSTANCE hPrevInstance, LPSTR lpCmdLine, int nCmdShow) {
    RegClass(hInstance);
    mainWindow = CreateWindowEx(0, TEXT("MyWindowClass"), TEXT("lab2 app"), WS_OVERLAPPEDWINDOW, CW_USEDEFAULT, CW_USEDEFAULT, 800, 600, NULL, NULL, hInstance, NULL);
    if (!mainWindow) return FALSE;

    ShowWindow(mainWindow, nCmdShow);
    UpdateWindow(mainWindow);

    MSG msg;
    while (GetMessage(&msg, NULL, 0, 0)) {
        TranslateMessage(&msg);
        DispatchMessage(&msg);
    }
    return (int)msg.wParam;
}

LRESULT CALLBACK WndProc(HWND hwnd, UINT message, WPARAM wParam, LPARAM lParam) {
    switch (message) {
    case WM_CREATE: {
        threadWindow = CreateWindowEx(0, TEXT("STATIC"), NULL, WS_CHILD | WS_VISIBLE | SS_CENTER | SS_WHITERECT, 10, 10, 400, 300, hwnd, NULL, (HINSTANCE)GetWindowLong(hwnd, GWL_HINSTANCE), NULL);

        progressbar[0].create(threadWindow, 30, 50);
        progressbar[0].repaint(0, 100);

        progressbar[1].create(threadWindow, 30, 100);
        progressbar[1].repaint(0, 100);

        progressbar[2].create(threadWindow, 30, 150);
        progressbar[2].repaint(0, 100);


        HWND bottomMenu = CreateWindowEx(0, TEXT("STATIC"), NULL, WS_CHILD | WS_VISIBLE | SS_CENTER | SS_WHITERECT, 10, 320, 400, 230, hwnd, NULL, (HINSTANCE)GetWindowLong(hwnd, GWL_HINSTANCE), NULL);
        hComboBox = CreateWindowEx(0, TEXT("COMBOBOX"), L"", WS_CHILD | WS_VISIBLE | CBS_DROPDOWNLIST | WS_VSCROLL, 30, 60, 220, 100, bottomMenu, (HMENU)GUI_PRIORITY_LIST, NULL, NULL);

        SendMessage(hComboBox, CB_ADDSTRING, 0, (LPARAM)TEXT("Простаивающий"));
        SendMessage(hComboBox, CB_ADDSTRING, 0, (LPARAM)TEXT("Низкий"));
        SendMessage(hComboBox, CB_ADDSTRING, 0, (LPARAM)TEXT("Ниже обычного"));
        SendMessage(hComboBox, CB_ADDSTRING, 0, (LPARAM)TEXT("Обычный"));
        SendMessage(hComboBox, CB_ADDSTRING, 0, (LPARAM)TEXT("Выше обычного"));
        SendMessage(hComboBox, CB_ADDSTRING, 0, (LPARAM)TEXT("Высокий"));
        SendMessage(hComboBox, CB_ADDSTRING, 0, (LPARAM)TEXT("Реального времени"));

        CreateWindowEx(0, TEXT("BUTTON"), TEXT("SetPriority"), WS_TABSTOP | WS_VISIBLE | WS_CHILD | BS_DEFPUSHBUTTON, 30, 500, 100, 30, hwnd, (HMENU)GUI_SET_PRIORITY, (HINSTANCE)GetWindowLong(hwnd, GWL_HINSTANCE), NULL);
        CreateWindowEx(0, TEXT("BUTTON"), TEXT("Suspend"), WS_TABSTOP | WS_VISIBLE | WS_CHILD | BS_DEFPUSHBUTTON, 150, 500, 100, 30, hwnd, (HMENU)GUI_SUSPEND, (HINSTANCE)GetWindowLong(hwnd, GWL_HINSTANCE), NULL);
        CreateWindowEx(0, TEXT("BUTTON"), TEXT("Resume"), WS_TABSTOP | WS_VISIBLE | WS_CHILD | BS_DEFPUSHBUTTON, 270, 500, 100, 30, hwnd, (HMENU)GUI_RESUME, (HINSTANCE)GetWindowLong(hwnd, GWL_HINSTANCE), NULL);

        CreateWindowEx(0, L"BUTTON", L"Thread 1", WS_CHILD | WS_VISIBLE | BS_RADIOBUTTON, 270, 380, 100, 30, hwnd, (HMENU)GUI_RADIO_1, NULL, NULL);
        CreateWindowEx(0, L"BUTTON", L"Thread 2", WS_CHILD | WS_VISIBLE | BS_RADIOBUTTON, 270, 420, 100, 30, hwnd, (HMENU)GUI_RADIO_2, NULL, NULL);
        CreateWindowEx(0, L"BUTTON", L"Thread 3", WS_CHILD | WS_VISIBLE | BS_RADIOBUTTON, 270, 460, 100, 30, hwnd, (HMENU)GUI_RADIO_3, NULL, NULL);

        SendMessage(GetDlgItem(hwnd, GUI_RADIO_1), BM_SETCHECK, BST_CHECKED, 0);

        HWND threadWorkWindow = CreateWindowEx(0, TEXT("STATIC"), NULL, WS_CHILD | WS_VISIBLE | SS_CENTER | SS_WHITERECT, 420, 10, 150, 300, hwnd, NULL, (HINSTANCE)GetWindowLong(hwnd, GWL_HINSTANCE), NULL);
        HWND threadButtonsWindow = CreateWindowEx(0, TEXT("STATIC"), NULL, WS_CHILD | WS_VISIBLE | SS_CENTER | SS_WHITERECT, 420, 320, 150, 230, hwnd, NULL, (HINSTANCE)GetWindowLong(hwnd, GWL_HINSTANCE), NULL);

        CreateWindowEx(0, TEXT("BUTTON"), TEXT("Create (All)"), WS_TABSTOP | WS_VISIBLE | WS_CHILD | BS_DEFPUSHBUTTON, 445, 350, 100, 30, hwnd, (HMENU)GUI_CREATE_ALL, (HINSTANCE)GetWindowLong(hwnd, GWL_HINSTANCE), NULL);
        CreateWindowEx(0, TEXT("BUTTON"), TEXT("Start (All)"), WS_TABSTOP | WS_VISIBLE | WS_CHILD | BS_DEFPUSHBUTTON, 445, 390, 100, 30, hwnd, (HMENU)GUI_START_ALL, (HINSTANCE)GetWindowLong(hwnd, GWL_HINSTANCE), NULL);
        CreateWindowEx(0, TEXT("BUTTON"), TEXT("Stop (All)"), WS_TABSTOP | WS_VISIBLE | WS_CHILD | BS_DEFPUSHBUTTON, 445, 430, 100, 30, hwnd, (HMENU)GUI_STOP_ALL, (HINSTANCE)GetWindowLong(hwnd, GWL_HINSTANCE), NULL);
        CreateWindowEx(0, TEXT("BUTTON"), TEXT("Terminate (All)"), WS_TABSTOP | WS_VISIBLE | WS_CHILD | BS_DEFPUSHBUTTON, 445, 470, 100, 30, hwnd, (HMENU)GUI_TERMINATE_ALL, (HINSTANCE)GetWindowLong(hwnd, GWL_HINSTANCE), NULL);

        contextWindow = CreateWindowEx(0, TEXT("EDIT"), NULL, WS_CHILD | WS_VISIBLE | WS_VSCROLL | ES_MULTILINE | ES_READONLY, 580, 10, 180, 540, hwnd, NULL, (HINSTANCE)GetWindowLong(hwnd, GWL_HINSTANCE), NULL);

        break;
    } case WM_COMMAND: {
        switch (LOWORD(wParam)) {
        case GUI_SET_PRIORITY: {
            int selectedIndex = SendMessage(hComboBox, CB_GETCURSEL, 0, 0);
            if (selectedIndex == -1) break;
            DWORD priorities[] = {
                THREAD_PRIORITY_IDLE,
                THREAD_PRIORITY_LOWEST,
                THREAD_PRIORITY_BELOW_NORMAL,
                THREAD_PRIORITY_NORMAL,
                THREAD_PRIORITY_ABOVE_NORMAL,
                THREAD_PRIORITY_HIGHEST,
                THREAD_PRIORITY_TIME_CRITICAL
            };

            DWORD priority = priorities[selectedIndex];

            SuspendThread(hThread[selectedThread]);
            SetThreadPriority(hThread[selectedThread], priority);
            ResumeThread(hThread[selectedThread]);
            break;
        } case GUI_SUSPEND: {
            SuspendThread(hThread[selectedThread]);
            break;
        } case GUI_RESUME: {
            ResumeThread(hThread[selectedThread]);
            break;
        } case GUI_RADIO_1: {
            SendMessage(GetDlgItem(hwnd, GUI_RADIO_1), BM_SETCHECK, BST_CHECKED, 0);
            SendMessage(GetDlgItem(hwnd, GUI_RADIO_2), BM_SETCHECK, BST_UNCHECKED, 0);
            SendMessage(GetDlgItem(hwnd, GUI_RADIO_3), BM_SETCHECK, BST_UNCHECKED, 0);

            int priority_normal = 0;
            switch (GetThreadPriority(hThread[0])) {
            case THREAD_PRIORITY_IDLE:
                priority_normal = 0;
                break;
            case THREAD_PRIORITY_LOWEST:
                priority_normal = 1;
                break;
            case THREAD_PRIORITY_BELOW_NORMAL:
                priority_normal = 2;
                break;
            case THREAD_PRIORITY_NORMAL:
                priority_normal = 3;
                break;
            case THREAD_PRIORITY_ABOVE_NORMAL:
                priority_normal = 4;
                break;
            case THREAD_PRIORITY_HIGHEST:
                priority_normal = 5;
                break;
            case THREAD_PRIORITY_TIME_CRITICAL:
                priority_normal = 6;
                break;
            }
            SendMessage(hComboBox, CB_SETCURSEL, (WPARAM)priority_normal, 0);

            selectedThread = 0;
            fillThreadContext(0);
            break;
        } case GUI_RADIO_2: {
            SendMessage(GetDlgItem(hwnd, GUI_RADIO_1), BM_SETCHECK, BST_UNCHECKED, 0);
            SendMessage(GetDlgItem(hwnd, GUI_RADIO_2), BM_SETCHECK, BST_CHECKED, 0);
            SendMessage(GetDlgItem(hwnd, GUI_RADIO_3), BM_SETCHECK, BST_UNCHECKED, 0);

            int priority_normal = 0;
            switch (GetThreadPriority(hThread[1])) {
            case THREAD_PRIORITY_IDLE:
                priority_normal = 0;
                break;
            case THREAD_PRIORITY_LOWEST:
                priority_normal = 1;
                break;
            case THREAD_PRIORITY_BELOW_NORMAL:
                priority_normal = 2;
                break;
            case THREAD_PRIORITY_NORMAL:
                priority_normal = 3;
                break;
            case THREAD_PRIORITY_ABOVE_NORMAL:
                priority_normal = 4;
                break;
            case THREAD_PRIORITY_HIGHEST:
                priority_normal = 5;
                break;
            case THREAD_PRIORITY_TIME_CRITICAL:
                priority_normal = 6;
                break;
            }
            SendMessage(hComboBox, CB_SETCURSEL, priority_normal, 0);

            selectedThread = 1;
            fillThreadContext(1);
            break;
        } case GUI_RADIO_3: {
            SendMessage(GetDlgItem(hwnd, GUI_RADIO_1), BM_SETCHECK, BST_UNCHECKED, 0);
            SendMessage(GetDlgItem(hwnd, GUI_RADIO_2), BM_SETCHECK, BST_UNCHECKED, 0);
            SendMessage(GetDlgItem(hwnd, GUI_RADIO_3), BM_SETCHECK, BST_CHECKED, 0);

            int priority_normal = 0;
            switch (GetThreadPriority(hThread[2])) {
            case THREAD_PRIORITY_IDLE:
                priority_normal = 0;
                break;
            case THREAD_PRIORITY_LOWEST:
                priority_normal = 1;
                break;
            case THREAD_PRIORITY_BELOW_NORMAL:
                priority_normal = 2;
                break;
            case THREAD_PRIORITY_NORMAL:
                priority_normal = 3;
                break;
            case THREAD_PRIORITY_ABOVE_NORMAL:
                priority_normal = 4;
                break;
            case THREAD_PRIORITY_HIGHEST:
                priority_normal = 5;
                break;
            case THREAD_PRIORITY_TIME_CRITICAL:
                priority_normal = 6;
                break;
            }
            SendMessage(hComboBox, CB_SETCURSEL, priority_normal, 0);

            selectedThread = 2;
            fillThreadContext(2);
            break;
        } case GUI_CREATE_ALL: {
            if (dwThreadId[0] != -1 || dwThreadId[1] != -1 || dwThreadId[2] != -1) {
                for (int i = 0; i < 3; i++) {
                    TerminateThread(hThread[i], 0);
                    dwThreadId[i] = -1;
                    progressbar[i].repaint(0, 100);
                }
                SendMessage(mainWindow, WM_PAINT, 0, 0);
            }

            for (int i = 0; i < 3; i++)
                hThread[i] = CreateThread(NULL, 0, ThreadProc, thread_nums + i, CREATE_SUSPENDED, dwThreadId + i);

            break;
        } case GUI_START_ALL: {
            for (int i = 0; i < 3; i++) {
                ResumeThread(hThread[i]);
            }
            break;
        } case GUI_STOP_ALL: {
            for (int i = 0; i < 3; i++) {
                SuspendThread(hThread[i]);
            }
            break;
        } case GUI_TERMINATE_ALL: {
            for (int i = 0; i < 3; i++) {
                TerminateThread(hThread[i], 0);
                dwThreadId[i] = -1;
                progressbar[i].repaint(0, 100);
            }
            SendMessage(mainWindow, WM_PAINT, 0, 0);
            break;
        }
        }
        break;
    } case WM_PAINT: {
        const RECT redraw = { 450, 60, 500, 180 };

        InvalidateRect(hwnd, &redraw, FALSE);

        PAINTSTRUCT ps;
        HDC hdc = BeginPaint(hwnd, &ps);
        int sum_amount_ptr = max(amount[0] + amount[1] + amount[2], 1);
        std::wstring pr1 = std::to_wstring(amount[0]) + L" " + std::to_wstring(amount[0] / (float)sum_amount_ptr);
        std::wstring pr2 = std::to_wstring(amount[1]) + L" " + std::to_wstring(amount[1] / (float)sum_amount_ptr);
        std::wstring pr3 = std::to_wstring(amount[2]) + L" " + std::to_wstring(amount[2] / (float)sum_amount_ptr);

        const wchar_t* text1 = TEXT("Поток 1");
        TextOut(hdc, 40, 40, text1, lstrlenW(text1));
        TextOut(hdc, 450, 40, text1, lstrlenW(text1));
        TextOut(hdc, 450, 60, pr1.c_str(), static_cast<int>(pr1.size()));

        const wchar_t* text2 = TEXT("Поток 2");
        TextOut(hdc, 40, 90, text2, lstrlenW(text2));
        TextOut(hdc, 450, 90, text2, lstrlenW(text2));
        TextOut(hdc, 450, 110, pr2.c_str(), static_cast<int>(pr2.size()));

        const wchar_t* text3 = TEXT("Поток 3");
        TextOut(hdc, 40, 140, text3, lstrlenW(text3));
        TextOut(hdc, 450, 140, text3, lstrlenW(text3));
        TextOut(hdc, 450, 160, pr3.c_str(), static_cast<int>(pr3.size()));

        const wchar_t* priorityText = TEXT("Уровень приоритета");
        TextOut(hdc, 40, 350, priorityText, lstrlenW(priorityText));

        EndPaint(hwnd, &ps);
        break;
    } case WM_DESTROY: {
        PostQuitMessage(0);
        break;
    } default: {
        return DefWindowProc(hwnd, message, wParam, lParam);
    }}
    return 0;
}

LRESULT CALLBACK ProgressBarProc(HWND hwnd, UINT message, WPARAM wParam, LPARAM lParam) {
    switch (message) {
    case WM_PAINT: {
        if (lParam == DRAW_PROGRESS) {
            InvalidateRect(hwnd, NULL, TRUE);
            int barIndex = wParam;
            int max_amount_ptr = max(*std::max_element(amount, amount + 2), 1);
            progressbar[barIndex].repaint(amount[barIndex], max_amount_ptr);
        }
        break;
    } case WM_DESTROY: {
        PostQuitMessage(0);
        break;
    } default: {
        return DefWindowProc(hwnd, message, wParam, lParam);
    }}
    return 0;
}

DWORD WINAPI ThreadProc(LPVOID lpParam) {
    int thread_id = *((int*)lpParam);

    
    while (true) {
        thread_work[thread_id]++;
        if (thread_work[thread_id] % 10000000 == 0) {
            thread_work[thread_id] = 0;
            amount[thread_id]++;

            for(int i = 0; i < 3; i++)
                SendMessage(progressbar[i].hwnd, WM_PAINT, (WPARAM)i, DRAW_PROGRESS);

            SendMessage(mainWindow, WM_PAINT, 0, 0);
            //SwitchToThread();
        }
    }
    return 0;
}

void RegClass(HINSTANCE hInstance) {
    WNDCLASSEX wc;
    ZeroMemory(&wc, sizeof(WNDCLASSEX));
    wc.cbSize = sizeof(WNDCLASSEX);
    wc.style = CS_HREDRAW | CS_VREDRAW;
    wc.lpfnWndProc = WndProc;
    wc.cbClsExtra = 0;
    wc.cbWndExtra = 0;
    wc.hInstance = hInstance;
    wc.hIcon = LoadIcon(NULL, IDI_APPLICATION);
    wc.hCursor = LoadCursor(NULL, IDC_ARROW);
    wc.hbrBackground = (HBRUSH)(CreateSolidBrush(RGB(255, 255, 255)));
    wc.lpszMenuName = NULL;
    wc.lpszClassName = TEXT("MyWindowClass");
    wc.hIconSm = LoadIcon(NULL, IDI_HAND);
    RegisterClassEx(&wc);

    wc.lpszClassName = TEXT("ProgressBar");
    wc.lpfnWndProc = ProgressBarProc;
    wc.hbrBackground = (HBRUSH)(CreateSolidBrush(RGB(200, 200, 200)));
    RegisterClassEx(&wc);
}

void fillThreadContext(int threadIndex) {
    CONTEXT ct;
    ct.ContextFlags = CONTEXT_FULL;
    std::wstring out = TEXT("CONTEXT OF THREAD ");
    out += std::to_wstring(threadIndex + 1);
    SuspendThread(hThread[threadIndex]);
    if (GetThreadContext(hThread[threadIndex], &ct) == 0) {
        DWORD errorCode = GetLastError();

        LPWSTR messageBuffer = nullptr;
        FormatMessage(FORMAT_MESSAGE_ALLOCATE_BUFFER | FORMAT_MESSAGE_FROM_SYSTEM | FORMAT_MESSAGE_IGNORE_INSERTS,
            nullptr, errorCode, MAKELANGID(LANG_NEUTRAL, SUBLANG_DEFAULT),
            (LPWSTR)&messageBuffer, 0, nullptr);

        if (messageBuffer != nullptr) {
            out += TEXT("Не удалось получить контекст потока.\r\nКод ошибки: ");
            out += std::to_wstring(errorCode);
            out += TEXT(".\r\nОписание ошибки: ");
            out += messageBuffer;

            LocalFree(messageBuffer);
        }
        else {
            out += TEXT("Не удалось получить контекст потока. Код ошибки: ") + std::to_wstring(errorCode);
        }

        SendMessage(contextWindow, WM_SETTEXT, 0, (LPARAM)out.c_str());
        SendMessage(contextWindow, WM_PAINT, 0, 0);
        ResumeThread(hThread[threadIndex]);
        return;
    }

    out = TEXT("CONTEXT OF THREAD ");
    out += std::to_wstring(threadIndex + 1);

    out += TEXT("\r\nContextFlags: ");
    out += std::to_wstring(ct.ContextFlags);

    out += TEXT("\r\nEax: ");
    out += std::to_wstring(ct.Eax);

    out += TEXT("\r\nEbx: ");
    out += std::to_wstring(ct.Ebx);

    out += TEXT("\r\nEcx: ");
    out += std::to_wstring(ct.Ecx);

    out += TEXT("\r\nEdx: ");
    out += std::to_wstring(ct.Edx);

    out += TEXT("\r\nEbp: ");
    out += std::to_wstring(ct.Ebp);

    out += TEXT("\r\nEdi: ");
    out += std::to_wstring(ct.Edi);

    out += TEXT("\r\nEip: ");
    out += std::to_wstring(ct.Eip);

    out += TEXT("\r\nEsi: ");
    out += std::to_wstring(ct.Esi);

    out += TEXT("\r\nEsp: ");
    out += std::to_wstring(ct.Esp);

    out += TEXT("\r\nDr0: ");
    out += std::to_wstring(ct.Dr0);

    out += TEXT("\r\nDr1: ");
    out += std::to_wstring(ct.Dr1);

    out += TEXT("\r\nDr2: ");
    out += std::to_wstring(ct.Dr2);

    out += TEXT("\r\nDr3: ");
    out += std::to_wstring(ct.Dr3);

    out += TEXT("\r\nDr6: ");
    out += std::to_wstring(ct.Dr6);

    out += TEXT("\r\nDr7: ");
    out += std::to_wstring(ct.Dr7);

    out += TEXT("\r\nSegCs: ");
    out += std::to_wstring(ct.SegCs);

    out += TEXT("\r\nSegDs: ");
    out += std::to_wstring(ct.SegDs);

    out += TEXT("\r\nSegEs: ");
    out += std::to_wstring(ct.SegEs);

    out += TEXT("\r\nSegFs: ");
    out += std::to_wstring(ct.SegFs);

    out += TEXT("\r\nSegGs: ");
    out += std::to_wstring(ct.SegGs);

    out += TEXT("\r\nSegSs: ");
    out += std::to_wstring(ct.SegSs);

    ResumeThread(hThread[threadIndex]);

    SendMessage(contextWindow, WM_SETTEXT, 0, (LPARAM)out.c_str());
    SendMessage(contextWindow, WM_PAINT, 0, 0);
}