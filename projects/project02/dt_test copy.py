import sys
from math import log
import os
import argparse
import pandas as pd
import numpy as np


parser = argparse.ArgumentParser()
parser.add_argument("--train", help="train data file",  default='dt_train1.txt', type=str)
parser.add_argument("--test", help="test data file", default='dt_test1.txt', type=str)
parser.add_argument("--output", help="output path", default='dt_result1.txt', type=str)
args = parser.parse_args()

def load_data(train=args.train, test=args.test):
    train = pd.DataFrame(pd.read_csv(train, sep='\t'))
    test = pd.DataFrame(pd.read_csv(test, sep='\t'))
    return np.array(train).tolist(), np.array(test).tolist()


class Node:
    def __init__(self, attr=-1, att_value=None, results=None, left=None, right=None):
        self.attr = attr
        self.att_value = att_value
        self.results = results
        self.left = left
        self.right = right


def recursive_tree(df):
    def entropy(df):
        results = count(df)
        ent = .0
        for label in results:
            p = float(results[label]) / len(df)
            ent = ent - p * log(p) / log(2)
        return ent
    
    current_score = entropy(df)
    top_value = .0
    top_att = None
    top_splits = None
    column_count = len(df[0]) - 1

    for attr in range(0, column_count):
        column_att_values = {}

        for row in df:
            column_att_values[row[attr]] = 1

        for att_value in column_att_values.keys():
            left = [row for row in df if row[attr] == att_value]
            right = [row for row in df if not row[attr] == att_value]

            p = float(len(left)) / len(df)
            gain = current_score - p*entropy(left) - (1-p)*entropy(right)

            if gain > top_value and len(left) > 0 and len(right) > 0:
                top_value = gain
                top_att = (attr, att_value)
                top_splits = (left, right)

    if top_value > 0:
        Leftbranch = recursive_tree(top_splits[0])
        Rightbranch = recursive_tree(top_splits[1])
        return Node(attr=top_att[0], att_value=top_att[1], left=Leftbranch, right=Rightbranch)
    else:
        return Node(results=count(df))


def count(tups):
    res = {}
    for t in tups:
        label = t[len(t)-1]
        if label not in res:
            res[label] = 0
        res[label] += 1
    return res


def Classifier(data, tree):
    def classify(row, tree):
        if tree.results:
            return tree.results
        else:
            branch = tree.left if row[tree.attr] == tree.att_value else tree.right
            return classify(row, branch)

    for i in range(len(data)):
        data[i].append(list(classify(data[i], tree).keys())[0])

    return data


def save_result(data, header=""):
    f = open(args.output, 'w')
    f.write("\t".join(header))
    [f.write("\n{}".format("\t".join(data[i]))) for i in range(len(data))]
    return f.close()


if __name__ == "__main__":
    train, test = load_data()
    result = Classifier(test, recursive_tree(train))
    header = pd.DataFrame(pd.read_csv(args.train, sep='\t')).columns.values
    Result = save_result(result, header)

    os.system('dt_test.exe dt_answer1.txt dt_result1.txt')