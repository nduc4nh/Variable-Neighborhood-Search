import numpy as np
import matplotlib.pyplot as plt
from vns.util_funcs import get_all_neighbors

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
def GVNS_2(x,Ns, kmax, lmax,
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
            neighbors = get_all_neighbors(x,Ns,evaluation)
            x1 = shaking(k,neighbors)
            x2 = improvement(x1,lmax,Ns,evaluation)
            x,k = change_step(x,x2,k)
            print(evaluation(x[0]), k )
        s = evaluation(x[0])
        re = x
        print("-----")
        
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

