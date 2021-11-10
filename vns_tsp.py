from vns.shake import shake
from vns.change_step import sequential_change_step
from vns.improvement import BVND
from vns.stop_condition import NonImprovemnt
from vns.vns_framework import GVNS

from neighbor_opt.permutation import insert_one, swap_move, two_opt
import numpy as np

nodes = {}

with open("./data/tspdata.txt", "r") as f:
    for line in f:
        tmp = line.strip().split()
        if len(tmp) != 3:
            continue
        nodes[int(tmp[0])] = np.array((int(tmp[1]), int(tmp[2])))

n = len(nodes)
d = [[0 for i in range(n + 1)] for i in range(n + 1)]
for i in range(1, n + 1):
    for j in range(1, n + 1):
        d[i][j] = np.math.dist(nodes[i], nodes[j])


def get_travel_distance(permutation):
    global d
    n = len(permutation)
    s = d[permutation[0]][permutation[-1]]
    for i in range(n-1):
        s += d[permutation[i]][permutation[i+1]]
    return s


def init_x():
    global n
    return np.random.permutation([i for i in range(1, n+1)])


Ns = [insert_one, swap_move, two_opt]
kmax = len(Ns)
lmax = kmax
x = init_x()
stop_condition = NonImprovemnt(1000)

if __name__ == "__main__":
    re = GVNS(x,Ns, kmax, lmax,
        evaluation=get_travel_distance,
        change_step=sequential_change_step,
        improvement=BVND,
        shaking=shake,
        stop_condition=stop_condition)

    print(re)