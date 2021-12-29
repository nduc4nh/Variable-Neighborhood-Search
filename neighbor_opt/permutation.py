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

def insert_three(x):
    x = list(x)
    n = len(x)
    x_ = x[:]
    i,j = np.random.choice([i for i in range(n-3)],size = 2,replace = False)
    if i > j: i,j = j,i
    tmp = x_[i:i+3]
    tmp1 = x_[:i]
    tmp2 = x_[i+3:]
    tmp1 = tmp1 + tmp2
    if j == 0: re = tmp + tmp1
    else: re = tmp1[:j] + tmp + tmp1[j:]
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


#Whole neighbors with search strategy
def insert_one_whole(x, f_x, fitness, search_strat = "first"):
    x = list(x)
    n = len(x)
    neighbors = []
    permute_candidate = x
    best = f_x
    for i in range(n):
        for j in range(n):
            if j == i - 1 or i == j:
                continue
            x_ = x[:]
            tmp = x_[i]
            tmp1 = x_[:i]
            tmp2 = x_[i+1:]
        
            tmp1 = tmp1 + tmp2
            if j == 0: candidate_tmp = [tmp] + tmp1
            else: candidate_tmp = tmp1[:j] + [tmp] + tmp1[j:]
            candidate_tmp_f = fitness(candidate_tmp) 
            if  candidate_tmp_f < best:
                permute_candidate = candidate_tmp
                best = candidate_tmp_f    
                if search_strat == 'first':
                    return permute_candidate,best

    return permute_candidate,best

def swap_move_whole(x, f_x, fitness, search_strat = "first", valid = None):
    x = list(x)
    n = len(x)
    best = f_x
    permutation_candidate = x
    for i in range(n-1):
        for j in range(i+1,n):
            x_ = x[:]
            x_[i],x_[j] = x_[j],x_[i]
            f_x_ = fitness(x_)
            if f_x_ < best:
                if valid and not valid(x):
                    continue
                best = f_x_
                permutation_candidate = x_
                if search_strat == "first":
                    return permutation_candidate, best
    return permutation_candidate, best


def two_opt_whole(x, f_x, fitness, search_strat = "first", valid = None):
    """
    x: permutation
    f_x: fitness of permutation
    search_strat = ['first', 'best] default: 'first
    """
    x = list(x)
    n = len(x)
    if n <= 2:
        return x,f_x
    best = f_x
    
    permute_candidate = x
    for i in range(n-1):
        for j in range(i+1,n):
            tmp = x[:i] + x[i:j+1][::-1] + x[j+1:]
            tmp_f = fitness(tmp) 
            if tmp_f < best:
                if valid and not valid(x):
                    continue
                permute_candidate = tmp
                best = tmp_f
                if search_strat == 'first':
                    return permute_candidate, best
        
    return permute_candidate, best

def insert_three_whole(x, f_x, fitness, search_strat = "first"):
    x = list(x)
    n = len(x)
    neighbors = []
    permute_candidate = x
    best = f_x
    for i in range(n):
        for j in range(n-3):
            if j == i - 1 or i == j:
                continue
            x_ = x[:]
            tmp = x_[i:i+3]
            tmp1 = x_[:i]
            tmp2 = x_[i+3:]
        
            tmp1 = tmp1 + tmp2
            if j == 0: candidate_tmp = tmp + tmp1
            else: candidate_tmp = tmp1[:j] + tmp + tmp1[j:]
            candidate_tmp_f = fitness(candidate_tmp) 
            if  candidate_tmp_f < best:
                permute_candidate = candidate_tmp
                best = candidate_tmp_f    
                if search_strat == 'first':
                    return permute_candidate,best
    return permute_candidate,best



