import matplotlib.pyplot as plt
from matplotlib.ticker import MultipleLocator
import numpy as np

basin_labels = {
    'northwestpacific': 'Northwest Pacific',
    'northeastpacific': 'Northeast Pacific',
    'northatlantic': 'North Atlantic',
    'southindian': 'South Indian',
    'southpacific': 'South Pacific',
    'northindian': 'North Indian',
}

# from bottom to top, how Chris stacked his bars
basin_sort_order = [
    'northwestpacific',
    'northeastpacific',
    'northatlantic',
    'southindian',
    'southpacific',
    'northindian',
]

# Discovered from Mac's builtin Digital Color Meter app which has a color picker
basin_colors = {
    'northwestpacific': '#15027d',
    'northeastpacific': '#4677a3',
    'northatlantic': '#34aa9f',
    'southindian': '#54dacb',
    'southpacific': '#638312',
    'northindian': '#cc9c09',
}

def make_chart(df):
    # Set time window 
    years = [int(year) for year in df.columns[1:]] 

    # basin_hurricanes as dict {basin: list of major_hurricane values}
    basin_hurricanes = {row[0]: list(row[1:]) for row in df.rows()}

    # Calculate # of stacks needed (one for each year)
    n_stacks = len(years)
    
    # Convert pixels x pixels to inches x inches for matplotlib reasons
    width_pixels, height_pixels = 638, 522  # OG dimensions
    dpi = 100  # dealer's choice
    fudge = 1  # easier to do this than to figure out why exact dimensions causes matching weirdness
    width_inches = width_pixels / dpi + fudge
    height_inches = height_pixels / dpi
    
    # init
    plt.style.use('default')

    # Global settings for all text in the figure
    plt.rcParams['font.family'] = 'serif'
    plt.rcParams['font.serif'] = ['Charter', 'Times New Roman', 'Georgia', 'Charter', 'Didot']
    
    # Create the figure and an axes 
    fig, ax = plt.subplots(figsize=(width_inches, height_inches))

    # Build the stacks of bars
    bar_width = 0.8
    stack_bottoms = np.zeros(n_stacks)
    
    for basin in basin_sort_order:
        p = ax.bar(
            years,
            basin_hurricanes[basin],
            width=bar_width,
            label=basin,
            bottom=stack_bottoms,
            color=basin_colors[basin]
        )
        stack_bottoms += basin_hurricanes[basin]

    # Set min/max for x- and y-axis
    ax.set_xlim(1979, 2024)
    ax.set_ylim(0, 40)

    # Set the major and minor tick frequency
    ax.xaxis.set_major_locator(MultipleLocator(5))
    ax.xaxis.set_minor_locator(MultipleLocator(1))
    ax.tick_params(labelsize=10)

    ax.set_ylabel('Number of Hurricanes', fontsize=12)
    plt.title('Global Major Hurricane Frequency\n1980-2023', fontsize=14)

    # Add a footer
    footer_text_1 = 'Data source: Colorado State University (CSU) Department of Atmospheric Science'
    footer_text_2 = 'https://tropical.atmos.colostate.edu/Realtime/' 
    footer_text_3 = 'Chart: Chris Martz'

    fig.text(0.13, 0.06, footer_text_1, ha='left', va='bottom', fontsize=10, fontstyle='italic')
    fig.text(0.13, 0.03, footer_text_2, ha='left', va='bottom', fontsize=9)
    fig.text(0.13, 0.00, footer_text_3, ha='left', va='bottom', fontsize=9)

    # plt.subplots_adjust(left=0.1, right=0.9, top=0.9, bottom=0.14)  # won't add this space if nothing uses that space
    # plt.margins(x=0)
    plt.subplots_adjust(bottom=0.14) 
    
    # Set the legend
    legend = ax.legend(
        ncol=3,
        loc='upper left',
        bbox_to_anchor=(0, 1),
        fontsize=9,
        handlelength=2#1.75
    )

    # Rewrite the legend labels to human-ify the basin
    basin_labels_list = list(basin_labels.values())
    for text, label in zip(legend.get_texts(), basin_labels_list):
        text.set_text(label)

    return
