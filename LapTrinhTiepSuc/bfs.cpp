#include <bits/stdc++.h>

using namespace std;

const int N = 1e3 + 10;

int n;
int d[N];
vector<int> adj[N];

void BFS(int s) {
    queue<int> Q;
    memset(d, -1, sizeof(d));
    d[s] = 0;
    Q.push(s);
    while (Q.size()) {
        int u = Q.front(); Q.pop();
        for (int v : adj[u]) {
            if (d[v] == -1) {
                d[v] = d[u] + 1;
                Q.push(v);
            }
        }
    }
    for (int i = 1; i <= n; ++i) cout << d[i] << ' ';
}

int main() {
    int m;
    cin >> n >> m;
    while (m--) {
        int u, v; cin >> u >> v;
        adj[u].push_back(v);
        adj[v].push_back(u); // undirected 
    }
    BFS(1);
    return 0;
}