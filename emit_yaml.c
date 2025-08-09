#include <stdio.h>
#include "C_header.h"

int main(void) {
    printf("---\n");
    for (size_t i = 0; i < INST_COUNT; i++) {
        printf("%s: \"%s\"\n", INST_DATA[i].key, INST_DATA[i].value);
    }
    return 0;
}

