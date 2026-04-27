#include <windows.h>
#include <time.h>
#include <stdio.h>

int main() {
    SYSTEM_INFO sys_info;
    GetSystemInfo(&sys_info);
    long page_size = sys_info.dwPageSize;
    printf("Page size: %ld bytes\n", page_size);
    printf("Starting memory fill...\n");
    
    FILE *log = fopen("memory_log.csv", "w");
    if (log == NULL) {
        printf("Failed to open log file\n");
        return 1;
    }
    
    fprintf(log, "timestamp,pages_allocated,total_mb\n");
    
    DWORD start_time = GetTickCount();
    long long pages_allocated = 0;
    long long total_bytes = 0;
    
    #define LOG_INTERVAL_MS 100  
    #define LOG_INTERVAL_PAGES 1024 
    
    DWORD last_log_time = start_time;
    
    while (1) {
        void *page = VirtualAlloc(NULL, page_size,
                                 MEM_COMMIT | MEM_RESERVE,
                                 PAGE_READWRITE);

        if (page == NULL) {
            printf("\nVirtualAlloc failed with error %lu\n", GetLastError());
            break;
        }

        memset(page, 0, page_size);
        
        pages_allocated++;
        total_bytes += page_size;
        
        DWORD current_time = GetTickCount();
        if (current_time - last_log_time >= LOG_INTERVAL_MS || 
            pages_allocated % LOG_INTERVAL_PAGES == 0) {
            
            float total_mb = (float)total_bytes / (1024.0f * 1024.0f);
            fprintf(log, "%lu,%lld,%.2f\n", 
                    current_time - start_time, 
                    pages_allocated, 
                    total_mb);
            fflush(log);
            
            last_log_time = current_time;
            
            if (pages_allocated % (LOG_INTERVAL_PAGES * 10) == 0) {
                printf("\rAllocated: %lld pages (%.2f MB)", 
                       pages_allocated, total_mb);
            }
        }
    }
    
    DWORD end_time = GetTickCount();
    float total_mb = (float)total_bytes / (1024.0f * 1024.0f);
    fprintf(log, "%lu,%lld,%.2f\n", 
            end_time - start_time, 
            pages_allocated, 
            total_mb);
    
    fclose(log);
    
    printf("\n\nAllocation stopped\n");
    printf("Total allocated: %lld pages\n", pages_allocated);
    printf("Total memory: %.2f MB\n", total_mb);
    printf("Total time: %lu ms\n", end_time - start_time);
    printf("Log saved to memory_log.csv\n");
    
    getchar();
    
    return 0;
}
