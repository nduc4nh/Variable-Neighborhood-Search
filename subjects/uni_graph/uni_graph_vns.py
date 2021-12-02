from algorithm_operation import fitness, init_individual, init_vns
import sys
import os
sys.path.append(os.path.abspath("../../"))
from vns.stop_condition import NonImprovemnt
from vns.shake import shake
from vns.change_step import sequential_change_step_
from vns.improvement import BVND_non_random
from neighbor_opt.permutation import insert_one_whole, swap_move_whole, two_opt_whole, insert_one, swap_move, two_opt
from vns.vns_framework import GVNS_2
from graph_io import read_graph
import numpy as np

if __name__ == '__main__':
    np.random.seed(0)
    stop = sys.argv[1]
    meta, data, d = read_graph(
        '/home/nducanh/Desktop/Variable-Neighborhood-Search/data/idpc_data_10x10x1000.text')
    n = range(1, meta["num"]+1)
    colors = meta["colors"]
    start = meta["start"]
    end = meta["end"]
    
    #Defining params for GVNS
    Ns = [insert_one_whole, swap_move_whole, two_opt_whole]
    Ns_opt = [insert_one, swap_move, two_opt]
    kmax = len(Ns)
    lmax = kmax
    fitness_func = fitness(n, d, start, end)
    x = init_vns(colors, fitness_func)
    stop = NonImprovemnt(int(stop))
    sol = GVNS_2(x, Ns, Ns_opt, kmax, lmax, evaluation=fitness_func,
           shaking=shake,
           change_step=sequential_change_step_,
           improvement=BVND_non_random,
           stop_condition=stop)

    print(sol)