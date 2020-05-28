import sys

import src.kmeans as km
import pandas as pd


def main(file):
    df = pd.read_csv(file, names=["type", "nb", "reviews", "sat", "acc", "bed", "price", "lat", "lon"])
    rows = [km.Point(x[-2], x[-1]) for x in df]
    print(rows)
    print(km.kclusters(rows, kcentroid=8))


if __name__ == '__main__':
    if len(sys.argv) != 2:
        print("USAGE: python -m src.graph <file-name>")
        sys.exit()
    with open(sys.argv[1]) as file:
        main(file)
    print('exiting')
    sys.exit()
