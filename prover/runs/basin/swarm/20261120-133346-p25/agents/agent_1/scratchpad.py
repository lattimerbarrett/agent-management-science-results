"""Finite checks accompanying the proof. Python 3; requires numpy, networkx, z3, sympy."""
import itertools as it
import numpy as np
import networkx as nx
import z3
from fractions import Fraction


def adjacency(G):
    return nx.to_numpy_array(G, nodelist=list(G), dtype=np.int64)


def no_C3_C5(G):
    # A closed odd walk of length 3 or 5 exists iff an odd cycle of length <=5 exists.
    A = adjacency(G)
    A2 = A @ A
    A3 = A2 @ A
    return np.trace(A3) == 0 and np.trace(A3 @ A2) == 0


def colorable(G, q):
    s = z3.Solver()
    col = {v: z3.Int('v_' + str(i)) for i, v in enumerate(G)}
    s.add(*[z3.And(0 <= col[v], col[v] < q) for v in G])
    s.add(*[col[u] != col[v] for u, v in G.edges()])
    return s.check() == z3.sat


def lower_example(N, k, t):
    sets = list(it.combinations(range(N), k))
    labels = [frozenset(s) for s in sets]
    F = nx.Graph()
    F.add_nodes_from(range(len(sets)))
    F.add_edges_from((i,j) for i in F for j in F if i<j and labels[i].isdisjoint(labels[j]))
    C = nx.Graph()
    typ, lab = {}, {}
    for i in F:
        v = ('o', i)
        C.add_node(v); typ[v]=0; lab[v]=labels[i]
    for e,(i,j) in enumerate(F.edges()):
        a,b = ('a',e),('b',e)
        C.add_edges_from([(('o',i),a),(a,b),(b,('o',j))])
        typ[a]=1; lab[a]=labels[i]
        typ[b]=2; lab[b]=labels[j]
    order=list(C)
    A=adjacency(C); A3=A@A@A
    for i,u in enumerate(order):
        for j,v in enumerate(order):
            if typ[u]==typ[v] and A3[i,j]>0:
                assert lab[u].isdisjoint(lab[v])
    G=C.copy()
    for i in range(3):
        aa=[('A',i,r,s) for r in range(N) for s in range(t)]
        bb=[('B',i,r,s) for r in range(k) for s in range(t)]
        G.add_nodes_from(aa+bb)
        G.add_edges_from(it.product(aa,bb))
        for v in C:
            if typ[v]==i:
                G.add_edges_from((v,('A',i,r,s)) for r in lab[v] for s in range(t))
    assert no_C3_C5(C)
    assert no_C3_C5(G)
    assert min(dict(G.degree()).values()) >= k*t
    assert len(G)==len(C)+3*(N+k)*t
    return F,C,G


def exhaustive_local_check():
    total=0
    # graph_atlas contains every unlabeled graph on at most seven vertices.
    for G in nx.graph_atlas_g():
        if len(G)==0 or not no_C3_C5(G):
            continue
        A=adjacency(G); A3=A@A@A
        # Endpoints of any 3-walk have disjoint neighborhoods.
        assert not np.any((A3>0)&((A@A)>0))
        # Every set of vertices with > half of a fixed set as neighbors is 2-wide.
        vertices=list(G)
        for mask in range(1,1<<len(G)):
            S=[j for j in range(len(G)) if (mask>>j)&1]
            D=[i for i in range(len(G)) if 2*int(A[i,S].sum())>len(S)]
            if D:
                assert not np.any(A3[np.ix_(D,D)])
        total+=1
    print('All local/wide-class claims checked on',total,'unlabeled C3,C5-free graphs of order <=7.')


def packing_check():
    # Membership in three supports and their three reduced neighborhoods.
    # Verify that the abstract conditions used in the proof permit at most
    # one membership for every point, without any assumptions on graph size.
    s=z3.Solver()
    bits=[z3.Bool('set_'+str(i)) for i in range(6)]
    # supports 0,1,2; neighborhoods 3,4,5
    for i,j in it.combinations(range(3),2):
        s.add(z3.Not(z3.And(bits[i],bits[j])))
        s.add(z3.Not(z3.And(bits[i+3],bits[j+3])))
    for i in range(3):
        for j in range(3):
            s.add(z3.Not(z3.And(bits[i],bits[j+3])))
    s.add(z3.Sum([z3.If(b,1,0) for b in bits])>=2)
    assert s.check()==z3.unsat
    # Explicit safe upper-bound parameters for any c>1/9:
    # g=c-1/9; d=g; epsilon=g/100. Then 9c-3d-24eps > 1.
    import sympy as sp
    g=sp.Symbol('g',positive=True)
    excess=sp.expand(9*(sp.Rational(1,9)+g)-3*g-24*g/100-1)
    assert excess==sp.Rational(144,25)*g
    print('Packing checked by SAT; upper-bound slack =',excess)


if __name__=='__main__':
    exhaustive_local_check()
    packing_check()
    for N,k,t in [(5,2,1),(6,2,1),(6,2,2)]:
        F,C,G=lower_example(N,k,t)
        q=N-2*k+2
        assert colorable(F,q) and not colorable(F,q-1)
        print('KG(%d,%d), reservoir multiplier %d: chi=%d, core=%d, total=%d, min_degree=%d, ratio=%s; no C3,C5 verified.' %
              (N,k,t,q,len(C),len(G),min(dict(G.degree()).values()),Fraction(min(dict(G.degree()).values()),len(G))))
    # Exact arithmetic for large, implicit lower-bound examples, very near 1/9.
    from math import comb
    for c,h in [(Fraction(1,10),3),(Fraction(11,100),4),(Fraction(111,1000),10)]:
        b=3*c*h/(1-9*c)
        k=b.numerator//b.denominator+1
        N=2*k+h
        core=comb(N,k)*(1+comb(N-k,k))
        gap=k-3*c*(N+k)
        assert gap>0
        b=c*core/gap
        t=b.numerator//b.denominator+1
        n=core+3*(N+k)*t
        assert Fraction(k*t,n)>c
        assert N-2*k+2>h
        print('Exact implicit lower example checked: c=%s, |H|=%d, k=%d, n has %d bits.' % (c,h,k,n.bit_length()))
    print('All finite tests passed. General regularity and Kneser theorems are used as theorems, not inferred from tests.')
