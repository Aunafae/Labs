#include <windows.h>
#include <windowsx.h>
#include <tchar.h>
#include <stack>

#define ZOOM_X 0
#define ZOOM_Y 1
#define INVERT 1
#define ZOOM_DONT_KEEP 0

using namespace std;

enum TypeObject {
    TO_LINE,
    TO_RECTANGLE,
    TO_ELLIPSE,
    TO_ZOOM
};

struct MyPrim {
    DOUBLE x1, y1, x2, y2;
    TypeObject typeObject;
};

void DrawPrimitives(HWND hwnd, WPARAM wParam, LPARAM lParam);
void ClientDraw(HWND hwnd, WPARAM wParam, LPARAM lParam);
void PressMouse(HWND hwnd, WPARAM wParam, LPARAM lParam);
void MoveMouse(HWND hwnd, WPARAM wParam, LPARAM lParam);
void ReleaseMouse(HWND hwnd, WPARAM wParam, LPARAM lParam);
DOUBLE normal(DOUBLE value, bool invert = false);
DOUBLE zoom(DOUBLE value, bool zoom_y, bool invert = false);
void setZoom(HWND hwnd, MyPrim newZoom, bool keep=true);


// Объявление функций
BOOL RegClass(WNDPROC, LPCTSTR, HBRUSH);
LRESULT CALLBACK WndProc(HWND, UINT, WPARAM, LPARAM);

// Описание глобальных переменных
HINSTANCE hInst;
HBRUSH hBrushBackground;
HGDIOBJ hPenOld;
HGDIOBJ hBrushOld;
HGDIOBJ hPen;
HDC winHDC;
POINT pointStart;
POINT pointEnd;
POINT Center = { 325, 325 };
tagPOINT VpMin = { 0, 0 };
tagPOINT VpMax = { 750, 750 };
MyPrim	Model[1000];
INT PrimCount = 0;
TypeObject objtype = TO_LINE;

stack<MyPrim> zoomStack;
MyPrim currentZoom;
DOUBLE zoomScale;
DOUBLE zoomPointX;
DOUBLE zoomPointY;

HWND hwndButtonLine;
HWND hwndButtonRectangle;
HWND hwndButtonEllipse;
HWND hwndButtonZoom;
HWND hwndButtonUnzoom;


// Описание главной функции
int WINAPI WinMain(HINSTANCE hInstance, HINSTANCE hPrevlnstance, LPSTR lpszCmdLine, int nCmdShow) {
    currentZoom.x1 = 0;
    currentZoom.y1 = 0;
    currentZoom.x2 = 1;
    currentZoom.y2 = 1;
    currentZoom.typeObject = TO_ZOOM;

    MSG msg;
    HWND hwnd;
    hInst = hInstance;
    hBrushBackground = CreateSolidBrush(RGB(250, 240, 255));

    if (!RegClass(WndProc, L"My class", hBrushBackground)) {
        return false;
    }

    hwnd = CreateWindow(L"My class", L"Компьютерная графика, 1 лаба",
        WS_OVERLAPPEDWINDOW | WS_VISIBLE, CW_USEDEFAULT, CW_USEDEFAULT, 
        1000, 750, 0, 0, hInstance, NULL);

    hwndButtonLine = CreateWindow(L"BUTTON", L"Линия", 
        WS_TABSTOP | WS_VISIBLE | WS_CHILD | BS_DEFPUSHBUTTON, 
        750, 0, 235, 187, hwnd, NULL, (HINSTANCE)GetWindowLongPtr(hwnd, GWLP_HINSTANCE), NULL);
    hwndButtonRectangle = CreateWindow(L"BUTTON", L"Прямоугольник",
        WS_TABSTOP | WS_VISIBLE | WS_CHILD | BS_DEFPUSHBUTTON,
        750, 187, 235, 187, hwnd, NULL, (HINSTANCE)GetWindowLongPtr(hwnd, GWLP_HINSTANCE), NULL);
    hwndButtonEllipse = CreateWindow(L"BUTTON", L"Эллипс",
        WS_TABSTOP | WS_VISIBLE | WS_CHILD | BS_DEFPUSHBUTTON,
        750, 374, 235, 187, hwnd, NULL, (HINSTANCE)GetWindowLongPtr(hwnd, GWLP_HINSTANCE), NULL);
    hwndButtonZoom = CreateWindow(L"BUTTON", L"+",
        WS_TABSTOP | WS_VISIBLE | WS_CHILD | BS_DEFPUSHBUTTON,
        750, 561, 118, 185, hwnd, NULL, (HINSTANCE)GetWindowLongPtr(hwnd, GWLP_HINSTANCE), NULL);
    hwndButtonUnzoom = CreateWindow(L"BUTTON", L"-",
        WS_TABSTOP | WS_VISIBLE | WS_CHILD | BS_DEFPUSHBUTTON,
        867, 561, 118, 185, hwnd, NULL, (HINSTANCE)GetWindowLongPtr(hwnd, GWLP_HINSTANCE), NULL);

    setZoom(hwnd, currentZoom, ZOOM_DONT_KEEP);
    InvalidateRect(hwnd, NULL, false);
    UpdateWindow(hwnd);

    if (!hwnd) {
        return false;
    }

    while (GetMessage(&msg, NULL, 0, 0) > 0) {
        TranslateMessage(&msg);
        DispatchMessage(&msg);
    }

    // Освобождение кисти перед выходом
    DeleteObject(hBrushBackground);

    return msg.wParam;
}

// Описание функции регистрации классов
BOOL RegClass(WNDPROC Proc, LPCTSTR szName, HBRUSH brBackground) {
    WNDCLASS wc;
    wc.style = wc.cbClsExtra = wc.cbWndExtra = 0;
    wc.lpfnWndProc = Proc;
    wc.hInstance = hInst;
    wc.hIcon = LoadIcon(NULL, IDI_APPLICATION);
    wc.hCursor = LoadCursor(NULL, IDC_ARROW);
    wc.hbrBackground = brBackground;
    wc.lpszMenuName = NULL;
    wc.lpszClassName = szName;
    return(RegisterClass(&wc) != 0);
}

// Описание функции окон
LRESULT CALLBACK WndProc(HWND hwnd, UINT msg, WPARAM wParam, LPARAM lParam) {
    static HWND hwndChild = NULL;
    MSG timermsg;
    switch (msg) {
    case WM_PAINT:
        DrawPrimitives(hwnd, wParam, lParam);
        ClientDraw(hwnd, wParam, lParam);
        break;
    case WM_LBUTTONDOWN:
        PressMouse(hwnd, wParam, lParam);
        break;
    case WM_MOUSEMOVE:
        MoveMouse(hwnd, wParam, lParam);
        break;
    case WM_LBUTTONUP:
        ReleaseMouse(hwnd, wParam, lParam);
        break;
    case WM_COMMAND:
        if ((HWND)lParam == hwndButtonLine)
            objtype = TO_LINE;
        else if ((HWND)lParam == hwndButtonRectangle)
            objtype = TO_RECTANGLE;
        else if ((HWND)lParam == hwndButtonEllipse)
            objtype = TO_ELLIPSE;
        else if ((HWND)lParam == hwndButtonZoom)
            objtype = TO_ZOOM;
        else if ((HWND)lParam == hwndButtonUnzoom)
            if (!zoomStack.empty()) {
                setZoom(hwnd, zoomStack.top(), ZOOM_DONT_KEEP);
                zoomStack.pop();
            }
        break;
    case WM_CLOSE:
        PostQuitMessage(0);
        break;
    case WM_DESTROY:
        break;
    default:
        return DefWindowProc(hwnd, msg, wParam, lParam);
    }
    return 0;
}

// Функция рисования
void DrawPrimitives(HWND hwnd, WPARAM wParam, LPARAM lParam) {
    // Структура, описывающая заливку линии
    LOGBRUSH lb;
    lb.lbHatch = 0;
    lb.lbStyle = PS_SOLID;

    lb.lbColor = RGB(0, 0, 0);
    HGDIOBJ hPen1 = ExtCreatePen(PS_GEOMETRIC | PS_SOLID, 4, &lb, 0, NULL);
    lb.lbColor = RGB(250, 200, 0);
    HGDIOBJ hPen2 = ExtCreatePen(PS_GEOMETRIC | PS_DOT, 7, &lb, 0, NULL);
    lb.lbColor = RGB(21, 51, 173);
    HGDIOBJ hPen3 = ExtCreatePen(PS_GEOMETRIC | PS_DASH, 5, &lb, 0, NULL);

    HBRUSH hBrushDiagonal = CreateHatchBrush(HS_BDIAGONAL, RGB(0, 0, 0));

    PAINTSTRUCT ps;
    HDC hdc = BeginPaint(hwnd, &ps);

    HRGN clip = CreateRectRgn(VpMin.x, VpMin.y, VpMax.x, VpMax.y);
    SelectClipRgn(hdc, clip);
    Rectangle(hdc, VpMin.x, VpMin.y, VpMax.x, VpMax.y);

    // ЛИНИИ
    // Выбрали перо 1, старое сохранили в hPenOld
    hPenOld = SelectObject(hdc, hPen1);
    MoveToEx(hdc, Center.x - 250, Center.y, NULL);
    LineTo(hdc, Center.x + 250, Center.y);
    // Выбрали перо 2
    SelectObject(hdc, hPen2);
    MoveToEx(hdc, Center.x, Center.y - 150, NULL);
    LineTo(hdc, Center.x, Center.y + 150);

    // ЭЛЛИПС
    // Выбрали перо 3
    SelectObject(hdc, hPen3);
    SelectObject(hdc, GetStockObject(NULL_BRUSH));
    Ellipse(hdc, Center.x - 235, Center.y - 135, Center.x + 235, Center.y + 135);

    // ПРЯМОУГОЛЬНИК
    // Выбрали перо 2
    SelectObject(hdc, hPen2);
    SelectObject(hdc, GetStockObject(LTGRAY_BRUSH));
    Rectangle(hdc, Center.x + 200, Center.y - 300, Center.x + 320, Center.y - 180);
    // Выбрали перо 3
    SelectObject(hdc, hPen3);
    SelectObject(hdc, hBrushDiagonal);
    Rectangle(hdc, Center.x - 300, Center.y + 250, Center.x, Center.y + 350);


    // Вернули старое перо, удалили созданные, освободив место в памяти
    SelectClipRgn(hdc, NULL);
    SelectObject(hdc, hPenOld);
    DeleteObject(hPen1);
    DeleteObject(hPen2);
    DeleteObject(hPen3);
    DeleteObject(hBrushDiagonal);

    EndPaint(hwnd, &ps);
}

void ClientDraw(HWND hwnd, WPARAM wParam, LPARAM lParam) {
    HRGN clipRegion = CreateRectRgn(VpMin.x, VpMin.y, VpMax.x, VpMax.y);

    LOGBRUSH lb;
    lb.lbHatch = 0;
    lb.lbStyle = PS_SOLID;

    lb.lbColor = RGB(250, 200, 0);
    HGDIOBJ hPenDraw = ExtCreatePen(PS_GEOMETRIC | PS_DASH, 5, &lb, 0, NULL);
    HGDIOBJ hBrushDraw = CreateSolidBrush(RGB(255, 240, 220));

    PAINTSTRUCT ps;
    winHDC = BeginPaint(hwnd, &ps);
    SetROP2(winHDC, R2_COPYPEN);
    SelectClipRgn(winHDC, clipRegion);

    hBrushOld = SelectObject(winHDC, hBrushBackground);
    Rectangle(winHDC, VpMin.x, VpMin.y, VpMax.x, VpMax.y);
    hPenOld = SelectObject(winHDC, hPenDraw);
    SelectObject(winHDC, hBrushDraw);


    for (int i = 0; i <= PrimCount; i++) {
        // берём элемент массива
        MyPrim prim = Model[i];

        DOUBLE x1 = normal(zoom(prim.x1, ZOOM_X), INVERT);
        DOUBLE x2 = normal(zoom(prim.x2, ZOOM_X), INVERT);
        DOUBLE y1 = normal(zoom(prim.y1, ZOOM_Y), INVERT);
        DOUBLE y2 = normal(zoom(prim.y2, ZOOM_Y), INVERT);

        switch (prim.typeObject) {
        case TO_LINE: {
            MoveToEx(winHDC, x1 + VpMin.x, y1 + VpMin.y, NULL);
            LineTo(winHDC, x2 + VpMin.x, y2 + VpMin.y);
            break;
        } case TO_RECTANGLE: {
            Rectangle(winHDC, x1 + VpMin.x, y1 + VpMin.y, x2 + VpMin.x, y2 + VpMin.y);
            break;
        } case TO_ELLIPSE: {
            Ellipse(winHDC, x1 + VpMin.x, y1 + VpMin.y, x2 + VpMin.x, y2 + VpMin.y);
            break;
        }
        }
    }

    SelectObject(winHDC, hPenOld);
    SelectObject(winHDC, hBrushOld);
    SelectClipRgn(winHDC, NULL);

    DeleteObject(hPenDraw);
    DeleteObject(hBrushDraw);
    EndPaint(hwnd, &ps);
}

BOOL press_mouse = false;

void PressMouse(HWND hwnd, WPARAM wParam, LPARAM lParam) {
    tagPOINT Point;

    Point.x = lParam % 0x10000;
    Point.y = lParam / 0x10000;

    // Начальная точка
    pointStart = Point;
    pointEnd = pointStart;
    press_mouse = true;

    winHDC = GetDC(hwnd);
    HRGN clipRegion = CreateRectRgn(VpMin.x, VpMin.y, VpMax.x, VpMax.y);
    SelectClipRgn(winHDC, clipRegion);

    // Устанавливаем XOR режим
    SetROP2(winHDC, R2_NOTXORPEN);

    LOGBRUSH lb;
    lb.lbHatch = 0;
    lb.lbStyle = PS_SOLID;
    lb.lbColor = RGB(21, 51, 173);
    hPen = ExtCreatePen(PS_GEOMETRIC | PS_SOLID, 5, &lb, 0, NULL);

    hPenOld = SelectObject(winHDC, hPen);
    
    // Начинаем рисовать
    MoveToEx(winHDC, pointStart.x, pointStart.y, NULL);
    LineTo(winHDC, pointEnd.x, pointEnd.y);
}

void MoveMouse(HWND hwnd, WPARAM wParam, LPARAM lParam) {
    tagPOINT Point;

    Point.x = lParam % 0x10000;
    Point.y = lParam / 0x10000;

    if (GetAsyncKeyState(VK_LBUTTON)) {
        // Стираем предыдущую линию
        MoveToEx(winHDC, pointStart.x, pointStart.y, NULL);
        LineTo(winHDC, pointEnd.x, pointEnd.y);

        // Обновляем конечную точку
        pointEnd = Point;

        // Рисуем новую линию
        MoveToEx(winHDC, pointStart.x, pointStart.y, NULL);
        LineTo(winHDC, pointEnd.x, pointEnd.y);
    }
    else if (press_mouse) ReleaseMouse(hwnd, wParam, lParam);
}

void ReleaseMouse(HWND hwnd, WPARAM wParam, LPARAM lParam) {
    if (!press_mouse) return;
    tagPOINT Point;
    Point.x = lParam % 0x10000;
    Point.y = lParam / 0x10000;

    press_mouse = false;
    MoveToEx(winHDC, pointStart.x, pointStart.y, NULL);
    LineTo(winHDC, pointEnd.x, pointEnd.y);
    pointEnd = Point;

    SelectObject(winHDC, hPenOld);
    DeleteObject(hPen);
    ReleaseDC(hwnd, winHDC);

    MyPrim prim;
    prim.x1 = zoom(normal(pointStart.x), ZOOM_X, INVERT);
    prim.x2 = zoom(normal(pointEnd.x), ZOOM_X, INVERT);
    prim.y1 = zoom(normal(pointStart.y), ZOOM_Y, INVERT);
    prim.y2 = zoom(normal(pointEnd.y), ZOOM_Y, INVERT);
    prim.typeObject = objtype;

    if (prim.typeObject == TO_ZOOM) {
        setZoom(hwnd, prim);
        return;
    }
    
    Model[PrimCount++] = prim;

    RECT prect;
    prect.left = min(pointStart.x, pointEnd.x) - 5;
    prect.top = min(pointStart.y, pointEnd.y) - 5;
    prect.right = max(pointStart.x, pointEnd.x) + 5;
    prect.bottom = max(pointStart.y, pointEnd.y) + 5;

    InvalidateRect(hwnd, &prect, false);
}

void setZoom(HWND hwnd, MyPrim newZoom, bool keep) {
    if(keep) zoomStack.push(currentZoom);
    currentZoom = newZoom;

    zoomScale = min(max(max(abs(currentZoom.x2 - currentZoom.x1), abs(currentZoom.y2 - currentZoom.y1)), 0.01), 1);

    zoomPointX = ((currentZoom.x1 + currentZoom.x2) * 0.5) - (zoomScale * 0.5);
    zoomPointY = ((currentZoom.y1 + currentZoom.y2) * 0.5) - (zoomScale * 0.5);

    if (zoomPointX < 0) zoomPointX = 0;
    if (zoomPointY < 0) zoomPointY = 0;
    if (zoomPointX > 1 - zoomScale) zoomPointX = 1 - zoomScale;
    if (zoomPointY > 1 - zoomScale) zoomPointY = 1 - zoomScale;

    InvalidateRect(hwnd, NULL, false);
}

DOUBLE zoom(DOUBLE value, bool zoom_y, bool invert) {
    if (invert) {
        if (!zoom_y) return (value * zoomScale) + zoomPointX;
        else return (value * zoomScale) + zoomPointY;
    }
    else {
        if (!zoom_y) return (value - zoomPointX) / zoomScale;
        else return (value - zoomPointY) / zoomScale;
    }
}
DOUBLE normal(DOUBLE value, bool invert) {
    if (invert)
        return value * (VpMax.x - VpMin.x);
    return value / (VpMax.x - VpMin.x);
}