import sympy as s
n=s.symbols('n', integer=True, positive=True)
p,u,dp,du,H=s.symbols('psi u dpsi du H', nonzero=True)
b=(n-2)/(2*(n-1))
# After taking out psi^(-n/(n-2)), the transformed Robin operator is:
transformed=du-u*dp/p+b*(H+2*(n-1)/(n-2)*dp/p)*u
original=du+b*H*u
print('Conformal Robin covariance residual:',s.simplify(transformed-original))
# Linearization under a boundary deformation of normal speed f.
f_lap,f,A2,Ricnn,v_normal=s.symbols('Delta_boundary_f f A_squared Ric_normal_normal dnu_v')
Hprime=-f_lap-(A2+Ricnn)*f
print('Robin condition linearized about a constant solution on a minimal boundary:')
print(s.Eq(v_normal, -b*Hprime))
print('In flat ambient space at a flat boundary:')
print(s.Eq(v_normal,b*f_lap))
