import numpy as np

def two_opt(x):
    x = list(x)
    n = len(x)
    x_ = x[:]
    
    i,j = np.random.choice([i for i in range(n)],size = 2,replace = False)
    if i > j: i,j = j,i
    
    re = x_[:i+1] + x_[i+1:j+1][::-1] + x_[j+1:]
    return re

def insert_one(x):
    x = list(x)
    n = len(x)
    x_ = x[:]
    i,j = np.random.choice([i for i in range(n)],size = 2,replace = False)
    if i > j: i,j = j,i
    tmp = x_[i]
    tmp1 = x_[:i]
    tmp2 = x_[i+1:]
    tmp1 = tmp1 + tmp2
    if j == 0: re = [tmp] + tmp1
    else: re = tmp1[:j] + [tmp] + tmp1[j:]
    return re

def swap_move(x):
    x = list(x)
    n = len(x)
    x_ = x[:]
    i,j = np.random.choice([i for i in range(n)],size = 2,replace = False)
    if i > j: i,j = j,i
    re = x_[:]
    re[i],re[j] = re[j],re[i]
    return re