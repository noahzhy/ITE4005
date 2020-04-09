import argparse
import numpy as np
import pandas as pd

from itertools import chain


parser = argparse.ArgumentParser()
parser.add_argument("--train", help="train data file",  default='dt_train.txt', type=str)
parser.add_argument("--test", help="test data file", default='dt_test.txt', type=str)
parser.add_argument("--output", help="output path", default='dt_output.txt', type=str)
args = parser.parse_args()


def load_data(train=args.train, test=args.test):
    train_data = pd.read_csv(train, sep='\t')
    test_data = pd.read_csv(test, sep='\t')


if __name__ == "__main__":
    load_data()