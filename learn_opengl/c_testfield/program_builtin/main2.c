#include <stdlib.h>
#include <stdio.h>


#if defined(__linux__)
    extern char etext, edata, end;
    void* get_etext() {
        return &etext;
    }
    void* get_edata() {
        return &edata;
    }
    void* get_end() {
        return &end;
    }
#elif defined(__APPLE__)
#include <mach-o/getsect.h>  // https://stackoverflow.com/a/9187099
#else
    printf("only support linux & osx \n");
    abort();
#endif

void f1(void) {
    puts("pushed first");
}

void f2(void) {
    puts("pushed second");
}

int main(void) {
    atexit(f1);
    atexit(f2);

    printf("    program text (etext)      %10p\n", (void*)get_etext());
    printf("    initialized data (edata)  %10p\n", (void*)get_edata());
    printf("    uninitialized data (end)  %10p\n", (void*)get_end());

    printf("## etext: \n");
    char* ptr_etext = get_etext();
    for (int i=0; i<100; ++i) {
        printf("%d,", (int)ptr_etext[i]);
    }
    printf("\n");
    printf("## edata: \n");

    char* ptr_edata = get_edata();
    for (int i=0; i<100; ++i) {
        printf("%d,", (int)ptr_edata[i]);
    }
    printf("\n");

    printf("## end: \n");
    char* ptr_end = get_end();
    for (int i=0; i<100; ++i) {
        printf("%d,", (int)ptr_end[i]);
    }
    printf("\n");

    exit(EXIT_SUCCESS);
}
