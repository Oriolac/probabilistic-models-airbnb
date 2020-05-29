import sys

import pandas as pd
import numpy as np
from sklearn.cluster import DBSCAN
import math as mt
import matplotlib.pyplot as plt


def categorize_dataframe_nquartiles(dataframe, column, number_quantiles):
    dataframe[column] = pd.qcut(dataframe[column], number_quantiles, labels=False)

def parse_weka(df):
    pass


def main(filename):
    df = pd.read_csv(filename, header=0)
    categorize_dataframe_nquartiles(df, 'price', 4)
    categorize_dataframe_nquartiles(df, 'reviews', 4)
    categorize_dataframe_nquartiles(df, 'latitude', 4)
    categorize_dataframe_nquartiles(df, 'longitude', 4)

    parse_weka(df)



if __name__ == '__main__':
    if len(sys.argv) != 2:
        print("USAGE: python -m src.graph <file-name>")
        sys.exit()
    main(sys.argv[1])
    print('exiting')
    sys.exit()
