#define _CRT_SECURE_NO_WARNINGS
#include <stdio.h>
#include <iostream>
#include <string>

using namespace std;
int newBit[1000];
int main() {
	freopen("input.txt", "r", stdin);
	freopen("output.txt", "w", stdout);
	string st;
	int K;
	while (true) {
		getline(cin, st);
		cin >> K; cin.ignore(1);
		if (K == 0) break;
		int curBit = 0;
		for (int i = 0; i < st.size(); ++i) {
			st[i] ^= K;
			for (int j = 7; j >= 0; --j) {
				newBit[curBit++] = st[i] >> j & 1;
			}
		}
		for (int i = 0; i < curBit / 5; ++i) {
			int mask = 1 << 5;
			for (int j = 0; j < 5; ++j) 
				mask |= newBit[i * 5 + j] << (4 - j);
			cout << (char)mask;
		}
		cout << endl << K << endl;
	}
	return 0;
}