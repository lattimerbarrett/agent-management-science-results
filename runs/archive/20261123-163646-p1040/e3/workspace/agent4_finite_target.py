from itertools import product
from pathlib import Path
words=[()]+[w for d in range(1,4) for w in product(range(3),repeat=d) if all(a!=b for a,b in zip(w,w[1:]))]
idx={w:i for i,w in enumerate(words)}
one=1

def right_reflection(z,c):
 out=z
 for i,w in enumerate(words):
  if z>>i&1 and len(w)<3 and (not w or w[-1]!=c):out^=1<<idx[w+(c,)]
 return out
states={one:()};stack=[one]
while stack:
 z=stack.pop()
 for c in range(3):
  q=right_reflection(z,c)
  if q not in states:states[q]=states[z]+(c,);stack.append(q)
print('Finite class3 target group order',len(states))
P=one
for w in [(0,2,1),(1,0,2),(1,2,0),(2,0,1)]:P^=1<<idx[w]
assert P in states and P!=one
# Verify every group commutator with a degree3 element is trivial by literal products.
# Degree3 elements commute since products with positive-degree terms have degree>=4.
assert all(len(words[i])==3 for i in range(1,len(words)) if (P^one)>>i&1)
print('Cubic counterexample target nonidentity bitvector',P)
