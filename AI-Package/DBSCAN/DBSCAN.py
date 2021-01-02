# -*- coding: utf-8 -*-

import numpy
import math
from sklearn.datasets._samples_generator import make_blobs
from sklearn.cluster import DBSCAN
from sklearn.preprocessing import StandardScaler


#for making density data 
centers = [[1, 1], [-1, -1], [1, -1]]
X, labels_true = make_blobs(n_samples=750, centers=centers, cluster_std=0.4,
                            random_state=0)

X = StandardScaler().fit_transform(X)
#------------------------------------------------------------------
visited_points = set()
NOISE = -1
def MyDBSCAN(D, eps, MinPts):
    """
    Cluster the dataset `D` using the DBSCAN algorithm.
    
    MyDBSCAN takes a dataset `D` (a list of vectors), a threshold distance
    `eps`, and a required number of points `MinPts`.
    
    It will return a list of cluster labels. The label -1 means noise, and then
    the clusters are numbered starting from 1.
    """
    # This list will hold the final cluster assignment for each point in D.
    # There are two reserved values:
    #    -1 - Indicates a noise point
    #     0 - Means the point hasn't been considered yet.
    # Initially all labels are 0.
    cluster_num = 0
    label = [0]*len(D)      # list of zeros (final labels)
    for i in range(0 , len(D)):
        point = (D[i][0], D[i][1])
        if i in visited_points:
            continue
        visited_points.add(i)
        sphere_points = regionQuery(D,point,eps)
        if len(sphere_points) < MinPts:      # Noise
            label[i] = NOISE
        else:                               # a cluster is found
            cluster_num += 1
            growCluster(D, label, i, sphere_points, cluster_num, eps, MinPts)
    return label


def growCluster(D, labels, P, NeighborPts, C, eps, MinPts):
    """
    Grow a new cluster with label `C` from the seed point `P`.

    This function searches through the dataset to find all points that belong
    to this new cluster. When this function returns, cluster `C` is complete.

    Parameters:
      `D`      - The dataset (a list of vectors)
      `labels` - List storing the cluster labels for all dataset points
      `P`      - Index of the seed point for this new cluster
      `NeighborPts` - All of the neighbors of `P`
      `C`      - The label for this new cluster.
      `eps`    - Threshold distance
      `MinPts` - Minimum required number of neighbors
    """
    labels[P] = C
    for point in NeighborPts:
        if point in visited_points:
            continue
        visited_points.add(point)
        sphere_points = regionQuery(D, (D[point][0],D[point][1]), eps)
        if len(sphere_points) >= MinPts:
            for x in sphere_points:
                if x not in NeighborPts and x not in visited_points:    # join all the unvisited point to the neighbours
                    NeighborPts.append(x)
            #growCluster(D ,labels,point,sphere_points,C,eps,MinPts)
        labels[point] = C           # assign the current item the current cluster number




def regionQuery(D, P, eps):
    """
    Find all points in dataset `D` within distance `eps` of point `P`.

    This function calculates the distance between a point P and every other
    point in the dataset, and then returns only those points which are within a
    threshold distance `eps`.
    """
    sphere_points = []
    for i in range(0, len(D)):
        point = (D[i][0] , D[i][1])
        if IsNeighbour(P,point,eps):
            sphere_points.append(i)
    return sphere_points            # return index of neighbours

def CalculateEuclideanDistance(P1 , P2):
    return math.sqrt( ((P1[0]-P2[0])*(P1[0]-P2[0])) + ((P1[1]-P2[1])*(P1[1]-P2[1])))

def IsNeighbour(P1, P2, eps):
    return CalculateEuclideanDistance(P1, P2) <= eps



my_labels = MyDBSCAN(X, eps=0.3, MinPts=10)
#print(my_labels)

print("==========================================")
# built in DBSCAN Function
db = DBSCAN(eps=0.3, min_samples=10).fit(X)
skl_labels = db.labels_


# Scikit learn uses -1 to for NOISE, and starts cluster labeling at 0. I start
# numbering at 1, so increment the skl cluster numbers by 1.
for i in range(0, len(skl_labels)):
    if not skl_labels[i] == -1:
        skl_labels[i] += 1
#print(skl_labels)

num_disagree = 0
#---------------------------------
#compare built in and custom made dbscan function
# Go through each label and make sure they match (print the labels if they 
# don't)
for i in range(0, len(skl_labels)):
    if not skl_labels[i] == my_labels[i]:
        print ('Scikit learn:', skl_labels[i], 'mine:', my_labels[i])
        num_disagree += 1

if num_disagree == 0:
    print ('PASS - All labels match!')
else:
    print ('FAIL -', num_disagree, 'labels don\'t match.')
