#given indices of vertices n, distance matrix d--> find adjencent vertices of x
def find_adj(n,d,x,color):
    """
    input: v
    output: u,w
    """
    re = []
    for i in range(1,len(n)+1):
        weight = d[color][x][i]
        if weight != 0 and weight != float("inf"):
            re.append((i, weight))
    return re 

#given indices of vertices n, distance matrix d--> find shorstest distance from start to vertices having color "c" in-edge
def get_next(n,d,cur_v,cur_dist,c,path = None):
    queue = []
    dist = {}
    traversed = []
    for ele in n:
        dist[ele] = float("inf")

    for v in cur_v:
        dist[v] = cur_dist[v]
        if path:
            path[v] = path[v]
        queue.append([v, dist[v]])
    if path: print(path)
    queue.sort(key = lambda x: x[1])
    while queue:
        v,s = queue.pop(0)
        adj = find_adj(n,d,v,c)
        for ele in adj:
            #print(adj)
            u,w = ele
            if s + w < dist[u]:
                dist[u] = s + w
                queue.append((u, dist[u]))
                queue.sort(key = lambda x:x[1])
                if path:    
                    tmp = path[v][:]
                    tmp.append((u,c))
                    path[u] = tmp  
                if ele[0] not in traversed:
                    traversed.append(u)
    if path: return dist,traversed,path
    return dist,traversed
            
            

