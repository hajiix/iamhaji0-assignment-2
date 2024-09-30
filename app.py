from flask import Flask
from markupsafe import escape
from flask import render_template, request
import numpy as np
import random
import matplotlib
import matplotlib.pyplot as plt
from kmeans import KMeans
from plotting import create_scatter_plot


import os

app = Flask(__name__)
matplotlib.use('Agg')

def get_random():
    return random.uniform(-10, 10)

@app.route("/run-convergence", methods=["POST"])
def run_convergence(data, initialize_method="random", k=4):
    if k == 0:
        k = 1
    kmeans = KMeans(data, k)
    kmeans.lloyds(initialize_method)
    kmeans.initialize_farthest_first()
    images = kmeans.snaps
    images[0].save(
        'kmeans.gif',
        optimize=False,
        save_all=True,
        append_images=images[1:],
        loop=0,
        duration=500
    )
    convergence_path = os.path.join('static', 'temp0.png')

    return {"convergence_url": convergence_path}

        
@app.route("/generate-dataset", methods=["POST"])
def generate_dataset():
    data = []
    for _ in range(300):
        x = (get_random())
        y = (get_random())
        data.append([x, y])
    return (data)

@app.route('/', methods=['GET', 'POST'])
def index():
    # Create a scatter plot
    dataset = np.array(generate_dataset())
    data_x = [x for x, _ in dataset]
    data_y = [y for _, y in dataset]

    if request.method == 'POST':
        k_clusters = request.form.get("k_clusters")
        print(k_clusters)
        initialization_method = request.form.get("initialization_method")
        print(initialization_method)
        if k_clusters:
            run_convergence(np.array(dataset), initialization_method, int(k_clusters))
        print(initialization_method)

    plt.figure(figsize=(8, 6))  # Set the figure size
    plt.title("K-Means Clustering Data", fontsize=16, pad=20)
    plt.gcf().patch.set_facecolor("white")  # Set figure background color

    # Use a color palette for the scatter points
    plt.scatter(data_x, data_y, c='blue', alpha=0.6, edgecolor='k', s=80, marker='o')

    # Set limits for x and y axes
    plt.xlim(-10, 10)
    plt.ylim(-10, 10)

    # Set specific ticks for x and y axes
    plt.xticks([-10, -5, 0, 5, 10])
    plt.yticks([-10, -5, 0, 5, 10])

    # Add gridlines with lighter opacity

    # Add horizontal and vertical lines at specified y-values and x-values
    for y in range(-10, 11, 5):  # From -10 to 10, step by 5
        if (y == 0):
            plt.axhline(y=y, color='black', linewidth=0.8, linestyle='-')
        elif (y != 10 and y != -10):
            plt.axhline(y=y, color='lightgrey', linewidth=0.6, linestyle='-')

    for x in range(-10, 11, 5):  # From -10 to 10, step by 5
        if(x == 0):
            plt.axvline(x=x, color='black', linewidth=0.8, linestyle='-')
        elif (x != 10 and x != -10):
            plt.axvline(x=x, color='lightgrey', linewidth=0.6, linestyle='-')

    # Customize the axes
    ax = plt.gca()
    ax.spines['top'].set_visible(False)
    ax.spines['right'].set_visible(False)
    ax.spines['left'].set_visible(False)
    ax.spines['bottom'].set_visible(False)

    # Save the plot
    plot_path = os.path.join('static', 'plot.png')  # Save in the static folder
    plt.savefig(plot_path)  # Use tight layout and high DPI
    plt.close()  # Close the figure to free memory

    converged = False
    
    convergence_path = os.path.join('static', 'temp.png')
    
    return render_template('index.html', plot_url=plot_path, convergence_url=convergence_path)


@app.route('/plot', methods=["POST"])
def plot():
    # Get the data from the request
    data = request.get_json()
    data_x = [x for x, _ in data]
    data_y = [y for _, y in data]
    

    # Create a scatter plot
    plt.figure(figsize=(8, 6))  # Set the figure size
    plt.title("K-Means Clustering Data", fontsize=16, pad=20)
    plt.gcf().patch.set_facecolor("white")  # Set figure background color

    # Use a color palette for the scatter points
    plt.scatter(data_x, data_y, c='blue', alpha=0.6, edgecolor='k', s=80, marker='o')

    # Set limits for x and y axes
    plt.xlim(-10, 10)
    plt.ylim(-10, 10)

    # Set specific ticks for x and y axes
    plt.xticks([-10, -5, 0, 5, 10])
    plt.yticks([-10, -5, 0, 5, 10])

    # Add gridlines with lighter opacity
    # Add horizontal and vertical lines at specified y-values and x-values
    for y in range(-10, 11, 5):  # From -10 to 10, step by 5
        if (y == 0):
            plt.axhline(y=y, color='black', linewidth=0.8, linestyle='-')
        elif (y != 10 and y != -10):
            plt.axhline(y=y, color='lightgrey', linewidth=0.6, linestyle='-')

    for x in range(-10, 11, 5):  # From -10 to 10, step by 5
        if (x == 0):
            plt.axvline(x=x, color='black', linewidth=0.8, linestyle='-')
        elif (x != 10 and x != -10):
            plt.axvline(x=x, color='lightgrey', linewidth=0.6, linestyle='-')

    # Customize the axes
    ax = plt.gca()
    ax.spines['top'].set_visible(False)
    ax.spines['right'].set_visible(False)
    ax.spines['left'].set_visible(False)
    ax.spines['bottom'].set_visible(False)

    # Save the plot
    plot_path = os.path.join('static', 'plot.png')  # Save in the static folder
    plt.savefig(plot_path)  # Use tight layout and high DPI
    plt.close()  # Close the figure to free memory

    convergence_path = os.path.join('static', 'temp.png')

    return {"plot_url": plot_path, "convergence_url":convergence_path}