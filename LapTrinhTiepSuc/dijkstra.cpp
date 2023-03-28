#include <bits/stdc++.h>

using namespace std;

const int N = 1e3 + 10;

typedef pair<int, int> ii;

int n;
vector<ii> adj[N];
int d[N];

void dij(int s) {
    priority_queue<ii, vector<ii>, greater<ii>> heap;
    for (int i = 1; i <= n; ++i)
        d[i] = 1e9;
    d[s] = 0;
    heap.push({0, s});
    while (heap.size()) {
        int u = heap.top().second;
        heap.pop();
        // for (auto [v, w] : adj) // uoc gi duoc for nhu nay
        for (int i = 0; i < adj[u].size(); ++i) {
            int v = adj[u][i].second;
            int w = adj[u][i].first;
            if (d[v] > d[u] + w) {
                d[v] = d[u] + w;
                heap.push({d[v], v});
            }
        }
    }

    for (int i = 1; i <= n; ++i) {
        cout << d[i] << ' ';
    }
}

int main() {
    int m; cin >> n >> m;
    while (m--) {
        int u, v, w;
        cin >> u >> v >> w;
        adj[u].push_back({w, v});
        adj[v].push_back({w, u});
    }
    
    dij(1);

    return 0;
}