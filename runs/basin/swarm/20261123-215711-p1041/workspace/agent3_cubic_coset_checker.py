"""Exact bit-vector enumeration of small cubic cosets used in 64+112 proof."""
from itertools import combinations

def mon(mask):
 return sum(1<<x for x in range(64) if x&mask==mask)
low=[mon(sum(1<<i for i in S)) for d in range(3) for S in combinations(range(6),d)]
assert len(low)==22
x3,z3,m1,m2=map(mon,(7,56,49,42))
tops=[x3]+[x3^z3^(m1 if e1 else 0)^(m2 if e2 else 0) for e1 in (0,1) for e2 in (0,1)]
state=tops[:]
small=[set([s.bit_count()]) for s in state]
mins=[s.bit_count() for s in state]
for i in range(1,1<<22):
 j=(i&-i).bit_length()-1
 q=low[j]
 for k in range(5):
  state[k]^=q
  w=state[k].bit_count()
  if w<16:small[k].add(w)
  if w<mins[k]:mins[k]=w
assert small[0]=={8}
assert mins[1:]==[14]*4
assert all(s=={14} for s in small[1:])
print('Exact 5 cubic cosets, 2^22 words each:',small,'minima',mins)
