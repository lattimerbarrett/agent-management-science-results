import sys
sys.path.insert(0,'workspace')
from agent3_exact_cycles import mul,forest_paths
import networkx as nx
from math import comb,factorial
from itertools import combinations

def cycle_count(polys,sizes,internal=0):
 trans=[]
 for p in polys:
  q=[0]*len(p);q[0]=1
  for k in range(1,len(p)):
   for l in range(1,k+1):q[l]+=p[k]*(-1)**(k-l)*comb(k-1,l-1)*factorial(k)//factorial(l)
  trans.append(q)
 Q=[1]
 for q in trans:Q=mul(Q,q)
 for q in trans:
  for l in range(1,len(q)):Q[l]-=q[l]
 twice=sum(factorial(k-1)*Q[k] for k in range(2,len(Q)))
 twice-=sum(a*b for a,b in combinations(sizes,2))
 assert twice%2==0
 return twice//2+internal

def branch_poly(m,s,branch):
 p=[1]
 if branch=='P':p=forest_paths(nx.path_graph(2));m-=2
 a,b=divmod(m,s)
 full=forest_paths(nx.star_graph(s-1) if branch=='S' else nx.path_graph(s))
 for _ in range(a):p=mul(p,full)
 if b:p=mul(p,forest_paths(nx.star_graph(b-1) if branch=='S' else nx.path_graph(b)))
 return p

def candidate(n,r,s,m,branch):
 q,z=divmod(n-m,r-1);sizes=[m]+[q+1]*z+[q]*(r-1-z)
 polys=[branch_poly(m,s,branch)]+[[comb(v,k) for k in range(v+1)] for v in sizes[1:]]
 E=m-(branch=='P')-((m-2*(branch=='P')+s-1)//s)
 edges=(n*n-sum(v*v for v in sizes))//2+E
 return edges,cycle_count(polys,sizes,0),(m,branch)

if __name__=='__main__':
 import pathlib
 for r,s,ns in [(3,6,[108,216]),(4,8,[128,256,512,1024]),(5,11,[220,440])]:
  for n in ns:
   rows=[candidate(n,r,s,m,b) for m in range(n//r-2,n//r+4) for b in ['P','S'] if m>=3]
   em=max(x[0] for x in rows);cm=max(x[1] for x in rows)
   er=[x for x in rows if x[0]==em];cr=[x for x in rows if x[1]==cm]
   ec=max(x[1] for x in er)
   p=candidate(n,r,s,n//r+1,'P')[1];st=candidate(n,r,s,n//r,'S')[1]
   print('r,s,n',r,s,n,'edge args',[(x[2],x[0]) for x in er],'cyc args',[(x[2],x[0]) for x in cr],'ratio_gain',float((cm-ec)/ec),'scaled_second',float((p-st)/st*n*n))
