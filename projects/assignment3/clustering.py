import argparse
import numpy as np
from math import sqrt
from collections import defaultdict


class Point:
    def __init__(self, args):
        self.id = int(args[0])
        self.x = args[1]
        self.y = args[2]
        self.type = None


class DBSCAN:
    def __init__(self, data, eps, minPts):
        self.data = data
        self.eps = eps
        self.minPts = minPts
        self.clusters = defaultdict(list)

    def regionQuery(self, curr_p):
        def dist(p1, p2):
            return sqrt((p1.x-p2.x)**2 + (p1.y-p2.y)**2)

        return [p for p in self.data if dist(p, curr_p) <= self.eps]

    def clustering(self):
        count_cluster = 0
        for p in self.data:
            if p.type: continue
            p.type = count_cluster
            neighbors = self.regionQuery(p)
            if len(neighbors) < self.minPts:
                p.type = -1
            else:
                count_cluster += 1
                self.clusters[count_cluster].append(p)
                for q in neighbors:
                    if not q.type:
                        q.type = count_cluster
                        neighbor = self.regionQuery(q)
                        if len(neighbor) >= self.minPts:
                            [neighbors.append(n) for n in neighbor]
                    if not (q in self.clusters[count_cluster]):
                        self.clusters[count_cluster].append(q)

        return self.clusters


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("input", type=str)
    parser.add_argument("n", type=int)
    parser.add_argument("eps", type=int)
    parser.add_argument("minPts", type=int)
    args = parser.parse_args()

    data = list(map(Point, np.loadtxt(args.input).tolist()))
    clusters = DBSCAN(data, args.eps, args.minPts).clustering()
    dict_slice = lambda adict, start, end: { k:adict[k] for k in list(adict.keys())[start:end] }
    clusters = dict_slice(clusters, 0, args.n)

    for key, value in clusters.items():
        np.savetxt(
            '{}_cluster_{}.txt'.format(args.input.split('.')[0], key-1),
            list(map(lambda x: x.id, value)),
            fmt='%d'
        )
