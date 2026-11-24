import itertools as it
import numpy as np
import networkx as nx
from z3 import Solver, Int, Distinct, And, sat, unsat

def kneser(m,k):
    sets=list(it.combinations(range(m),k)); masks=[sum(1<<x for x in s) for s in sets]
    F=nx.Graph(); F.add_nodes_from(range(len(sets)))
    F.add_edges_from((i,j) for i in range(len(sets)) for j in range(i) if not masks[i]&masks[j])
    return F,masks

def construction(m,k,t):
    F,labels=kneser(m,k)
    G=nx.Graph(); G.add_nodes_from(range(len(F)))
    colors={v:0 for v in F}; lab=dict(enumerate(labels)); nxt=len(F)
    for u,v in F.edges():
        a,b=nxt,nxt+1; nxt+=2
        G.add_edges_from([(u,a),(a,b),(b,v)])
        colors[a]=1; colors[b]=2; lab[a]=labels[u]; lab[b]=labels[v]
    core=G.copy()
    for i in range(3):
        U={a:list(range(nxt+a*t,nxt+(a+1)*t)) for a in range(m)}
        nxt+=m*t
        W=list(range(nxt,nxt+k*t)); nxt+=k*t
        G.add_nodes_from(W)
        for a in range(m):
            G.add_nodes_from(U[a]); G.add_edges_from(it.product(U[a],W))
        for v in core:
            if colors[v]==i:
                for a in range(m):
                    if (lab[v]>>a)&1: G.add_edges_from((v,x) for x in U[a])
    return F,core,G,colors,lab

def chromatic(F):
    vs=list(F); x={v:Int('x'+str(v)) for v in vs}
    for q in range(1,len(F)+1):
        s=Solver(); s.add([And(x[v]>=0,x[v]<q) for v in vs]); s.add([x[u]!=x[v] for u,v in F.edges()])
        if s.check()==sat: return q

for m,k,t in [(5,2,1),(6,2,2),(7,2,1),(8,3,1)]:
    F,C,G,col,lab=construction(m,k,t)
    A=nx.to_numpy_array(G,nodelist=list(G),dtype=np.int64); A2=A@A; A3=A2@A
    assert np.trace(A3)==0 and np.trace(A2@A3)==0
    D=nx.to_numpy_array(C,nodelist=list(C),dtype=np.int64); D3=D@D@D
    for u in C:
        for v in C:
            if col[u]==col[v] and D3[u,v]: assert lab[u]&lab[v]==0
    assert len(G)==len(F)+2*F.number_of_edges()+3*(m+k)*t
    assert min(dict(G.degree()).values())>=k*t
    chi=chromatic(F)
    assert chi==m-2*k+2
    print('lower check:',(m,k,t),'core',len(C),'n',len(G),'delta',min(dict(G.degree()).values()),'chi(F)',chi,'traces',int(np.trace(A3)),int(np.trace(A2@A3)))

# Small-label part of the Tucker labeling: order preservation never gives opposite labels.
for m in range(1,8):
    count=0
    for y in it.product((-1,0,1),repeat=m):
        supp=[i for i in range(m) if y[i]]
        if not supp: continue
        def lowlabel(z):
            seq=[s for s in z if s]
            alt=1+sum(a!=b for a,b in zip(seq,seq[1:]))
            return seq[0]*alt
        ly=lowlabel(y)
        for bits in range(1,1<<len(supp)):
            x=[0]*m
            for j,a in enumerate(supp):
                if bits>>j&1: x[a]=y[a]
            assert lowlabel(x)!=-ly
            count+=1
    print('Tucker comparable pairs checked:',m,count)

# Exhaustive set-counting lemma on all unlabeled graphs of at most six vertices.
cases=0
for R in nx.graph_atlas_g():
    n=len(R)
    if not 1<=n<=6 or min(dict(R.degree()).values())==0: continue
    N=[sum(1<<w for w in R[v]) for v in range(n)]
    supports=[]
    for a in range(1,1<<n):
        b=0
        for v in range(n):
            if a>>v&1: b|=N[v]
        if not a&b: supports.append((a,b))
    for triple in it.combinations(supports,3):
        aa=[p[0] for p in triple]; bb=[p[1] for p in triple]
        if any(bb[i]&bb[j] for i in range(3) for j in range(i)): continue
        if any(aa[i]&bb[j] for i in range(3) for j in range(3)): continue
        six=aa+bb
        assert all(not six[i]&six[j] for i in range(6) for j in range(i))
        assert sum(s.bit_count() for s in six)<=n
        cases+=1
print('upper counting configurations checked:',cases)
R=nx.disjoint_union_all([nx.star_graph(2) for _ in range(3)])
AA=[{1,2},{4,5},{7,8}]; BB=[set().union(*(set(R[a]) for a in s)) for s in AA]
assert [len(s) for s in AA+BB]==[2,2,2,1,1,1]
assert len(set.union(*(AA+BB)))==9
print('9-part equality certificate checked')

from fractions import Fraction
from math import comb

def ceil_fraction(x):
    return -((-x.numerator)//x.denominator)

def obstruction_parameters(c,q):
    c=Fraction(c); q=max(1,q)
    assert 0<=c<Fraction(1,9)
    x=3*c*q/(1-9*c)
    k=x.numerator//x.denominator+1
    m=2*k+q
    core=comb(m,k)*(1+comb(m-k,k))
    gap=k-3*c*(m+k)
    assert gap>0
    t=max(1,ceil_fraction(c*core/gap))
    n=core+3*(m+k)*t
    assert k*t>=c*n and m-2*k+2>q
    return m,k,t,n

for c in [Fraction(0),Fraction(1,100),Fraction(1,10),Fraction(11,100),Fraction(111,1000)]:
    for q in range(1,8): obstruction_parameters(c,q)
print('35 exact rational obstruction-parameter checks passed')

import sympy as sp
c=sp.symbols('c',real=True)
eta=(9*c-1)/30
assert sp.expand(9*c-15*eta-1)==(9*c-1)/2
assert sp.simplify(c-2*eta-(6*c+1)/15)==0
print('upper-bound slack identities checked symbolically')
