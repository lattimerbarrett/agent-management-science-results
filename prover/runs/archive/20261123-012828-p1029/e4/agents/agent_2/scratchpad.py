"""Exact checks for the tracial obstruction to the proposed construction."""
from fractions import Fraction
import sympy as sp
from pathlib import Path

# Check the telescoping identity with symbolic selfadjoint-element labels.
for N in range(1, 101):
    a = sp.symbols(f'a0:{N+1}')
    assert sp.expand(sum(a[k+1]-a[k] for k in range(N))-(a[N]-a[0])) == 0

# If eta > 0 is rational, N=floor(1/eta)+1 forces N*eta > 1.
# Exhaustively check all fractions p/q with 1<=p,q<=200.
for p in range(1,201):
    for q in range(1,201):
        eta = Fraction(p,q)
        N = eta.denominator // eta.numerator + 1
        assert N*eta > 1

# Save reproducible checked statement, not a claimed construction.
Path('workspace/agent2_trace_obstruction.txt').write_text(
    'Checked symbolic telescoping for N=1..100 and exact rational obstruction '
    'for all eta=p/q with 1<=p,q<=200. Mathematical general proof: '
    'for any real eta>0 choose integer N>1/eta; additivity and positivity give '
    'N eta=tau(a_N)-tau(a_0)<=1, contradiction. '
    'This excludes all tracial examples, not arbitrary 2-quasitraces.\n')
print('PASS: 100 symbolic telescoping identities; 40000 exact rational Archimedean-bound checks.')
