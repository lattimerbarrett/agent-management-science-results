import sympy as s

t = s.symbols('t', real=True)
x = s.Matrix([s.sin(t), 0, s.cos(t)])
y = s.Matrix([s.sin(t), 0, -s.cos(t)])
assert s.trigsimp(x.dot(x)-1) == 0
assert s.trigsimp(y.dot(y)-1) == 0
assert s.simplify(x[2]+y[2]) == 0
# The squared norm of the gradient of z_1+z_2 on the product.
grad_sq = s.trigsimp(2-x[2]**2-y[2]**2)
assert s.trigsimp(grad_sq-2*s.sin(t)**2)==0
speed_sq = s.trigsimp(x.diff(t).dot(x.diff(t))+y.diff(t).dot(y.diff(t)))
assert speed_sq == 2
print('Arc: sphere constraints, level-zero constraint, gradient norm and embedding speed checked.')

for e1 in [-1,1]:
    for e2 in [-1,1]:
        hess = s.diag(-e1,-e1,-e2,-e2)
        index = sum(1 for v in hess.diagonal() if v < 0)
        assert hess.det() == 1
        print('Critical point pole signs:',(e1,e2),'value:',e1+e2,'Morse index:',index)

r = s.symbols('r', positive=True)
b = s.exp(-1/r**2)
for k in range(9):
    derivative = s.diff(b, r, k)
    assert s.limit(derivative, r, 0, dir='+') == 0
    # Check stronger domination by powers needed in the radial smoothing.
    for power in range(9):
        assert s.limit(derivative/r**power, r, 0, dir='+') == 0
print('Flat radial function: derivatives through order 8, divided by r^j for j<=8, checked.')

# The radial ellipsoid parametrization has positive Jacobian.
# psi(r,u)=(a(r)u_1,b(r)u_2,...,b(r)u_4), a=1+b.
# Its Jacobian relative to dr times spherical volume is
# a*b^3 * ((a'/a)*u_1^2 + (b'/b)*(1-u_1^2)).
v = s.symbols('v', nonnegative=True)
a = 1+b
expr = s.factor(a*b**3*((s.diff(a,r)/a)*v+(s.diff(b,r)/b)*(1-v)))
assert s.simplify(expr - 2*b**3*(1+b-v)/r**3)==0
print('Ellipsoid radial Jacobian =', expr)
print('Strictly positive for r>0 and 0<=v<=1, since 1+b-v >= b > 0.')
