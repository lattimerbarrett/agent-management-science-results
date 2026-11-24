import networkx as nx
from itertools import combinations
# Q=KG(5,2); replace each edge by a path of length 3.
m,k=5,2
sets=list(combinations(range(m),k))
G=nx.Graph(); label={}; typ={}
for i,S in enumerate(sets):
    G.add_node(('v',i));label[('v',i)]=S;typ[('v',i)]=0
for i,j in combinations(range(len(sets)),2):
    if set(sets[i]).isdisjoint(sets[j]):
        a=('a',i,j);b=('b',i,j)
        G.add_edges_from([(('v',i),a),(a,b),(b,('v',j))])
        label[a]=sets[i];typ[a]=1
        label[b]=sets[j];typ[b]=2
for v in list(label):
    for i in label[v]: G.add_edge(v,('aux',typ[v],i))
for t in range(3):
    for i in range(m): G.add_edge(('aux',t,i),('booster',t))
# A 5-cycle exists iff an edge has a simple alternate path of length 4.
def cycle_exists(length):
    nodes=list(G);rank={v:i for i,v in enumerate(nodes)}
    def search(path):
        if len(path)==length:return G.has_edge(path[-1],path[0])
        return any(search(path+[w]) for w in G[path[-1]] if rank[w]>rank[path[0]] and w not in path)
    return any(search([v]) for v in nodes)
F=G.subgraph(label).copy()
bad=[]
for u in F:
    reach={u}
    for _ in range(5): reach={w for v in reach for w in F[v]}
    for v in reach:
        if typ[u]==typ[v] and not set(label[u]).isdisjoint(label[v]): bad.append((u,v))
print('Length-three walks violating same-type disjointness:',len(bad))
print('Vertices:',len(G),'edges:',G.number_of_edges())
print('Triangle:',cycle_exists(3),'Pentagon:',cycle_exists(5),'7-cycle:',cycle_exists(7))
print('In general, auxiliary classes of total size 3*m*T and boosters of total size 3*k*T give minimum degree at least k*T, while the subdivided graph is fixed.')
print('As m/k tends to 2, the minimum-degree proportion tends to 1/9.')
