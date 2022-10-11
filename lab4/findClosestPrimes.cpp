#include <iostream>
#include <cmath>

using namespace std;

inline bool is_prime(uint64_t n) {
    for (uint64_t i = 2; i < sqrt(n); i++) {
        if (n % i == 0) {
            return false;
        }
    }
    
    return true;
}

uint64_t find_closest_prime(uint64_t n) {
    if (n % 2 == 0) n++;
    
    uint64_t step = 0;
    while (!(is_prime(n + step) || is_prime(n - step))) {
        cout << "Step " << step << " checked" << endl;
        step += 2;
    }
    
    return is_prime(n + step) ? (n + step) : (n - step);
}

uint64_t find_lower_prime(uint64_t n) {
    if (n % 2 == 0) n--;
    
    for (uint64_t i = 0; i < n; i++) {
        if (is_prime(n - i)) {
            return n - i;
        }
        cout << "Step " << i << " checked" << endl;
    }
    return 1;
}

int main()
{
    uint64_t n = 10000000;
    auto result = find_closest_prime(n);
    cout << "Closest prime to " << n << ": " << result << endl;
    
    n = 1000000;
    result = find_closest_prime(n);
    cout << "Closest prime to " << n << ": " << result << endl;

    return 0;
}
