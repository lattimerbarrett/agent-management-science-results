import sympy as s
# Symbolic residual coefficient for successive convex interpolation.
t0,t1,t2=s.symbols('t0 t1 t2', real=True)
x,z0,z1,z2=s.symbols('x z0 z1 z2')
y=(1-t0)*x+t0*z0
y=(1-t1)*y+t1*z1
y=(1-t2)*y+t2*z2
P=(1-t0)*(1-t1)*(1-t2)
remainder=t0*(1-t1)*(1-t2)*z0+t1*(1-t2)*z1+t2*z2
assert s.expand(y-P*x-remainder)==0
assert s.expand(t0*(1-t1)*(1-t2)+t1*(1-t2)+t2-(1-P))==0
print('Interpolation residual identity verified exactly.')
print('All target coefficients are nonnegative for 0<=t_i<=1, and sum to 1-P.')
# Verify this calculation does not require commutation.
I=s.eye(2); Z=s.zeros(2)
S=s.diag(s.Rational(1,8),0)
R=s.Matrix([[1,1],[1,1]])/16
T=S+R
assert S*T!=T*S
u=s.Rational(1,3); v=s.Rational(2,5)
A0=Z
A1=(1-u)*A0+u*S
A2=(1-v)*A1+v*T
assert A2-((1-u)*(1-v)*A0+u*(1-v)*S+v*T)==Z
print('Exact noncommuting matrix interpolation identity verified.')
print('If every interpolation weight is >=eta>0, P_r<=(1-eta)^r -> 0.')
print('Hence upper bounds of the interpolated sequence also bound every fixed target.')
