"""Exact 52-pattern cap patch certificate (source 0, sinks 2 and 4)."""
from itertools import combinations
import networkx as nx
import sympy as sp

def verify_patch():
    vals=[]
    for xy in (False, True):
        for A in combinations([1,2,3,4],3-int(xy)):
            for B in combinations([1,2,3,4],3-int(xy)):
                G=nx.Graph([(0,1),(1,2),(0,3),(3,4),(0,5),(0,6)])
                G.add_edges_from((5,a) for a in A)
                G.add_edges_from((6,b) for b in B)
                if xy: G.add_edge(5,6)
                assert G.degree(5)==G.degree(6)==4
                # Ground vertex 6. Demand vector sums to zero after extension.
                L=sp.Matrix([[G.degree(v) if v==w else -int(G.has_edge(v,w))
                              for w in range(6)] for v in range(6)])
                b=sp.Matrix([1,0,-sp.Rational(1,2),0,-sp.Rational(1,2),0])
                energy=(b.T*L.inv()*b)[0]
                assert energy<=sp.Rational(4,5)
                vals.append(energy)
    assert len(vals)==52 and max(vals)==sp.Rational(4,5)
    return sorted(set(vals))
if __name__=='__main__':
    print(verify_patch())
