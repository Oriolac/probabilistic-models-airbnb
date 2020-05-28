import sys

import src.kmeans as km
import pandas as pd
import numpy as np
from sklearn.cluster import DBSCAN
import math as mt
import matplotlib.pyplot as plt


def plot(db,df):
    plt.scatter(df['latitude'], df['longitude'], c=db.core_sample_indices_)
    plt.savefig('algo.png')



def main(file):
    df = pd.read_csv(file, header=0,
                     dtype={"latitude": np.float, "longitude": np.float})
    coords = df[['latitude', 'longitude']]
    db = DBSCAN(eps=0.19/6371., algorithm='ball_tree', metric='haversine').fit(np.radians(coords))
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
