import numpy as np
import matplotlib.pyplot as plt
from vns.util_funcs import get_all_neighbors

np.random.seed(0)
#GVNS with random procedure
def GVNS(x,Ns, kmax, lmax,
         evaluation=None, 
         shaking=None, 
         change_step=None, 
         improvement=None,
         stop_condition=None,
         history=None,
         callback=None):
    
    best = float("inf")
    re = None
    history = []
    while not stop_condition.is_met():
        k = 1
        while k != kmax:
        #print(k)    
            x1 = shaking(x,k,Ns)
            x2 = improvement(x1,lmax,Ns,evaluation)
            x,k = change_step(x,x2,k,evaluation)
        s = evaluation(x)
        re = x
        
        if s < best:
            history.append((x,s))
            print(s)
            callback(x)
            stop_condition.start_over()
            best = s
        else:
            stop_condition.update()
    plt.show()
    return best,re


#GVNS 
def GVNS_2(x,Ns, Ns_opt, kmax, lmax,
         evaluation=None, 
         shaking=None, 
         change_step=None, 
         improvement=None,
         stop_condition=None,
         search_strat = "first",
         history=None,
         callback=None):

    best = float("inf")
    re = None
    history = []
    while not stop_condition.is_met():
        k = 1
        while k != kmax:
        #print(k)    
            shaked_data = shaking(x[0],k,Ns_opt)
            x1 = [shaked_data, evaluation(shaked_data)]
            x2 = improvement(x1,lmax,Ns,evaluation,search_strat)
            x,k = change_step(x,x2,k)
            print(evaluation(x[0]), k)
        s = evaluation(x[0])
        re = x
        print("-----")
        print(stop_condition.count, stop_condition.stop)
        if s < best:
            history.append((x,s))
            print(s)
            if callback:
                callback(x[0])
            stop_condition.start_over()
            best = s
        else:
            stop_condition.update()
    plt.show()
    return best,re

