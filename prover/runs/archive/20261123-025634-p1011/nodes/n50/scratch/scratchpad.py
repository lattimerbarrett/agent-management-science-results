import sympy as s
n,r,z,F,E,D=s.symbols('n r z F E D', positive=True)
# r denotes squared tangential radius; E=x'.grad f; D=Delta' f.
a=(n-2)/2
U=(1+r+z*z)**(-a)
V=s.diff(U,z)
lapV=4*r*s.diff(V,r,2)+2*(n-1)*s.diff(V,r)+s.diff(V,z,2)
potential=n*(n+2)/(1+r+z*z)**2
assert s.simplify(-lapV-potential*V)==0
print('CHECK: V=partial_n U is an exact full-space Jacobi field.')
beta=(n-2)/(2*(n-1))
# Physical first Robin variation = grad f.grad U - f U_nn + beta Delta f U.
physical=s.simplify(2*E*s.diff(U,r).subs(z,0)-F*s.diff(U,z,2).subs(z,0)+beta*D*U.subs(z,0))
expected=(n-2)*(F-E)*(1+r)**(-n/2)+beta*D*(1+r)**(-(n-2)/2)
assert s.simplify(physical-expected)==0
print('CHECK: exact first physical Robin residual:',s.factor(physical))
# Direct first energy variation cancels against the curvature boundary term.
u0=U.subs(z,0)
k=n*(n-2); q=2*n/(n-2);c=(n-2)/(4*(n-1))
D0=s.Rational(1,2)*4*r*s.diff(u0,r)**2 - (n-2)**2/s.Integer(2)*(1+r)**(-n)
lap_u02=4*r*s.diff((1+r)**(-(n-2)),r,2)+2*(n-1)*s.diff((1+r)**(-(n-2)),r)
assert s.simplify(D0-c*lap_u02)==0
print('CHECK: fixed-ambient-bubble first shape derivative vanishes.')
print('Exact flattened quadratic coefficient: B_f - (1/2)<R_f,A^{-1}R_f>, B_f=(1/2) integral |grad f|^2 U_n^2.')
print('Let W=f U_n. Jacobi integration by parts gives A(W,W)=2 B_f, and R_f(W)=-2 B_f.')
print('Thus shifting to the physical bubble gives R_phys=R_f+A W and direct coefficient B_f+R_f(W)+A(W,W)/2=0.')
print('For each FIXED compactly supported smooth f the coefficient is consequently -(1/2)<R_phys,A^{-1}R_phys>.')
print('These identities alone give no uniform nonlinear remainder for epsilon-dependent polynomial/cutoff shapes.')
