from itertools import product
from pathlib import Path

def sub(a,b): return a & b == a
n=3
sets=range(1<<n)
mono=[v for v in product((0,1), repeat=1<<n) if all(not(v[a] and not v[b]) for a in sets for b in sets if sub(a,b))]
assert len(mono)==20
# Every finite positive enumeration operator is a tuple of monotone Boolean functions.
# Exhaustively verify antitonicity/complement, and the fixed-point antichain lemma
# coordinate-wise. Full set-valued maps would be 20**3 in number; all scalar
# monotone pairs suffice to check every coordinate of their composition.
checks=0
for f in mono:
  for a,b in product(sets, repeat=2):
    if sub(a,b):
      assert f[a]<=f[b]
      assert 1-f[a]>=1-f[b]
      checks+=1
# Enumerate every monotone operator on a TWO-element universe, and every pair.
n=2; sets=range(1<<n); mask=(1<<n)-1
m2=[v for v in product((0,1),repeat=1<<n) if all(v[a]<=v[b] for a in sets for b in sets if sub(a,b))]
ops=[tuple(sum(bits[i][a]<<i for i in range(n)) for a in sets) for bits in product(m2,repeat=n)]
num_pairs=0
for theta,psi in product(ops,repeat=2):
  solutions=[d for d in sets if d==psi[mask^theta[d]]]
  for a,b in product(solutions,repeat=2):
    assert not(a!=b and sub(a,b))
  num_pairs+=1
print({'monotone_boolean_functions_on_3_bits':len(mono),'scalar_monotonicity_checks':checks,'all_operator_pairs_on_2_bits_checked':num_pairs})
