import math, json
from pathlib import Path
import numpy as np
rng=np.random.default_rng(202604)
def params(p,K):
 q=p/(p-1); ea=1/K; eb=K**(-1/(p-1)); ra=1-ea; rb=1-eb
 r=.25*ra**(1/p)*rb**(1/q); d=math.log(2)/math.log(1/r); kap=1-d
 alpha=kap+math.log(ra)/math.log(1/r); beta=kap+math.log(rb)/math.log(1/r)
 assert abs(alpha/p+beta/q-d)<1e-12
 return q,r,alpha,beta,K**(-1/p)
def gapint(a,b,z,r):
 if a>=b:return 0.
 mid=.5
 def prim(t):return t**(z+1)/(z+1)
 return ((prim(min(b,mid)-r)-prim(a-r)) if a<mid else 0)+((prim(1-r-max(a,mid))-prim(1-r-b)) if b>mid else 0)
def dint(a,b,z,r):
 # exact infinite-tail summation on whole cylinders, recursive endpoints only
 M=2*((1-2*r)/2)**(z+1)/(z+1)/(1-2*r**(z+1))
 def rec(a,b,depth=0):
  if a>=b:return 0.
  if a<=0 and b>=1:return M
  if depth>120:return 0.
  ans=gapint(max(a,r),min(b,1-r),z,r)
  if a<r:ans+=r**(z+1)*rec(a/r,min(b,r)/r,depth+1)
  if b>1-r:ans+=r**(z+1)*rec(max(a,1-r)/r-(1-r)/r,(b-(1-r))/r,depth+1)
  return ans
 return rec(a,b)
def stair(x,r):
 if x<=0:return 0.
 if x>=1:return 1.
 out=0.; mass=1.
 for _ in range(120):
  if x<r:x/=r;mass*=.5
  elif x>1-r:out+=mass*.5;x=(x-(1-r))/r;mass*=.5
  else:return out+mass*.5
 return out+mass*.5
rows=[]
for p in [1.25,1.5,2.,3.,5.]:
 for K in [100.,1000.]:
  q,r,A,B,h=params(p,K)
  intervals=[(0.,1.),(0.,r),(r,1-r),(r/2,r*1.1)]
  intervals += [tuple(sorted(rng.random(2))) for _ in range(30)]
  for n in [3,10,20]:
   intervals.append((0.,r**n)); intervals.append((r-r**n,r+r**n))
  ratios=[]
  for l,rr in intervals:
   L=rr-l
   ma=dint(l,rr,-A,r)/L; mai=dint(l,rr,A*q/p,r)/L
   mb=dint(l,rr,-B,r)/L; mbi=dint(l,rr,B*p/q,r)/L
   osc=stair(rr,r)-stair(l,r)
   root=ma**(1/p)*mai**(1/q)+mbi**(1/p)*mb**(1/q)+h*ma**(1/p)*mb**(1/q)*osc
   assert math.isfinite(root) and root>0
   ratios.append(root/K**(1/p))
  rows.append(dict(p=p,K=K,r=r,alpha=A,beta=B,max_root_triangle_over_Kroot=max(ratios),intervals=len(ratios)))
print(json.dumps(rows,indent=2))
