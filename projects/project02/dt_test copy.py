import os
from math import log
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
    def __init__(self, attr=None, value=None, leaf=None, left=None, right=None):
        self.attr = attr
        self.value = value
        self.leaf = leaf
        self.left = left
        self.right = right


def recursive_tree(dataset):
    def count(dataset):
        label_counts = dict()
        for feat in dataset:
            label = feat[-1]
            if label not in set(label_counts): label_counts[label] = 0
            label_counts[label] += 1
        return label_counts

    def entropy(dataset):
        e = .0
        label_counts = count(dataset)
        for key in label_counts:
            p = float(label_counts[key]) / len(dataset)
            e -= p * log(p, 2)
        return e
    
    base_e = entropy(dataset)
    best_gain = .0
    axis, value, splited = None, None, None

    for attr in range(0, len(dataset[0])-1):
        for v in set([row[attr] for row in dataset]):
            left = [row for row in dataset if row[attr] == v]
            right = [row for row in dataset if not row[attr] == v]

            p = len(left) / float(len(dataset))
            gain = base_e - p*entropy(left) - (1-p)*entropy(right)

            if gain > best_gain:
                best_gain = gain
                axis = (attr, v)
                splited = (left, right)

    if best_gain > 0:
        return Node(attr=axis[0], value=axis[1], left=recursive_tree(splited[0]), right=recursive_tree(splited[1]))
    else:
        return Node(leaf=count(dataset))


def Classifier(data, tree):
    def classify(row, tree):
        if tree.leaf:
            return tree.leaf
        else:
            branch = tree.left if row[tree.attr] == tree.value else tree.right
            return classify(row, branch)

    [data[i].append(list(classify(data[i], tree).keys())[0]) for i in range(len(data))]
    return data


if __name__ == "__main__":
    train, test = load_data()
    result = Classifier(test, recursive_tree(train))
    header = pd.DataFrame(pd.read_csv(args.train, sep='\t')).columns.values
    pd.DataFrame(result).to_csv(args.output, header=header, index=False, sep='\t')

    os.system('dt_test.exe dt_answer1.txt {}'.format(args.output))