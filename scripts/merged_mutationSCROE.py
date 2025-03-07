import glob
import re
import os
import pandas as pd
import numpy as np

#A function to search ligand files in a directory ***percentage specify the percent of database   ***ligand_string common pattern in the ligand string
def search_ligands(directory, percentage, ligand_string):
    result = {}
    file_list = [file for file in os.listdir(directory) if os.path.isfile(os.path.join(directory, file))]

    for file in file_list:
        file_path = os.path.join(directory, file)
        with open(file_path, 'r') as f:
            lines = f.readlines()
            num_lines = len(lines)
            end_index = int((num_lines * percentage) // 100)
                                                                                            #changed position in line to accomodate FDA dataset
            ligands_found = [line.strip() for line in lines[:end_index] if ligand_string in line]
            if ligands_found:
                result[file] = ligands_found

    return result

#A function to strip strings from column
def lig_strip_strings(col): 
    lig = col.split('_')
    return '_'.join(lig[0:2])

#### Dataset #####
# Path to sorted results
directory_path = './FDA-approved/WT_fdaapproved/'

df1 = pd.read_csv('./FDA-approved/WT_fdaapproved_avg', sep = '\t', header=None)
df2 = pd.read_csv('./FDA-approved/WT_fdaapproved_min', sep = '\t', header=None)
dfs = {'Mutation_avg':df1, 'Mutation_min':df2}


percentage = 10  # % of lines to be searched in each file
ligand_prefix = 'pdbqt'  # Starting string pattern to search for

search_result = search_ligands(directory_path, percentage, ligand_prefix)

#print (search_result)

#Formatting the ave and min file 

data_df = {}         #To hold dataframe for formatting
data_list = {}          #To hold final formatted string

for key in dfs:
    df = dfs[key]
    num_top_ligands = int(len(df) * (percentage/100))
    top_ligands = df.head(num_top_ligands)
    top_ligands[1] = top_ligands[1].apply(lig_strip_strings)
    data_df[key] = top_ligands
    
    top_lig_list = list(top_ligands[1])
    data_list[key] = top_lig_list

# Format the name of the values in the dictionary
part_index = 3  # Index of the part you want to extract after splitting

# Create a new dictionary with extracted parts
extracted_search = {}

for key, value in search_result.items():
    if isinstance(value, str):
        split_parts = value.split('_')
        if len(split_parts) > part_index:
            extracted_value = '_'.join(split_parts[part_index:part_index+2])
            extracted_value = extracted_value.replace(".pdbqt", "")
            extracted_search[key] = extracted_value
    elif isinstance(value, list):
        extracted_values = []
        for item in value:
            split_parts = item.split('_')
            if len(split_parts) > part_index:
                extracted_value = '_'.join(split_parts[part_index:part_index+2])
                extracted_value = extracted_value.replace(".pdbqt", "")
                extracted_values.append(extracted_value)
        extracted_search[key] = extracted_values

#print(extracted_search)

#Format the name of the keys in dictionary 
prefix_to_delete = '_sorted_results_cleaned'

formatted_dict = {}

for key, value in extracted_search.items():
    if key.endswith(prefix_to_delete):
        new_key = key[:-(len(prefix_to_delete))] # Delete the prefix from the key (note: edit this part as deemed fit)
    else:
        new_key = key

    formatted_dict[new_key] = value

#Add the 'ave and min' data_list to the formatted dictionary
formatted_dict.update(data_list)
#print (formatted_dict)

max_length = max(len(arr) for arr in formatted_dict.values())  # Find the maximum length among all arrays

# Pad arrays with shorter lengths with NaN values to match the maximum length
processed_data = {key: arr + [float('nan')] * (max_length - len(arr)) for key, arr in formatted_dict.items()}

df = pd.DataFrame.from_dict(processed_data)
#print (df.head(50))

#Drop NaN values from the DataFrame
df.fillna('y',inplace=True)

# Get unique items from all columns
unique_items = set(df.values.flatten())

# Create a new DataFrame with the unique items as the index
new_df = pd.DataFrame(index=unique_items, columns=df.columns)

# Replace values with 1 where the item is present
for column in df.columns:
    for item in df[column]:
        if pd.notnull(item):
            new_df.loc[item, column] = 1

# Fill NaN values with 0
new_df.fillna(0, inplace=True)

print (new_df.head(40))


#This part will write the tabulated output in an excel format without the avg and min
'''file_path = f'/Users/ibrahimimam/Desktop/Project1/new_result_analysis/trials/FDA_del19_table{percentage}DB.xlsx'
new_df.to_excel(file_path, index=True)'''

#To part will obtained the intersect (common ligand) between the two dataframes
'''recommend = set(df['Mutation_avg']) & set(df['Mutation_min'])
r_df= pd.DataFrame(recommend)'''


#Handling the avg and min dataset - preparing for merging with formatted df
df_min = df2
df_avg = df1
df_min.columns = ['Rank', 'Ligand']
df_avg.columns = ['Rank', 'Ligand']

print (df_min)

# Reset index column in df2
new_df1 = new_df.reset_index().rename(columns={'index': 'Lig'})
new_df1

#Merge the dataframes
merged_df1 = new_df1.merge(df_avg, left_on='Lig', right_on='Ligand')
merged_df2 = merged_df1.merge(df_min, left_on='Lig', right_on='Ligand')
merged_df2

#Writing the final result into excel file
f_path = f'/Users/ibrahimimam/Desktop/Project1/new_result_analysis/trials/merged_clean_WT_tableDB.xlsx'
merged_df2.to_excel(f_path, index=False)


