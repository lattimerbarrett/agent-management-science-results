from itertools import product
from pathlib import Path
T={322,326,330,334}
powers=[0]+[1<<i for i in range(8)]
def possible_three(dims):
 ans=[]
 total=sum(1<<d for d in dims)
 for a,b,c,t in product(powers,repeat=4):
  # a=A&B,b=A&C,c=B&C,t=triple.
  if a>1<<min(dims[0],dims[1]) or b>1<<min(dims[0],dims[2]) or c>1<<min(dims[1],dims[2]):continue
  if t>min(a,b,c):continue
  w=total-2*(a+b+c)+4*t
  if w not in T:continue
  if t:
   ea,eb,ec,et=[x.bit_length()-1 for x in [a,b,c,t]]
   if ea+eb>dims[0]+et or ea+ec>dims[1]+et or eb+ec>dims[2]+et:continue
  elif a and b and c:
   ea,eb,ec=[x.bit_length()-1 for x in [a,b,c]]
   if ea+eb-ec>dims[0]-1 or ea+ec-eb>dims[1]-1 or eb+ec-ea>dims[2]-1:continue
  ans.append((w,a,b,c,t))
 return ans
assert possible_three((7,7,7))==[]
assert possible_three((7,8,7))==[]
P=[0]+[1<<i for i in range(7)]
Q=[0]+[1<<i for i in range(6)]
maxsum=0
for p,q,a,b,r in product(P,P,Q,Q,Q):
 if p and a*p>128:continue
 if q and b*q>128:continue
 if p==q==64:continue
 maxsum=max(maxsum,p+q+a+b+r)
assert maxsum==134
assert 638-2*maxsum==370
hs=set()
for r in Q:
 for t in powers:
  if t>r:continue
  if t and 2*t<r:continue
  h=256-2*r+4*t
  hs.add(h)
  assert h==192 or h>=224
  for I in range(6):assert 128+h-2*I not in T
print('All exact mixed-flat bounds passed; maxsum=',maxsum,'h weights=',sorted(hs))
