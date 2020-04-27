import argparse
import functools
import collections
import numpy as np
import pandas as pd

from itertools import chain

parser = argparse.ArgumentParser()
parser.add_argument("--train", help="train data file",  default='dt_train1.txt', type=str)
parser.add_argument("--test", help="test data file", default='dt_test1.txt', type=str)
parser.add_argument("--output", help="output path", default='dt_result1.txt', type=str)
args = parser.parse_args()


class DecisionTree():
    def __init__(self, metric=0):
        self.tree = None
        self._metric = metric

    def _terminal(self, train):
        return collections.Counter(train[:, -1]).most_common()[0][0]
  
    def _tree(self, train, depth=1):
        # gini index
        _metric = lambda groups: sum([(1.-sum([(v/len(g))**2 for k, v in collections.Counter(g[:, -1]).items()])) * (len(g)/len(list(chain(*groups)))) for g in filter(np.any, groups)])
        # split data where value lower than v and else
        _split = lambda i, v: (train[np.where(train[:, i] < v)], train[np.where(train[:, i] >= v)])
        # _split and calc value using _metric
        _apply = np.vectorize(lambda v, i: _metric(_split(i, v)))
        # get index of _applyed minimum
        _mini = lambda uni, idx, i: idx[_apply(uni, i).argmin()]
        
        m = np.apply_along_axis(lambda i: _mini(*np.unique(train[:, i], return_index=True), i), 1, np.array([np.arange(self._c-1)]).T)
        i, j = min(enumerate(m), key=lambda t: _metric(_split(t[0], train[t[1]][t[0]])))
        l, r = _split(i, train[j][i])
        
        node = {
            'index': i,
            'value': train[j][i],
            'left': l,
            'right': r
        }
        
        if not len(l) or not len(r):
            node['left'] = self._terminal(np.concatenate([l, r]))
            node['right'] = self._terminal(np.concatenate([l, r]))
        elif depth >= self.max_depth:
            node['left'] = self._terminal(l)
            node['right'] = self._terminal(r)
        else:
            if len(l) < self.min_size:
                node['left'] = self._terminal(l) 
            else:
                node['left'] = self._tree(l, depth+1)

            if len(r) < self.min_size:
                node['right'] = self._terminal(r)
            else:
                node['right'] = self._tree(r, depth+1)
        return node
    
    def fit(self, X, y, max_depth, min_size=.0):
        self.max_depth = max_depth
        self.min_size = min_size
        
        train = np.concatenate([X, np.array([y]).T], axis=1)
        self._r, self._c = train.shape
        self.tree = self._tree(train)

    def _predict(self, node, x):
        tar = node['left'] if x[node['index']] < node['value'] else node['right']
        return self._predict(tar, x) if isinstance(tar, dict) else tar
    
    def predict(self, X):
        return np.apply_along_axis(functools.partial(self._predict, self.tree), 1, X)


def load_data(train=args.train, test=args.test):
    train = pd.read_csv(train, sep='\t')
    # print(train)
    test = pd.read_csv(test, sep='\t')
    # parse data
    labels = dict()
    print(labels)
    y_label = (set(train.columns) - set(test.columns)).pop()
    print(y_label)
    df = pd.concat([train, test])

    for i in df:
        df[i], labels[i] = pd.factorize(df[i])

    x_train = df.iloc[:len(train)].drop(y_label, axis=1)
    x_test = df.iloc[len(train):].drop(y_label, axis=1)
    y_train = df.iloc[:len(train)][y_label]

    classifier = DecisionTree(0)
    classifier.fit(x_train, y_train, 16, 0)
    test[y_label] = pd.Series(map(lambda y: labels[y_label][y], classifier.predict(x_test)))
    test.to_csv(args.output, sep='\t', index=None)
    # answer = pd.read_csv('dt_answer1.txt', sep='\t')
    # print(sum(test[y_label] == answer[y_label]), len(test[y_label]))

if __name__ == "__main__":
    load_data()