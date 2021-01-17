#include <iostream>
#include <vector>
#include <algorithm>
#include <cmath>
#include <string>
#include <utility>
#include <tuple>
 
// #define f first
// #define s second
#define input(v) for (auto& val : v) cin >> val;
#define output(v, c) for (auto& val : v) cout << val << c;
#define pb push_back
 
using namespace std;
 
typedef long long ll;
typedef unsigned long ul;
typedef long double ld;
 
int main() {
    ios_base::sync_with_stdio(false);
    cin.tie(0);
    cout.tie(0);
    cout << fixed;
    cout.precision(6);
 
    // В массивах хранятся числители дроби со знаменателем 10^i
    ll E[10];
    ll O[10];
    ll I[10];
    E[0] = 1;
    O[0] = 0;
    I[0] = 0;
 
    ll sum = 0; // Числитель дроби суммы I
 
    for (long i = 1; i <= 9; ++i) {
        E[i] = 5 * O[i - 1] + 7 * I[i - 1];
        O[i] = 2 * E[i - 1] + 3 * I[i - 1];
        I[i] = 8 * E[i - 1] + 5 * O[i - 1];
        sum = I[i] + 10 * sum;
    }
 
    cout << sum;
 
    return 0;
}