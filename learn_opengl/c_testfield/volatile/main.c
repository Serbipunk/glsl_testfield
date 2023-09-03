// https://en.cppreference.com/w/c/language/volatile
// type in C:  qualified version of
// * const
// * volatile
// * restrict
// "volatile access" made through a lvalue expression of volatile type = observable side effect:
//            optimized & evaluated strictly,
//   == a volatile access cannot be optimized out or reordered
//
// volatile declaration in function : `void f(double x[volatile], const double y[volatile])`

#include <stdio.h>
#include <time.h>

int main(void) {
    clock_t t = clock();
    double d = 0.0;
    for (int n=0; n<10000; ++n) {
        for (int m=0; m<10000; ++m) {
            d += d*n*m;  // r & w non-volatile variable
        }
    }
    printf("Modified a non-volatile variable 100m times. "
           "Time used: %.2f seconds\n",
           (double)(clock() - t)/CLOCKS_PER_SEC);

    t = clock();
    volatile double vd = 0.0;
    for (int n=0; n<10000; ++n) {
        for (int m = 0; m < 10000; ++m) {
            volatile double prod = vd * n * m;  // r volatile variable
            vd += prod;  // w volatile variable
        }
    }
    printf("Modified a volatile variable 100m times. "
           "Time used: %.2f seconds\n",
           (double)(clock() - t)/CLOCKS_PER_SEC);
}
