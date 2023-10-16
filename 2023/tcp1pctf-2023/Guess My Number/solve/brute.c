#include <stdio.h>
#include <stdlib.h>

int main() {
    int i = 0;
    for (i = 0; i < 20; i++) {
        srand(1337);
        printf("%d\n", rand());
    }
    return 0;
}