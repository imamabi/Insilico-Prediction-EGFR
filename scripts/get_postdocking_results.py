import glob
import os

# Get the current directory name
current_directory = os.path.basename(os.getcwd())

# Get list of result files in the directory
file_list = glob.glob('*.pdbqt*')

# Dictionary for storing results
results = {}

print(len(file_list))

for file_name in file_list:
    result_file = open(file_name, 'r')
    line = result_file.readline()
    # Skip to best energy
    line = result_file.readline()
    # Get energy
    energy_line = line.split()
    try:
        best_energy = float(energy_line[3])
    except IndexError:
        print(file_name)

    # Store in dictionary
    if best_energy not in results:
        results[best_energy] = []
    results[best_energy].append(file_name)
    result_file.close()

# Sort by energies
sorted_energies = sorted(results.keys())
size_elist = len(sorted_energies)

# Print sorted output
output_filename = current_directory + "_sorted_results"
out_file = open(output_filename, 'w')
rank = 1
out_file.write('Rank\tEnergy\tLigand')
for energy in sorted_energies:
    num_ener = len(results[energy])
    for x in range(num_ener):
        out_file.write('\n' + str(rank) + '\t' + str(energy) + '\t' + results[energy][x])
        rank = rank + 1

out_file.close()
