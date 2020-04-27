import os
import math
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
        label_counts = count(df)
        e = .0
        for label in label_counts:
            p = float(label_counts[label]) / len(df)
            e -= p * math.log(p, 2)
        return e
    
    current_score = entropy(df)
    best_gain = .0
    _att = None
    _splits = None

    for attr in range(0, len(df[0])-1):
        att_values = dict()

        for row in df:
            att_values[row[attr]] = 1

        for value in att_values.keys():
            left = [row for row in df if row[attr] == value]
            right = [row for row in df if not row[attr] == value]

            p = len(left) / float(len(df))
            gain = current_score - p*entropy(left) - (1-p)*entropy(right)

            if gain > best_gain:
                best_gain = gain
                _att = (attr, value)
                _splits = (left, right)

    if best_gain > 0:
        return Node(attr=_att[0], att_value=_att[1], left=recursive_tree(_splits[0]), right=recursive_tree(_splits[1]))
    else:
        return Node(results=count(df))


def count(tups):
    res = {}
    for i in tups:
        label = i[len(i)-1]
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

    [data[i].append(list(classify(data[i], tree).keys())[0]) for i in range(len(data))]
    return data


if __name__ == "__main__":
    train, test = load_data()
    result = Classifier(test, recursive_tree(train))
    header = pd.DataFrame(pd.read_csv(args.train, sep='\t')).columns.values
    pd.DataFrame(result).to_csv(args.output, header=header, sep='\t')

    os.system('dt_test.exe dt_answer1.txt {}'.format(args.output))