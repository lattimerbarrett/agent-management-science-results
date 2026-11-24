import sympy as s
from pathlib import Path
t, q, qq, m, mp = s.symbols('t Fprime Fsecond moment momentprime', nonzero=True,real=True)
sol=s.solve([m-t-q*t*(1-t),mp-1-qq*t*(1-t)-q*(1-2*t)],[q,qq])
D=s.factor(t*(qq*(1-t)-q)).subs(sol).simplify()
assert s.simplify(D-(mp-m/t))==0
k=1-mp+(mp-m/t)**2/mp
assert s.simplify(k-(1-2*m/t+(m/t)**2/mp))==0
print('Verified full-profile Schur coefficient k=1−2s/t+s²/(t² s_prime); mixed=t*alpha*(s_prime−s/t).')
Path('workspace/agent2_profile_schur_check.py').write_text(Path(__file__).read_text())
