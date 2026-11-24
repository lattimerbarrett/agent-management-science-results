from fractions import Fraction as Q
from itertools import product
from pathlib import Path

def partitions(n,m=None):
 if n==0:yield[];return
 for a in range(min(n,m or n),0,-1):
  for p in partitions(n-a,a):yield[a]+p
bad=[];worst=Q(0)
for kind,h,lsum in [('trans',6,2)]+[('equal',h,h//2) for h in [2,4,6,8]]:
 for pp in partitions(h):
  if max(pp)>8:continue
  d=pp+[0]*(10-len(pp));ds=[1+x for x in d]
  lam=max(Q(di)+Q(sum(sorted(ds[:i]+ds[i+1:],reverse=True)[:di]),di) for i,di in enumerate(ds))
  gap=10-lam
  for L0 in product(*(range(x+1) for x in pp)):
   if sum(L0)!=lsum:continue
   L=list(L0)+[0]*(10-len(pp));R=[d[i]-L[i] for i in range(10)]
   j=[Q(L[i],2)-Q(R[i],4) if kind=='trans' else Q(L[i]-R[i],4) for i in range(10)]
   norm=sum(x*x for x in j)
   if norm==0:continue
   if gap<=0 or norm/gap>Q(3,4):bad.append((kind,pp,L0,lam,norm))
   else:worst=max(worst,norm/gap)
print('Badprofiles',bad,'worst',worst)
assert not bad and worst==Q(5,8)
