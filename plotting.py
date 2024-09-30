# plotting.py
import matplotlib.pyplot as plt
import numpy as np
import os

def create_scatter_plot(data_x, data_y, assignments, centers=None, plot_path='static/plot.png'):
    plt.figure(figsize=(8, 6))
    plt.title("K-Means Clustering Data", fontsize=16, pad=20)
    plt.gcf().patch.set_facecolor("white")

    # Create a color map for the clusters
    unique_assignments = np.unique(assignments)
    colors = plt.cm.get_cmap('tab10', len(unique_assignments))

    # Scatter plot with colors based on cluster assignment
    for i, cluster in enumerate(unique_assignments):
        plt.scatter(data_x[assignments == cluster], data_y[assignments == cluster],
                    color=colors(i), alpha=0.6, edgecolor='k', s=80, marker='o', label=f'Cluster {cluster}')

    if centers is not None:
        plt.scatter(centers[:, 0], centers[:, 1], c='red', marker='x', s=100, label='Centers')

    plt.xlim(-10, 10)
    plt.ylim(-10, 10)
    plt.xticks([-10, -5, 0, 5, 10])
    plt.yticks([-10, -5, 0, 5, 10])

    for y in range(-10, 11, 5):
        if y == 0:
            plt.axhline(y=y, color='black', linewidth=0.8, linestyle='-')
        elif y != 10 and y != -10:
            plt.axhline(y=y, color='lightgrey', linewidth=0.6, linestyle='-')

    for x in range(-10, 11, 5):
        if x == 0:
            plt.axvline(x=x, color='black', linewidth=0.8, linestyle='-')
        elif x != 10 and x != -10:
            plt.axvline(x=x, color='lightgrey', linewidth=0.6, linestyle='-')

    ax = plt.gca()
    ax.spines['top'].set_visible(False)
    ax.spines['right'].set_visible(False)
    ax.spines['left'].set_visible(False)
    ax.spines['bottom'].set_visible(False)

    plt.legend()
    plt.savefig(plot_path)
    plt.close()
