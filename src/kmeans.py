"""
    Module to make clusters. Can be executed with
    python3 clusters.py
"""

import random
import functools
import collections
from math import sin, cos, sqrt, atan2, radians

Point = collections.namedtuple("Point", ["lat", "lon"])

def spheric_distance(point1, point2):
    # approximate radius of earth in km
    R = 6373.0
    lat1 = radians(point1.lat)
    lon1 = radians(point1.lon)
    lat2 = radians(point2.lat)
    lon2 = radians(point2.lon)
    dlon = lon2 - lon1
    dlat = lat2 - lat1
    a = sin(dlat / 2)**2 + cos(lat1) * cos(lat2) * sin(dlon / 2)**2
    c = 2 * atan2(sqrt(a), sqrt(1 - a))
    return R * c


def kmeans(rows, distance=spheric_distance, k=4):
    """
        Builds kmeans. Extracted from slides.
    """
    ranges = [(min([row[i] for row in rows]),
               max([row[i] for row in rows])) for i in range(len(rows[0]))]
    clusters = [[random.random() * (ranges[i][1] - ranges[i][0]) + ranges[i][0]
                 for i in range(len(rows[0]))] for j in range(k)]
    lastmatches = None
    for _ in range(100):
        bestmatches = [[] for i in range(k)]
        for j, row in enumerate(rows):
            bestmatch = 0
            for i in range(k):
                d = distance(clusters[i], row)
                if d < distance(clusters[bestmatch], row):
                    bestmatch = i
            bestmatches[bestmatch].append(j)

        if bestmatches == lastmatches:
            return bestmatches, clusters
        lastmatches = bestmatches

        for i in range(k):
            avgs = [0.0] * len(rows[0])
            for rowid in bestmatches[i]:
                for m in range(len(rows[rowid])):
                    avgs[m] += rows[rowid][m]
            for j, item in enumerate(avgs):
                item /= len(bestmatches[i])
            clusters[i] = avgs
    return bestmatches, clusters

def kclusters(rows, distance=spheric_distance, kcentroid=4, ntimes=10):
    """
        Calculates k-means given a dataset. Distance, number of clusters,
        and restarting policies can be changed.
    """
    assert ntimes > 0, "At least ntimes must be 1!!"
    sum_distances = lambda x: sum(map(lambda y: distance(rows[y], x[1]), x[0]))
    scoref = lambda res: sum(map(sum_distances, zip(*res)))
    bresult = kmeans(rows, distance, kcentroid)
    bscore = scoref(bresult)
    for _ in range(1, ntimes):
        res = kmeans(rows, distance, kcentroid)
        score = scoref(res)
        if score < bscore:
            bresult = res
    return bresult[0]


