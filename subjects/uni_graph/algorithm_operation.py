import sys
import os

from vns.shake import shake


sys.path.append(os.path.abspath("../../"))
import numpy as np
from utils import find_adj,get_next,get_available_colors
from graph_io import construct_possible_matrix
from copy import deepcopy
from andevola.operation.permutation.mutation import swap_mutation
from andevola.operation.permutation.crossover import ox
from neighbor_opt.permutation import swap_move_whole, two_opt_whole
from vns.improvement import BVND_non_random
#init individual with a given number of population
def init_individual(n,d,possible_matrix,start,end,size,colors):
    num = np.math.factorial(colors)
    if size > num:
        size = int(2*n/3)
    re = []
    
    firsts = get_available_colors(n,d,start,colors)
    ends = get_available_colors(n,d,end,colors)
    #print("hi")
    count = 0
    while count != size:
        tmp = list(np.random.permutation(range(1,colors+1)))
        valid = True
        for i in range(colors - 1):
            if possible_matrix[tmp[i]][tmp[i+1]] != 1:
                valid = False
                break
        if not valid:
            continue
        if tmp not in re and tmp[0] in firsts:
            re.append([tmp,tmp[-1]])
            count += 1
        
    #print("init done!")
    return re

"""def init_individual(n,d,start,end,size,colors):
    num = np.math.factorial(colors)
    if size > num:
        size = int(2*n/3)
    re = []

    firsts = get_available_colors(n,d,start,colors)
    ends = get_available_colors(n,d,end,colors)

    for i in range(size):
        tmp = list(np.random.permutation(range(1,colors+1)))
        print(i)
        if tmp not in re and tmp[0] in firsts and tmp[-1] in ends:
            re.append(tmp)
    
    print("init done!")
    return re"""

def init_func(n,d,possible_matrix,start,end,colors, fitness):
    def func(size):
        x = init_individual(n,d,possible_matrix,start,end,size,colors)
        re = [[ele,fitness(ele)] for ele in x] 
        return re
    return func


#init 1 individual for vns algorithm
def init_vns(n,d,possible_matrix,start,end,colors,defined_fitness):
    stop = 0
    while True:
        x = init_individual(n,d,possible_matrix,start,end,1,colors)[0]
        f = defined_fitness(x)
        
        if f != float("inf"):
            return x,f
        stop += 1
        #print("{}%".format(int(stop/int(np.math.factorial(colors)/100))))
        if stop == int(np.math.factorial(colors)/100):
            print("done")
            return x,f
            
def fitness_2(n,d,start,end,mem = True):
    
    def func(individual_and_mark):
        stop = individual_and_mark[1]
        cur_v = [start]
        cur_dist = {start:0}
        path = {start:[]}
        l = len(individual_and_mark[0])    
        best = float("inf")
        #print(start,end)
        for i,color in enumerate(individual_and_mark[0]):
            
            if mem:
                cur_dist,cur_v,path = get_next(n,d,cur_v,cur_dist,color,path)
            else:
                cur_dist,cur_v = get_next(n,d,cur_v,cur_dist,color)
            #print(cur_dist)
            if end in cur_dist:
                #print(path)
                if best > cur_dist[end]:
                    best = cur_dist[end]
                    stop = color
            if color == individual_and_mark[1]:
                break
        
        individual_and_mark[1] = stop 
        return best
    return func

#VNS wrapper operation

def fitness_for_neighbor(fitness):
    def func(x):
        x_and_mark = [x,x[-1]]
        return fitness(x_and_mark)
    return func


def two_opt_neighbor_wrapper(fitness,fitness_for_neigh, valid):
    improve = True

    def func(x): #standard input
        x_and_mark,f = x
        
        permute, stop = x_and_mark 
        index = permute.index(stop)
        candidate = permute[:index+1]
        rest = permute[index+1:]
        print(candidate)
        last_f = f
        while improve:
            last_f = f
            candidate,f = two_opt_whole(candidate, f,fitness_for_neigh,valid=valid)
            if f >= last_f:
                break
        tmp = [candidate,candidate[-1]]
        f = fitness(tmp)
        candidate.extend(rest)
        neighbor = [[candidate, candidate[1]], f]
        return neighbor
    
    return func

def swap_move_neighbor_wrapper(fitness,fitness_for_neigh, valid):
    improve = True

    def func(x): #standard input
        x_and_mark,f = x
        permute, stop = x_and_mark 
        index = permute.index(stop)
        candidate = permute[:index+1]
        rest = permute[index+1:]
        last_f = f
        while improve:
            last_f = f
            candidate,f = swap_move_whole(candidate, f,fitness_for_neigh,valid=valid)
            if f >= last_f:
                break
        tmp = [candidate,candidate[-1]]
        f = fitness(tmp)
        candidate.extend(rest)
        neighbor = [[candidate, candidate[1]], f]
        return neighbor
    
    return func

def add_move_neighbor_wrapper(fitness,fitness_for_neigh, valid):
    def find_pos(inserted_value, candidate,rest):
        l = len(candidate)
        index = 0
        best = float("inf")
        
        j = rest.index(inserted_value)
        rest.pop(j)
        l_rest = len(rest)
        
      
        for i in range(l + 1):
            candidate.insert(i,inserted_value)
            candidate.extend(rest)
            if not valid(candidate):
                candidate = candidate[:-l_rest]
                if i == l:
                    candidate = candidate[:-1]
                else:
                    candidate.pop(i)
                continue
            f_ = fitness_for_neigh(candidate)
            if f_ < best:
                best = f_
                index = i
            candidate = candidate[:-l_rest]
            
            if i == l:
                candidate = candidate[:-1]
            else:
                candidate.pop(i)
        
        candidate.insert(index, inserted_value)
        candidate.extend(rest)
        tmp = [candidate,candidate[-1]]
        f = fitness(tmp)
        
        neighbor = [[candidate, candidate[1]], f]
        return neighbor

    def func(x): #standard input
        
        improve = True
        neighbor = x
        while improve:
            improve = False
            x_and_mark,f = neighbor
            last_f = f
            permute, stop = x_and_mark
            index = permute.index(stop)
            candidate = permute[:index+1]
            rest = permute[index+1:]
            
            for i,ele in enumerate(rest):
                neighbor_tmp = find_pos(ele, candidate[:], rest[:])
                if neighbor_tmp[1] < last_f:
                    last_f = f
                    f = neighbor_tmp[1]
                    neighbor = deepcopy(neighbor_tmp)
                    #print(neighbor)
                    del neighbor_tmp
                    improve = True
                    break
            if last_f <= f:
                improve = False
        
        return neighbor
    
    return func

def shaking_wrapper(x,k,Ns_opt_wrp): #x and mark
    neighbor = Ns_opt_wrp[k](x)
    return neighbor
    
def Ns_opt_wrapper(N_opt):
    def func(x): #x and mark
        candidate = N_opt(x[0])
        return [candidate, candidate[-1]]
    return func

def add_random(x): #x and mark
    permutation, mark = x
    index = x.index(mark)
    candidate = permutation[:index + 1]
    rest = permutation[index:]
    if not rest:
        return x
    i = np.random.randint(len(candidate))
    j = np.random.randint(len(rest))
    ins_value = rest.pop(j)
    candidate.insert(i, ins_value)
    candidate.extend(rest)
    return [candidate, candidate[-1]]


def improvement(lmax, Ns):
    def func(x): #standard input
        return BVND_non_random(x, lmax, Ns)
    return func

def valid_sol(possible_matrix):
    def func(x): #permutation input
        n = len(x) 
        if n <= 1:
            return True
        for i in range(n-1):
            if possible_matrix[x[i]][x[i+1]] != 1:

                return False
        return True
    return func

#GA operation
def cross_over(x1,x2):
    n = len(x1)
    clone1 = deepcopy(x1)
    clone2 = deepcopy(x2)
    sub_x1,sub_x2 = ox(n, clone1[0], clone2[0])
    return [sub_x1,sub_x1[-1]],[sub_x2, sub_x2[-1]]
    
def mutation(x):
    clone = deepcopy(x)
    n = len(x)
    sub_x = swap_mutation(n,clone[0])
    return [sub_x, sub_x[-1]]