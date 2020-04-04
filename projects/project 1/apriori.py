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
    candidates = set(frozenset([i]) for i in set(chain(*data)))

    def scan_data(data=data, candidates=candidates):
        candidate_count = defaultdict(int)
        for tid in data:
            for cand in candidates:
                if cand.issubset(tid):
                    candidate_count[cand] += 1
        res = dict()
        for key, value in candidate_count.items():
            if float(value/len(data)) >= support:
               res[key] = float(value/len(data))
        return res

    def item_set(item, k=2):
        new_candidates = []
        for i in itemset:
            for j in itemset:
                if len(i.union(j)) == k:
                    new_candidates.append(i.union(j))
        candidates = set(new_candidates)
        return itemset

    res = dict()
    count = 0
    # k = 2
    while candidates:
        print(len(candidates))

        itemset = scan_data(candidates=candidates)
        res[k-1] = item_set(itemset, k)
        k += 1

        # break

        count += 1
        if count >= 3:
            break
    return res


def rules(res):
    def get_support(item):
        return res[len(item)][item]

    for key, value in res.items():
        for item in value:
            elements = [combinations(item, i) for i, e in enumerate(item, 1)]
            for ele in map(frozenset, chain(*elements)):
                if item.difference(ele):
                    conf = get_support(item) / get_support(ele)
                    yield ele, item.difference(ele), round(get_support(item)*100, 2), round(conf*100, 2)


def write_data(rules, path=args.output_file):
    with open('output.txt', 'w') as f:
        for item, ass, sup, conf in rules:
            f.write('{:10s}\t{:10s}\t{:.2f}\t{:.2f}\n'.format(
                '{{{}}}'.format(','.join(map(str, item))),
                '{{{}}}'.format(','.join(map(str, ass))),
                sup,
                conf
            ))


if __name__ == "__main__":
    res = rules(apriori())
    write_data(res)
