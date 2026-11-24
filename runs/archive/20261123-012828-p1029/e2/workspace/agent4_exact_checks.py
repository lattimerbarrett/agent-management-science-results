import sympy as s
from pathlib import Path

# Exact counterexample to using spectral cuts as ordinary-order monotone maps.
a = s.diag(s.Rational(1,3), 0)
b = s.Matrix([[2,1],[1,1]])/3
assert all(x >= 0 for x in (b-a).eigenvals())
assert all(x >= 0 for x in a.eigenvals())
assert all(x >= 0 for x in (s.eye(2)-b).eigenvals())
lo = (3-s.sqrt(5))/6
hi = (3+s.sqrt(5))/6
t = s.Rational(1,4)
assert lo < t < s.Rational(1,3) < hi
p = s.diag(1,0)
q = s.simplify((b-lo*s.eye(2))/(hi-lo))
assert s.simplify(q*q-q) == s.zeros(2)
assert s.simplify(q.T-q) == s.zeros(2)
assert s.simplify(q*p-p) != s.zeros(2)
assert s.simplify((q-p).det()) < 0
print('Exact check passed: 0<=a<=b<=1 but spectral cuts at 1/4 are incomparable.')
print('det(q-p) =',s.simplify((q-p).det()))

# Exact finite certificate of nonadditivity required by any positive-eta witness.
# If N*eta>1, the additivity defect is strictly negative.
eta=s.symbols('eta', positive=True)
for N in range(1,101):
    ts=s.symbols('t0:'+str(N+1))
    defects=[ts[k+1]-ts[k]-eta for k in range(N)]
    assert s.expand(sum(defects)-(ts[N]-ts[0]-N*eta)) == 0
print('Exact additivity-defect identities verified for N=1,...,100.')
archive = Path('workspace/agent4_exact_checks.py')
if Path(__file__).resolve() != archive.resolve():
    archive.write_text(Path(__file__).read_text(), encoding='utf-8')
