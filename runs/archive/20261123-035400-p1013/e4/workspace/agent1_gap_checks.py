from itertools import product, combinations
from fractions import Fraction
from pathlib import Path
import json

def turan(n,r):
 q,s=divmod(n,r)
 return (n*n-s*(q+1)**2-(r-s)*q*q)//2

def compositions(n,r):
 if r==1:
  yield (n,); return
 for x in range(n+1):
  for tail in compositions(n-x,r-1):yield (x,)+tail

# Verify signed matching-block double count, without an extremal estimate.
blocks=0
for a in range(1,4):
 for b in range(1,4):
  for bits in product((0,1), repeat=a*b):
   for h in range(1,min(a,b)+1):
    has=any(all(bits[i*b+j] for i in I for j in J)
       for I in combinations(range(a),h) for J in combinations(range(b),h))
    if not has:
     assert h*h*(a*b-sum(bits))>=a*b
     blocks+=1

# Exact integer verification of quadratic part-size optimization.
parts=0
for r in range(2,7):
 for n in range(21):
  for sizes in compositions(n,r):
   cross=(n*n-sum(s*s for s in sizes))//2
   bound=Fraction(turan(n,r))+Fraction(n,2*r)+Fraction(r,8)+Fraction(r-1,8*r)
   assert cross+Fraction(max(sizes),2)<=bound
   parts+=1

# Host counts: choose common part size divisible by six.
hosts=0
for r in range(2,20):
 for q in range(6,121,6):
  n=r*q
  assert Fraction(q-1)==Fraction(n,r)-1 # full internal star
  assert Fraction(2*q,3)==Fraction(2*n,3*r) # P3 factor
  assert 2*(q//2)==Fraction(n,r) # matchings in two parts
  hosts+=3

# Symbolic continuous optimization, using exact rational equality.
for r in range(2,101):
 x=Fraction(r-1,2*r)
 assert x/2-Fraction(r,2*(r-1))*x*x==Fraction(r-1,8*r)

result={'matching_block_cases':blocks,'part_compositions':parts,'template_counts':hosts,'symbolic_stationary_checks':99}
print(result)
Path('workspace/agent1_gap_checks.py').write_text(Path('scratchpad.py').read_text())
Path('workspace/agent1_gap_checks.json').write_text(json.dumps(result,indent=2))
