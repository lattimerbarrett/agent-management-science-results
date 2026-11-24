import sympy as s
n=s.symbols('n', integer=True, positive=True)
p=(n+2)/(n-2); k=n*(n-2)
u0=2**(-(n-2)/s.Integer(2))
a=n*(n-2)/4
print('Linearized zero-order coefficient:',s.simplify(k*p*u0**(p-1)-a))
print('At n=19: p=',p.subs(n,19))
print('Quadratic interior forcing coefficient divided by u0^(p-2):',s.factor(-k*p*(p-1)/2))
print('At n=19:',s.factor((-k*p*(p-1)/2).subs(n,19)))
print('Resonant Green identity: integral_boundary v = integral_hemisphere z*(Delta+n)v, where z=x_(n+1), z|boundary=0, d_nu z=-1.')
print('At first order with homogeneous interior forcing, mean boundary trace is zero.')
print('At second order, the nonlinear forcing includes -k*p*(p-1)/2*u0^(p-2)*v1^2; its z projection is nonzero for v1 !=0.')
from pathlib import Path
for f in ['experiments/e4/agent2_finite_domain_shape_reduction.md','experiments/e3/agent1_high_dim_analytic_bridge.md']:
 t=Path(f).read_text()
 print('\n',f)
 for i,line in enumerate(t.splitlines()):
  if any(key in line.lower() for key in ['l=0','ell=0','degree-zero','degree zero','resonance']):
   print('\n'.join(t.splitlines()[max(0,i-2):i+4]))
