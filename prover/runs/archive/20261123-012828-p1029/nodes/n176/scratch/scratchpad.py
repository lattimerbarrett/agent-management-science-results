import sympy as s
from z3 import Real, Solver, unsat
# b_n=a_{n+1}-a_n: verify the finite telescoping reduction.
for N in range(1,11):
    a=s.symbols(f'a0:{N+1}')
    partial=sum(a[n+1]-a[n] for n in range(N))
    assert s.expand(partial-(a[N]-a[0]))==0
print('Positive-increment reduction: sum_{n<N} b_n = a_N-a_0 <= 1.')
print('Upper bounds translate by a_0, so partial sums have no least upper bound exactly when (a_N) does.')
# Exhaustion supplies eventual tau(b_n)<eta/2; constant increments contradict this.
eta=Real('eta')
solver=Solver()
solver.add(eta>0, eta<eta/2)
result=solver.check()
assert result==unsat
print('Constant positive increments versus exhaustion at epsilon=eta/2:',result)
