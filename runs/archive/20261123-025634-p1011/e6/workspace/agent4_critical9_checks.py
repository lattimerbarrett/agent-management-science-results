"""Exact n18 critical-degree-nine spectral logarithmic coefficients.
This checks uncut coefficient asymptotics only, not cutoff spectral matching.
"""
import sympy as s
from pathlib import Path
k=s.symbols('k',positive=True)
n=18
for q in [1,3,5,7,9]:
 i=(9-q)//2;ss=q-1+i;alpha=s.Rational(n-3,2)+q;l=k+q
 D=s.prod(l-1+2*r for r in range(n//2+1))/s.prod(l+2*r for r in range(n//2))
 C=2**(2*alpha-2*ss+1)*s.gamma(alpha-ss+1)**2/s.gamma(ss)**2
 T=s.factor(4**i*C*(2*k+2*alpha+1)*s.rf(k,ss)**2*s.rf(k,int(2*alpha+1))/(s.rf(k,1)*s.rf(k,int(2*alpha-ss+2))**2)*((l-1)*(l+n-1))**2/D)
 expected=2**19*s.gamma(s.Rational(q+10,2))**2/s.gamma(s.Rational(q+7,2))**2
 assert s.simplify(s.limit(k*T,k,s.oo)-expected)==0
 assert expected>0
 # all cross terms with strictly lower degrees have summable exponent >=3.
 for j in range(i):
  degree=q+2*j
  assert n+1-(9+degree)>=3
 print('q',q,'critical coefficient/pi',s.simplify(expected/s.pi),'dilation log coefficient/pi',s.simplify(8*expected/s.pi))
print('PASS exact positive critical logarithmic coefficients and cross-decay powers')
if Path(__file__).name=='scratchpad.py':Path('workspace/agent4_critical9_checks.py').write_text(Path(__file__).read_text())
