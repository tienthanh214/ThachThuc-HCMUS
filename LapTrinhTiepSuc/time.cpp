#include <bits/stdc++.h>
#include <ctime>
 
using namespace std;
 
typedef long long LL;
 
LL getTime(const string& x) {
    istringstream ss(x);
    tm t{};
    ss >> std::get_time(&t, "%d-%m-%Y");
    return mktime(&t);
}
 
LL nextDay(LL x, int k) {
    time_t temp = x + k * 24 * 60 * 60;
    tm t;
    t = *localtime(&temp);
    cout << t.tm_wday + 1 << " " << t.tm_mday << " " << t.tm_mon + 1 << " " << t.tm_year + 1900 << endl;
    return mktime(&t);
}
 
/*
tm t;
t.tm_wday = [0..7] Sunday to Saturday
t.tm_mday = ngay
t.tm_mon = thang [0..11] + 1 them nhe
t.tm_year = nam (+ 1900 them nhe)
*/
 
int main() {
    // get different day
    cout << (getTime("20-03-2021") - getTime("18-03-2021")) / (24 * 60 * 60) << endl;
    // get next k day
    nextDay(getTime("21-03-2021"), 0);
    return 0;
}