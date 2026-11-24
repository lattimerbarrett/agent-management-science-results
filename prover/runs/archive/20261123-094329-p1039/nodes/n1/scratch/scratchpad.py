import sympy as s
x,a,b=s.symbols('x a b', positive=True)
# rho=(|z1|^2-a)^2+sum_{j>1}|zj|^2-b.
# On the boundary at z1=0, |z'|^2=b-a^2, the complex tangent
# includes e1 and n-2 transverse z' directions.
print('Tangential Levi eigenvalues at z1=0:', -2*a, 'and 1 with multiplicity n-2')
# For the standard smooth solid torus rho=(log |z1|)^2+|zprime|^2-r^2
r=s.symbols('r', positive=True)
f=s.log(x)**2/4
print('z1 Levi coefficient of (log |z1|)^2:',s.simplify(s.diff(f,x)+x*s.diff(f,x,2)))
print('Projection from complement of A x closed ball to C\\A is not defined as a map into C\\A: points with z1 in A and zprime outside the ball remain in the complement.')