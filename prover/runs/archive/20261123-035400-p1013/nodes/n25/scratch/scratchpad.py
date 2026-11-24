# Matching-based near-Turan templates: exact edge optimization.
# Primary part of size s, disjoint matching plus a bounded triangular gadget.
from fractions import Fraction
for r in (2,3,4):
 n=12*r
 best={}
 def comp(n,k,p=()):
  if k==1:
   yield p+(n,);return
  for x in range(n+1):yield from comp(n-x,k-1,p+(x,))
 for sizes in comp(n,r):
  if max(sizes)-min(sizes)>4:continue
  cross=(n*n-sum(x*x for x in sizes))//2
  s=sizes[0]
  for typ,internal in [('matching',s//2),('triangle_matching',3+(s-3)//2 if s>=3 else -10**9),('matching_secondary_edge',s//2+1 if sizes[1]>=2 else -10**9)]:
   e=cross+internal
   if typ not in best or e>best[typ][0]:best[typ]=(e,sizes)
 print('r =',r,'matching-template edge optima:',best)
print('The bounded triangular and secondary-edge modifications must both be included; neither alone establishes edge/cycle separation.')