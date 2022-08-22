#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <stdbool.h>
#include <pthread.h>

#define MEMORY_SIZE (1 << 14)
#define PARTITION_SIZE (1 << 10)
#define NUM_PARTITIONS (MEMORY_SIZE / PARTITION_SIZE)
#define NONE '_'

char memory[MEMORY_SIZE];
char bitmap[NUM_PARTITIONS];


typedef struct {
    char id;
    char* name;
    size_t size;
} Process;

// get the number of partitions for a size of memory ceiling
int get_num_partitions(size_t size) {
    return size/PARTITION_SIZE + ((size % PARTITION_SIZE != 0) ? 1 : 0);
}

// search through bitmap and return the index which has space for allocation
int first_fit(size_t size) {
    const int num_parts = get_num_partitions(size);
    for (size_t i = 0; i < NUM_PARTITIONS; i++) {
        int available = i;
        while (bitmap[available] == NONE && available < NUM_PARTITIONS) {
            available++; 
            if (available - i >= num_parts)
                return i;
        }
    }
    return -1;
}

void* alloc(Process process, int(*algorithm)(size_t)) {
    int begin = algorithm(process.size);
    if (begin == -1) return NULL;
    
    int count = get_num_partitions(process.size);
    memset(bitmap + begin, process.id, count);
    return &memory[begin];
}

void dealloc(Process process) {
    int i = 0;
    while(bitmap[i] != process.id && i < NUM_PARTITIONS)
        i++;
    if (i == NUM_PARTITIONS) return;

    int count = get_num_partitions(process.size);
    memset(bitmap + i, NONE, count);
}

void print_bitmap() {
    printf("bitmap [");
    for (int i = 0; i < NUM_PARTITIONS; i++)
        printf("%c ", bitmap[i]);
    printf("\b]\n\n");
}

void* verbose_alloc(Process process) {
    int parts = get_num_partitions(process.size);
    printf(">> Allocating \'%s\' (id: '%c', partitions: %d)\n", 
        process.name, process.id, parts);

    void* result = alloc(process, first_fit);
    if (result == NULL) printf(">> (FAILED)\n");
    print_bitmap();

    return result;
}

void verbose_dealloc(Process process) {
    int parts = get_num_partitions(process.size);
    printf("<< Deallocating \'%s\' (id: '%c', partitions: %d)\n", 
        process.name, process.id, parts);
    dealloc(process);
    print_bitmap();
}


int main(int argc, char const *argv[]) {
    printf(
        "Memory size: %d | Partition size: %d | Bitmap size: %d\n",
        MEMORY_SIZE, PARTITION_SIZE, NUM_PARTITIONS
    );
    memset(bitmap, NONE, NUM_PARTITIONS);
    print_bitmap();

    Process p[] = {
        {'A', "Process 1", 1025}, // 2 parts
        {'B', "Process 2", 2050}, // 3 parts
        {'C', "Process 3", 5672}, // 6 parts
        {'D', "Process 4", 3202}, // 4 parts
    };

    verbose_alloc(p[2]);
    verbose_alloc(p[1]);

    verbose_dealloc(p[2]);
    
    verbose_alloc(p[0]);
    verbose_alloc(p[3]);
    verbose_alloc(p[2]);
    verbose_alloc(p[1]);
    return 0;
}