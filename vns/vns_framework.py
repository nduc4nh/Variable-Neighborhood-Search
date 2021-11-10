import numpy as np

def GVNS(x,Ns, kmax, lmax,
         evaluation=None, 
         shaking=None, 
         change_step=None, 
         improvement=None,
         stop_condition=None):
    
    best = float("inf")
    re = None
    while not stop_condition.is_met():
        k = 1
        while k != kmax:
        #print(k)
            x1 = shaking(x,np.random.randint(kmax-1),Ns)
            x2 = improvement(x1,lmax,Ns,evaluation)
            x,k = change_step(x,x2,k,evaluation)
        s = evaluation(x)
        re = x
        print(s)
        if s < best:
            stop_condition.start_over()
            best = s
        else:
            stop_condition.update()
    return best,re