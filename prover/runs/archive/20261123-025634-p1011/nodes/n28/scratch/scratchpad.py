from pathlib import Path
import sympy as s
r=Path('experiments/e3')
text=(r/'agent3_local_pohozaev_bridge.md').read_text()
print('### Local compactness conclusion\n',text[-8500:])
print('### Certified dimensional profiles\n',(r/'agent2_finite_profiles.txt').read_text()[:3500])
n=s.symbols('n',integer=True,positive=True)
c=(n-2)/(4*(n-1)); A=2**((n-2)/2); p=(n+2)/(n-2)
print('### Normalization audit')
print('R for original equation =',s.simplify(n*(n-2)/c))
print('Coefficient after v=A*u =',s.simplify(n*(n-2)*A**(1-p)))
print('Trace-H Robin coefficient =',s.simplify(2*c))
print('Average-H Robin coefficient =',s.simplify(2*c*(n-1)))
