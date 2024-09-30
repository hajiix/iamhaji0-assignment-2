import numpy as np
from PIL import Image as im
import matplotlib.pyplot as plt
import sklearn.datasets as datasets
import os
from plotting import create_scatter_plot


class KMeans():

    def __init__(self, data, k):
        self.data = data
        self.k = k
        self.assignment = [-1 for _ in range(len(data))]
        self.snaps = []
    
    def snap(self, centers):
        TEMPFILE = "temp.png"
        plot_path = os.path.join('static', TEMPFILE)

        # Use the centralized plotting function
        data_x = self.data[:, 0]
        data_y = self.data[:, 1]
        create_scatter_plot(data_x, data_y, self.assignment, centers, plot_path)

        self.snaps.append(im.fromarray(np.asarray(im.open(plot_path))))

    def isunassigned(self, i):
        return self.assignment[i] == -1

    def initialize(self):
        return self.data[np.random.choice(len(self.data) - 1, size=self.k, replace=False)]

    def initialize_farthest_first(self):
      #This is the first center
      first_center = np.random.choice(len(self.data))
      centers = [self.data[first_center]]
      #Finds the farthest point from any centers
      for _ in range(self.k - 1):
          distances = np.array([min(self.dist(point, center) for center in centers) for point in self.data])
          
          farthest_point_index = np.argmax(distances)
          centers.append(self.data[farthest_point_index])
      return np.array(centers)    
    
    def initialize_kmeans(self):
    # This is the first center
      first_center = np.random.choice(len(self.data))
      centers = [self.data[first_center]]

      # Algorithm for kmeans++ 
      for _ in range(1, self.k):
          # Find the nearest existing center to each point
          distances = np.array([
              min(self.dist(point, center) for center in centers) for point in self.data
          ])

          # Find probabilites and normalize them
          probabilities = distances ** 2
          probabilities /= probabilities.sum()

          next_center = np.random.choice(len(self.data), p=probabilities)
          centers.append(self.data[next_center])

      return np.array(centers)


    def make_clusters(self, centers):
        for i in range(len(self.assignment)):
            for j in range(self.k):
                if self.isunassigned(i):
                    self.assignment[i] = j
                    dist = self.dist(centers[j], self.data[i])
                else:
                    new_dist = self.dist(centers[j], self.data[i])
                    if new_dist < dist:
                        self.assignment[i] = j
                        dist = new_dist
                    
        
    def compute_centers(self):
        centers = []
        for i in range(self.k):
            cluster = []
            for j in range(len(self.assignment)):
                if self.assignment[j] == i:
                    cluster.append(self.data[j])
            centers.append(np.mean(np.array(cluster), axis=0))

        return np.array(centers)
    
    def unassign(self):
        self.assignment = [-1 for _ in range(len(self.data))]

    def are_diff(self, centers, new_centers):
        for i in range(self.k):
            if self.dist(centers[i], new_centers[i]) != 0:
                return True
        return False

    def dist(self, x, y):
        # Euclidean distance
        return sum((x - y)**2) ** (1/2)

    def lloyds(self, initialize_method: str):
        if initialize_method == "random":
            centers = self.initialize()
        elif initialize_method == "farthest_first":
            centers = self.initialize_farthest_first()
        elif initialize_method == "kmeans":
            centers = self.initialize_kmeans()
        else:
            centers = self.initialize_kmeans()
        self.make_clusters(centers)
        new_centers = self.compute_centers()
        self.snap(new_centers)
        while self.are_diff(centers, new_centers):
            self.unassign()
            centers = new_centers
            self.make_clusters(centers)
            new_centers = self.compute_centers()
            self.snap(new_centers)
        return
