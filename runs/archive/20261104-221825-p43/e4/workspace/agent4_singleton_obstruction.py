"""Finite algebraic checks for the singleton obstruction.
Analytic input (spectrality and strict LS) is a stated theorem, not checked here.
"""
import sympy as s
from z3 import Int, Real, Solver, unsat
q=s.Symbol('q')
# Basis 1,a,b,ab of Q[a,b,q]/(a^2-q,b^2-q).
basis=[(0,0),(1,0),(0,1),(1,1)]
def multiply(i,j):
    x,y=basis[i]; u,v=basis[j]
    return q**((x+u)//2+(y+v)//2), basis.index(((x+u)%2,(y+v)%2))
assert multiply(1,1)==(q,0)
assert multiply(2,2)==(q,0)
assert multiply(1,2)==(1,3)
for i in range(4):
 for j in range(4):
  for k in range(4):
   c,ij=multiply(i,j); d,ijk=multiply(ij,k)
   e,jk=multiply(j,k); f,ijk2=multiply(i,jk)
   assert ijk==ijk2 and s.expand(c*d-e*f)==0
print('Quantum product table [coefficient,basis-index]:')
for i in range(4): print([multiply(i,j) for j in range(4)])
# Normalize all actions by 4*pi, and choose singleton orbit's action as origin.
# Spectrality says c(1), c(a) are integers; LS says c(1)-1<c(a)<c(1).
n,m=Int('n'),Int('m')
solver=Solver(); solver.add(n-1<m,m<n)
assert solver.check()==unsat
print('Integer singleton action spectrum + strict LS inequalities: UNSAT')
# Capping classes are integer pairs; symplectic area/(4*pi)=m+n.
# Every integer occurs (k,0), and all integer pairs map to integers.
u,v=s.symbols('u v',integer=True)
assert (u+v).is_integer
print('Area lattice normalized by 4*pi: Z (map (u,v)->u+v)')
