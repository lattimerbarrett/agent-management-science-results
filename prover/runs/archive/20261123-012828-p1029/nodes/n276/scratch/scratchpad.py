import sympy as s
# Verify the two algebraic certificates used in the repaired reduction.
t,u,v,a,b=s.symbols('t u v a b', real=True)
next_a=(1-t)*a+t*b
assert s.expand(next_a-a-t*(b-a))==0
x=s.symbols('x',real=True)
g=s.Matrix([[1,x],[x,x*x]])/(1+x*x)
E=s.diag(1,0)
assert s.simplify(g*g-g)==s.zeros(2)
assert s.simplify(g*(2*E-s.eye(2))*g-(1-x*x)/(1+x*x)*g)==s.zeros(2)
print('Graph and constant-gap interpolation identities checked.')
print('Analytic conclusion from the verified finite-factor graph closure:')
print('a bounded monotone quasitrace-Cauchy sequence has a limit in M.')
print('Leastness in full self-adjoint order follows by compressing an arbitrary')
print('self-adjoint upper bound to the full-dimension cutoff projections.')
print('A missing supremum therefore forces non-Cauchy tails; interpolation')
print('then constructs constant-gap sequences with the same upper bounds.')
print('This proves an equivalence, not the missing unconditional monotone-completeness theorem.')
