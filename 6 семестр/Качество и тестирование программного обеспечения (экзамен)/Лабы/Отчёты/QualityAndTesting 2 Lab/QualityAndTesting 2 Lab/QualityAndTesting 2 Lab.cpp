#include <iostream>
using namespace std;

const int MAX_NODES = 10;

int graph[MAX_NODES][MAX_NODES];
int visited[MAX_NODES];
int parent[MAX_NODES];

void addEdge(int u, int v) {
    graph[u][v] = 1;
    graph[v][u] = 1;
}

bool bfsPath(int start, int end, int numNodes) {
    int queue[MAX_NODES], front = 0, rear = 0;

    for (int i = 0; i < numNodes; i++) {
        visited[i] = 0;
        parent[i] = -1;
    }

    queue[rear++] = start;
    visited[start] = 1;

    while (front < rear) {
        int node = queue[front++];

        if (node == end) {
            return true;
        }

        for (int neighbor = 0; neighbor < numNodes; neighbor++) {
            if (graph[node][neighbor] == 1 && !visited[neighbor]) {
                visited[neighbor] = 1;
                parent[neighbor] = node;
                queue[rear++] = neighbor;
            }
        }
    }

    return false;
}

void printPath(int start, int end) {
    if (parent[end] == -1) {
        cout << "Путь не найден." << endl;
        return;
    }

    int path[MAX_NODES];
    int pathLength = 0;

    for (int at = end; at != -1; at = parent[at]) {
        path[pathLength++] = at;
    }

    cout << "Путь от " << start << " до " << end << ": ";
    for (int i = pathLength - 1; i >= 0; i--) {
        cout << path[i] << (i > 0 ? " -> " : "");
    }
    cout << endl;
}

int main() {
    setlocale(LC_ALL, "Russian");

    int numNodes = 6;
    addEdge(1, 2);
    addEdge(1, 3);
    addEdge(2, 4);
    addEdge(3, 4);
    addEdge(4, 5);

    int start, end;

    while (true) {
        cout << "Введите начальную и конечную вершины (от 1 до " << numNodes-1 << "): ";
        cin >> start >> end;

        if (start < 1 || start > numNodes-1 || end < 1 || end > numNodes-1) {
            cout << "Некорректный ввод. Попробуйте снова." << endl << endl;
            continue;
        }

        if (bfsPath(start, end, numNodes)) {
            printPath(start, end);
            break; 
        }
        else {
            cout << "Путь не найден. Попробуйте снова." << endl;
        }
    }

    return 0;
}