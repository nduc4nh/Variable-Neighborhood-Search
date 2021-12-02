import numpy as np
from evaluation_func import find_adj,get_next

#init individual with a given number of population
def init_individual(size,colors):
    n = np.math.factorial(colors)
    if size > n:
        size = int(2*n/3)
    re = []
    for i in range(size):
        tmp = list(np.random.permutation(range(1,colors+1)))
        print(i)
        if tmp not in re:
            re.append(tmp)
    return re

#init 1 individual for vns algorithm
def init_vns(colors,defined_fitness):
    stop = 0
    while True:
        x = init_individual(1,colors)[0]
        f = defined_fitness(x)
        if f != float("inf"):
            return x,f
        stop += 1
        if stop == int(np.math.factorial(colors)*2/3):
            return x,f
            
def fitness(n,d,start,end):
    def func(individual_x):
        cur_v = [start]
        cur_dist = {start:0}
        for ele in find_adj(n,d,start,individual_x[0]):
            cur_v.append(ele[0])
            cur_dist[ele[0]] = ele[1]
        l = len(individual_x)    
        for i,color in enumerate(individual_x):
            if i != l - 1:
                if end in cur_dist:
                    cur_dist[end] = float("inf")
                    cur_v.remove(end)

            cur_dist,cur_v = get_next(n,d,cur_v,cur_dist,color)
            
        return cur_dist[end]
    return func


