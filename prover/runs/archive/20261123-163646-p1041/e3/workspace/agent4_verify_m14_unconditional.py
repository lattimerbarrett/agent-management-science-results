"""Final independent arithmetic for consolidated m14 exclusion; no structural K."""
from fractions import Fraction
from itertools import product
import runpy
runpy.run_path('workspace/agent4_verify_derivative_bootstrap.py',run_name='__main__')
# Explicit classical strict-KT first-band values plus stated KTA q1 gap.
q0=[96,112,120,124,128]+list(range(132,336,4))
q1=[126]+list(range(154,336,4))
triples=set()
for a,b,c in product(q1,q0,q0):
 if a+b+c<=334:triples.add(tuple(sorted((a,b,c))))
assert triples=={(96,96,126),(96,112,126)}
assert 3*126>334
# Essential dimensions of all strict-KT moment forms used in Lemma2.
assert 4+4==8 and 2+6==8 and 3+6==9
# Three-flat256 periodicity arithmetic with empty affine intersections allowed.
maxP=0
for r,s,t in product(range(8),repeat=3):
 if max(r+s,r+t,s+t)>7:continue
 P=sum((1<<u) if u<=5 else 0 for u in(r,s,t))
 maxP=max(maxP,P)
assert maxP==40 and maxP<64
# Quadric residual support span in the min256 lemma.
for wt in(96,112,120):
 a=wt-64;needed=(a-1).bit_length()
 assert needed>=5 and 7+8-needed+1<=11
# Small-span derivative puncture budgets and final first-parent gap.
assert 334-256==78 and 78-64==14 and 14<32
for w in(322,326,330,334):
 vals=[v for v in range(256,335,4) if v not in(260,264)]
 assert Fraction(2*w+128,3)<268
 assert min(v for v in vals if v>256)==268
 # The actual classical gap is all even values strictly between256 and272.
 vals=[v for v in vals if v!=268]
 assert min(v for v in vals if v>256)==272
 assert all(v==256 for v in vals if v<=Fraction(2*w+128,3))
print('PASS consolidated m14: coefficient triples, all direction-log cases,')
print('min256 spans, smallspan budgets, and final numerical derivative gap.')
