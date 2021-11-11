import numpy as np
import matplotlib.pyplot as plt

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
            x1 = shaking(x,np.random.randint(kmax-1),Ns)
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