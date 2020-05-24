import argparse
import numpy as np
from math import sqrt
from collections import defaultdict


parser = argparse.ArgumentParser()
parser.add_argument("input", type=str, default='input2.txt')
parser.add_argument("n", type=int, default=5)
parser.add_argument("eps", type=int, default=2)
parser.add_argument("minPts", type=int, default=7)
args = parser.parse_args()


class Point:
    def __init__(self, args):
        self.id = int(args[0])
        self.x = args[1]
        self.y = args[2]
        # -1: Noise; other num: cluster
        self.type = None


class DBSCAN:
    def __init__(self, data, eps, minPts):
        self.data = data
        self.eps = eps
        self.minPts = minPts
        self.clusters = defaultdict(list)

    def dist(self, p1, p2):
        return sqrt((p1.x-p2.x)**2 + (p1.y-p2.y)**2)

    def get_neighbor(self, curr_pt):
        neighbor = [p for p in self.data if self.dist(curr_pt, p) <= self.eps]
        neighbor.remove(curr_pt)
        return neighbor

    def expand(self, p, neighbors, count):
        self.clusters[count].append(p)
        for q in neighbors:
            if not q.type:
                q.type = count
                neighbor = self.get_neighbor(q)
                if len(neighbor) >= self.minPts:
                    [neighbors.append(n) for n in neighbor]
            if not (q in self.clusters[count]):
                self.clusters[count].append(q)

    def clustering(self):
        cluster_count = 0
        for p in self.data:
            if p.type: continue
            p.type = cluster_count
            neighbors = self.get_neighbor(p)
            if len(neighbors) < self.minPts:
                p.type = -1
            else:
                cluster_count += 1
                self.expand(p, neighbors, cluster_count)
        return self.clusters


if __name__ == "__main__":
    data_list = np.loadtxt(args.input).tolist()
    data = list(map(Point, data_list))
    clusters = DBSCAN(data, args.eps, args.minPts).clustering()

    for key, value in clusters.items():
        np.savetxt(
            '{}_cluster_{}.txt'.format(args.input.split('.')[0], key-1),
            list(map(lambda x: x.id, value)),
            fmt='%d'
        )