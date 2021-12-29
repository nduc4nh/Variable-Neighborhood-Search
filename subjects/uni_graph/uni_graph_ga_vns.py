import sys
import os
sys.path.append(os.path.abspath("../../"))
from subjects.uni_graph.utils import find_adj, get_available_colors
from copy import deepcopy
import numpy as np
from graph_io import construct_possible_matrix, read_graph
from vns.vns_framework import GVNS_2
from neighbor_opt.permutation import insert_one_whole, swap_move_whole, two_opt_whole, insert_one, swap_move, two_opt, insert_three_whole, insert_three
from vns.improvement import BVND_non_random
from vns.change_step import sequential_change_step_
from vns.shake import shake
from vns.stop_condition import NonImprovemnt
from algorithm_operation import cross_over, fitness, fitness_2, mutation
from andevola.framework.GA import GA
from algorithm_operation import init_vns, init_func


np.random.seed(1)
if __name__=="__main__":
    stop = sys.argv[1]
    meta, data, d = read_graph(
        '/home/nducanh/Desktop/Variable-Neighborhood-Search/data/idpc_data_10x10x1000.text')
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


    # Defining params for GVNS
    Ns = [insert_one_whole, swap_move_whole, two_opt_whole, insert_three_whole]
    Ns_opt = [insert_one, swap_move, two_opt, insert_three]
    kmax = len(Ns)
    lmax = kmax
    print(n)
    fitness_func = fitness_2(n, d, start, end)
    x = init_vns(n,d,possible_matrix,start,end,colors, fitness_func)
    print(x)
    stop = NonImprovemnt(int(stop))

    # vns definition


    def vns(Ns, Ns_opt, kmax, lmax, evaluation,
            shaking,
            change_step,
            improvement,
            stop_condition,
            callback):
        #stop_condition.start_over()
        def func(X):
            X_ = deepcopy(X)
            X_.sort(key = lambda x:x[1])
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
                shaking=shake, #-> need wrapper
                change_step=sequential_change_step_,
                improvement=BVND_non_random, #-> need wrapper
                stop_condition=stop,
                callback=print_best(fitness_2(n, d, start, end, mem=True)))

    #callback = {"INITIAL":vns_func, "END-OPERATION":vns_func}
    callback = None
    #GA definition
    ga = GA(init=init_func(n, d,possible_matrix,start, end, colors,fitness_func),
            population_size=100,
            offset=100,
            iters=50,
            cr_prob=0.7,
            mu_prob=0.2,
            crossover=cross_over,
            mutation=mutation,
            fitness=fitness_func,
            valid=None,
            callbacks=callback,
            mode="min",
            )

    sol = ga.act()
    print(sol)