"""Exact certificates for all odd-n extremal lower bounds.
Run with Python; dependencies networkx,sympy. All computations rational.
"""
import networkx as nx
import sympy as S
CAPS={
6:[(0,1),(0,2),(1,3),(1,4),(1,5),(2,3),(2,4),(2,5),(3,4),(3,5),(4,5)],
7:[(0,1),(0,2),(0,4),(0,6),(1,2),(2,3),(2,5),(3,4),(3,5),(3,6),(4,5),(4,6),(5,6)],
9:[[0, 4], [0, 5], [1, 7], [1, 3], [1, 2], [1, 6], [2, 7], [2, 6], [2, 8], [3, 5], [3, 4], [3, 7], [4, 5], [4, 8], [5, 8], [6, 8], [6, 7]],
10:[[0, 4], [0, 7], [1, 6], [1, 9], [1, 7], [1, 4], [2, 9], [2, 3], [2, 5], [2, 8], [3, 9], [3, 5], [3, 8], [4, 7], [4, 6], [5, 8], [5, 9], [6, 8], [6, 7]]}
# cap7's unique degree-two vertex is 1; normalize to 0.
CAPS[7]=[(1 if a==0 else 0 if a==1 else a,1 if b==0 else 0 if b==1 else b) for a,b in CAPS[7]]
BULKS={6:[(0,2),(0,3),(1,4),(1,5)]+list(__import__('itertools').combinations(range(2,6),2)),8:[[0, 5], [0, 3], [1, 6], [1, 4], [2, 3], [2, 6], [2, 4], [2, 5], [3, 5], [3, 7], [4, 6], [4, 7], [5, 7], [6, 7]]}
EXPECTED_CAP={6:S.Rational(4,5),7:S.Rational(104,115),9:S.Rational(52,45),10:S.Rational(31,20)}
EXPECTED_BULK={6:S.Rational(5,4),8:S.Rational(3,2)}
def resistance_matrix(G):
    vertices=list(G); L=S.Matrix(nx.laplacian_matrix(G,nodelist=vertices).toarray())
    Z=L[:-1,:-1].inv(); Z=Z.row_insert(len(vertices)-1,S.zeros(1,len(vertices)-1)); Z=Z.col_insert(len(vertices)-1,S.zeros(len(vertices),1))
    return {(u,v):Z[i,i]+Z[j,j]-2*Z[i,j] for i,u in enumerate(vertices) for j,v in enumerate(vertices)}
def module_graph(edges):
    return nx.Graph(edges)
def check_modules():
    for n,e in CAPS.items():
        G=module_graph(e); assert len(G)==n and nx.is_connected(G)
        assert dict(G.degree())[0]==2 and all(G.degree(v)==4 for v in G if v!=0)
        R=resistance_matrix(G); ecc=max(R[0,v] for v in G)
        assert ecc==EXPECTED_CAP[n],(n,ecc)
        assert max(R.values())==ecc
        print('cap',n,'root eccentricity',ecc,'diameter',max(R.values()))
    for n,e in BULKS.items():
        G=module_graph(e); assert len(G)==n and nx.is_connected(G)
        assert all(G.degree(v)==(2 if v in [0,1] else 4) for v in G)
        R=resistance_matrix(G); assert R[0,1]==EXPECTED_BULK[n]
        assert max(R.values())==R[0,1]
        print('bulk',n,'terminal resistance',R[0,1],'diameter',max(R.values()))
def construct(n):
    assert n>=15 and n%2==1
    r=n%5
    # join modules by identifying degree-two ports; all resulting degrees four.
    if r==0: cap_sizes=[6,10]; mids=[]
    elif r==1:cap_sizes=[6,6]; mids=[]
    elif r==2:cap_sizes=[6,7]; mids=[]
    elif r==3:cap_sizes=[6,6]; mids=[8]
    else:cap_sizes=[6,9]; mids=[]
    base=sum(cap_sizes)-1+sum(b-1 for b in mids)
    assert (n-base)%5==0 and n>=base
    mids += [6]*((n-base)//5)
    G=module_graph(CAPS[cap_sizes[0]]); current=0
    R=resistance_matrix(G); first=max(G,key=lambda v:R[0,v])
    for b in mids:
        H=module_graph(BULKS[b]); labels={0:current}; labels.update({v:len(G)+i for i,v in enumerate(v for v in sorted(H) if v!=0)})
        G.add_edges_from((labels[a],labels[b]) for a,b in H.edges());current=labels[1]
    H=module_graph(CAPS[cap_sizes[1]]); R=resistance_matrix(H); last=max(H,key=lambda v:R[0,v]);labels={0:current}; labels.update({v:len(G)+i for i,v in enumerate(v for v in sorted(H) if v!=0)})
    G.add_edges_from((labels[a],labels[b]) for a,b in H.edges());last=labels[last]
    assert len(G)==n and nx.is_connected(G) and all(G.degree(v)==4 for v in G)
    return G,first,last

def predicted(n):
    c={0:S.Rational(28,5),1:S.Rational(23,5),2:S.Rational(596,115),3:S.Rational(28,5),4:S.Rational(278,45)}[n%5]
    return n*n-c*n
if __name__=='__main__':
    check_modules()
    for n in range(15,66,2):
        G,a,b=construct(n);R=resistance_matrix(G)
        assert 4*n*R[a,b]==predicted(n),(n,R[a,b],predicted(n))
        assert max(R.values())==R[a,b]
        print(n,'commute diameter',4*n*R[a,b])
