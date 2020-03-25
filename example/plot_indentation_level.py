from sys import argv
import json
import math
import matplotlib.pyplot as plt
from matplotlib.image import NonUniformImage
import matplotlib.colors as colors

import numpy as np
'''
Plot a heatmap of start index, end index location.
x is start/end idx's, y is the lineno, and frequency is 
the heat
'''
with open(argv[1]) as json_file:
    data = json.load(json_file)


    # Set up data
    # print(data['avg_file_length'])
    data = data['line_freqs'][:math.ceil(data['avg_file_length'])]
    x = []
    y = []
    heat = []
    for line_num, line_obj in enumerate(data):
        for idx, freq in line_obj['start_indexes'].items():
            y.append(line_num)
            x.append(int(idx))
            heat.append(freq)

    # Get the max x to convert to an array
    max_x = max(x)
    print(max_x)
    frequencies = np.zeros((len(data), max_x+1), dtype=int)
    for line_num, line_obj in enumerate(data):
        for idx, freq in line_obj['start_indexes'].items():
            frequencies[line_num][int(idx)] = freq

    # frequencies = frequencies[:, :40]
    # Get rid of the odd layers
    # frequencies = np.delete(frequencies, np.s_[1::2], 1)
    print(frequencies)

    ax = plt.gca()

    im = plt.imshow(frequencies, aspect='equal', cmap='inferno',
        norm=colors.LogNorm(vmin=1, vmax=np.amax(frequencies)))
    
    
    cbar = ax.figure.colorbar(im, ax=ax, orientation="horizontal")

    plt.xticks(np.arange(0, frequencies.shape[1], step=2))
    plt.yticks(np.arange(0, frequencies.shape[1], step=10))
    ax.set_title('Clang: Heatmap of indentation levels')
    ax.set_xlabel('Indentation level')
    ax.set_ylabel('Line number')
    plt.grid()
    plt.show()

