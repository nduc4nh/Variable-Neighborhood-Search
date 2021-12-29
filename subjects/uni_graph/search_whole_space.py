import pickle

from graph_io import construct_matrix, read_graph, construct_possible_matrix
from algorithm_operation import add_move_neighbor_wrapper, fitness_2, fitness_for_neighbor, init_func, init_individual, swap_move_neighbor_wrapper, two_opt_neighbor_wrapper, valid_sol
from subjects.uni_graph.utils import find_adj, get_available_colors

with open("../../data/space.pkl","rb") as f:
    space = pickle.load(f)

meta, data, d = read_graph(
        '/home/nducanh/Desktop/Variable-Neighborhood-Search/data/idpc_data_10x10x1000.text')
n = range(1, meta["num"]+1)
colors = meta["colors"]
start = meta["start"]
end = meta["end"]

possible_matrix = construct_possible_matrix(meta, data)

fitness = fitness_2(n, d, start, end,True)

pop = init_func(n, d, possible_matrix, start, end, colors, fitness)(5)
print(pop)
f_neigh = fitness_for_neighbor(fitness)
valid = valid_sol(possible_matrix)
# #print(pop)

print(add_move_neighbor_wrapper(fitness, f_neigh, valid)(pop[0]))
# print(f_neigh(pop[0][0][0]))

# print(get_available_colors(n,d,end,colors))

# for color in range(1,colors + 1):
    
#     print(color, [ele for ele in find_adj(n,d,1,color) if ele[1] <= 7])
# print("-")
# for color in range(1,colors + 1):
#     re = [[i,d[color][i][6]] for i in n if d[color][i][6] <= 7 and i != 6]
#     print(color, re)

#print(fitness([[2,3,1,4,5,6,7,8,9,10],10]))
# c2-1 c6-6 c8-9 c3-2 c9-8 c4-7

print(fitness([[2,6,8,3,9,4,1,5,7,10],10]), "yay")
print(find_adj(n,d,1,3))
