from .change_step import sequential_change_step

def BVND(x,lmax,N, fitness):
    x_ = x
    while True:
        l = 0
        x1 = x_
        while l != lmax:
            x2 = N[l](x_)
            x_,l = sequential_change_step(x_,x2,l, fitness)
        #print(get_travel_distance(x1),get_travel_distance(x_))
        if fitness(x1)  <= fitness(x_):
            return x1


def BVND_non_random(x,lmax,neighbors,fitness):
    x_ = x
    while True:
        l = 0
        x1 = x_
        while l != lmax:
            x2 = min([(ele, fitness(ele)) for ele in neighbors[l]], key=lambda x:x[1])[0]
            x_,l = sequential_change_step(x_,x2,l, fitness)
        #print(get_travel_distance(x1),get_travel_distance(x_))
        if fitness(x1)  <= fitness(x_):
            return x1
