#utils

def get_all_neighbors(x,Ns,fitness):
    tmp = [opt(x[0]) for opt in Ns]
    re = []
    for neigh in tmp:
        tmp2 = [(ele,fitness(ele)) for ele in neigh]
        tmp2.sort(key=lambda x:x[1])
        re.append(tmp2)
    return re
            