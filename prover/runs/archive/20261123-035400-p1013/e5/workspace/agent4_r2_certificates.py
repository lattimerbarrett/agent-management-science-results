from itertools import combinations
import networkx as nx
from fractions import Fraction
# H consists of four fan triangles, with indices 1,2,3 linked by 21 even paths
# in each leaf family. Since all candidate gadgets have <=20 total internal
# edges, linked endpoints must have equal colors. Check every remaining case.
k=4;fan=nx.Graph();fan.add_node(0)
for i in range(k):
    a,b=1+2*i,2+2*i
    fan.add_edges_from([(0,a),(0,b),(a,b)])

def fits_2K3(vertices):
    G=fan.subgraph(vertices)
    comps=[G.subgraph(c) for c in nx.connected_components(G) if len(c)>1]
    return len(comps)<=2 and all(len(C)<=3 and max(dict(C.degree()).values())<=2 for C in comps)
count=0
for code in range(1<<8):
    colors=[0]+[(code>>i)&1 for i in range(8)]
    if len({colors[1+2*i] for i in [1,2,3]})>1:continue
    if len({colors[2+2*i] for i in [1,2,3]})>1:continue
    count+=1
    assert not(all(fits_2K3([i for i,c in enumerate(colors) if c==z]) for z in [0,1])),colors
print('All',count,'connector-compatible leaf colorings exclude split 2K3.')
# Explicit onepart 10-edge competitor, obtained by subdividing an edge of K33.
Q=nx.complete_bipartite_graph(3,3);Q.remove_edge(0,3);Q.add_edges_from([(0,6),(6,3)])
assert Q.number_of_edges()==10
assert max(dict(Q.degree()).values())==3
assert len(nx.max_weight_matching(Q,maxcardinality=True))==3
print('Onepart gadget verified: edges10, maxdegree3, matching3.')
# Coefficientwise Bessel certificate I2(2)<=I0(2)/2.
# Difference at index j: 1/(2*j!^2)-1/(j!*(j+2)!)
# =j*(j+3)/(2*(j+1)*(j+2)*j!^2), nonnegative for all j>=0.
import sympy as s
j=s.symbols('j',integer=True,nonnegative=True)
assert s.cancel(s.Rational(1,2)-1/((j+1)*(j+2))-j*(j+3)/(2*(j+1)*(j+2)))==0
print('Bessel inequality coefficient polynomial:',s.expand(j*(j+3)))
import shutil
shutil.copyfile('scratchpad.py','workspace/agent4_r2_certificates.py')
