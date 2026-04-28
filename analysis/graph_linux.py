import pandas as pd
import matplotlib.pyplot as plt

data = pd.read_csv('memlog.csv')

data['time'] -= data['time'].min()

max_memory = data['mb'].max()
max_time = data.loc[data['mb'].idxmax(), 'time']

plt.figure(figsize=(12, 6))

plt.step(data['time'], data['mb'], where='post',
         linewidth=2, color='blue', label=f'Allocated memory (100 MB steps)')

if len(data) > 1:
    plt.plot(data['time'], data['mb'], color='green',
             alpha=0.3, linewidth=1, linestyle='--', label='Linear interpolation')

plt.axhline(y=max_memory, color='red', linestyle='--', alpha=0.7,
            label=f'Max: {max_memory:.0f} MB')
plt.axvline(x=max_time, color='red', linestyle='--', alpha=0.7)

plt.scatter([max_time], [max_memory], color='red', s=100, zorder=5)

plt.xlabel('Time (seconds)', fontsize=12)
plt.ylabel('Allocated memory (MB)', fontsize=12)

plt.title(f'Membomb via mmap\nMax allocated: {max_memory:.0f} MB', fontsize=14)

plt.grid(True, alpha=0.3)
plt.legend(loc='best')

plt.annotate(f'Max\n{max_memory:.0f} MB',
             xy=(max_time, max_memory),
             xytext=(10, 10),
             textcoords='offset points',
             bbox=dict(boxstyle='round,pad=0.3', facecolor='yellow', alpha=0.7))

plt.tight_layout()
plt.savefig('membomb.png', dpi=150)
plt.savefig('membomb.pdf')
plt.show()

print("=" * 50)
print("MEMORY ALLOCATION STATISTICS:")
print("=" * 50)
print(f"Maximum allocated memory: {max_memory:.0f} МБ")
print(f"Time to reach maximum: {max_time:.1f} сек")
print(f"Number of records: {len(data)}")
print(f"Unique timestamps: {data['time'].nunique()}")

if data['time'].duplicated().any():
    print(f"WARNING: Duplicate timestamps detected")
    print(f"Number of duplicates: {data['time'].duplicated().sum()}")
    
    duplicates = data[data['time'].duplicated(keep=False)]
    print("Duplicate entries:")
    print(duplicates.head())

print(f"Total runtime: {data['time'].iloc[-1]:.1f} sec")

if len(data) > 1:
    total_time = data['time'].iloc[-1] - data['time'].iloc[0]
    
    if total_time > 0:
        avg_rate = max_memory / total_time
        print(f"Average rate: {avg_rate:.1f} MB/sec")
    else:
        print("Time between measurements is too small to calculate rate")

memory_changes = data['mb'].diff()
actual_steps = memory_changes[memory_changes > 0]

if len(actual_steps) > 0:
    print(f"Average step size: {actual_steps.mean():.0f} МБ")
    print(f"Number of actual allocations: {len(actual_steps)}")
    
print("=" * 50)