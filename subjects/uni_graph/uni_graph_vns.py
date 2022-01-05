import numpy as np
import sys
import os
sys.path.append(os.path.abspath("../../"))
from graph_io import construct_possible_matrix, read_graph
from vns.vns_framework import GVNS_2
from neighbor_opt.permutation import insert_one_whole, move_up, remove_insert, swap_move_whole, two_opt_whole, insert_one, swap_move, two_opt
from vns.improvement import BVND_non_random
from vns.change_step import sequential_change_step_
from vns.shake import shake
from vns.stop_condition import NonImprovemnt
from algorithm_operation import Ns_opt_wrapper, add_move_neighbor_wrapper, add_random, fitness_2, fitness_for_neighbor, improvement, init_individual, init_vns, move_up_neighbor_wrapper, remove_insert_neighbor_wrapper, shaking_wrapper, swap_move_neighbor_wrapper, two_opt_neighbor_wrapper, valid_sol


if __name__ == '__main__':
    stop = sys.argv[1]
    seed = sys.argv[2]
    exp_data = sys.argv[3]
    print(seed)
    np.random.seed(int(seed))
    meta, data, d = read_graph(
        '/home/nducanh/Desktop/Variable-Neighborhood-Search/data/' + exp_data)
    n = range(1, meta["num"]+1)
    colors = meta["colors"]
    start = meta["start"]
    end = meta["end"]
    possible_matrix = construct_possible_matrix(meta, data)
    path = None
    # get path

    def print_best(fitness):
        global path

        def func(x):
            return fitness(x)
        return func

    # Defining params for GVNS
    fitness_func = fitness_2(n, d, start, end)
    f_neigh = fitness_for_neighbor(fitness_func)
    valid = valid_sol(possible_matrix)

    Ns = [add_move_neighbor_wrapper(fitness_func, f_neigh, valid),
          two_opt_neighbor_wrapper(fitness_func, f_neigh, valid),
          swap_move_neighbor_wrapper(fitness_func, f_neigh, valid),
          move_up_neighbor_wrapper(fitness_func, f_neigh, valid),
          remove_insert_neighbor_wrapper(fitness_func, f_neigh, valid)]

    Ns_opt = [add_random,
              Ns_opt_wrapper(two_opt),
              Ns_opt_wrapper(swap_move),
              Ns_opt_wrapper(move_up),
              Ns_opt_wrapper(remove_insert)]
    
    kmax = len(Ns)
    lmax = kmax
    x = init_vns(n, d, possible_matrix, start, end, colors, fitness_func)
    print(x)
    stop = NonImprovemnt(int(stop))

    sol = GVNS_2(x, Ns, Ns_opt, kmax, lmax, evaluation=fitness_func,
                 shaking=shaking_wrapper,
                 change_step=sequential_change_step_,
                 improvement=improvement(lmax, Ns),
                 stop_condition=stop,
                 callback=print_best(fitness_2(n, d, start, end, mem=True)))

    with open("./result/vns_" +exp_data+".txt", "a+") as f:
        f.write("seed: {} - result: {} \n".format(seed, sol.__str__())) 
    print(sol)
