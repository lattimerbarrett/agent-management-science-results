"""Independent exact checks for the diagnostic eight-vertex forbidden graph."""
import networkx as nx
from math import factorial
from fractions import Fraction as F
from agent4_cycle_checks import power,mul,brute_cycles
E=[(0,4),(0,7),(0,8),(1,7),(1,8),(2,7),(2,8),(3,4),(3,5),(4,8),(5,8),(7,8)]
H=nx.Graph(E)
assert len(H)==8
assert nx.is_tree(H.subgraph(set(H)-{8}))
# EVERY possible preimage of the independent complete-bipartite class.
for mask in range(1<<len(H)):
 A=[v for i,v in enumerate(H) if mask>>i&1];B=set(H)-set(A)
 if H.subgraph(B).number_of_edges():continue
 J=H.subgraph(A)
 assert not all(len(C)<=3 and nx.is_tree(J.subgraph(C)) for C in nx.connected_components(J))
# Verify exact three forbidden one-part patterns and two-edge pattern.
assert nx.is_isomorphic(H.subgraph([8,4,5,7]),nx.star_graph(3))
assert H.subgraph([0,1,2,3]).number_of_edges()==0
assert nx.is_isomorphic(H.subgraph([4,7,8,3]),nx.path_graph(4))
assert H.subgraph([0,1,2,5]).number_of_edges()==0
J=H.subgraph([0,7,8,3]).copy();J.remove_nodes_from(list(nx.isolates(J)))
assert nx.is_isomorphic(J,nx.complete_graph(3))
assert H.subgraph([1,2,4,5]).number_of_edges()==0
assert H.subgraph([7,8,3]).number_of_edges()==1
assert H.subgraph([0,4,1,2,5]).number_of_edges()==1

def cycles_P3(m,shift=0):
 assert m%3==0 and shift in (0,1)
 a,b=m+shift,m-shift
 q=power([1,9,7,1],m//3)
 if shift:q=mul(q,[1,1])
 z=F(b*(q[1]-a),2)
 for k in range(2,min(a,b)+1):z+=F(q[k]*(factorial(b)//factorial(b-k))*factorial(k-1),2)
 assert z.denominator==1
 return z.numerator

def certify_gap():
 z=F(7,3);J=12
 S0=sum((z**j/F(factorial(j)**2) for j in range(J+1)),F(0))
 tail0=z**(J+1)/F(factorial(J+1)**2)/(1-z/F((J+2)**2))
 S1=sum((z**(j+2)/F(factorial(j)*factorial(j+2)) for j in range(J+1)),F(0))
 assert S1>S0+tail0
 return S1-S0-tail0

if __name__=='__main__':
 print('All 256 defect partitions checked: P3-union template is H-free.')
 print('Exact defect witnesses verified; H minus vertex8 is a tree.')
 print('Certified positive cycle-limit gap:',certify_gap())
 for m in [6,12,24,30,60,120]:
  a=cycles_P3(m,0);b=cycles_P3(m,1)
  print('n=',2*m,'unbalanced/balanced exact count ratio=',float(F(b,a)),'unbalanced wins:',b>a)
