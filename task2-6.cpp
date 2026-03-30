#include <iostream>
#include <vector>
#include <ctime>
#include <cstdlib>
#include <boost/multiprecision/cpp_int.hpp>

using namespace std;
using boost::multiprecision::cpp_int;

long long tinhmod(long long a, long long b, long long m) {
    long long res = 1;
    a %= m;
    while (b > 0) {
        if (b % 2 == 1) {
            res = (__int128)res * a % m;
        }
        a = (__int128)a * a % m;
        b /= 2;
    }
    return res;
}

cpp_int binaryPower(cpp_int a, cpp_int k, cpp_int n) {
    a %= n;
    cpp_int res = 1;
    while (k > 0) {
        if ((k & 1) != 0)
            res = (res * a) % n;
        a = (a * a) % n;
        k >>= 1;
    }
    return res;
}

bool test(cpp_int a, cpp_int n, cpp_int k, cpp_int m) {
    cpp_int mod = binaryPower(a, m, n);
    if (mod == 1 || mod == n - 1)
        return true;

    for (cpp_int l = 1; l < k; ++l) {
        mod = (mod * mod) % n;
        if (mod == n - 1)
            return true;
    }
    return false;
}

bool RabinMiller(cpp_int n) {
    if (n == 2 || n == 3 || n == 5 || n == 7)
        return true;
    if (n < 2 || (n % 2) == 0)
        return false;

    cpp_int k = 0, m = n - 1;
    while ((m % 2) == 0) {
        m /= 2;
        ++k;
    }

    vector<long long> bases = {2, 3, 5, 7, 11, 13, 17};
    for (long long b : bases) {
        if (cpp_int(b) >= n)
            continue;
        if (!test(cpp_int(b), n, k, m))
            return false;
    }
    return true;
}

bool miller_rabin(long long n, int a) {
    if (n <= 1) return false;
    if (n == 2 || n == 3) return true;
    if (n % 2 == 0) return false;

    if (a % n == 0) return true;

    long long d = n - 1;
    while (d % 2 == 0) d /= 2;

    long long x = tinhmod(a, d, n);
    if (x == 1 || x == n - 1) return true;

    while (d != n - 1) {
        x = (__int128)x * x % n;
        d *= 2;
        if (x == n - 1) return true;
        if (x == 1) return false;
    }
    return false;
}

bool isPrimeSmall(long long num) {
    if (num <= 1) return false;
    if (num <= 3) return true;
    if (num % 2 == 0 || num % 3 == 0) return false;
    for (long long i = 5; i * i <= num; i += 6) {
        if (num % i == 0 || num % (i + 2) == 0) return false;
    }
    return true;
}

bool taosoprime(int lc) {
    srand((unsigned)time(0));

    if (lc == 1) {
        while (true) {
            int num = rand() % 8 + 2; // 2..9
            if (isPrimeSmall(num)) {
                cout << "So duoc tao: " << num << endl;
                return true;
            }
        }
    }
    else if (lc == 2) {
        while (true) {
            int num = rand() % 91 + 10; // 10..100
            if (isPrimeSmall(num)) {
                cout << "So duoc tao: " << num << endl;
                return true;
            }
        }
    }
    else if (lc == 3) {
        while (true) {
            long long num = rand() % (100000000 - 10000000) + 10000000;
            if (RabinMiller(num)) {
                cout << "So duoc tao: " << num << endl;
                return true;
            }
        }
    }

    return false;
}

int gcd(int a, int b) {
    if (b == 0) return a;
    return gcd(b, a % b);
}

int main() {
    int lc;
    cout << "Nhap lua chon do lon cua so nguyen to (1.8bit, 2.16bit, 3.64bit): ";
    cin >> lc;

    if (taosoprime(lc)) {
        cout << "So da tao co kha nang la so nguyen to." << endl;
    } else {
        cout << "Lua chon khong hop le hoac so tao ra khong phai so nguyen to." << endl;
    }

    int x, y;
    cout << "Nhap x va y: ";
    cin >> x >> y;
    cout << "Uoc chung lon nhat cua " << x << " va " << y << " la: " << gcd(x, y) << endl;

    cpp_int mersenne10 = (cpp_int(1) << 89) - 1;
    cpp_int z = mersenne10 - 1;

    cout << "Mersenne 2^89 - 1 = " << mersenne10 << endl;
    cout << "z = mersenne10 - 1 = " << z << endl;

    vector<cpp_int> primes;
    cpp_int start = mersenne10 - 1;

    while (primes.size() < 10 && start > 2) {
        if (RabinMiller(start)) {
            primes.push_back(start);
        }
        --start;
    }

    cout << "10 so nguyen to lon nhat nho hon so Mersenne thu 10:" << endl;
    for (size_t i = 0; i < primes.size(); ++i) {
        cout << i + 1 << ": " << primes[i] << endl;
    }

    cpp_int t;
    cout << "Nhap mot so n < 2^89 - 1: ";
    cin >> t;

    if (t < mersenne10 && RabinMiller(t))
        cout << t << " la so nguyen to." << endl;
    else
        cout << t << " khong phai la so nguyen to (hoac khong hop le)." << endl;

    return 0;
}