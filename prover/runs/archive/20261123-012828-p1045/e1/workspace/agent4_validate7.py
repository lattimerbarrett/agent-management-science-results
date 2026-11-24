import sys,numpy as np, networkx as nx
from itertools import combinations,product
from math import factorial
sys.path.insert(0,'workspace')
from agent4_books7 import build
B0,B1,pats=build();graphs=[g for g in nx.graph_atlas_g() if len(g)==7];edges=list(combinations(range(7),2));parts=np.array(list(product(range(3),repeat=7)))
within=np.zeros(len(parts),dtype=np.int64);cross=np.zeros(len(parts),dtype=np.int64)
for j,(u,v) in enumerate(edges):
 same=(parts[:,u]==parts[:,v]);within|=same.astype(np.int64)<<j;cross+=~same
p=.52;ran=[];tri=[]
for gi,g in enumerate(graphs):
 aut=sum(1 for _ in nx.algorithms.isomorphism.GraphMatcher(g,g).isomorphisms_iter());mult=factorial(7)/aut;m=g.number_of_edges();mask=sum(1<<j for j,e in enumerate(edges) if g.has_edge(*e))
 ran.append(mult*p**m*(1-p)**(21-m));tri.append(mult*p**m*np.sum((1-p)**(cross[(within&mask)==0]-m))/3**7)
ran=np.array(ran);tri=np.array(tri)
assert abs(sum(ran)-1)<1e-10 and abs(sum(tri)-1)<1e-10
m=len(pats);c=np.array([(1-p)**2]*m+[p*p]*m)
assert max(abs((c[:,None]*B0-B1)@ran))<1e-12
c=np.array([(1+2*(1-p)**2)/3]*m+[p*p/3]*m);g=(c[:,None]*B0-B1)@tri
assert min(g)>-1e-12 and max(abs(g[m:]))<1e-12
np.savez('workspace/agent4_extremal_vectors7.npz',random=ran,tripartite=tri,p=p)
print('All1992bookconstraints validated on homogeneous and tripartite exactmodel densities.')
