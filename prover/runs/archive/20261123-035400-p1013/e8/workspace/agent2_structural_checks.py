"""Finite checks for agent 2's bounded-component lemma.
The mathematical lemma is independent of H: greedily removing disjoint trees
on d+1 vertices leaves components of size at most d; bounded degree bounds
the total size of original components touched by the removal.
"""
import networkx as nx

def extract(G,d):
    R=G.copy(); X=set(); packing=[]
    while True:
        C=next((c for c in nx.connected_components(R) if len(c)>d),None)
        if C is None: break
        root=next(iter(C)); chosen={root}; queue=[root]
        while len(chosen)<d+1:
            v=queue.pop(0)
            for w in R[v]:
                if w not in chosen:
                    chosen.add(w);queue.append(w)
                    if len(chosen)==d+1: break
        T=nx.minimum_spanning_tree(R.subgraph(chosen))
        assert len(T)==d+1 and nx.is_tree(T)
        packing.append((chosen.copy(),T.copy()))
        X.update(chosen);R.remove_nodes_from(chosen)
    return X,R,packing

def check():
    tested=0
    for G in nx.graph_atlas_g():
        for d in range(1,6):
            X,R,packing=extract(G,d)
            assert all(len(c)<=d for c in nx.connected_components(R))
            D=max(dict(G.degree()).values(),default=0)
            large=sum(len(c) for c in nx.connected_components(G) if len(c)>d)
            assert large<=len(X)*(1+D*d)
            # Isomorphism-group packing witnesses are all disjoint.
            assert sum(len(S) for S,T in packing)==len(X)
            for S,T in packing:
                assert len(S)==d+1 and set(T)==S
            tested+=1
    return tested
if __name__=='__main__':
    print('verified graph/component instances:',check())


def check_shape_bounds():
    from fractions import Fraction as Q
    checked=0
    for k in range(2,12):
        trees=list(nx.nonisomorphic_trees(k))
        for T in trees:
            W=sum(d*(d-1)//2 for _,d in T.degree())
            assert k-2 <= W <= (k-1)*(k-2)//2
            checked+=1
    for G in nx.graph_atlas_g():
        if len(G) and nx.is_forest(G):
            k=max(map(len,nx.connected_components(G)))
            W=sum(d*(d-1)//2 for _,d in G.degree())
            assert W>=max(0,2*G.number_of_edges()-len(G))
            if k>=2:
                assert W<=Q((k-2)*G.number_of_edges(),2)
            else: assert W==0
    return checked

def check_threshold_algebra():
    import sympy as s
    r,k=s.symbols('r k', positive=True)
    gap=-1+2*(k-1)/(k*(r-1))+(r-2)*(k-2)*(k-3)/(2*k*(r-1)**2)
    assert s.cancel(gap.subs(k,2*r)+(r-4)/(2*r*(r-1)))==0
    assert s.cancel(gap.subs(k,2*r+1)-3/((r-1)*(2*r+1)))==0
    assert gap.subs({r:3,k:5})==-s.Rational(1,20)
    assert gap.subs({r:3,k:6})==s.Rational(1,12)
    assert gap.subs({r:4,k:7})==-s.Rational(1,9)
    assert gap.subs({r:4,k:8})==0
    return True

if __name__=='__main__':
    print('unlabeled tree shape inequalities checked:',check_shape_bounds())
    print('threshold rational identities:',check_threshold_algebra())
