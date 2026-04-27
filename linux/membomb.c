#include <stdio.h>
#include <sys/mman.h>
#include <time.h>
#include <stdlib.h>
#include <string.h>
#include <unistd.h>

#define MB (1024*1024UL)
#define CHUNK_SIZE (100*MB)  // 100 МБ
#define PAGE_SIZE 4096

int main() {
    FILE *log = fopen("memlog.csv", "w");
    if (!log) return 1;
    
    fprintf(log, "timestamp,mb\n");
    
    size_t total_mb = 0;
    time_t start_time = time(NULL);
    
    while (1) {
        void *p = mmap(NULL, CHUNK_SIZE,
                      PROT_READ|PROT_WRITE,
                      MAP_PRIVATE|MAP_ANONYMOUS,
                      -1, 0);
        
        if (p == MAP_FAILED) break;
        
        char *ptr = (char*)p;
        size_t pages = CHUNK_SIZE / PAGE_SIZE;
        
        for (size_t i = 0; i < pages; i++) {
            ptr[i * PAGE_SIZE] = 0;
        }
        
        total_mb += 100;
        
        time_t current_time = time(NULL);
        fprintf(log, "%ld,%zu\n", 
                current_time - start_time,
                total_mb);
        fflush(log);
    }
    
    fclose(log);
    pause();
    
    return 0;
}
