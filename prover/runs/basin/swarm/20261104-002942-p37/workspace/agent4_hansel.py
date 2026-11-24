from math import comb
from pathlib import Path
chains=[(0,)]
for n in range(0,13):
 N=1<<n
 assert sorted(x for C in chains for x in C)==list(range(N))
 assert len(chains)==comb(n,n//2)
 pos={x:j for j,C in enumerate(chains) for x in C}
 for j,C in enumerate(chains):
  assert (C[0].bit_count()+C[-1].bit_count())==n
  for a,b,c in zip(C,C[1:],C[2:]):
   diff=c^a
   assert diff.bit_count()==2
   z=a|(diff^(b^a))
   assert pos[z]<j,(n,C,a,b,c,z,pos[z],j)
 print(n,len(chains),'diamond property verified')
 new=[]
 for C in chains:
  if len(C)>1: new.append(tuple(x|N for x in C[:-1]))
  new.append(C+(C[-1]|N,))
 chains=new
