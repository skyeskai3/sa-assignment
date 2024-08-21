import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.animation as animation
import seaborn as sns

data = pd.read_csv('sa_assign2_money.csv', parse_dates=['Date'])

# Clean and convert data
data['Alpha Picks'] = data['Alpha Picks'].replace('[\$,]', '', regex=True).astype(float)
data['Magnificent 7'] = data['Mag 7'].replace('[\$,]', '', regex=True).astype(float)
data['S&P 500'] = data['S&P 500'].replace('[\$,]', '', regex=True).astype(float)
data['S&P 493'] = data['S&P 493'].replace('[\$,]', '', regex=True).astype(float)
data['RSP Equal Weight'] = data['RSP Equal Weight'].replace('[\$,]', '', regex=True).astype(float)

# Set up the visualization
sns.set_theme(style="whitegrid")
fig, ax = plt.subplots(figsize=(10, 6))

colors = sns.color_palette("Greens", len(data.columns)-1)[::-1]

def update(num):
    ax.clear()
    
    current_date = data['Date'].iloc[num].strftime('%b %d, %Y')  

    bars = ax.barh(['Alpha Picks', 'Magnificent 7', 'S&P 500', 'S&P 493', 'RSP Equal Weight'],
            [data['Alpha Picks'].iloc[num],
             data['Magnificent 7'].iloc[num],
             data['S&P 500'].iloc[num],
             data['S&P 493'].iloc[num],
             data['RSP Equal Weight'].iloc[num]], 
            color=colors)
    
    for bar in bars:
        ax.text(bar.get_width() + 0.1, bar.get_y() + bar.get_height()/2, 
                f'${bar.get_width():,.2f}', va='center', ha='left')
    
    ax.set_title(f'Total AUM as of {current_date}', fontsize=16, fontweight='bold')
    ax.set_xlabel('Total AUM ($)', fontsize=14, fontweight='bold')
    ax.grid(False)
    
    # Set x-axis limits
    ax.set_xlim(10000000, 15000000)
    
    # Format x-axis ticks as currency
    ax.xaxis.set_major_formatter(plt.FuncFormatter(lambda x, _: f'${x:,.0f}'))

    y_ticks = ['Alpha Picks', 'Magnificent 7', 'S&P 500', 'S&P 493', 'RSP Equal Weight']
    ax.set_yticks(range(len(y_ticks)))
    ax.set_yticklabels(y_ticks, fontsize=14)

    plt.tight_layout()

# Create animation
ani = animation.FuncAnimation(fig, update, frames=len(data), repeat=False, interval=150)

# Save animation
ani.save('aum_animation.mp4', writer='ffmpeg', fps=8)

plt.show()
