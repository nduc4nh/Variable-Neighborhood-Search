def sequential_change_step(x,x1,k, fitness):
    s1 = fitness(x)
    s2 = fitness(x1)
    if s2 < s1:
        x = x1
        return x,1
    return x,k+1

def sequential_change_step_(x,x1,k):
    if x1[1] < x[1]:
        x = x1
        return x,1
    return x,k+1
