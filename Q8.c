#include <stdio.h>

int main() {

    char c[]={'c', 'o', 'l', 'u', 'm', 'b', 'i', 'a'};
    char u[]={'u', 'n', 'i', 'v', 'e', 'r', 's', 'i', 't','y'};
    char *pc = c;
    char *pu = u;
    char t[10];
    // Q1
    for (int i = 0; i < 10; i++) {
        t[i] = u[i];
    }
    
    // Q2
    char *pt = t;
    for (int i = 0; i < 10; i++) {
        printf("%c", *(pt+i));
    }
    // Q3
    printf("\nThe last character of the array t is: %c\n", *(pt+9));
    return 0;
}