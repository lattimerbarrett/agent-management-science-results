import sympy as s
r,L=s.symbols('r L', positive=True, real=True)
# For rho(g,t)=||g||^2+|t|^4-|t|^2-1, evaluate
# g=(sqrt(17)/4,2 L^2 z^2), t=Lz, with r=|z|^2.
val=s.Rational(17,16)+4*L**4*r**2+L**4*r**2-L**2*r-1
certificate=5*L**4*(r-1/(10*L**2))**2+s.Rational(1,80)
assert s.simplify(val-certificate)==0
print('Entire-curve avoidance identity verified:')
print(s.Eq(val,certificate,evaluate=False))
print('The right side is strictly positive for every r>=0, L>0.')
print('Thus a negative obstacle Levi eigenvalue is not detected by the scalar entire-curve obstruction.')
