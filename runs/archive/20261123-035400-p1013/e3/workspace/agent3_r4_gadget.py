import sys
sys.path.insert(0,'workspace')
import agent3_branches as A
import networkx as nx
from math import comb
from functools import lru_cache

@lru_cache(None)
def block(L,star=False):
 if not star:return A.forest_paths(nx.path_graph(L))
 p=[comb(L,k) for k in range(L+1)]
 if L>=2:
  for j in range(L-1):p[j+1]+=2*(L-1)*comb(L-2,j)
 if L>=3:
  for j in range(L-2):p[j+1]+=2*comb(L-1,2)*comb(L-3,j)
 return p

def poly(m,s,branch):
 L=2*s if branch=='S' else 2*s-1
 p=block(L,branch=='S');m-=L
 a,b=divmod(m,s)
 for _ in range(a):p=A.mul(p,block(s,branch=='S'))
 if b:p=A.mul(p,block(b,branch=='S'))
 return p

def cand(n,r,s,m,b):
 q,z=divmod(n-m,r-1);sizes=[m]+[q+1]*z+[q]*(r-1-z)
 ps=[poly(m,s,b)]+[[comb(v,k) for k in range(v+1)] for v in sizes[1:]]
 L=2*s if b=='S' else 2*s-1
 E=m-1-((m-L+s-1)//s)
 e=(n*n-sum(v*v for v in sizes))//2+E
 return e,A.cycle_count(ps,sizes),m,b

import pathlib
for n in [128,256,512,1024]:
 r=4;s=8
 rows=[cand(n,r,s,m,b) for m in range(n//r-2,n//r+4) for b in ['P','S']]
 em=max(x[0] for x in rows);cm=max(x[1] for x in rows)
 er=[x for x in rows if x[0]==em];cr=[x for x in rows if x[1]==cm]
 S=cand(n,r,s,n//r,'S')[1];P=cand(n,r,s,n//r+1,'P')[1]
 print(n,'edge args',[(x[2:],x[0]) for x in er],'cycle args',[(x[2:],x[0]) for x in cr], 'n2ratio',float((P-S)/S*n*n))
