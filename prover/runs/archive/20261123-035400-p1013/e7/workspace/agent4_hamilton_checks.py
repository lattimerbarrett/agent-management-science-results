"""Exact multipartite Hamilton-cycle counts, plus sparse-internal contraction."""
from math import factorial,comb
from functools import lru_cache

def mul(a,b):
 c=[0]*(len(a)+len(b)-1)
 for i,x in enumerate(a):
  for j,y in enumerate(b):c[i+j]+=x*y
 return c

def power(a,k):
 c=[1]
 for _ in range(k):c=mul(c,a)
 return c

@lru_cache(None)
def hmp(parts):
 parts=tuple(a for a in parts if a)
 n=sum(parts)
 if n<3:return 0
 p=[1]
 for a in parts:
  q=[0]+[(-1)**(a-j)*comb(a-1,j-1)*(factorial(a)//factorial(j)) for j in range(1,a+1)]
  p=mul(p,q)
 z=sum(factorial(k-1)*v for k,v in enumerate(p) if k)
 assert z%2==0
 return z//2

def triangle_hamilton(m,r=3):
 q=power([1,6,6],m//3)
 return sum(v*hmp(tuple([m-k]+[m]*(r-1))) for k,v in enumerate(q))

def two_matching_hamilton(m,r=3):
 q=power([1,2],m//2)
 return sum(v*w*hmp(tuple([m-j,m-k]+[m]*(r-2))) for j,v in enumerate(q) for k,w in enumerate(q))

if __name__=='__main__':
 import sys
 sys.path.insert(0,'workspace')
 from agent4_cycle_checks import brute_cycles,graph
 # Compare Hamilton count with elementary complete-bipartite formula.
 for m in range(2,12):assert hmp((m,m))==factorial(m)*factorial(m-1)//2
 assert hmp((1,1,1))==1
 assert hmp((1,1,1,1))==3
 for r in [3,4]:
  target=2*r/((r-1)*(r-2))
  print('r=',r,'predicted coefficient',target)
  for m in [6,12,18,24]:
   A=triangle_hamilton(m,r);B=two_matching_hamilton(m,r)
   print('n=',r*m,'n*(ratio-1)=',r*m*(B-A)/A)
