import sys
import os
sys.path.append(os.path.abspath("../../"))
from algorithm_operation import init_vns, init_func
from andevola.framework.GA import GA
from algorithm_operation import Ns_opt_wrapper, add_move_neighbor_wrapper, add_random, cross_over, fitness_2, fitness_for_neighbor, improvement, move_up_neighbor_wrapper, mutation, remove_insert_neighbor_wrapper, shaking_wrapper, swap_move_neighbor_wrapper, two_opt_neighbor_wrapper, valid_sol
from vns.stop_condition import NonImprovemnt
from vns.shake import shake
from vns.change_step import sequential_change_step_
from vns.improvement import BVND_non_random
from neighbor_opt.permutation import insert_one_whole, move_up, remove_insert, swap_move_whole, two_opt_whole, insert_one, swap_move, two_opt, insert_three_whole, insert_three
from vns.vns_framework import GVNS_2
from graph_io import construct_possible_matrix, read_graph
import numpy as np
from copy import deepcopy
from subjects.uni_graph.utils import find_adj, get_available_colors
import time


if __name__ == "__main__":
    stop = sys.argv[1]
    seed = sys.argv[2]
    exp_data = sys.argv[3]
    dest_path = None
    try:
        export_path = sys.argv[4]
        dest_path = os.path.join(export_path, exp_data)[:-5]        
        if not os.path.exists(dest_path):
            os.mkdir(dest_path)
    except:
        pass

    np.random.seed(int(seed))
    meta, data, d = read_graph(
        '/home/nducanh/Desktop/Variable-Neighborhood-Search/data/' + exp_data)
    n = range(1, meta["num"]+1)
    colors = meta["colors"]
    start = meta["start"]
    end = meta["end"]
    for color in range(1, colors + 1):
        print(d[color][start][end])
    


    possible_matrix = construct_possible_matrix(meta, data)
    path = None
    # get path

    def print_best(fitness):
        global path
        print(path)

        def func(x):
            return fitness(x)
        return func

    fitness_func = fitness_2(n, d, start, end)
    # Defining params for GVNS
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
    stop = NonImprovemnt(int(stop))

    # vns definition

    def vns(Ns, Ns_opt, kmax, lmax, evaluation,
            shaking,
            change_step,
            improvement,
            stop_condition,
            callback):
        # stop_condition.start_over()
        def func(X):
            X_ = deepcopy(X)
            X_.sort(key=lambda x: x[1])
            x = X_[0]
            sol = GVNS_2(x, Ns, Ns_opt, kmax, lmax, evaluation,
                         shaking,
                         change_step,
                         improvement,
                         stop_condition,
                         callback)
            X_[0] = list(sol[1]) if sol[0] < X_[0][1] else X_[0]
            return X_
        return func

    vns_func = vns(Ns, Ns_opt, kmax, lmax, evaluation=fitness_func,
                   shaking=shaking_wrapper,  # -> need wrapper
                   change_step=sequential_change_step_,
                   improvement=improvement(lmax, Ns),  # -> need wrapper
                   stop_condition=stop,
                   callback=print_best(fitness_2(n, d, start, end, mem=True)))

    callback = {"INITIAL": vns_func, "END-OPERATION": vns_func}
    #callback = None
    # GA definition
    ga = GA(init=init_func(n, d, possible_matrix, start, end, colors, fitness_func),
            population_size=100,
            offset=100,
            iters=30,
            cr_prob=0.7,
            mu_prob=0.2,
            crossover=cross_over,
            mutation=mutation,
            fitness=fitness_func,
            valid=None,
            callbacks=callback,
            mode="min",
            select_type="MIXING"
            )
    t1 = time.perf_counter()
    sol = ga.act()
    t2 = time.perf_counter()
    exec_time = int(t2 - t1)
    h = exec_time//3600
    m = (exec_time - h*3600)//60
    s = (exec_time - h*3600 - m*60)
    readable_time = "{:02d}:{:02d}:{:02d}".format(h,m,s)
    output_name = exp_data + "_seed_{}.opt".format(seed)
    


    # with open("./result/gavns" + exp_data + ".txt", "a+") as f:
    #     f.write("seed: {} - result: {} \n".format(seed, sol.__str__()))
    # print(sol)

    with open(os.path.join(dest_path,output_name), "w+") as f:
        f.writelines([
            "Filename: {}".format(exp_data),
            "Seed: {}".format(seed),
            "Fitness: {}".format(sol[1]),
            "Time: {}".format(readable_time)
            ])
    
