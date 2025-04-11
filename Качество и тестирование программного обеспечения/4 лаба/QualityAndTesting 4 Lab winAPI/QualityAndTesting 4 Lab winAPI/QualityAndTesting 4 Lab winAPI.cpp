#include <windows.h>
#include <windowsx.h>
#include <tchar.h>
#include <iostream>
#include <sstream>
#include <vector>

using namespace std;

// Объявление функций
BOOL RegClass(WNDPROC, LPCTSTR, HBRUSH);
LRESULT CALLBACK WndProc(HWND, UINT, WPARAM, LPARAM);
void addEdge(int, int);
bool edgeExists(int, int);
void findAllPaths(int, int, vector<int>&, vector<vector<int>>&); 
void printAllPaths(vector<vector<int>>&, HWND); 
void CreateControls(HWND);
void HandleCommand(HWND, WPARAM);

// Описание глобальных переменных
HINSTANCE hInst;
HBRUSH hBrushBackground;
static HWND hNumNodes, hAddEdge, hAddStart, hAddEnd, hStart, hEnd, hEdgeList;
const int MAX_NODES = 10;
int graph[MAX_NODES][MAX_NODES] = { 0 };
int visited[MAX_NODES] = { 0 };
int numNodes = 0;

int WINAPI WinMain(HINSTANCE hInstance, HINSTANCE hPrevlnstance, LPSTR lpszCmdLine, int nCmdShow) {
    MSG msg;
    HWND hwnd;
    hInst = hInstance;
    hBrushBackground = CreateSolidBrush(RGB(230, 220, 250));

    if (!RegClass(WndProc, L"My class", hBrushBackground)) {
        return false;
    }

    hwnd = CreateWindow(L"My class", L"Качество и тестирование ПО, 4 лаба",
        WS_OVERLAPPEDWINDOW | WS_VISIBLE,
        CW_USEDEFAULT, CW_USEDEFAULT, 570, 400, 0, 0, hInstance, NULL);
    if (!hwnd) {
        return false;
    }

    while (GetMessage(&msg, NULL, 0, 0) > 0) {
        TranslateMessage(&msg);
        DispatchMessage(&msg);
    }

    DeleteObject(hBrushBackground);

    return msg.wParam;
}

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

LRESULT CALLBACK WndProc(HWND hwnd, UINT msg, WPARAM wParam, LPARAM lParam) {
    switch (msg) {
    case WM_CREATE:
        CreateControls(hwnd);
        break;
    case WM_COMMAND:
        HandleCommand(hwnd, wParam);
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

HWND setbutton;
HWND addbutton;
HWND findbutton;

void CreateControls(HWND hwnd) {
    CreateWindow(L"STATIC", L"Количество вершин (не более 10):", WS_VISIBLE | WS_CHILD, 20, 20, 270, 30, hwnd, NULL, NULL, NULL);
    hNumNodes = CreateWindow(L"EDIT", L"", WS_VISIBLE | WS_CHILD | WS_BORDER, 300, 20, 100, 30, hwnd, NULL, NULL, NULL);
    setbutton = CreateWindow(L"BUTTON", L"Установить", WS_VISIBLE | WS_CHILD, 410, 20, 100, 30, hwnd, (HMENU)1, NULL, NULL);

    CreateWindow(L"STATIC", L"Введите две связанные вершины:", WS_VISIBLE | WS_CHILD, 20, 70, 270, 30, hwnd, NULL, NULL, NULL);
    hAddStart = CreateWindow(L"EDIT", L"", WS_VISIBLE | WS_CHILD | WS_BORDER, 300, 70, 45, 30, hwnd, NULL, NULL, NULL);
    hAddEnd = CreateWindow(L"EDIT", L"", WS_VISIBLE | WS_CHILD | WS_BORDER, 355, 70, 45, 30, hwnd, NULL, NULL, NULL);
    addbutton = CreateWindow(L"BUTTON", L"Добавить", WS_VISIBLE | WS_CHILD | WS_DISABLED, 410, 70, 100, 30, hwnd, (HMENU)2, NULL, NULL);

    CreateWindow(L"STATIC", L"Начальная и конечная вершины:", WS_VISIBLE | WS_CHILD, 20, 120, 270, 30, hwnd, NULL, NULL, NULL);
    hStart = CreateWindow(L"EDIT", L"", WS_VISIBLE | WS_CHILD | WS_BORDER, 300, 120, 45, 30, hwnd, NULL, NULL, NULL);
    hEnd = CreateWindow(L"EDIT", L"", WS_VISIBLE | WS_CHILD | WS_BORDER, 355, 120, 45, 30, hwnd, NULL, NULL, NULL);
    findbutton = CreateWindow(L"BUTTON", L"Найти путь", WS_VISIBLE | WS_CHILD | WS_DISABLED, 410, 120, 100, 30, hwnd, (HMENU)3, NULL, NULL);

    hEdgeList = CreateWindow(L"LISTBOX", NULL, WS_CHILD | WS_VISIBLE | LBS_HASSTRINGS | WS_VSCROLL,
        20, 170, 510, 150, hwnd, NULL, NULL, NULL);
}

void addEdge(int u, int v) {
    graph[u - 1][v - 1] = 1; 
    graph[v - 1][u - 1] = 1; 
}

bool edgeExists(int u, int v) {
    return graph[u - 1][v - 1] == 1; 
}

void findAllPaths(int start, int end, vector<int>& path, vector<vector<int>>& allPaths) {
    visited[start - 1] = 1;
    path.push_back(start);

    if (start == end) {
        allPaths.push_back(path); 
    }
    else {
        for (int neighbor = 0; neighbor < numNodes; neighbor++) {
            if (graph[start - 1][neighbor] == 1 && !visited[neighbor]) {
                findAllPaths(neighbor + 1, end, path, allPaths);
            }
        }
    }

    path.pop_back(); 
    visited[start - 1] = 0; 
}

void printAllPaths(vector<vector<int>>& allPaths, HWND hwnd) {
    if (allPaths.empty()) {
        MessageBox(hwnd, L"Пути не найдены.", L"Результат", MB_OK);
        return;
    }

    std::wstringstream pathStream;
    for (const auto& path : allPaths) {
        for (size_t i = 0; i < path.size(); ++i) {
            pathStream << path[i];
            if (i != path.size() - 1) {
                pathStream << L" -> ";
            }
        }
        pathStream << L"\n";
    }

    std::wstring pathStr = pathStream.str();
    MessageBox(hwnd, pathStr.c_str(), L"Все пути", MB_OK);
}

void HandleCommand(HWND hwnd, WPARAM wParam) {
    if (LOWORD(wParam) == 1) {
        TCHAR buffer[10];
        GetWindowText(hNumNodes, buffer, 10);
        numNodes = _ttoi(buffer);
        if (numNodes <= 0 || numNodes > MAX_NODES) {
            SendMessage(hEdgeList, LB_RESETCONTENT, 0, 0);
            MessageBox(hwnd, L"Некорректное количество вершин.", L"Ошибка", MB_OK);
        }
        else {
            memset(graph, 0, sizeof(graph));
            SendMessage(hEdgeList, LB_RESETCONTENT, 0, 0);
            EnableWindow(addbutton, TRUE);
            EnableWindow(findbutton, FALSE);
            MessageBox(hwnd, L"Количество вершин установлено.", L"Успех", MB_OK);
        }
    }
    else if (LOWORD(wParam) == 2) {
        TCHAR startBuffer[10], endBuffer[10];
        GetWindowText(hAddStart, startBuffer, 10);
        GetWindowText(hAddEnd, endBuffer, 10);

        int u = _ttoi(startBuffer);
        int v = _ttoi(endBuffer);

        if (u >= 1 && u <= numNodes && v >= 1 && v <= numNodes) {
            if (!edgeExists(u, v)) {
                addEdge(u, v);
                MessageBox(hwnd, L"Связь добавлена.", L"Успех", MB_OK);
                EnableWindow(findbutton, TRUE);

                wstringstream edgeStream;
                edgeStream << u << L" <-> " << v;
                SendMessage(hEdgeList, LB_ADDSTRING, 0, (LPARAM)edgeStream.str().c_str());

                SetWindowText(hAddStart, L"");
                SetWindowText(hAddEnd, L"");
            }
            else {
                SetWindowText(hAddStart, L"");
                SetWindowText(hAddEnd, L"");
                MessageBox(hwnd, L"Связь уже существует.", L"Ошибка", MB_OK);
            }
        }
        else {
            SetWindowText(hAddStart, L"");
            SetWindowText(hAddEnd, L"");
            MessageBox(hwnd, L"Некорректные вершины.", L"Ошибка", MB_OK);
        }
    }
    else if (LOWORD(wParam) == 3) {
        TCHAR startBuffer[10], endBuffer[10];
        GetWindowText(hStart, startBuffer, 10);
        GetWindowText(hEnd, endBuffer, 10);
        int start = _ttoi(startBuffer);
        int end = _ttoi(endBuffer);

        if (start >= 1 && start <= numNodes && end >= 1 && end <= numNodes) {
            vector<int> path;
            vector<vector<int>> allPaths;
            memset(visited, 0, sizeof(visited));
            findAllPaths(start, end, path, allPaths);

            SetWindowText(hStart, L"");
            SetWindowText(hEnd, L"");

            printAllPaths(allPaths, hwnd);
        }
        else {
            SetWindowText(hStart, L"");
            SetWindowText(hEnd, L"");
            MessageBox(hwnd, L"Некорректные начальная или конечная вершина.", L"Ошибка", MB_OK);
        }
    }
}