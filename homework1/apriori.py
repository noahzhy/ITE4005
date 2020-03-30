import math
import argparse
import itertools

from itertools import combinations, chain
from collections import defaultdict


parser = argparse.ArgumentParser(description='three arguments: minimum support, input file name, output file name')
parser.add_argument('--min_sup', type=int, default=5, help='percent format')
parser.add_argument('--input_file', type=str, default='input.txt')
parser.add_argument('--output_file', type=str, default='output.txt')
args = parser.parse_args()


def read_data(path=args.input_file):
    with open(path) as f:
        return [list(map(int, line.split())) for line in f.readlines()]


def apriori(data=read_data(), support=args.min_sup/100, k=2):
    candidates = {frozenset([i]) for i in set(chain(*data))}

    def scan_data(data=data, candidates=candidates):
        candidate_count = defaultdict(int)
        for tid in data:
            for can in candidates:
                if can.issubset(tid):
                    candidate_count[can] += 1 
        res = {}
        for key, value in candidate_count.items():
            if float(value)/len(data) >= support:
               res[key] = value/len(data)
        return res

    def item_set(can, k=2):
        itemset = scan_data(candidates=can)
        new_candidates = {i.union(j) for i in itemset for j in itemset if len(i.union(j)) == k}
        return new_candidates, itemset

    res = {}
    while candidates:
        candidates, res[k-1] = item_set(candidates, k)
        k += 1
    return res


def rules(parameter_list):
    pass


def write_data(rules, path=args.output_file):
    with open('output.txt', 'w') as f:
        for item, asso, sup, conf in rules:
            f.write('{:10s}\t{:10s}\t{:.2f}\t{:.2f}\n'.format(
                '{{{}}}'.format(','.join(map(str, item))),
                '{{{}}}'.format(','.join(map(str, asso))),
                sup,
                conf
            ))

if __name__ == "__main__":
    res = apriori()
    print(res)
