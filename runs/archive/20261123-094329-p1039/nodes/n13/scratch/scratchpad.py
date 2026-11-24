import sympy as s
x=s.symbols('x', positive=True)
f=s.log(x)**2/4
print('rho = (log|z1|)^2 + sum_{j>=2}|zj|^2 - 4')
print('Levi coefficient in z1:',s.simplify(s.diff(f,x)+x*s.diff(f,x,2)))
print('Other Levi coefficients: 1')
print('Minimum |z1| on K: exp(-2); maximum: exp(2)')
print('For 1 <= |z1| <= 2 and ||zprime|| <= 1:')
print('rho <= log(2)^2 + 1 - 4 =',s.N(s.log(2)**2-3))
print('Thus this is a smooth strongly pseudoconvex solid torus containing the indicated Hartogs ring. A rank obstruction for entire maps is still required to infer non-Okaness.')