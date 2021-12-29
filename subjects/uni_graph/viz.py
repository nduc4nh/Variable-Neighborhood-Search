import matplotlib as mpl
import matplotlib.pyplot as plt
import networkx as nx
from networkx.algorithms.shortest_paths import weighted
from graph_io import read_graph
from subjects.uni_graph.utils import find_adj

meta, data, d = read_graph("/home/nducanh/Desktop/Variable-Neighborhood-Search/data/idpc_data_10x10x1000.text")
n = [i for i in range(1,meta["num"] + 1)]
colors = meta['colors']
G = nx.Graph()
color_label = dict(zip(range(1,colors + 1),list("abcdefghij")))
for v in n:
    for color in range(1,colors+1):
        re = find_adj(n,d,v,color)
        if re:
            for ele in re:
                u,w = ele
                G.add_edge(v,u,weighted = w, color = color_label[color])

pos = nx.spring_layout(G, seed=7)
edges = G.edges()
colors = [G[u][v]['color'] for u,v in edges]
weights = [G[u][v]['weighted'] for u,v in edges]

n# nodes
nx.draw_networkx_nodes(G, pos, node_size=700)

# edges
nx.draw_networkx_edges(G, pos, edgelist=edges, width=6)

ax = plt.gca()
ax.margins(0.08)
plt.axis("off")
plt.tight_layout()
plt.show()
