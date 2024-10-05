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
    'southpacific': '#648412',
    'northindian': '#cc9c09',
}

def make_chart(df):
    # Set time window 
    years = [int(year) for year in df.columns[1:]] 

    # basin_hurricanes as dict {basin: list of major_hurricane values}
    basin_hurricanes = {row[0]: list(row[1:]) for row in df.rows()}

    # Calculate # of stacks needed (one for each year)
    n_stacks = len(years)

    # Initialize stack_bottoms to np.zeros(n_stacks)
    stack_bottoms = np.zeros(n_stacks)

    width = 0.8
    fig, ax = plt.subplots(figsize=(6, 4.25))

    # Build the stack
    for basin in basin_sort_order:
        p = ax.bar(
            years,
            basin_hurricanes[basin],
            width=width,
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
    ax.tick_params(labelsize=8)

    # Customize the plot
    plt.rcParams['font.family'] = 'serif'
    plt.rcParams['font.serif'] = ['Charter', 'Didot']
    plt.ylabel('Number of Hurricanes', fontsize=10)
    plt.title('Global Major Hurricane Frequency\n1980-2023')

    # Add a footer
    plt.subplots_adjust(bottom=0.14)  # won't add this space if nothing uses that space
    footer_text_1 = 'Data source: Colorado State University (CSU) Department of Atmospheric Science'
    footer_text_2 = 'https://tropical.atmos.colostate.edu/Realtime/' 
    footer_text_3 = 'Chart: Chris Martz'

    fig.text(.13, 0.06, footer_text_1, ha='left', va='center', fontsize=7)
    fig.text(.13, 0.03, footer_text_2, ha='left', va='center', fontsize=7)
    fig.text(.13, 0, footer_text_3, ha='left', va='center', fontsize=7)

    # Set the legend
    legend = ax.legend(
        ncol=3,
        loc='upper left',
        bbox_to_anchor=(0, 1),
        fontsize=8,
        handlelength=1.75
    )

    # Rewrite the legend labels to human-ify the basin
    basin_labels_list = list(basin_labels.values())
    for text, label in zip(legend.get_texts(), basin_labels_list):
        text.set_text(label)

    return
