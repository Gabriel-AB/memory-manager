#include <stdio.h>
#include <stdlib.h>
#include <pthread.h>


#define MAX_MEM (1 << 14)
#define MAX_PAR (1 << 10)

typedef struct {
    int id;
    char* nome;
    size_t size;
} process;

char memory[MAX_MEM] = {0};

int print_memory() {
    printf("")
}

int main(int argc, char const *argv[]) {
    process processes[] = {
        {1, "max", 1025},
        {2, "creito", 2049},
    };
    
    
    return 0;
}
