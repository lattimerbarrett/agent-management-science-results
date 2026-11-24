import sympy as s
x=s.symbols('x', positive=True)
rho=s.log(x)**2/4
print('Solid torus defining function: (log |z1|)^2 + ||zprime||^2 - r^2')
print('Levi coefficient in z1:', s.simplify(s.diff(rho,x)+x*s.diff(rho,x,2)))
print('Other Levi coefficients: 1')
print('It is strictly pseudoconvex and has a Stein neighbourhood basis.')
print('Nevertheless it is not polynomially convex: its central unit circle has the unit disc in its polynomial hull.')
print('Thus the polynomially convex complement theorem alone does not settle the question.')