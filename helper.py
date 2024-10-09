import matplotlib.pyplot as plt
from matplotlib.ticker import MultipleLocator
import numpy as np
import polars as pl
from pathlib import Path
import json
import os
# import altair as alt
# import matplotlib.pyplot as plt
# from matplotlib.ticker import MultipleLocator
# import numpy as np

ALLOWABLE_BASINS = ['northwestpacific', 'northeastpacific', 'northatlantic', 'southindian', 'southpacific', 'northindian']
    
BASIN_LABELS = {
    'northwestpacific': 'Northwest Pacific',
    'northeastpacific': 'Northeast Pacific',
    'northatlantic': 'North Atlantic',
    'southindian': 'South Indian',
    'southpacific': 'South Pacific',
    'northindian': 'North Indian',
}

# from bottom to top, how Chris stacked his bars
BASIN_SORT_ORDER = [
    'northwestpacific',
    'northeastpacific',
    'northatlantic',
    'southindian',
    'southpacific',
    'northindian',
]

# Discovered from Mac's builtin Digital Color Meter app which has a color picker
BASIN_COLORS = {
    'northwestpacific': '#15027d',
    'northeastpacific': '#4677a3',
    'northatlantic': '#34aa9f',
    'southindian': '#54dacb',
    'southpacific': '#638312',
    'northindian': '#cc9c09',
}

def process_one_basin(basin):
    file_path = f'data/{basin}.json'

    with open(file_path, 'r') as file:
        # Read in json data (one file for each basin)
        data = json.load(file)
         
        # Convert json data to a list of dicts (to facilitate to conversion to a dataframe)
        records = [
            {
                'season': season,
                'named_storms': values[0],
                'named_storm_days': values[1],
                'hurricanes': values[2],
                'hurricane_days': values[3],
                'major_hurricanes': values[4],
                'major_hurricane_days': values[5],
                'ace': values[6],
            }
            for season, values in data.items()
        ]

        # Make a dataframe from the list-o-dicts
        df = (
            pl.DataFrame(records)
            .with_columns(
                pl.lit(basin).alias('basin'),
                pl.col('season').cast(pl.UInt16),
            )
        )

        # Put 'basin' column first and scoot the rest to the right
        cols = df.columns
        cols = cols[-1:] + cols[:-1]

    return df[cols]


def combine_input_sources():
    # Grab data from source .json files
    data_dir = Path('data')
    json_files = [file for file in data_dir.glob('*.json') if file.is_file()]

    # Combine all basin's pertinent data into one dataframe
    master_df = pl.DataFrame()

    for file in json_files:
        basin = file.stem
        master_df = master_df.vstack(process_one_basin(basin))

    return master_df


def extract_chart_data(master_df, metric='major_hurricanes'):
    # Grab only the data needed for the chart
    chart_df = (
        master_df
        .filter(
            pl.col('season').is_between(1980, 2023),
            pl.col('basin').is_in(ALLOWABLE_BASINS)
        )
        .select(['basin', 'season', metric])
    )

    # Convert the long table to wide
    wide = chart_df.pivot(on='season', values=metric)

    # Write df to file if necessary
    file_path = f'data/chart-source-{metric}.parquet'
    if os.path.exists(file_path):
        print('No action necessary.')
    else:
        wide.write_parquet(file_path)
        print(f'Wrote chart-source-{metric}.parquet.')

    return wide 


def make_chart(df, metric='major_hurricanes'):
    # Set metric-specific chart options
    metric_params = {
        'hurricanes': {'chart_title': 'Hurricane', 'yaxis_max': 70},
        'major_hurricanes': {'chart_title': 'Major Hurricane', 'yaxis_max': 40},
    }

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
    # plt.rcParams['font.serif'] = ['Charter', 'Times New Roman', 'Georgia', 'Charter', 'Didot']
    
    # Create the figure and an axes 
    fig, ax = plt.subplots(figsize=(width_inches, height_inches))

    # Build the stacks of bars
    bar_width = 0.8
    stack_bottoms = np.zeros(n_stacks)
    
    for basin in BASIN_SORT_ORDER:
        p = ax.bar(
            years,
            basin_hurricanes[basin],
            width=bar_width,
            label=basin,
            bottom=stack_bottoms,
            color=BASIN_COLORS[basin]
        )
        stack_bottoms += basin_hurricanes[basin]

    # Set min/max for x- and y-axis
    ax.set_xlim(1979, 2024)
    ax.set_ylim(0, metric_params[metric]['yaxis_max'])

    # Set the major and minor tick frequency
    ax.xaxis.set_major_locator(MultipleLocator(5))
    ax.xaxis.set_minor_locator(MultipleLocator(1))
    ax.tick_params(labelsize=9)

    chart_title_metric = metric_params[metric]['chart_title']
    plt.title(f'Global {chart_title_metric} Frequency (CSU data)\n1980-2023', fontsize=12)
    ax.set_ylabel('Number of Hurricanes', fontsize=10)

    # Add a footer
    footer_text_1 = 'Data source: Colorado State University (CSU) Department of Atmospheric Science'
    footer_text_2 = 'https://tropical.atmos.colostate.edu/Realtime/' 
    footer_text_3 = 'Chart: Chris Martz, Reformatted: Doug Devine'

    fig.text(0.12, 0.06, footer_text_1, ha='left', va='bottom', fontsize=8, style='italic')
    fig.text(0.12, 0.03, footer_text_2, ha='left', va='bottom', fontsize=8, style='italic')
    fig.text(0.12, 0.00, footer_text_3, ha='left', va='bottom', fontsize=8, style='italic', weight='bold')
    
    # plt.subplots_adjust(left=0.1, right=0.9, top=0.9, bottom=0.14)  # won't add this space if nothing uses that space
    # plt.margins(x=0)
    plt.subplots_adjust(bottom=0.14) 
    
    # Set the legend
    legend = ax.legend(
        ncol=3,
        loc='upper left',
        bbox_to_anchor=(0, 1),
        fontsize=8,
        handlelength=2,
    )

    # Rewrite the legend labels to human-ify the basin
    basin_labels_list = list(BASIN_LABELS.values())
    for text, label in zip(legend.get_texts(), basin_labels_list):
        text.set_text(label)

    plt.show()

    return
