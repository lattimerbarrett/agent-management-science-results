import sympy as s
import json
x,y=s.symbols('x y', real=True)
r=(x*x+y*y-1)**2
# Wirtinger Hessian in one coordinate: rho_{z zbar}=Delta rho/4.
levi=s.simplify((s.diff(r,x,2)+s.diff(r,y,2))/4)
assert s.expand(levi-(4*(x*x+y*y)-2))==0
# At the standard totally real plane R^n in C^n, squared distance
# is sum y_j^2 and its Levi matrix is exactly I/2 in every dimension.
for n in range(2,13):
    xs=s.symbols('x0:'+str(n),real=True)
    ys=s.symbols('y0:'+str(n),real=True)
    rho=sum(t*t for t in ys)
    H=s.Matrix(n,n,lambda j,k:(s.diff(rho,xs[j],xs[k])+s.diff(rho,ys[j],ys[k])+s.I*(s.diff(rho,xs[j],ys[k])-s.diff(rho,ys[j],xs[k])))/4)
    assert H==s.eye(n)/2
result={'torus_radial_Levi':str(levi),'standard_totally_real_plane_Levi_checked_dimensions':list(range(2,13)),'note':'These verify tube Levi formulas only; no Oka/non-Oka claim is checked.'}
open('workspace/agent4_tube_checks.json','w').write(json.dumps(result,indent=2))
open('workspace/agent4_tube_checks.py','w').write(open('scratchpad.py').read())
print(json.dumps(result,indent=2))