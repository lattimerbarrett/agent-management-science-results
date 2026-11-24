import sys
sys.path.insert(0,'workspace')
from agent4_pairing import *
from functools import lru_cache
from random import Random
@lru_cache(None)
def split(a):
 c=Counter(a);ks=tuple(c);cs=tuple(c[k] for k in ks);out=[]
 for vv in product(*(range(v+1) for v in cs)):
  x=tuple(sorted((k for k,v in zip(ks,vv) for _ in range(v)),reverse=True))
  y=tuple(sorted((k for k,c0,v in zip(ks,cs,vv) for _ in range(c0-v)),reverse=True))
  z=1
  for c0,v in zip(cs,vv):z*=comb(c0,v)
  out.append((x,y,z))
 return out
@lru_cache(None)
def point(a,t,g):
 assert sum(a)+t==g-1
 out=0
 for x,y,z in split(a):
  s=t+sum(y)
  if s==0:continue
  k=s-1
  if k==0:v=(2*g-2)*intersection(x,g)
  else:v=intersection(tuple(sorted(x+(k,),reverse=True)),g)
  out+=z*v
 return out%P
basis=list(partitions(12));R=[];rng=Random(4);g=12;h=13
for run in range(300):
 degI=rng.randrange(12);degJ=rng.randrange(12-degI)
 I=rng.choice(list(partitions(degI)));J=rng.choice(list(partitions(degJ)))
 t=rng.randrange(12-degI-degJ);u=11-degI-degJ-t
 row=[]
 for p in basis:
  val=0
  for x,y,z in split(p):
   if sum(x)+degI+t!=g-1:continue
   val+=z*point(tuple(sorted(x+I,reverse=True)),t,g)*point(tuple(sorted(y+J,reverse=True)),u,h)
  row.append(val%P)
 R.append(row)
 rk=rank_certificate(R)[0]
 if run%10==0:print(run,rk,flush=True)
 if rk==77:break
print('final rank',rk,'using',run+1,'rows')
assert rk==77
