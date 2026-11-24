from z3 import Real, Solver, sat
N=10
eta=Real('eta')
a=[Real(f'alpha_{n}') for n in range(N+1)]
s=Solver(); s.add(eta==RealVal('1/2')) if False else None
# Encode exactly the scalar consequences of monotonicity and abelian
# complementation, without importing strict order preservation.
s.add(eta*2==1)
for n in range(N+1): s.add(a[n]>=0,a[n]<=1)
for n in range(N):
    s.add(a[n]<=a[n+1],eta<=a[n+1],eta<=1-a[n])
s.add(a[0]==0)
print('Endpoint scalar constraints:',s.check())
if s.check()==sat:
    m=s.model(); print('alpha values:',[m.eval(x) for x in a])
for n in range(1,N):
    q=Solver(); q.add(s.assertions()); q.add(a[n]*2!=1)
    assert str(q.check())=='unsat'
print('Every interior alpha is forced to 1/2, but the constraints are consistent.')
