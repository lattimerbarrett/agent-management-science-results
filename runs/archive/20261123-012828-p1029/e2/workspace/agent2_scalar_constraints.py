"""Exact checks for necessary scalar constraints, not an AW*-existence test."""
import sympy as s
from z3 import Real, Solver, sat, unsat
eta,t0,t1,t2= [Real(x) for x in ('eta','t0','t1','t2')]
# t_i=tau(a_i); order and complement bound for each positive increment.
constraints=[eta>0,0<=t0,t0<=t1,t1<=t2,t2<=1,
             eta<=t1,eta<=1-t0,eta<=t2,eta<=1-t1]
solver=Solver(); solver.add(*constraints,eta>s.Rational(1,2).__str__())
assert solver.check()==unsat
for t in [t1]:
    solver=Solver(); solver.add(*constraints,eta==0.5,t!=0.5)
    assert solver.check()==unsat
print('Exact Z3 certificates: eta>1/2 impossible; eta=1/2 forces tau(a_1)=1/2.')
# t_n telescoping identity in the additive case, all N up to 100.
for N in range(1,101):
    ts=s.symbols('t:'+str(N+1))
    assert s.expand(sum(ts[k+1]-ts[k] for k in range(N))-(ts[-1]-ts[0]))==0
print('Symbolic telescoping verified for N=1,...,100.')
# Endpoint is NOT ruled out by these scalar constraints: check satisfiability.
solver=Solver(); solver.add(*constraints,eta==0.5)
assert solver.check()==sat
print('Endpoint scalar relaxation is satisfiable:', solver.model())
from pathlib import Path
Path('workspace/agent2_scalar_constraints.py').write_text(Path('scratchpad.py').read_text())

