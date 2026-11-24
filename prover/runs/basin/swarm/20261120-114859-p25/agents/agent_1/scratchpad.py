import itertools as it
import numpy as np
import networkx as nx
from fractions import Fraction
from z3 import Solver, Int, Or, And, sat, unsat

def kneser(m,k):
    sets=list(it.combinations(range(m),k))
    F=nx.Graph(); F.add_nodes_from(range(len(sets)))
    for u,v in it.combinations(F.nodes,2):
        if set(sets[u]).isdisjoint(sets[v]): F.add_edge(u,v)
    return F,[frozenset(s) for s in sets]

def construction(m,k,t=1):
    F,sets=kneser(m,k)
    Q=nx.Graph(); groups={}; labels={}
    for v in F:
        q=('x',v); Q.add_node(q); groups[q]=0; labels[q]=sets[v]
    for u,v in F.edges:
        a=('a',u,v); b=('b',u,v)
        Q.add_edges_from([(('x',u),a),(a,b),(b,('x',v))])
        groups[a]=1; groups[b]=2
        labels[a]=sets[u]; labels[b]=sets[v]
    G=Q.copy()
    for i in range(3):
        R=[('r',i,j,l) for j in range(m) for l in range(t)]
        Z=[('z',i,l) for l in range(k*t)]
        G.add_nodes_from(R+Z)
        G.add_edges_from(it.product(R,Z))
        for v in Q:
            if groups[v]==i:
                G.add_edges_from((v,('r',i,j,l)) for j in labels[v] for l in range(t))
    return F,Q,G,groups,labels

def walk_power3(G):
    nodes=list(G); A=nx.to_numpy_array(G,nodelist=nodes,dtype=np.int64)
    A2=A@A; A3=A2@A
    assert np.trace(A3)==0, 'triangle'
    assert np.sum(A2*A3)==0, 'closed 5-walk'
    P=nx.Graph(); P.add_nodes_from(nodes)
    for i,j in zip(*np.where(np.triu(A3>0,1))): P.add_edge(nodes[i],nodes[j])
    return P

def colorable(F,q):
    vs=list(F); col={v:Int('c'+str(i)) for i,v in enumerate(vs)}
    s=Solver()
    for v in vs:s.add(col[v]>=0,col[v]<q)
    for u,v in F.edges:s.add(col[u]!=col[v])
    return s.check()==sat

def hom_exists(G,H):
    vs=list(G); hs=list(H); hindex={v:i for i,v in enumerate(hs)}
    col={v:Int('f'+str(i)) for i,v in enumerate(vs)}; s=Solver()
    for v in vs:s.add(col[v]>=0,col[v]<len(hs))
    arcs=[(hindex[u],hindex[v]) for u,v in H.edges for u,v in [(u,v),(v,u)]]
    for u,v in G.edges:
        s.add(Or(*[And(col[u]==a,col[v]==b) for a,b in arcs]))
    return s.check()==sat

def universal(q):
    vertices=[(i,mask) for i in range(q) for mask in range(1<<q) if not(mask>>i&1)]
    H=nx.Graph(); H.add_nodes_from(vertices)
    for x,y in it.combinations(vertices,2):
        i,S=x; j,T=y
        if (T>>i&1) and (S>>j&1) and not(S&T): H.add_edge(x,y)
    assert sum(nx.triangles(H).values())==0
    return H

def test_universal_exhaustive():
    # All unlabeled simple graphs through seven vertices are in the atlas.
    count=0
    for G in nx.graph_atlas_g():
        if len(G)==0 or sum(nx.triangles(G).values()):continue
        # Only triangle-freeness is needed for the universal-target reduction.
        vs=list(G); A=nx.to_numpy_array(G,nodelist=vs,dtype=np.int64)
        B=A@A@A
        P=nx.Graph(); P.add_nodes_from(vs)
        for i,j in zip(*np.where(np.triu(B>0,1))):P.add_edge(vs[i],vs[j])
        coloring=nx.coloring.greedy_color(P,strategy='largest_first')
        image={v:(coloring[v],frozenset(coloring[w] for w in G[v])) for v in G}
        for u,v in G.edges:
            i,S=image[u]; j,T=image[v]
            assert i in T and j in S and not S.intersection(T)
        count+=1
    return count

for m,k,t in [(5,2,1),(5,2,4),(6,1,1),(8,2,1)]:
    F,Q,G,groups,labels=construction(m,k,t)
    Pq=walk_power3(Q)
    for u,v in Pq.edges:
        if groups[u]==groups[v]:assert labels[u].isdisjoint(labels[v])
    Pg=walk_power3(G)
    assert len(G)==len(Q)+3*(m+k)*t
    assert min(dict(G.degree()).values())>=k*t
    if len(F)<=28:
        expected=m-2*k+2
        assert colorable(F,expected)
        assert not colorable(F,expected-1)
    print('construction', (m,k,t), '|F|=',len(F),'|G|=',len(G),
          'min degree=',min(dict(G.degree()).values()),'guaranteed ratio=',Fraction(k*t,len(G)),
          'C3/C5 absent, same-class labels checked; Kneser chromatic number checked')
    if (m,k,t)==(6,1,1):
        assert not hom_exists(G,nx.cycle_graph(5))
        print('  Z3 independently confirms: no homomorphism to C5')
for q in range(1,5):
    H=universal(q)
    print('universal target',q,'vertices',len(H),'edges',H.number_of_edges(),'triangle-free checked')
print('universal reduction checked on',test_universal_exhaustive(),'triangle-free atlas graphs')
# Check the numerical gap used by the upper-bound proof, exactly, not in floats.
for c in [Fraction(1,9)+Fraction(1,1000),Fraction(1,8),Fraction(1,5),Fraction(1,2),Fraction(1)]:
    tau=(c-Fraction(1,9))/10
    assert 9*c-15*tau>1
print('exact upper-bound gap checks passed')

from math import comb

def lower_parameters(c,h):
    assert 0<=c<Fraction(1,9) and h>=1
    k=int(3*c*h/(1-9*c))+1
    m=2*k+h
    s=comb(m,k)*(1+comb(m-k,k))
    gap=k-3*c*(m+k)
    assert gap>0
    t=int(c*s/gap)+1
    n=s+3*(m+k)*t
    assert Fraction(k*t,n)>c
    assert m-2*k+2>h
    return m,k,t,n
for c,h in [(Fraction(1,10),5),(Fraction(11,100),5),(Fraction(1,9)-Fraction(1,10000),10)]:
    m,k,t,n=lower_parameters(c,h)
    print('exact lower-parameter check:',str(c),'target order',h,'k',k,
          'digits(n)',len(str(n)),'density inequality verified')

# Exhaustive check of the six-set packing lemma on all simple R with <=4 vertices.
packings=0
for k in range(1,5):
    pairs=list(it.combinations(range(k),2))
    for mask in range(1<<len(pairs)):
        nb=[set() for _ in range(k)]
        for j,(u,v) in enumerate(pairs):
            if mask>>j&1: nb[u].add(v);nb[v].add(u)
        delta=min(map(len,nb))
        if not delta:continue
        sets=[{v for v in range(k) if mask>>v&1} for mask in range(1,1<<k)]
        def N(S): return set().union(*(nb[v] for v in S))
        for I,J,L in it.combinations(sets,3):
            U=I|J|L
            if U & N(U):continue
            neighbors=[N(I),N(J),N(L)]
            if any(A&B for A,B in it.combinations(neighbors,2)):continue
            six=[I,J,L]+neighbors
            assert all(not A&B for A,B in it.combinations(six,2))
            assert sum(map(len,[I,J,L]))+3*delta<=k
            packings+=1
# Non-vacuous equality case: three disjoint two-leaf stars.
R=nx.disjoint_union_all([nx.star_graph(2) for _ in range(3)])
IJK=[{1,2},{4,5},{7,8}]
Ns=[set().union(*(set(R[v]) for v in S)) for S in IJK]
six=IJK+Ns
assert all(not A&B for A,B in it.combinations(six,2))
assert sum(map(len,IJK))+3*min(dict(R.degree()).values())==len(R)==9
print('packing lemma checked exhaustively for |R|<=4; non-vacuous 9-vertex equality case checked')
