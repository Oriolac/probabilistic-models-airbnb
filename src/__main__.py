import sys

import pandas as pd
import numpy as np
from sklearn.cluster import DBSCAN
import math as mt
import matplotlib.pyplot as plt


def categorize_dataframe_nquartiles(dataframe, column, number_quantiles):
    dataframe[column] = pd.qcut(dataframe[column],
                                number_quantiles, labels=False)

def parse_weka(df, relation_name):
    '''
        Parses a pandas.DataFrame to weka format, independently
        from the weka format. All attributes must be categorized
        before this function.
        It's a pure function.

        :param df: pandas.DataFrame -> DataFrame to be parsed.
        :param relation_name: str -> relation name used in weka.
        Its the first line containing:
         `@RELATION {relation_name}`

        :return string with weka format-like. With this it's
        straight-forward to save it in a file.
    '''
    res = f"@RELATION {relation_name}\n\n"

    res += '\n'.join(f'@ATTRIBUTE {col} ' + '{' +
            ','.join(map(str, df[col].unique()))
            + '}' for col in df.columns)

    res += '\n\n@DATA\n'
    res += '\n'.join(','.join(map(str, row)) for row in df.values)
    return res


def main(infile, outfile):
    df = pd.read_csv(infile, header=0)
    categorize_dataframe_nquartiles(df, 'price', 4)
    categorize_dataframe_nquartiles(df, 'reviews', 4)
    categorize_dataframe_nquartiles(df, 'latitude', 4)
    categorize_dataframe_nquartiles(df, 'longitude', 4)

    res = parse_weka(df, "airbnb")
    with open(outfile, 'w') as out:
        print(res, file=out)



if __name__ == '__main__':
    if len(sys.argv) != 3:
        print("USAGE: python -m src.graph <input-filename> <output-filename")
        sys.exit()
    main(sys.argv[1], sys.argv[2])
    print('exiting')
    sys.exit()


