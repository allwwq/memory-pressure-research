import pandas as pd
import matplotlib.pyplot as plt

data = pd.read_csv('memory_log.csv')
data['time_seconds'] = data['timestamp'] / 1000.0

plt.figure(figsize=(12, 6))
plt.plot(data['time_seconds'], data['total_mb'], 'b-', linewidth=3)

max_memory = data['total_mb'].max()
max_time = data.loc[data['total_mb'].idxmax(), 'time_seconds']

plt.axvline(x=max_time, color='red', linestyle='--', alpha=0.7, linewidth=1)
plt.axhline(y=max_memory, color='green', linestyle='--', alpha=0.7, linewidth=1)

plt.xlabel('Time (seconds)', fontsize=12)
plt.ylabel('Memory (MB)', fontsize=12)
plt.title(f'Windows Memory Allocation\nMax: {max_memory:.0f} MB in {max_time:.1f} sec', fontsize=14)
plt.grid(True, alpha=0.3)

plt.annotate(f'Growth phase\n{max_time:.1f} sec', 
             xy=(max_time/2, max_memory/2), 
             ha='center', va='center',
             bbox=dict(boxstyle='round', facecolor='lightgreen', alpha=0.8))

plt.annotate(f'Plateau phase\n{data["time_seconds"].max()-max_time:.1f} sec', 
             xy=(max_time + (data["time_seconds"].max()-max_time)/2, max_memory/2), 
             ha='center', va='center',
             bbox=dict(boxstyle='round', facecolor='lightcoral', alpha=0.8))

plt.tight_layout()
plt.savefig('simple_memory_plot.png', dpi=150)
plt.show()

print(f"Maximum memory: {max_memory:.0f} MB")
print(f"Time to reach maximum: {max_time:.1f} sec")
print(f"Total time: {data['time_seconds'].max():.1f} sec")
print(f"Number of records: {len(data)}")
