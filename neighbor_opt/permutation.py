import numpy as np

#Random 
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


#Whole
def two_opt_whole(x):
    x = list(x)
    n = len(x)
    
    neighbors = []
    for i in range(n-1):
        for j in range(i+1,n):
            x_ = x[:]
            neighbors.append(x_[:i] + x_[i:j+1][::-1] + x_[j+1:])
        
    return neighbors

def insert_one_whole(x):
    x = list(x)
    n = len(x)
    neighbors = []
    for i in range(n):
        for j in range(n):
            if j == i - 1 or i == j:
                continue
            x_ = x[:]
            tmp = x_[i]
            tmp1 = x_[:i]
            tmp2 = x_[i+1:]
        
            tmp1 = tmp1 + tmp2
            if x[i] == 0:
                print(tmp1,tmp,j,[tmp] + tmp1)
            if j == 0: neighbors.append([tmp] + tmp1)
            else: neighbors.append(tmp1[:j] + [tmp] + tmp1[j:])

    return neighbors

def swap_move_whole(x):
    x = list(x)
    n = len(x)
    neighbors = []
    for i in range(n-1):
        for j in range(i+1,n):
            x_ = x[:]
            x_[i],x_[j] = x_[j],x_[i]
            neighbors.append(x_)
    return neighbors