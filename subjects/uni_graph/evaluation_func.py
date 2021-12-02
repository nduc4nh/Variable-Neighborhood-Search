#given indices of vertices n, distance matrix d--> find adjencent vertices of x
def find_adj(n,d,x,color):
    re = []
    for i in range(1,len(n)+1):
        weight = d[color][x][i]
        if weight != 0 and weight != float("inf"):
            re.append((i, weight))
    return re 

#given indices of vertices n, distance matrix d--> find shorstest distance from start to vertices having color "c" in-edge
def get_next(n,d,cur_v,cur_dist,c):
    queue = []
    dist = {}
    traversed = []
    
    for ele in n:
        dist[ele] = float("inf")
    for ele in cur_v:
        dist[ele] = cur_dist[ele]
        queue.append([ele, dist[ele]])
    queue.sort(key = lambda x: x[1])
    
    while queue:
        x,s = queue.pop(0)
        adj = find_adj(n,d,x,c)
        for ele in adj:
            #print(adj)
            if s + ele[1] < dist[ele[0]]:
                dist[ele[0]] = s + ele[1]
                queue.append((ele[0], dist[ele[0]]))
                queue.sort(key = lambda x:x[1])
                if ele[0] not in traversed:
                    traversed.append(ele[0])
    return dist,traversed
            
            

