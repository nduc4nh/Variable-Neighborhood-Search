import os,sys

sys.path.append(os.path.abspath("./"))

from vns.shake import shake
from vns.change_step import sequential_change_step
from vns.improvement import BVND_non_random
from vns.stop_condition import NonImprovemnt
from vns.vns_framework import GVNS_2

from neighbor_opt.permutation import insert_one_whole, swap_move_whole, two_opt_whole
import numpy as np
import matplotlib.pyplot as plt


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


Ns = [insert_one_whole, swap_move_whole, two_opt_whole]
kmax = len(Ns)
lmax = kmax
x = init_x()
stop_condition = NonImprovemnt(10000)

def plotting(x):
    print(x)
    global nodes
    x_ = [nodes[i][0] for i in x]
    y_ = [nodes[i][1] for i in x]
    plt.cla()
    plt.plot(x_,y_,)
    plt.scatter(x_,y_)
    plt.pause(0.02)
    

if __name__ == "__main__":
    re = GVNS_2(x,Ns, kmax, lmax,
        evaluation=get_travel_distance,
        change_step=sequential_change_step,
        improvement=BVND_non_random,
        shaking=shake,
        stop_condition=stop_condition,
        callback=plotting)

    print(re)