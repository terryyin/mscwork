#include "stdio.h"
#include "unistd.h"
int main() {
    printf("start trip\n");
    if( access("grocery_store", F_OK ) != -1 ) {
        printf("I saw it.\n");
    } else {
        printf("what?\n");
    }
    printf("thanks for using our service\n");
}