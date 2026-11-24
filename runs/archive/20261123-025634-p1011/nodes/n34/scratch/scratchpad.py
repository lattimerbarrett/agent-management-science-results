import sympy as s
n=18
mu=lambda L:2*s.gamma(s.Rational(L+n+1,2))*s.gamma(s.Rational(L,2))/(s.gamma(s.Rational(L-1,2))*s.gamma(s.Rational(L+n,2)))
q=lambda L:s.Integer((L-1)*(L+n-1))**2/mu(L)
r=s.simplify(q(3)/q(2))
print(r, s.simplify(20-r))
# Documentation size of supplied compactness bridge and exact line concern
from pathlib import Path
text=Path('experiments/e3/agent3_local_pohozaev_bridge.md').read_text()
print(text[9000:18000])
