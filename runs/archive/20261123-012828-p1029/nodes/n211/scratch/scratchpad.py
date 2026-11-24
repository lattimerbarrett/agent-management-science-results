# Endpoint scalar consequences, independently checked using Z3.
from z3 import Real, Solver, Or, sat
eta=Real('eta')
t=[Real(f't{i}') for i in range(1,6)]
s=Solver(); s.add(eta==1/2)
for x in t:s.add(x>=eta,x<=1-eta)
s.add(Or(*[x!=eta for x in t]))
print('Endpoint permits an interior quasitrace value other than 1/2:',s.check())
# With a strictly increasing scalar sequence, equality is impossible.
s2=Solver(); s2.add(t[0]>=1/2,t[1]<=1/2,t[0]<t[1])
print('Endpoint plus strict order preservation:',s2.check())
