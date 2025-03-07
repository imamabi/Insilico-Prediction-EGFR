#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue May  9 19:49:56 2023

@author: ibrahimimam
"""


import pandas as pd
import os
import sys

# Set the directory containing the sorted results
directory = "./"

# Get the percentage of sorted results from the command line argument
if len(sys.argv) < 2:
    print("Usage: python count_common_ligands.py <percentage>")
    sys.exit(1)

#percentage = 0.01 

percentage = float(sys.argv[1])

# Initialize a dictionary to hold the ligands and their counts
ligand_counts = {}
 
# Loop through each file in the directory
for filename in os.listdir(directory):
    # Read the sorted results into a pandas dataframe
    sorted_results = pd.read_csv(os.path.join(directory, filename), delimiter="\t")

    # Calculate the number of ligands in the top percentage
    num_top_ligands = int(len(sorted_results) * percentage)
    top_ligands = sorted_results.head(num_top_ligands)

    lig_split = top_ligands['Ligand'].str.split('_', n=1, expand = True)
    
    # Count the number of unique ligands in the top percentage
    top_ligand_counts = lig_split[1].value_counts()

    # Add the counts to the overall ligand counts
    for ligand, count in top_ligand_counts.items():
        if ligand not in ligand_counts:
            ligand_counts[ligand] = count
        else:
            ligand_counts[ligand] += count

# Get the list of ligands that appear in all files
common_ligands = [ligand for ligand, count in ligand_counts.items() if count == len(os.listdir(directory))]

# Print the common ligands and their counts
print("Common Ligands:")
for ligand in common_ligands:
    print(ligand, ligand_counts[ligand])

#print (ligand_counts)
df = pd.DataFrame(ligand_counts, index = [0])
melted_df = df.melt(id_vars=None, var_name='Ligand', value_name='Frequency')
sorted_df = melted_df.sort_values(by='Frequency',ascending = False)
reset_df = sorted_df.reset_index(drop=True)

#write dataframe into file
formated_string = reset_df.to_string(index =False)
with open(f"del19_sorted-count_{percentage}DB.txt", 'w') as file:
    file.write(formated_string)
    
print(reset_df)
