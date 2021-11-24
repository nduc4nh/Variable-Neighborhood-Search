import numpy as np
import os,sys
sys.path.append(os.path.abspath("./"))
from evaluation_func import contains,find_adj,get_next

if __name__=="__main__":

    #generate random uni-derection graph with colors
    n = list(range(9))
    colors = 3
    d = dict([(ele,[]) for ele in range(colors)])

    d_adj = {}
    for ele in n:
        for color in range(colors):
            adjs = list(np.random.choice(n,4,replace = False))
            if ele in adjs: adjs.remove(ele)
            weights = [np.random.randint(1,20) for i in range(len(adjs))]
            full_adjs = list(zip(adjs,weights))
            d_adj[(color, ele).__str__()] = full_adjs


    #construct matrix presentation for Graph
    for color in range(colors):
        tmp_matrix = [[float("inf") for ele in n] for ele in n]
        d[color] = tmp_matrix
        for i in n:
            for j in n:
                if i == j:
                    d[color][i][j] = 0
                    
                edge = contains( j,d_adj[(color, i).__str__()])
                if edge:
                    d[color][i][j] = edge[1]

    #initiate starting vertex data
    cur_v = [0]
    cur_dist = {0:0}
    for ele in find_adj(n,d,0,0):
        cur_v.append(ele[0])
        cur_dist[ele[0]] = ele[1]

    print(get_next(n,d,cur_v,cur_dist,0))