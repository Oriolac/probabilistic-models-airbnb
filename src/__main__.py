import sys

import random
import pandas as pd
import numpy as np
import math as mt
import matplotlib.pyplot as plt
import argparse


def categorize_dataframe_nquartiles(dataframe, column, number_quantiles):
    dataframe[column] = pd.qcut(dataframe[column],
                                number_quantiles, labels=False)

def parse_weka(df, relation_name, seed):
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

    def sample_arff(prefix, sample):
        res = prefix + '\n\n@DATA\n'
        res += '\n'.join(','.join(f"'{str(x)}'" for x in row) 
                for row in sample.values)
        return res

    prefix = f"@RELATION {relation_name}\n\n"

    prefix += '\n'.join(f'@ATTRIBUTE {col} ' + '{' +
            ','.join(f"'{str(x)}'" for x in df[col].unique())
            + '}' for col in df.columns)
    train = df.sample(frac=0.75, random_state=seed)
    test = df.drop(train.index)
    return sample_arff(prefix, train), sample_arff(prefix, test)

def parse_arguments():
    parser = argparse.ArgumentParser(description='Parses parameters for '
            'tranforming the csv to an arff file')

    parser.add_argument('inputfile', metavar='input-file', type=str, 
            help='Input file in csv to be used for parsing')
    parser.add_argument('trainfile', metavar='train-file', type=str,
            help='Train file in arff format to be used at weka.'
            'Uses about a 75%% of the rows in the input file')
    parser.add_argument('testfile', metavar='test-file', type=str,
            help='Test file in arff format to be used at weka.'
            'Uses about a 25%% od the rows in the input file, and'
            'testfile union trainfile = inputfile in rows')
    for arg in ['price', 'reviews', 'latitude', 'longitude']:
        parser.add_argument(f'-{arg[:3]}', f'--nquartile-{arg}', dest=f'{arg}q',
            type=int, default=4, help=f'Number of quartiles for {arg}')
    parser.add_argument('-n', '--relation-name', dest='name',
            type=str, default='airbnb', help='Name of the relation in the file')
    parser.add_argument('-s', '--seed', dest='seed', type=int, default=2104011, 
        help='Seed to be used for spliting data')
    return parser.parse_args()


def main():
    args = parse_arguments()
    df = pd.read_csv(args.inputfile, header=0)
    categorize_dataframe_nquartiles(df, 'price', args.priceq)
    categorize_dataframe_nquartiles(df, 'reviews', args.reviewsq)
    categorize_dataframe_nquartiles(df, 'latitude', args.latitudeq)
    categorize_dataframe_nquartiles(df, 'longitude', args.longitudeq)

    train, test = parse_weka(df, args.name, args.seed)
    print(train, file=open(args.trainfile, 'w'))
    print(test, file=open(args.testfile, 'w'))


if __name__ == '__main__':
    main()
    print('exiting')
    sys.exit()


