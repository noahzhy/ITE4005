import os
import argparse
import numpy as np
import pandas as pd


parser = argparse.ArgumentParser()
parser.add_argument("input", dest="input data file name", type=str)
parser.add_argument("n", dest="number of clusters for the corresponding input data", type=int)
parser.add_argument("eps", dest="maximum radius of the neighborhood", type=int)
parser.add_argument("minPts", dest="minimum number of points in an Eps-neighborhood of a given point", type=int)
# parser.add_argument("--output", dest="output", help="output file", type=str)
# parser.add_argument("--image", dest="image", help="cluster image", action='store_true')

args = parser.parse_args()

class DBSCAN:
    def __init__(self):
        super().__init__()


if __name__ == "__main__":
    pass