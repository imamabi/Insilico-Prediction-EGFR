import matplotlib.pyplot as plt
import numpy as np
import os

def plot_rmsf(file_paths, labels, colors, vertical_lines, v_line, v1, v2, output_file, xlim=None, ylim=None):
    """
    Plots RMSF data from multiple files and saves the plot as an image.

    Parameters:
    - file_paths: List of paths to the RMSF data files.
    - labels: List of labels for each dataset.
    - colors: List of colors for each dataset.
    - vertical_lines: List of x-values for vertical dashed lines.
    - v_line: List of x-values for green vertical dashed lines.
    - v1: x-value for the blue vertical dashed line.
    - v2: x-value for the red vertical dashed line.
    - output_file: Path to save the output plot image.
    - xlim: Tuple (xmin, xmax) for x-axis limits.
    - ylim: Tuple (ymin, ymax) for y-axis limits.
    """
    # Create a figure and axis objects for the plot
    fig = plt.figure(figsize=(10, 6))
    ax = fig.add_subplot(111)

    # Loop through each file and plot the data
    for file_path, label, color in zip(file_paths, labels, colors):
        if os.path.exists(file_path):
            res, rmsf = np.loadtxt(file_path, comments=["@", "#"], unpack=True)
            ax.plot(res, rmsf, color=color, label=label)
        else:
            print(f"File not found: {file_path}")

    # Add vertical lines
    for x in vertical_lines:
        plt.axvline(x=x, color='gray', linestyle='--')

    for x in v_line:
        plt.axvline(x=x, color='green', linestyle='--')

    plt.axvline(v1, color='blue', linestyle='--')
    plt.axvline(v2, color='red', linestyle='--')

    # Set labels and title
    ax.set_xlabel("Residue")
    ax.set_ylabel(r"C$_\alpha$ RMSF (nm)")
    plt.title('RMS Fluctuation')

    # Set axis limits if provided
    if xlim:
        plt.xlim(xlim)
    if ylim:
        plt.ylim(ylim)

    # Add legend
    plt.legend(fontsize=9, loc='upper center', ncol=5)

    # Save the plot
    plt.savefig(output_file, format="png", dpi=600, bbox_inches="tight")

    # Display the plot
    plt.show()


def plot_rmsd(file_paths, labels, colors, output_file, xlim=None, ylim=None):
    """
    Plots RMSD data from multiple files and saves the plot as an image.

    Parameters:
    - file_paths: List of paths to the RMSD data files.
    - labels: List of labels for each dataset.
    - colors: List of colors for each dataset.
    - output_file: Path to save the output plot image.
    - xlim: Tuple (xmin, xmax) for x-axis limits.
    - ylim: Tuple (ymin, ymax) for y-axis limits.
    """
    # Create a figure and axis objects for the plot
    fig = plt.figure(figsize=(10, 6))
    ax = fig.add_subplot(111)

    # Loop through each file and plot the data
    for file_path, label, color in zip(file_paths, labels, colors):
        if os.path.exists(file_path):
            x, y = np.loadtxt(file_path, comments=["@", "#"], unpack=True)
            ax.plot(x, y, color=color, label=label)
        else:
            print(f"File not found: {file_path}")

    # Set labels and title
    ax.set_xlabel("Time (ps)")
    ax.set_ylabel(r"C$_\alpha$ RMSD (nm)")
    plt.title('RMS Deviation')


    # Set axis limits if provided
    if xlim:
        plt.xlim(xlim)
    if ylim:
        plt.ylim(ylim)

    # Add legend
    plt.legend(fontsize=9, loc='upper center', ncol=5)

    # Save the plot
    plt.savefig(output_file, format="png", dpi=600, bbox_inches="tight")

    # Display the plot
    plt.show()


# Example usage
if __name__ == "__main__":
    # Define file paths, labels, and colors
    file_paths = [
        "./data/md/full-wt-ca-rmsf.xvg",
        "./data/md/full-L858R-ca-rmsf.xvg",
        "./data/md/del19-rmsf.xvg",
        "./data/md/T790M-ca-rmsf.xvg"
    ]
    labels = ['wild-type', 'L858R', 'del19', 'T790M']
    colors = ['black', 'purple', 'teal', 'orange']

    # Define vertical lines
    binding_site = [718, 719, 720, 721, 722, 723, 724, 725, 726, 745, 790, 791, 837, 855]
    del19 = [745, 746, 747, 748, 749, 750]
    t_m = 790
    l_r = 858

    # Define output file
    output_file = "rmsfluctuation.png"

    # Call the function
    plot_rmsf(file_paths, labels, colors, binding_site, del19, t_m, l_r, output_file, xlim=(712, 980))

# Define file paths, labels, and colors for RMSD
    rmsd_file_paths = [
        "./data/md/full-wt-ca-rmsd.xvg",
        "./data/md/full-L858R-ca-rmsd.xvg",
        "./data/md/del19-rmsd.xvg",
        "./data/md/T790M-ca-rmsd.xvg"
    ]
    rmsd_labels = ['wild-type', 'L858R', 'del19', 'T790M']
    rmsd_colors = ['black', 'purple', 'teal', 'orange']

    # Define output file for RMSD
    rmsd_output_file = "rmsdeviation.png"

    # Call the RMSD plotting function
    plot_rmsd(rmsd_file_paths, rmsd_labels, rmsd_colors, rmsd_output_file, xlim=None, ylim=None)
