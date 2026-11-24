# Independent exact check of shift-reservoir counterconstruction, m=4.
from itertools import combinations
import networkx as nx
m=4
Y=list(combinations(range(m),2)); q=len(Y)
E=[(u,v) for u in Y for v in Y if u[1]==v[0]]
F=nx.Graph(); palette={}; col={}
for u in Y:
    F.add_node(('v',u)); col['v',u]=0
    palette['v',u]=(u[0],u[1])
idx={u:i for i,u in enumerate(Y)}
for j,(u,v) in enumerate(E):
    a=('a',j); b=('b',j)
    F.add_edges_from([(('v',u),a),(a,b),(b,('v',v))])
    col[a]=1;col[b]=2
    palette[a]=palette[b]=(idx[u],idx[v])
D=max(2**(q-2),len(F))
# q=6, D=16; each palette ground has q bits, including branch's m bits.
assert D==2**(q-2)
G=F.copy()
for i in range(3):
    aa=[('A',i,j) for j in range(D)]
    bb=[('B',i,j) for j in range(4*D)]
    G.add_edges_from((a,b) for a in aa for b in bb)
    for v in F:
        if col[v]!=i:continue
        tail,head=palette[v]
        for mask in range(4*D):
            if (mask>>tail)&1 and not (mask>>head)&1:
                G.add_edge(v,('B',i,mask))
assert len(G)==15*D+len(F)
assert min(dict(G.degree()).values())>=D
assert 16*min(dict(G.degree()).values())>=len(G)
# N^2(u)∩N^2(v)=empty for each edge uv iff no closed walk5.
N={v:set(G[v]) for v in G}
N2={v:set().union(*(N[w] for w in N[v])) for v in G}
for u,v in G.edges:
    assert not N[u]&N[v], ('triangle',u,v)
    assert not N2[u]&N2[v], ('closed5',u,v)
for u,v in E:
    assert nx.shortest_path_length(F,('v',u),('v',v))==3
print('m=',m,'Y vertices=',len(Y),'Y edges=',len(E),'F vertices=',len(F))
print('G vertices=',len(G),'G edges=',G.number_of_edges(),'minimum degree=',min(dict(G.degree()).values()))
print('Verified no C3 and no C5 by all edge endpoint neighborhood / 2-walk-neighborhood intersections.')
open('workspace/agent3_shift_check.py','w').write(open('scratchpad.py').read())
