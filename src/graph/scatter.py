import pandas as pd
import matplotlib.pyplot as plt
import numpy as np

def get_lat_longs():
    pass

def main(file):
    df = pd.read_csv(file, names=["type", "nb", "reviews", "sat", "acc", "bed", "price", "lat", "long"])
    fig, ax = plt.subplots()
    ax.scatter(df["lat"], df["long"])
    ax.set_xlabel('Latitude')
    ax.set_ylabel('Longitude')
    ax.set_title(f'Representation in a cartesian world')
    plt.savefig(f'cartesian.png')
