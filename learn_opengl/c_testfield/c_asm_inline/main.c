// https://www.ibiblio.org/gferg/ldp/GCC-Inline-Assembly-HOWTO.html
#include <stdio.h>


static inline char * strcpy_asm(char * dest,const char *src) {
    int d0, d1, d2;
    __asm__ __volatile__(  "1:\tlodsb\n\t"
                           "stosb\n\t"
                           "testb %%al,%%al\n\t"
                           "jne 1b"
            : "=&S" (d0), "=&D" (d1), "=&a" (d2)
            : "0" (src),"1" (dest)
            : "memory");
    return dest;
}

int main() {
    char src_str[20] = "Mia san Mia.";
    char dst_str[20];

    strcpy_asm(dst_str, src_str);

    printf("%s -> %s  \n", src_str, dst_str);
}