// __inline void enable_IRQ(void) {
//     int t;
//     __asm{
//         MRS t, CPRS
//         BIC t, t, #0x80
//         MSR CPSR_c, t
//     }
// }
//
// int main(void) {
//     enable_IRQ();
// }
// https://www.ibiblio.org/gferg/ldp/GCC-Inline-Assembly-HOWTO.html
#include <stdio.h>

int main(void)
{
    int foo = 10, bar = 15;
    __asm__ __volatile__("addl  %%ebx,%%eax"
            :"=a"(foo)
            :"a"(foo), "b"(bar)
            );
    printf("foo+bar=%d\n", foo);
    return 0;
}
