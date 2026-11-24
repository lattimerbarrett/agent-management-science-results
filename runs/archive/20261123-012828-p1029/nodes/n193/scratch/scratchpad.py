import sympy as s
eta, alpha0, alphaN, N = s.symbols('eta alpha0 alphaN N', positive=True)
# For a witness, the total positive-additivity defect is unavoidable.
# D_n = tau(a_n) + tau(a_{n+1}-a_n) - tau(a_{n+1}).
print('Sum of defects:', alpha0 + N*eta-alphaN)
print('Average defect limit:', s.limit((alpha0+N*eta-alphaN)/N,N,s.oo))
# Two increments give eta <= u <= 1-eta, without additivity.
from z3 import Real, Solver, sat
u,e=Real('u'),Real('e')
solver=Solver(); solver.add(e>0,e<=u,u<=1-e)
solver.push(); solver.add(e> s.Rational(1,2).__str__()); print('eta > 1/2 feasible:',solver.check()); solver.pop()
solver.push(); solver.add(e==s.Rational(1,3).__str__()); print('eta = 1/3 scalar constraints:',solver.check()); solver.pop()
print('A verified witness directly refutes monotone sequential completeness for its M; metric completeness alone does not supply the missing Cauchy property.')
