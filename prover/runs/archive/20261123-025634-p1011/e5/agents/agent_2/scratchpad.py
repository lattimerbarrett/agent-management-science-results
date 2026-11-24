import sympy as s
from pathlib import Path
n,t,f,G,L,K=s.symbols('n t f G L K', positive=True)
m=n-1;c=(n-2)/(4*(n-1));u02=2**(-(n-2))
a=s.cos(t*f)
W=s.sqrt(1+t*t*G/a**2)
H=m*s.tan(t*f)/W+t*t*s.sin(t*f)*G/(a**3*W**3)+t*L/(a*a*W)-t**3*K/(a**4*W**3)
area=a**m*W
H3=s.series(H,t,0,4).removeO().expand()
assert s.simplify(H3.coeff(t,1)-(L+m*f))==0
assert H3.coeff(t,0)==0 and H3.coeff(t,2)==0
assert s.simplify(H.subs(t,-t)+H)==0
assert s.simplify(area.subs(t,-t)-area)==0
# Constant solution u0=2^(-(n-2)/2), so u0^(q-2)=1/4.
cR=n*(n-2)/4
potential_hessian=s.simplify(cR-n*(n+2)/4)
assert potential_hessian==-n
bulk_density=s.simplify(cR*u02/2-(n-2)**2*u02/8)
assert s.simplify(bulk_density-(n-2)*u02/4)==0
# int L=0, int H'=m int f, volume'=-int f
assert s.simplify(-bulk_density+c*u02*m)==0
print('Exact round graph H first term = Laplacian f +(n-1) f')
print('Exact odd H, even area; all direct second shape terms vanish.')
print('Constant energy first shape coefficient cancels exactly.')
print('Jacobi potential exactly',potential_hessian)
print('Cubic H term:',s.factor(H3.coeff(t,3)))
Path('workspace/agent2_round_shape_audit.py').write_text(Path('scratchpad.py').read_text().split("Path('workspace/agent2_round_shape_audit.py')")[0])
