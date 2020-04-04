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
            for candidate in candidates:
                if candidate.issubset(transaction):
                    count[candidate] += 1

        res = {}
        for k, v in count.items():
            if float(v)/len(data) >= support:
               res[k] = v/len(data)
        
        return res

    while candidates:
        filtered = scan()
        print(len(filtered))
        result[k-1] = filtered
        candidates = {i.union(j) for i in filtered for j in filtered if len(i.union(j)) == k}
        # print('candidates:>>>', candidates)
        k += 1
    return result


def define(res, transactions, confidence=.0):
    # print(res)
    def get_support(item):
        # print(len(item))
        return res[len(item)][item]

    for key, value in res.items():
        for item in value:
            elements = [combinations(item, i) for i, e in enumerate(item, 1)]
            for ele in map(frozenset, chain(*elements)):
                if item.difference(ele):
                    conf = get_support(item) / get_support(ele)
                    yield ele, item.difference(ele), round(get_support(item)*100, 2), round(conf*100, 2)


with open('input.txt') as f:
    data = [list(map(int, line.split())) for line in f.readlines()]
    # print(data)


freq = apriori(data, .05)
# print(freq)
rules = list(define(freq, data))


with open('output.txt', 'w') as f:
    for item, asso, sup, conf in rules:
        f.write('{:10s}\t{:10s}\t{:.2f}\t{:.2f}\n'.format(
            '{{{}}}'.format(','.join(map(str, item))),
            '{{{}}}'.format(','.join(map(str, asso))),
            sup,
            conf
        ))