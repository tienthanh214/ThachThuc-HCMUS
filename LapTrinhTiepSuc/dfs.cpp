#include <bits/stdc++.h>

using namespace std;

const int N = 105;

int n;
vector<int> adj[N];
bool visited[N];
// check if found from src to b
bool DFS(int u, int b) {
    if (u == b) return true;
    visited[u] = true;
    for (int v : adj[u]) if (!visited[v]) {
        if (DFS(v, b)) return true;
    }
    return false;
}

int main() {
    int m;
    cin >> n >> m;
    while (m--) {
        int u, v; cin >> u >> v;
        adj[u].push_back(v);
        adj[v].push_back(u); // undirected 
    }
    cout << DFS(1, n) << endl;
    return 0;
}