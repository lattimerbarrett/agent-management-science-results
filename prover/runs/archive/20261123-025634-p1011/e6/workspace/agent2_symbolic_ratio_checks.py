import sympy as S
from pathlib import Path
n,k=S.symbols('n k',integer=True,positive=True)
a=(n+1)/2
for s in range(1,5):
 def I(ss):
  return 2**(2*a-ss+1)*S.rf(ss,k)/S.factorial(k)*S.gamma(a-ss+1)*S.gamma(a+k+1)/S.gamma(2*a+k-ss+2)
 ratio=S.rf(k+1,s-1)*S.rf(k+n+3-s,s-1)/(S.factorial(s-1)*S.prod(n+1-2*r for r in range(1,s)))
 # gamma simplification alone can leave unsimplified symbolic half shifts;
 # verify the exact recurrence in s and initial s=1 algebraically instead.
 if s==1:assert ratio==1
 else:
  prev=S.rf(k+1,s-2)*S.rf(k+n+4-s,s-2)/(S.factorial(s-2)*S.prod(n+1-2*r for r in range(1,s-1)))
  assert S.factor(ratio/prev-(k+s-1)*(k+n+3-s)/((s-1)*(n+3-2*s)))==0
 for N in (10,17,18,19,25):
  for K in (0,1,2,5,11):
   assert S.simplify((I(s)/I(1)-ratio).subs({n:N,k:K}))==0
print('Corrected symbolic Jacobi ratio incl. (s−1)! checked.')
Path('workspace/agent2_symbolic_ratio_checks.py').write_text(Path(__file__).read_text())
