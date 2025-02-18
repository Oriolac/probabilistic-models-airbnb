import sys
from typing import List

import pandas as pd
import argparse

from src.weka import categorize, parse_weka


def parse_arguments():
    """
        Parse comand line arguments. To know more about the arguments, use
        python3 -m src --help
    """
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
        parser.add_argument(f'-c{arg[:3]}', f'--categorize-function-{arg}', dest=f'c{arg}',
                            action='store_const', const=pd.qcut, default=pd.cut,
                            help='Changes function to categorize continues'
                                 f'values in column {arg}')
    parser.add_argument('-n', '--relation-name', dest='name',
                        type=str, default='airbnb', help='Name of the relation in the file')
    parser.add_argument('-s', '--seed', dest='seed', type=int, default=0o4011,
                        help='Seed to be used for spliting data')
    return parser.parse_args()


def write_dataset(args, test, train):
    """
    Writes the training set and the test set in two different files.
    :param args:
    :param test:
    :param train:
    :return:
    """
    print(train, file=open(args.trainfile, 'w'))
    print(test, file=open(args.testfile, 'w'))


def main():
    """
    Main function of the program
    :return: None
    """
    args = parse_arguments()
    df = pd.read_csv(args.inputfile, header=0)
    categorize(df, 'price', args.priceq, args.cprice)
    categorize(df, 'reviews', args.reviewsq, args.creviews)
    categorize(df, 'latitude', args.latitudeq, args.clatitude)
    categorize(df, 'longitude', args.longitudeq, args.clongitude)

    train, test = parse_weka(df, args.name, args.seed)
    write_dataset(args, test, train)


if __name__ == '__main__':
    main()
    sys.exit()
