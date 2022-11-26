import numpy as np
import json 
from urllib.request import Request, urlopen 
import random
import pandas as pd

def get_map_data(url_link):
    req = Request(
        url = url_link,
        headers = {'User-Agent': 'Mozilla/5.0'}
    )
    webpage = urlopen(req).read()
    data = json.loads(webpage)
    return data['Map']

class HomeLocations:
    def __init__(self, nloc, map_grid, xbound=200, ybound=112):
        #Initializing Input Variables
        self.xbound = xbound
        self.ybound = ybound
        self.nloc = nloc
        self.map_grid = map_grid
        self.food_points = self.get_food_points()
        self.free_points = self.get_free_points()
        self.cpoints = self.initialize_points()
        
    
    def get_food_points(self):
        #Function to return list of food points
        food_points = []
        for i in range(self.xbound):
            for j in range(self.ybound):
                if self.map_grid[i][j] == "f":
                    food_points.append([i, j])
        return food_points

    def get_free_points(self):
        #Function to return list of free points present 
        points_list = []
        for i in range(self.xbound):
            for j in range(self.ybound):
                if self.map_grid[i][j] == " ":
                    points_list.append([i, j])
        
        return points_list

    def initialize_points(self):
        #Intializes the list of clusters centers to start with
        cluster_points = []
        random_points = random.sample(range(len(self.free_points)), self.nloc)
        for i in range(self.nloc):
            cluster_points.append(self.free_points[random_points[i]])
        return cluster_points

    def get_cluster_centers(self, points):
        #Returns the free point which is closer the mean cluster center
        cluster_points = []
        for point in points:
            dist = np.linalg.norm(point - self.free_points, axis = 1)
            min_point = np.argmin(dist)
            cluster_points.append(self.free_points[min_point])
        
        return cluster_points

    def intMAP(self, map_grid):
        
        #Intializes the map grind - Assigns value to each point - Distance parameter
        mapxy = np.zeros((self.xbound, self.ybound))
        for x in range(self.xbound):
            for y in range(self.ybound):
                if map_grid[x][y] == " ":
                    mapxy[x][y] = 1
                elif map_grid[x][y] == "w":
                    mapxy[x][y] = 999999999
                elif map_grid[x][y] == "f":
                    mapxy[x][y] = 2
                elif map_grid[x][y] == "d":
                    mapxy[x][y] = 2
        return mapxy


    def cluster_bot(self, iterations = 10):
        #Optimization Algorithm
        cluster_points = self.initialize_points()
        for k in range(iterations):
            points_to_cluster = []
            for point in self.food_points:
                dist = []
                for cluster_point in cluster_points:
                    trail_dist = self.get_trail_distance(cluster_point, point)
                    dist.append(trail_dist)
                dist = np.array(dist)
                min_cluster = np.argmin(dist)
                points_to_cluster.append([point[0], point[1],min_cluster])
            
            cluster_df = pd.DataFrame(points_to_cluster, columns=['x', 'y','center'])
            center_points = []
            for i in range(self.nloc):
                seg_df = cluster_df[cluster_df['center'] == i]
                x_mean = seg_df['x'].mean()
                y_mean = seg_df['y'].mean()
                center_points.append([x_mean, y_mean])

            cluster_points = self.get_cluster_centers(center_points)
            print(cluster_points)

        return cluster_points




"""
map_url = "https://antgame.io/assets/dailyMaps/Apr_30_2022_305163.json"
map_grid_data = get_map_data(map_url)

print(map_grid_data[0])

newbot = HomeLocations(5, map_grid_data)
print(newbot.xbound)
"""
