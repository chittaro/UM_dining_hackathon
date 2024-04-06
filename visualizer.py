import matplotlib as mpl
import matplotlib.patches as patches
from matplotlib import pyplot as plt
import numpy as np
import pandas as pd

# Define constants
CATEGORIES = 6
LABELS = ["Cals", "Trans Fat", "Sat. Fat", "Sodium", "Protein", "Fiber"]

ANGLES = np.linspace(0, 2 * np.pi, CATEGORIES, endpoint = False)
WIDTH = 2 * np.pi / CATEGORIES
OFFSET = np.pi / 2

# Calories/gram for macros
CALS_FAT = 9
CALS_CRB = 4
CALS_PRO = 4

# Define colormap
NORM = mpl.colors.Normalize(1, 100)
CMAP = mpl.colors.LinearSegmentedColormap.from_list("gr", ["r", "w", "g"], N = 100)

def make_graph(vals: dict[str, float]):
    '''Create a graph for a given food'''

    # Create circular plot with given offset
    fig, ax = plt.subplots(figsize = (7.5, 7.5), subplot_kw = {"projection": "polar"})
    ax.set_theta_offset(OFFSET)

    # Set radial limit -- negative creates whole in middle
    ax.set_ylim(-.5, 1.5)

    # Turn off grid and ticks
    ax.set_frame_on(False)
    ax.xaxis.grid(False)
    ax.yaxis.grid(False)
    ax.set_xticks([])
    ax.set_yticks([])

    val_list = list(vals.values())[:-1]

    labs = [f"Cals: {round(val_list[0], 3)}", 
            f"Trans Fat Score: {round(val_list[1], 3)}", 
            f"Sat. Fat Score : {round(val_list[2], 3)}", 
            f"Sodium Score: {round(val_list[3], 3)}",
            f"Protein Score: {round(val_list[4], 3)}", 
            f"Fiber Score: {round(val_list[5], 3)}"]
    
    # Set cals to 1
    val_list[0] = 1

    # Set sodium to 0 if it's negative
    if (val_list[3] < 0): 
        val_list[3] = 0

    # Define colors for each bar
    colors = [CMAP(NORM(int(v * 110))) for v in val_list]

    # Add bars
    ax.bar(ANGLES, val_list, width = WIDTH, linewidth = 5, color = colors, edgecolor = "white", alpha = .8)

    # Add labels
    add_labels(ANGLES, val_list, labs, OFFSET, ax)

    # Add score
    circ = patches.Circle((0, 0), radius = .5, fc = CMAP(NORM(int(vals["Total"] * 20))), alpha = .8, transform = ax.transData._b)
    ax.add_patch(circ)

    ax.text(x = 0, y = -.5, s = round(vals["Total"], 3), ha = "center", va = "center", fontsize = "x-large", weight = "bold")
    plt.savefig('fig.png')


def get_label_rotation(angle, offset):
    '''Returns rotation and alignment in degrees'''

    rotation = np.rad2deg(angle + offset)

    if angle <= np.pi:
        alignment = "right"
        rotation = rotation + 180
    else:
        alignment = "left"

    return rotation, alignment

def add_labels(angles, values, labels, offset, ax):
    '''Adds labels to the given axis'''

    # Define padding between bar and label
    padding = .1

    for ang, val, lab in zip(angles, values, labels):
        # Get rotation and alignment
        rotation, alignment = get_label_rotation(ang, offset)

        # Plot column labels 
        ax.text(x = ang, y = val + padding, s = lab, ha = alignment, va = "center", rotation = rotation, rotation_mode = "anchor")

test = {'Calories': 108, 'Trans Fat': 1, 'Sat. Fat': 0.9166666666666666, 'Sodium': 0.40740740740740744, 'Protein': 0.6296296296296297, 'Fiber': 1, 'Total': 3.9537037037037037}
make_graph(test)