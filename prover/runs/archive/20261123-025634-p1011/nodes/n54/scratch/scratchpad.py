import runpy
import sympy as s
# Exact critical Pohozaev identity: no polynomial truncation of the boundary.
runpy.run_path('experiments/e4/agent3_pohozaev_checks.py',run_name='__main__')
n,R,Rs,A2,phi=s.symbols('n R R_boundary II_squared phi', real=True)
# For a minimal boundary: Ric(nu,nu)=(R-R_boundary-|II|^2)/2.
# Codazzi + tangential integration adds phi*|II|^2 to the normal tracefree-Ricci flux.
coefficient=s.expand((R-Rs-A2)/2-R/n+A2)
assert s.simplify(coefficient-((n-2)*R/(2*n)-Rs/2+A2/2))==0
print('\nGeometric conformal-Killing Pohozaev boundary coefficient:')
print(coefficient)
print('It contains boundary scalar curvature and the full second fundamental form; no jet truncation has been used.')
print('This identity alone has no universal pointwise sign on arbitrary boundary graphs.')
# Check the scalar-curvature normalization for applying the established exclusion.
c=(n-2)/(4*(n-1))
assert s.simplify(n*(n-2)/c-4*n*(n-1))==0
assert s.simplify((2**((n-2)/2))**(4/(n-2)))==4
print('\nConformal solution metric: scalar curvature 4*n*(n-1), mean curvature zero.')
print('Multiplying u by 2^((n-2)/2) gives the standard scalar-curvature n*(n-1) normalization.')
