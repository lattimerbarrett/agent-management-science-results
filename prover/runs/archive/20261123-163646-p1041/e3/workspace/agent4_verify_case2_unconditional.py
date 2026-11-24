"""Exact arithmetic/checkable finite steps of agent4_case2_unconditional_proof.txt.
Uses only Python stdlib plus NumPy. No SAT/UNKNOWN claim occurs here.
"""
from fractions import Fraction
from math import comb
from itertools import combinations, combinations_with_replacement
import numpy as np

W=(322,326,330,334);N=1<<14
for w in W:
 assert Fraction(w,2)>15*7
 upper=Fraction(w)-2*comb(w,2)*Fraction(15,N-1)+4*comb(w,3)*Fraction(210,(N-1)*(N-2))
 assert upper<256
 assert (338-w)//4 in (1,2,3,4)
 print('projection4',w,'exact upper',upper,'=',float(upper))
for t in range(335):assert t%2<=t-2*comb(t,2)+4*comb(t,3)
assert 16*167<31*96

def rank(rows):
 b={}
 for x in rows:
  while x:
   k=x.bit_length()-1
   if k in b:x^=b[k]
   else:b[k]=x;break
 return len(b)
def det(rows,n):return int(rank(rows)==n)
def kern(ell,n):
 basis=[]
 for x in range(1,1<<n):
  if (x&ell).bit_count()%2==0 and rank(basis+[x])>len(basis):basis.append(x)
 return basis
# ALL nonzero four-vectors in a five-space are decomposable, concretely.
wedge=set()
for ell in range(1,32):
 b=kern(ell,5);assert len(b)==4
 v=0
 for i,J in enumerate(combinations(range(5),4)):
  rows=[sum(((x>>j)&1)<<k for k,j in enumerate(J)) for x in b]
  v|=det(rows,4)<<i
 wedge.add(v)
assert wedge==set(range(1,32))

# Relative-gap KT section arithmetic.
quad={0,1}
for n in range(1,8):
 q={0,1<<n,1<<(n-1)}
 for r in range(2,n+1,2):
  delta=1<<(n-r//2-1);q|={(1<<(n-1))-delta,(1<<(n-1))+delta}
 quad|=q
 assert all(0<=x<=1<<n for x in q)
flat={0}|{1<<p for p in range(7)}
for e in (50,52,54):
 assert 64-e not in flat
 assert 96-e not in quad
 for a in (112-e,):
  if a<=58:
   assert a not in quad
   for A in flat:
    for B in flat:
     for C in ({0}|{1<<s for s in range(4)}):
      if C<=min(A,B):assert A+B-2*C!=a
assert 10**2<128<=12**2
print('relative gaps50/52/54: all KT sections PASS')

# Exact directions and functional event profiles in the four-dimensional fiber.
ells=list(range(1,16));directions=list(range(1,16))
line=[tuple((ell&v).bit_count()%2 for ell in ells) for v in directions]
assert all(sum(x)==8 for x in line)
planes=sorted({tuple(sorted((a,b,a^b))) for a in directions for b in directions if a!=b})
assert len(planes)==35
plane_profiles=[tuple(int(any((ell&v).bit_count()%2 for v in P)) for ell in ells) for P in planes]
assert len(set(plane_profiles))==35 and all(sum(x)==12 for x in plane_profiles)

def counts(S,ell):return sum((ell&x).bit_count()%2 for x in S)
# All odd3 feature profiles, including arbitrary affine translations.
triple_profiles=set()
for S in combinations(range(16),3):
 profile=[]
 for ell in ells:
  c=counts(S,ell);profile.append(c*(3-c)//2)
 triple_profiles.add(tuple(profile))
assert triple_profiles==set(plane_profiles)
# All even4 profiles; gamma1 absent iff the fiber is an affine plane.
quad_profiles=set();quad_plane_profiles=set()
for S in combinations(range(16),4):
 profile=tuple((counts(S,ell)*(4-counts(S,ell))-(counts(S,ell)%2))//2 for ell in ells)
 assert all(v in (0,1,2) for v in profile)
 xx=0
 for v in S:xx^=v
 assert (1 not in profile)==(xx==0)
 quad_profiles.add(profile)
 if xx==0:quad_plane_profiles.add(profile)
assert len(quad_profiles)==140
assert quad_plane_profiles=={tuple(2*v for v in p) for p in plane_profiles}
# All odd5 profiles have cost4 but strictly lower maximum value, excluding them.
for S in combinations(range(16),5):
 profile=[counts(S,ell)*(5-counts(S,ell))//2 for ell in ells]
 assert 0<max(profile)<=3
# Fiber defect cost excludes every other nonzero size under budget4.
for t in range(17):
 cost=((t//2)**2 if t%2 else (t//2)*(t//2-1))
 if cost<=4:assert t in (0,1,2,3,4,5)

# Exhaustively check ALL component multisets of budgets1..4.
# Cost1:15 deficit directions and35 odd-triple planes.
# Cost2: ALL140 possible even-four profiles (not only affine planes).
# Odd5 cost4 has been eliminated by max(profile)<=3 above.
U=np.array(line+plane_profiles,dtype=np.uint8)
Q=np.array(sorted(quad_profiles),dtype=np.uint8)
plane_index={p:i for i,p in enumerate(plane_profiles)}
solutions={B:[] for B in range(1,5)}
for B in range(1,5):
 for qcount in range(B//2+1):
  ucount=B-2*qcount
  ucombs=list(combinations_with_replacement(range(50),ucount))
  qcombs=list(combinations_with_replacement(range(140),qcount))
  usums=np.array([U[list(c)].sum(axis=0) if c else np.zeros(15,dtype=np.uint64) for c in ucombs],dtype=np.uint8)
  for qc in qcombs:
   qsum=Q[list(qc)].sum(axis=0) if qc else np.zeros(15,dtype=np.uint64)
   vals=usums+qsum
   ok=np.flatnonzero(np.all((vals==0)|(vals==4),axis=1))
   for j in ok:
    uc=ucombs[int(j)]
    # k_v<=3; only possible violation at this budget is four equal line units.
    if len(uc)==4 and uc[0]==uc[-1] and uc[0]<15:continue
    solutions[B].append((uc,qc))
 assert (len(solutions[B])==0 if B<4 else len(solutions[B])==105)
 for uc,qc in solutions[B]:
  assert all(i>=15 for i in uc)
  profiles=[tuple(U[i]) for i in uc]+[tuple(v//2 for v in Q[i]) for i in qc]
  assert profiles and len(set(profiles))==1
  assert profiles[0] in set(plane_profiles)
 print('budget',B,'complete component solutions',len(solutions[B]))

# All35 common-plane terminal models give projected296, pairs28, derivative240.
for P in planes:
 n={v:3 if v in P else 7 for v in directions}
 assert sum(n.values())==93
 assert sum(n[v] for v in directions if v not in P)==84
 assert 128+2*84==296
 for a in directions:
  if a in P:continue
  coset={a}|{a^v for v in P}
  assert len(coset)==4 and all(v not in P for v in coset)
  assert sum(n[v] for v in coset)==28
 assert 296-2*28==240
print('PASS: unconditional Case2 arithmetic, exterior normalization, relative gaps,')
print('all affine3/4/5 fiber profiles, ALL budget multisets, and terminal projection.')
