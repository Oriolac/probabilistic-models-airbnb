import pandas as pd
import matplotlib.pyplot as plt
import numpy as np

def get_lat_longs():
    pass

def main(filen):
    df = pd.read_csv(filen, header=0)
    fig, ax = plt.subplots()
    ax.scatter(df["latitude"], df["longitude"], c=df["overall_satisfaction"])
    ax.set_xlabel('Latitude')
    ax.set_ylabel('Longitude')
    ax.set_title(f'Representation in a cartesian world')
    plt.savefig(f'cartesian.png')
