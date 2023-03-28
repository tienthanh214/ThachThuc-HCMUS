#include <bits/stdc++.h>

using namespace std;

const int N = 1e5 + 10;

bool isPrime[N];
void sieve() {
    memset(isPrime, true, sizeof(isPrime));
    isPrime[0] = isPrime[1] = false;
    for (int i = 2; i * i < N; ++i) 
        if (isPrime[i])
            for (int j = i + i; j < N; j += i) 
                isPrime[j] = false;
    for (int i = 1; i <= 10; ++i) if (isPrime[i]) cout << i << ' '; cout << endl;
}

int sumDivisor[N];
void sieveSumDivisor() {
    // nlgn
    for (int i = 1; i < N; ++i) {
        for (int j = i; j < N; j += i)
            sumDivisor[j] += i;
    }
    for (int i = 1; i <= 10; ++i) cout << sumDivisor[i] << ' '; cout << endl;
}

int prime[N];
void sieveForFastFactorize() {
    for (int i = 1; i < N; ++i)
        prime[i] = i;
    for (int i = 2; i * i < N; ++i)
        if (prime[i] == i)
            for (int j = i + i; j < N; j += i)
                prime[j] = i;
}

void fact(int n) {
    while (n > 1) {
        int x = prime[n];
        while (n % x == 0) {
            n /= x;
            cout << x << ' ';
        }
    }
    cout << endl;
}

int main() {
    sieve();
    
    sieveSumDivisor();
    
    sieveForFastFactorize();
    fact(2 * 2 * 3 * 3 * 3 * 5);
    return 0;
}