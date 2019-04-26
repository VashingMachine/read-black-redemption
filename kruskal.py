from sptree import Set

n_nodes, n_edges = input().split(" ")
nodes = [Set(i + 1) for i in range(int(n_nodes))]
edges = []
for i in range(int(n_edges)):
    v1, v2, d = input().split(" ")
    edges.append((v1, v2, d))

edges.sort(key=lambda x: x[2])
for e in edges:
    ru = nodes[int(e[0]) - 1].find_set()
    rv = nodes[int(e[1]) - 1].find_set()
    if ru != rv:
        print(e)
        Set.union(ru, rv)
