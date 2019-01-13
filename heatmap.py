#code to plot the csv to hestmap

import numpy as np
import matplotlib.pyplot as plt
import time


def get_xyz_from_csv_file_np(csv_file_path):
    '''
    get a grid of values from a csv file
    csv file format: x0,y0,z0
    '''

    # Load the csv file into a single 2D array, 
    # then split the columns into individual variables.
    x, y, z = np.loadtxt(csv_file_path, delimiter=',', dtype=np.int).T

    # Create an empty 2D array of pixels and 
    # put all the values into the correct place
    plt_z = np.zeros((y.max()+1, x.max()+1))
    plt_z[y, x] = z

    return plt_z


def draw_heatmap(plt_z):
    # Generate y and x values from the dimension lengths
    plt_y = np.arange(plt_z.shape[0])
    plt_x = np.arange(plt_z.shape[1])

    # everything is the same from here on
    z_min = plt_z.min()
    z_max = plt_z.max() 

    plot_name = "heatmap"

    color_map = plt.cm.Reds #plt.cm.rainbow #plt.cm.hot #plt.cm.gist_heat
    fig, ax = plt.subplots()
    cax = ax.pcolor(plt_x, plt_y, plt_z, cmap=color_map, vmin=z_min, vmax=z_max,edgecolors='k', linewidths=2)
    ax.set_xlim(plt_x.min(), plt_x.max())
    ax.set_ylim(plt_y.min(), plt_y.max())
    fig.colorbar(cax).set_label(plot_name,rotation=270) 
    ax.set_title(plot_name)  
    ax.set_aspect('equal')
#    plt.ion()
#    plt.show()
#    time.sleep(10)
#    plt.close('all')

#    return figure
    manager = plt.get_current_fig_manager()
    manager.resize(*manager.window.maxsize())
    figure = plt.gcf()
    plt.show()
    figure.savefig("outputFile.png")
    return figure   

def main():
    fname = 'heatmap.csv'
    print('map done')
#    create_test_csv(fname)	
    res = get_xyz_from_csv_file_np(fname)
    draw_heatmap(res)


if __name__ == "__main__":
    main()
