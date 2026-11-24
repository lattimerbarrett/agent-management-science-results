from fractions import Fraction as F
from math import factorial
from itertools import product
import networkx as nx
V=(0,1,2,3,4,5,7,8)
E=((0,4),(0,7),(0,8),(1,7),(1,8),(2,7),(2,8),(3,4),(3,5),(4,8),(5,8),(7,8))
H=nx.Graph();H.add_nodes_from(V);H.add_edges_from(E)
assert len(H)==8 and len(H.edges())==12
assert nx.is_tree(H.subgraph(set(V)-{8}))
assert all(H.has_edge(u,v) for u,v in ((0,7),(0,8),(7,8)))
def p3union(g):
    return all(len(c)<=3 and g.subgraph(c).number_of_edges()==len(c)-1
               for c in nx.connected_components(g))
for bits in product(range(2), repeat=8):
    a={v for v,c in zip(V,bits) if c==0};b=set(V)-a
    assert H.subgraph(b).number_of_edges() or not p3union(H.subgraph(a))
# Verify every cross/internal edge in the four explicit witness colorings.
for a,expected in [({4,5,7,8},3),({3,4,7,8},3),({0,3,7,8},3)]:
    b=set(V)-a
    assert H.subgraph(b).number_of_edges()==0
    assert H.subgraph(a).number_of_edges()==expected
for a in ({3,7,8},):
    assert H.subgraph(a).number_of_edges()==1
    assert H.subgraph(set(V)-a).number_of_edges()==1

def mul(a,b):
    c=[0]*(len(a)+len(b)-1)
    for i,x in enumerate(a):
        for j,y in enumerate(b):c[i+j]+=x*y
    return c

def cycles(k, unbalanced=False):
    m=3*k; a=m+int(unbalanced);b=m-int(unbalanced)
    q=[1]
    for _ in range(k):q=mul(q,[1,9,7,1])
    if unbalanced:q=mul(q,[1,1])
    twice=b*(q[1]-a)
    for j in range(2,min(a,b)+1):
        twice+=q[j]*(factorial(b)//factorial(b-j))*factorial(j-1)
    assert twice%2==0
    return twice//2

def graph(k,unbalanced=False):
    m=3*k;a=m+int(unbalanced);b=m-int(unbalanced)
    g=nx.complete_bipartite_graph(a,b)
    for j in range(k):g.add_edges_from(((3*j,3*j+1),(3*j+1,3*j+2)))
    return g

def dfs_cycles(g):
    total=0
    def visit(start,path,used):
        nonlocal total
        for w in g[path[-1]]:
            if w==start and len(path)>=3:total+=1
            elif w>start and w not in used:
                visit(start,path+[w],used|{w})
    for s in g:visit(s,[s],{s})
    assert total%2==0
    return total//2
for k in (1,2):
    for flag in (False,True):
        assert dfs_cycles(graph(k,flag))==cycles(k,flag)
for k in (2,):
    for flag in (False,True):
        assert not nx.algorithms.isomorphism.GraphMatcher(graph(k,flag),H).subgraph_is_monomorphic()
for k in (8,10,20):
    x,y=cycles(k),cycles(k,True)
    assert y>x
    print('n=',6*k,'exact cycle ratio=',F(y,x))
z=F(7,3)
lower=z*z/2+z**3/6+z**4/48
upper=1+z+z*z/4+(z**3/36)/(1-z/16)
assert lower-upper==F(55709,159408)>0
print('Certified limiting gap >',lower-upper)
print('All finite checks passed.')
