import sys

import src.kmeans as km
import pandas as pd
import numpy as np
from sklearn.cluster import DBSCAN
import math as mt
import matplotlib.pyplot as plt


def plot(db,df):
    labels = db.labels_
    unique_labels = set(labels)
    core_samples_mask = np.zeros_like(db.labels_, dtype=bool)
    core_samples_mask[db.core_sample_indices_] = True
    colors = [plt.cm.Spectral(each)
              for each in np.linspace(0, 1, len(unique_labels))]
    for k, col in zip(unique_labels, colors):
        if k == -1:
            # Black used for noise.
            col = [0, 0, 0, 1]

        class_member_mask = (labels == k)

        xy = df[class_member_mask & core_samples_mask]
        plt.plot(xy['latitude'], xy['longitude'], 'o', markerfacecolor=tuple(col),
                 markeredgecolor='k', markersize=14)

        xy = df[class_member_mask & ~core_samples_mask]
        plt.plot(xy['latitude'], xy['longitude'], 'o', markerfacecolor=tuple(col),
                 markeredgecolor='k', markersize=6)

    plt.savefig('scatter.png')



def main(file):
    df = pd.read_csv(file, header=0,
                     dtype={"latitude": np.float, "longitude": np.float})
    coords = df[['latitude', 'longitude']]
    db = DBSCAN(eps=0.18/6371., min_samples=5, algorithm='ball_tree', metric='haversine').fit(np.radians(coords))
    cluster_labels = db.labels_
    plot(db,coords)
    num_clusters = len(set(cluster_labels))
    clusters = pd.Series([coords[cluster_labels == n] for n in range(num_clusters)])
    print('Number of clusters: {}'.format(num_clusters))
    print(clusters)


if __name__ == '__main__':
    if len(sys.argv) != 2:
        print("USAGE: python -m src.graph <file-name>")
        sys.exit()
    with open(sys.argv[1]) as file:
        main(file)
    print('exiting')
    sys.exit()
