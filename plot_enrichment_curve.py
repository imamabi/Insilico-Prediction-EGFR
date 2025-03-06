import os
import re
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.font_manager import FontProperties

# Set up font properties for the plot
font = {'weight': 'bold', 'size': 12}
plt.rc('font', **font)

def natural_sort_key(s):
    """Helper function to sort filenames in a natural order."""
    return [int(text) if text.isdigit() else text.lower() for text in re.split(r'(\d+)', s)]

def get_txt_files(directory):
    """Retrieve and sort all .txt files in the given directory."""
    txt_files = [f for f in os.listdir(directory) if f.endswith('.txt')]
    return sorted(txt_files, key=natural_sort_key)

def extract_prefix(directory):
    """Extract the last part of the directory path as a prefix."""
    return os.path.basename(directory)

def plot_enrichment(directory_path, save_prefix):
    """Generate and save enrichment plots based on data from the given directory."""
    prefix = extract_prefix(directory_path)
    txt_files_list = get_txt_files(directory_path)
    print(f"Processing {prefix}: {txt_files_list}")
    
    # Define special files with predefined roles
    specials = [
        f'{prefix}_avg_enrichment.txt', 
        f'{prefix}_min_enrichment.txt', 
        f'{prefix}-0-1_enrichment.txt', 
        f'sorted_results_{prefix}_0_1_enrichment.txt'
    ]
    
    # Iterate through each text file in the directory
    for file in txt_files_list:
        file_path = os.path.join(directory_path, file)
        
        # Process filename to extract meaningful labels
        name = re.sub(r'(_sorted_results|sorted_results_|_enrichment|bs|c)', '', file)
        name = name.replace(f'{prefix}-', '').replace(f'{prefix}_', '').replace('-', '_')
        
        # Load data from file (assumes two-column tab-separated format)
        x, y = np.loadtxt(file_path, delimiter='\t', unpack=True)
        
        # Skip processing for average and minimum enrichment files
        if file in [f'{prefix}_min_enrichment.txt', f'{prefix}_avg_enrichment.txt']:
            continue
        # Plot general enrichment curves
        elif file not in specials:
            plt.plot(x, y, label=f"${name}$", alpha=0.8)
        # Special handling for 0-1 enrichment files
        elif file in [f'{prefix}-0-1_enrichment.txt', f'sorted_results_{prefix}_0_1_enrichment.txt']:
            plt.plot(x, y, color='black', label="$0_1$")
    
    # Process and plot the special files
    for file in specials:
        file_path = os.path.join(directory_path, file)
        if not os.path.exists(file_path):
            continue
        x, y = np.loadtxt(file_path, delimiter='\t', unpack=True)
        if file == f'{prefix}_avg_enrichment.txt':
            plt.plot(x, y, color='blue', linestyle='--', label="average")
        elif file == f'{prefix}_min_enrichment.txt':
            plt.plot(x, y, color='maroon', linestyle='--', label="best energy")
    
    # Plot random baseline
    plt.plot([0, 100], [0, 100], color='black', linestyle='--', label="random")
    
    # Configure axis labels and limits
    plt.ylabel('Known binding molecules (%)', fontsize=16, fontweight='bold')
    plt.xlabel('Tested Molecules (%)', fontsize=16, fontweight='bold')
    plt.xlim(0, 10)
    plt.ylim(0, 55 if 'fda-approved' in directory_path else 25)
    
    # Configure legend placement and styling
    plt.legend(handlelength=3.5, handletextpad=0.2, fontsize=9, loc="center left", 
               bbox_to_anchor=(1, 0.52), title="Conformation$_{binding_ site}$")
    
    # Save the plot to a file
    plt.savefig(f'{save_prefix}_{prefix}.png', bbox_inches='tight', dpi=600)
    plt.show()


for directory in directories:
    plot_enrichment(directory, "enrichment_plot")

benchmarks=['fda-approved', 'dekois']
variants=['WT', 'T790M', 'L858R', 'del19']
directories = []
for benchmark in benchmarks:
    for variant in variants:
        directory=f'/Users/ibrahimimam/Desktop/Project1_docking/new_result_analysis/enrichment/{benchmark}/{variant}'
        directories.append(directory)

for directory in directories:
    plot_enrichment(directory, "enrichment_plot")

