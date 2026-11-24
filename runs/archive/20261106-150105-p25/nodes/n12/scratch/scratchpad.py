import networkx as nx
from itertools import combinations
m,k=6,2
sets=list(combinations(range(m),k)); Q=nx.Graph(); Q.add_nodes_from(sets)
Q.add_edges_from((u,v) for u,v in combinations(sets,2) if not set(u)&set(v))
G=nx.Graph(); labels={}; layer={}
for u in sets:
    x=('o',u); G.add_node(x); labels[x]=u; layer[x]=0
for e,(u,v) in enumerate(Q.edges()):
    a=('a',e); b=('b',e)
    G.add_edges_from([(('o',u),a),(a,b),(b,('o',v))])
    labels[a]=u; labels[b]=v; layer[a]=1; layer[b]=2
for j in range(3):
    for i in range(m):
        p=('p',j,i); G.add_edge(p,('z',j))
        for x in labels:
            if layer[x]==j and i in labels[x]: G.add_edge(x,p)
tri=sum(nx.triangles(G).values())//3
# A pentagon exists iff an edge xy has an injective length-four alternate path.
five=False
for x,y in G.edges():
    for a in G[x]:
        if a==y:continue
        for b in G[a]:
            if b in (x,y):continue
            for c in G[b]:
                if c not in (x,y,a) and G.has_edge(c,y):five=True
print('Q vertices, edges:',len(Q),Q.number_of_edges())
print('Extension vertices, edges:',len(G),G.number_of_edges())
print('triangles:',tri,'pentagon exists:',five)
print('As t grows, min-degree/order approaches k/(3*(m+k)) =', k/(3*(m+k)))