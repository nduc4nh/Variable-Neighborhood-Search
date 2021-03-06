def contains(x,li):
    for ele in li:
        if ele[0] == x:
            return ele
    return False

def read(path):
    meta = {
        "colors": None,
        "num": None,
        "start":None,
        "end":None
    }

    d_adj = {}

    with open(path, "r") as f:
        for i, ele in enumerate(f):
            line = ele.strip().split()
            line = list(map(int, line))
            
            if i == 0:
                meta["num"] = line[0]
                meta["colors"] = line[1]
                continue
            if i == 1:
                meta["start"] = line[0]
                meta["end"] = line[1]
                continue
           
            key = (line[-1], line[0]).__str__()
            value = (line[1], line[2])
            if d_adj.__contains__(key):
                d_adj[key].append(value)
            else:
                d_adj[key] = [value]

    return meta, d_adj


def construct_matrix(meta,d_adj):
    n = list(range(1, meta["num"] + 1))
    colors = meta["colors"]
    d = dict([(ele,[]) for ele in range(1,colors+1)])
    for color in range(1,colors+1):
        tmp_matrix = [[float("inf") for ele in range(meta["num"] + 1)] for ele in range(meta["num"] + 1)]
        d[color] = tmp_matrix
        for i in n:
            if not d_adj.__contains__((color, i).__str__()):
                    continue
            for j in n:
                if i == j:
                    d[color][i][j] = 0
                edge = contains( j,d_adj[(color, i).__str__()])
                
                if edge:
                    d[color][i][j] = edge[1]
    return d

def construct_possible_matrix(meta, d_adj):
    feasible_matrix = [[float("inf") for ele in range(meta["colors"] + 1)] for ele in range(meta["colors"] + 1)]
    colors = meta["colors"]
    n = list(range(1, meta["num"] + 1))
    for color_from in range(1, colors+1):
        for color_to in range(1, colors+1):
            for v in n:
                if not d_adj.__contains__((color_from,v).__str__()): #exist out-edge of begining color
                    continue
                for adj in n:
                    if not d_adj.__contains__((color_to,adj).__str__()): #other vertices exist out edge of targeting color 
                        continue
                    if contains(v,d_adj[(color_to,adj).__str__()]): #exist in-edge of targeting color
                        feasible_matrix[color_from][color_to] = 1
                        break
                
                if feasible_matrix[color_from][color_to] == 1:
                    break
    return feasible_matrix

def read_graph(path):
    meta, data = read(path)
    return meta,data,construct_matrix(meta, data)


if __name__ == '__main__':
    import sys
    path = sys.argv[1]
    print(read_graph(path))