from fractions import Fraction
from z3 import Solver, Real, RealVal, sat, unsat

def check_trace_obstruction(eta):
    assert isinstance(eta, Fraction) and eta > 0
    N = eta.denominator // eta.numerator + 1
    assert N * eta > 1
    s = Solver()
    vals = [Real(f't_{j}') for j in range(N+1)]
    e = RealVal(f'{eta.numerator}/{eta.denominator}')
    s.add(*(v >= 0 for v in vals), *(v <= 1 for v in vals))
    s.add(*(vals[j+1] - vals[j] == e for j in range(N)))
    outcome = s.check()
    assert outcome == unsat
    return N, str(outcome)

for eta in (Fraction(1,100), Fraction(1,3), Fraction(2,5), Fraction(1), Fraction(7,3)):
    print(f'eta={eta}: N, consistency under trace additivity = {check_trace_obstruction(eta)}')

# Symbolic free-vector telescoping: all intermediate coefficients cancel.
for N in range(1,101):
    coeff = [0]*(N+1)
    for j in range(N):
        coeff[j+1] += 1
        coeff[j] -= 1
    assert coeff == [-1] + [0]*(N-1) + [1]
print('Exact telescoping coefficient checks passed for N=1,...,100.')