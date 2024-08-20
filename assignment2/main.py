import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.animation as animation
from matplotlib.dates import date2num, DateFormatter
import matplotlib.dates as mdates
from matplotlib.ticker import PercentFormatter
import seaborn as sns

# Load and prepare data
data = pd.read_csv('sa_assign2.csv')
data['Date'] = pd.to_datetime(data['Date'], format='%m/%d/%y')

# Convert percentage to float
for column in data.columns[1:]:
    data[column] = data[column].str.rstrip('%').astype(float) / 100.0

# Set the style using seaborn
sns.set_theme(style="whitegrid")

# Set up the figure and axis
fig, ax = plt.subplots(figsize=(12, 8))  # Larger figure size

# Define colors and initialize lines
colors = sns.color_palette("husl", n_colors=len(data.columns[1:]))
lines = {col: ax.plot([], [], label=col, linestyle='-', linewidth=2, color=colors[i])[0] for i, col in enumerate(data.columns[1:])}

# Initialize text annotations
texts = {col: ax.text(0, 0, '', color='black', fontsize=10, ha='left', va='center', visible=False) for col in data.columns[1:]}

def init():
    ax.set_xlim(date2num(data['Date'].min()), date2num(data['Date'].max()))
    ax.set_ylim(-0.05, data.iloc[:, 1:].max().max() + 0.1)
    # Set x-axis date format to "Jan 2024", "Feb 2024", etc.
    ax.xaxis.set_major_formatter(DateFormatter('%b %Y'))
    ax.xaxis.set_major_locator(mdates.MonthLocator())
    ax.yaxis.set_major_formatter(PercentFormatter(xmax=1.0))
    ax.legend(loc='upper left', fontsize=10)
    ax.set_ylabel('Total Return (%)', fontsize=12, fontweight='bold')
    ax.set_title('Trading Strategies Total Return Over Time', fontsize=14, fontweight='bold')
    plt.xticks(rotation=45, ha='right', fontsize=10)
    plt.yticks(fontsize=10)
    ax.grid(True)
    plt.subplots_adjust(left=0.1, right=0.9, top=0.9, bottom=0.1)  # Adjust layout manually
    return [*lines.values()] + [*texts.values()]

def update(frame):
    if frame < len(data):
        # Update the plot with current frame data
        for col, line in lines.items():
            line.set_data(data['Date'][:frame + 1], data[col][:frame + 1])
        ax.set_title(f"Progress as of {data['Date'].iloc[frame].strftime('%b %Y')}", fontsize=14, fontweight='bold')
        # Hide the text annotations during the animation
        for text in texts.values():
            text.set_visible(False)
    else:
        # Show final frame data and text
        final_frame = len(data) - 1
        for col, line in lines.items():
            line.set_data(data['Date'][:final_frame + 1], data[col][:final_frame + 1])
            y_value = data[col].iloc[-1] * 100
            x_value = data['Date'].iloc[-1]
            # Ensure that the text is positioned correctly
            text_position = (date2num(x_value), y_value)
            texts[col].set_position(text_position)
            texts[col].set_text(f'{y_value:.1f}%')
            texts[col].set_visible(True)
        
        # Adjust y-limits to make sure final values are visible
        #ax.set_ylim(min(data.iloc[:, 1:].min()) - 0.1, max(data.iloc[:, 1:].max()) + 0.1)
        ax.set_title("Total Returns Per Strategy (YTD)", fontsize=14, fontweight='bold')

    #ax.relim()
    #ax.autoscale_view()
    return [*lines.values()] + [*texts.values()]

# Create the animation with extra frames to show the final values
extra_frames = 60  # Number of frames to show the final values
total_frames = len(data) + extra_frames
ani = animation.FuncAnimation(fig, update, frames=total_frames, init_func=init, blit=True, interval=75)

# Save the animation as an MP4
ani.save('trading_strategies_animation.mp4', writer='ffmpeg', dpi=100)

plt.show()
