import sys
sys.path.insert(0,'workspace')
from agent3_branches import cycle_count,mul
from math import comb

def power(p,k):
 q=[1]
 for _ in range(k):q=mul(q,p)
 return q

def star(L):
 p=[comb(L,k) for k in range(L+1)]
 for j in range(L-1):p[j+1]+=2*(L-1)*comb(L-2,j)
 for j in range(L-2):p[j+1]+=2*comb(L-1,2)*comb(L-3,j)
 return p
from pathlib import Path
for f in [1,2,3,4]:
 for k in [40,80,160]:
  m=2*k+1;n=2*m;L=4*f+1
  S=mul(star(L),power([1,4,1],(m-L)//2))
  T=mul([1,1],power([1,4,1],k))
  ind=[comb(m,j) for j in range(m+1)]
  Bedge=mul(power([1,4,1],f),[comb(m-2*f,j) for j in range(m-2*f+1)])
  cs=cycle_count([S,ind],[m,m],0);ct=cycle_count([T,Bedge],[m,m],0)
  print(f,n,float((ct-cs)/cs*n*n))
