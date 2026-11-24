"""Exact exterior certificates for remaining proper hyperplane slices in m=15.
All arithmetic is over F2; no external packages.
"""
import itertools
from fractions import Fraction
n=13

def rank(rows):
 P={}
 for v in rows:
  while v:
   p=v.bit_length()-1
   if p in P:v^=P[p]
   else:P[p]=v;break
 return len(P)

def wedge(T,v):
 out=set()
 for a in T:
  for i in range(n):
   if v>>i&1 and not a>>i&1:
    x=a|1<<i
    if x in out:out.remove(x)
    else:out.add(x)
 return out

def form(vs):
 T={0}
 for v in vs:T=wedge(T,v)
 return T

def hs(T,k=6):
 h=[]
 for j in range(k+1):
  cols={sum(1<<i for i in S):a for a,S in enumerate(itertools.combinations(range(n),k-j))}
  rows=[]
  for S in itertools.combinations(range(n),j):
   mask=sum(1<<i for i in S);r=0
   for t in T:
    if t&mask==mask:r^=1<<cols[t^mask]
   rows.append(r)
  h.append(rank(rows))
 return h

# alpha = two complementary six-volume forms.
alpha={63,4032};low=[];count=0
for a in range(7):
 for b in range(7-a):
  c=6-a-b
  vs=[1<<i for i in range(a)]+[1<<(6+i) for i in range(b)]
  vs +=[(1<<(a+i))^(1<<(6+b+i)) for i in range(c)]
  H=hs(alpha^form(vs));count+=1
  if sum(H)<=144:low.append(('inside',a,b,c,sum(H),H[1]))
for a in range(6):
 for b in range(6-a):
  c=5-a-b
  vs=[1<<i for i in range(a)]+[1<<(6+i) for i in range(b)]
  vs +=[(1<<(a+i))^(1<<(6+b+i)) for i in range(c)]+[1<<12]
  H=hs(alpha^form(vs));count+=1
  if sum(H)<=144:low.append(('outside',a,b,c,sum(H),H[1]))
assert count==49
expected={('inside',0,5,1,124,11),('inside',0,6,0,64,6),
 ('inside',1,5,0,126,12),('inside',5,0,1,124,11),
 ('inside',5,1,0,126,12),('inside',6,0,0,64,6),
 ('outside',0,5,0,126,12),('outside',5,0,0,126,12)}
assert set(low)==expected
print('49 crossstar+decomposable orbits: low cases exactly',sorted(low))

# beta decomposable plus first KT112 moment form.
# gamma=D2 wedge rho4; rho is symplectic dual four-form on Q6.
gamma={3|sum(1<<i for i in range(2,8) if i not in pair) for pair in [(2,3),(4,5),(6,7)]}
cnt1=0;maxess1=0
for a in range(3):
 for b in range(7):
  e=a+b
  if not 1<=e<=6:continue
  for s in range(4):
   t=b-2*s
   if t<0 or s+t>3:continue
   vs=[1<<i for i in range(a)]
   vs +=[1<<(2+2*j+k) for j in range(s) for k in [0,1]]
   vs +=[1<<(2+2*j) for j in range(s,s+t)]
   vs +=[1<<(8+j) for j in range(6-e)]
   H=hs(gamma^form(vs));cnt1+=1
   if sum(H)<=154:
    maxess1=max(maxess1,H[1]);assert H[1]<=11
# beta plus second KT112 form D3 wedge (volU3+volV3).
gamma={63,7|sum(1<<i for i in [6,7,8])};cnt2=0;maxess2=0
for a in range(4):
 for i in range(4):
  for j in range(4):
   for c in range(4):
    if i+c>3 or j+c>3:continue
    e=a+i+j+c
    if not 2<=e<=6:continue
    vs=[1<<k for k in range(a)]+[1<<(3+k) for k in range(i)]+[1<<(6+k) for k in range(j)]
    vs +=[(1<<(3+i+k))^(1<<(6+j+k)) for k in range(c)]
    vs +=[1<<(9+k) for k in range(6-e)]
    H=hs(gamma^form(vs));cnt2+=1
    if sum(H)<=154:
     maxess2=max(maxess2,H[1]);assert H[1]<=11
print('64+112 moment forms checked:',cnt1,cnt2,'orbits; max essential dimensions at L<=154:',maxess1,maxess2)

# Proper small-section split arithmetic. First/second weights are64/96.
partners={64,96,112,120,124,126,128,136,144}
exception=[]
for a in [128,136,144,148,152,154,156]:
 for w in [322,326,330,334]:
  total=w-a
  for b in [64,96]:
   c=total-b
   if b<=c and c in partners:exception.append((a,w,b,c))
assert exception==[(136,326,64,126),(144,334,64,126),(154,330,64,112)]
print('Proper-slice sumset exceptions exactly',exception)
# Moment-matrix proof uses L<=weight; relevant normal-form gap arithmetic.
for w in [136,144]:
 assert (w-128)//2 in [4,8] and (w-128)//2<16
 assert w//2 in [68,72] and 32<w//2-32<48
 assert 64<w-64<96
# Exact Parseval forcing a section <=156 for constant-Q support in F2^15.
for w in [322,326,330,334]:
 mean_square=Fraction(32768*w-w*w,32767)
 assert mean_square>(w-316)**2
print('All extended gap arithmetic and Parseval bounds checked.')
