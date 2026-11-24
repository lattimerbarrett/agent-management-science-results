import numpy as np
import networkx as nx
from itertools import product
from math import factorial
from agent3_books6 import build_books6

def induced_vectors(p=.52):
 graphs,_,_,_=build_books6()
 assignments=list(product(range(3),repeat=6))
 out_random=[];out_trip=[]
 for g in graphs:
  aut=sum(1 for _ in nx.algorithms.isomorphism.GraphMatcher(g,g).isomorphisms_iter())
  mult=factorial(6)/aut
  m=g.number_of_edges()
  out_random.append(mult*p**m*(1-p)**(15-m))
  total=0.
  for parts in assignments:
   if any(parts[u]==parts[v] for u,v in g.edges()):continue
   cross=sum(parts[u]!=parts[v] for u in range(6) for v in range(u+1,6))
   total+=p**m*(1-p)**(cross-m)
  out_trip.append(mult*total/3**6)
 return np.array(out_random),np.array(out_trip)

if __name__=='__main__':
 graphs,B0,B1,keys=build_books6()
 p=.52
 ran,tri=induced_vectors(p)
 assert abs(ran.sum()-1)<1e-10 and abs(tri.sum()-1)<1e-10
 cap=np.array([(1-p)**2]*120+[p*p]*120)
 assert np.max(np.abs((cap[:,None]*B0-B1)@ran))<1e-12
 cap=np.array([(1+2*(1-p)**2)/3]*120+[p*p/3]*120)
 gap=(cap[:,None]*B0-B1)@tri
 assert np.max(np.abs(gap[120:]))<1e-12
 assert min(gap)>-1e-12
 np.savez('workspace/agent3_extremal_vectors6.npz',random=ran,tripartite=tri,p=p)
 print('Homogeneous and tripartite exact-model densities sum1; all book constraints checked; vectors saved.')
