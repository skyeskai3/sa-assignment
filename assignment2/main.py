import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.animation as animation
from matplotlib.dates import date2num, DateFormatter
import matplotlib.dates as mdates
from matplotlib.ticker import PercentFormatter
import seaborn as sns

data = pd.read_csv('sa_assign2.csv')
data['Date'] = pd.to_datetime(data['Date'], format='%m/%d/%y')  

for column in data.columns[1:]:
    data[column] = data[column].str.rstrip('%').astype(float) / 100.0

sns.set(style="whitegrid")

fig, ax = plt.subplots(figsize=(10, 6))  

colors = sns.color_palette("husl", n_colors=len(data.columns[1:]))  
lines = {col: ax.plot([], [], label=col, linestyle='-', linewidth=2,color=colors[i])[0] for i, col in enumerate(data.columns[1:])}

def init():
    ax.set_xlim(date2num(data['Date'].min()), date2num(data['Date'].max()))
    ax.set_ylim(-0.05, data.iloc[:, 1:].max().max() + 0.1)
    ax.xaxis.set_major_formatter(DateFormatter('%Y-%m-%d'))
    ax.xaxis.set_major_locator(mdates.MonthLocator())
    ax.yaxis.set_major_formatter(PercentFormatter(xmax=1.0))  
    ax.legend(loc='upper left', fontsize=10)  
    ax.set_ylabel('Total Return (%)', fontsize=12, fontweight='bold')  
    ax.set_title('Trading Strategies Total Return Over Time', fontsize=14)  
    plt.xticks(rotation=45, ha='right', fontsize=10)  
    plt.yticks(fontsize=10)  
    ax.grid(True)  
    fig.tight_layout()  
    return lines.values()

def update(frame):
    current_date = data['Date'].iloc[frame]
    for col, line in lines.items():
        line.set_data(data['Date'][:frame + 1], data[col][:frame + 1])
    ax.set_title("Trading Strategies Total Return Over Time", fontsize=14, fontweight='bold')
    ax.relim()
    ax.autoscale_view()
    return lines.values()

ani = animation.FuncAnimation(fig, update, frames=len(data), init_func=init, blit=True, interval=75)  # interval in milliseconds

ani.save('trading_strategies_animation.mp4', writer='ffmpeg', dpi=100)

plt.show()
