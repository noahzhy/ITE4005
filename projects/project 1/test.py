from collections import defaultdict
from itertools import combinations, chain
from decimal import Decimal, getcontext, ROUND_HALF_UP
# 引入一些依赖


support = .05
getcontext().rounding = ROUND_HALF_UP

# 四舍五入
def rounding(value, k):
    return type(value)(round(Decimal(value), k))


def apriori(data, support):
    # 创建候选集合
    candidates = {frozenset([x]) for x in set(chain(*data))}
    # 用字典储存结果
    result = dict()
    k = 2

    def scan():
        count = defaultdict(int)
        for transaction in data:
            # print(transaction)
            for candidate in candidates:
                if candidate.issubset(transaction):
                    count[candidate] += 1

        res = {}
        for k, v in count.items():
            # print(k, v, '>>>')
            if float(v)/len(data) >= support:
               res[k] = v/len(data)
        
        return res

    while candidates:
        filtered = scan()
        result[k-1] = filtered
        candidates = {i.union(j) for i in filtered for j in filtered if len(i.union(j)) == k}
        print('candidates:>>>', candidates)
        k += 1
    return result


def define(freq, transactions, confidence=.0):
    def f(item): return freq[len(item)][item]
    for k, v in freq.items():
        if k == 1: continue
        for item in v:
            for element in map(frozenset, chain(*[combinations(item, i) for i, e in enumerate(item, 1)])):
                remain = item.difference(element)
                if remain:
                    (a, b), (c, d) = f(item).as_integer_ratio(), f(element).as_integer_ratio()
                    conf = (a/b)/(c/d)
                    if conf >= confidence:
                        yield element, remain, rounding(f(item) * 100, 2), rounding(conf * 100, 2)


with open('input.txt') as f:
    data = [list(map(int, line.split())) for line in f.readlines()]
    # print(data)


freq = apriori(data, .05)
rules = list(define(freq, data))


with open('output.txt', 'w') as f:
    for item, asso, sup, conf in rules:
        f.write('{:10s}\t{:10s}\t{:.2f}\t{:.2f}\n'.format(
            '{{{}}}'.format(','.join(map(str, item))),
            '{{{}}}'.format(','.join(map(str, asso))),
            sup,
            conf
        ))