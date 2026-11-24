import itertools,json
import numpy as np
import networkx as nx

def test(k,seed=71):
    rng=np.random.default_rng(seed)
    sets=list(itertools.combinations(range(3*k),k)); m=len(sets)
    edges=[(u,v) for u in range(m) for v in range(u+1,m) if not set(sets[u])&set(sets[v])]
    cuts=rng.integers(0,2,(128,m),dtype=np.int8)
    crosses={(u,v):list(np.flatnonzero((cuts[:,u]==0)&(cuts[:,v]==1))) for u,v in edges}
    d=min(map(len,crosses.values())); d-=d%k
    assert d>0
    G=nx.Graph(); assign={};palette=[list(range(3*k)),list(range(128)),list(range(128))]
    for u,S in enumerate(sets):
        G.add_node(('v',u));assign[('v',u)]=(0,list(S)*(d//k))
    for j,(u,v) in enumerate(edges):
        a=('a',j); b=('b',j)
        G.add_edges_from([(('v',u),a),(a,b),(b,('v',v))])
        assign[a]=(1,crosses[u,v][:d]);assign[b]=(2,crosses[u,v][:d])
    # For branch palette repeat individual B vertices d/k times.
    B={0:{i:[('B',0,i,j) for j in range(d//k)] for i in palette[0]},1:{i:[('B',1,i,0)] for i in palette[1]},2:{i:[('B',2,i,0)] for i in palette[2]}}
    for i in range(3):
        As=[('A',i,j) for j in range(d)]
        Bs=[x for L in B[i].values() for x in L]
        G.add_edges_from(itertools.product(As,Bs))
    for v,(i,S) in assign.items():
        for s in set(S): G.add_edges_from((v,b) for b in B[i][s])
    nodes=list(G); index={v:i for i,v in enumerate(nodes)}
    A=nx.to_numpy_array(G,nodelist=nodes,dtype=np.int32)
    A2=A@A
    # A closed walk of length 3 or 5 exists iff endpoints of some G edge have a shared length-2 target (5) or shared neighbor (3).
    assert np.trace(A@A2)==0
    bad=[]
    for u,v in G.edges():
        if np.any((A2[index[u]]>0)&(A2[index[v]]>0)):bad.append((u,v))
    assert not bad,bad[:1]
    # Every Y edge is length3 between branch vertices, retained in G.
    for j,(u,v) in enumerate(edges):assert G.has_edge(('v',u),('a',j)) and G.has_edge(('a',j),('b',j)) and G.has_edge(('b',j),('v',v))
    return {'k':k,'Y_vertices':m,'Y_edges':len(edges),'G_vertices':len(G),'G_edges':G.number_of_edges(),'min_degree':min(dict(G.degree()).values()),'D':d,'C3':False,'C5':False}

if __name__=='__main__':
    print(json.dumps([test(1),test(2)],indent=2))
