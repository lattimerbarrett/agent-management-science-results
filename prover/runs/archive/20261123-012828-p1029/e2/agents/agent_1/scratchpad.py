from fractions import Fraction
import sympy as s

# Verify the exact telescoping certificate, without assuming quasitrace additivity.
for N in range(1, 21):
    t = s.symbols('t0:'+str(N+1))
    e = s.symbols('eta')
    defects = [t[i+1]-t[i]-e for i in range(N)]
    assert s.expand(sum(defects)-(t[N]-t[0]-N*e)) == 0
print('Verified symbolic defect identity for N=1,...,20.')

# In the tracial case all defects vanish.  For any positive rational eta,
# N=floor(1/eta)+1 makes the necessary inequality N*eta<=1 impossible.
checks=0
for den in range(2, 101):
    for num in range(1, den):
        eta=Fraction(num,den)
        N=eta.denominator//eta.numerator+1
        assert N*eta>1
        checks+=1
print(f'Checked exact rational trace obstruction for {checks} choices of eta in (0,1).')

# Universal monotonicity constraints: eta <= t_n <= 1-eta (n>=1).
# This linear system excludes eta>1/2, but permits eta=1/2 only at t_n=1/2.
x,e=s.symbols('x eta', real=True)
assert s.solve([s.Eq(x,e),s.Eq(x,1-e)], [x,e]) == {x:s.Rational(1,2),e:s.Rational(1,2)}
print('Checked boundary constraints meet only at eta=t_n=1/2.')

# Save a reusable copy of these finite checks, not a purported construction.
from pathlib import Path
source = Path('scratchpad.py').read_text()
Path('workspace/agent1_obstruction_checks.py').write_text(source.split('# Save a reusable copy')[0])
