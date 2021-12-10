import numpy as np
from utils import find_adj,get_next,get_available_colors

#init individual with a given number of population
def init_individual(n,d,start,end,size,colors):
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
    return re

def init_func(n,d,start,end,colors, fitness):
    def func(size):
        x = init_individual(n,d,start,end,size,colors)
        re = [[ele,fitness(ele)] for ele in x] 
        return re
    return func


#init 1 individual for vns algorithm
def init_vns(n,d,start,end,colors,defined_fitness):
    stop = 0
    while True:
        x = init_individual(n,d,start,end,1,colors)[0]
        f = defined_fitness(x)
        if f != float("inf"):
            return x,f
        stop += 1
        if stop == int(np.math.factorial(colors)*2/3):
            return x,f
            
def fitness(n,d,start,end,mem = False):
    
    def func(individual_x):
        cur_v = []
        cur_dist = {start:0}
        path = {start:[]}
        for ele in find_adj(n,d,start,individual_x[0]):
            cur_v.append(ele[0])
            cur_dist[ele[0]] = ele[1]
            if mem:
                path[ele[0]] = [(start,individual_x[0])]
        l = len(individual_x)    
        for i,color in enumerate(individual_x):
            if i != l - 1:
                if end in cur_dist:
                    cur_dist[end] = float("inf")
                    cur_v.remove(end)
            if mem:
                cur_dist,cur_v,path = get_next(n,d,cur_v,cur_dist,color,path)
            else:
                cur_dist,cur_v = get_next(n,d,cur_v,cur_dist,color)
        
        return cur_dist[end]
    return func


