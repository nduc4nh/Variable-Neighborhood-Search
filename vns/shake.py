import numpy as np

def shake(x,k,N):
    return N[k](x)

def shake_(k,neighbors):
    n = len(neighbors[k])
    return neighbors[k][np.random.randint(n)]