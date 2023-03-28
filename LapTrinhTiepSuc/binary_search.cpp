#include <bits/stdc++.h>

using namespace std;

long long n;

bool check(int x) {
    return 1ll * x * x <= n;
}

int main() {
    // sample: find smallest x that x^2 <= n
    n = 123;
    int l = 0, h = 1e9;
    int res = -1;
    while (l <= h) {
        int mid = (l + h) / 2;
        if (check(mid)) {
            l = mid + 1;
            res = mid;
        } else {
            h = mid - 1;
        }
    }
    cout << res << endl;;
    // sample lower_bound
    vector<int> a({1, 2, 5, 7, 12, 15});
    cout << "First >= val: " << (*lower_bound(a.begin(), a.end(), 7)) << endl;;
    cout << "First > val: " << (*upper_bound(a.begin(), a.end(), 7)) << endl;;
    return 0;
}