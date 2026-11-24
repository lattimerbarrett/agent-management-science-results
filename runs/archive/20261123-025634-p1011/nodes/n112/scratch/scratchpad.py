import sympy as s
n,L=s.symbols('n L',integer=True,positive=True)
m=n-1
boundary_laplacian_eigenvalue=-L*(L+n-2)
forcing=s.factor(boundary_laplacian_eigenvalue+m)
print('Eigenvalue of Delta_boundary+(n-1):',forcing)
print('Degree zero:',forcing.subs(L,0))
print('Degree one (conformal kernel):',forcing.subs(L,1))
print('Degree zero resonance: x_(n+1) solves (Delta_S+n)v=0;')
print('its boundary trace is 0 and its outward normal derivative is -1.')
print('Thus a constant Neumann source must be solved by this resonance, not by inverting a Dirichlet-to-Neumann eigenvalue.')
# Check coordinate/base-point change of the optimized quadratic coefficient.
a,b,r1,r2,w1,w2,B=s.symbols('a b r1 r2 w1 w2 B',nonzero=True)
A=s.diag(a,b); R=s.Matrix([r1,r2]); W=s.Matrix([w1,w2])
old=B-(R.T*A.inv()*R)[0]/2
newR=R+A*W
newB=B+(R.T*W)[0]+(W.T*A*W)[0]/2
new=newB-(newR.T*A.inv()*newR)[0]/2
print('Full Schur-complement change under a coordinate/base shift:',s.simplify(new-old))
print('This checks structural consistency only; it does not certify the claimed PDE gluing or compactness proofs.')
