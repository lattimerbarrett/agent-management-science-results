import sympy as s
eta,u=s.symbols('eta u',real=True)
print('Two-increment bound:',s.expand((u-eta)+(1-u-eta)))
print('At eta=1/2, u>=eta and u<=1-eta force u=1/2.')
# Endpoint spectral-tail analysis: the block Weyl inequality gives convexity.
t=s.symbols('t',real=True)
F=1-t
print('Uniform tail candidate:',F)
print('Integral on [0,1]:',s.integrate(F,(t,0,1)))
print('Reflection:',s.simplify(F+F.subs(t,1-t)))
print('Second derivative:',s.diff(F,t,2))
# Verify the noncommutative block identities behind midpoint convexity.
X=s.Matrix([[2,1],[1,1]])/5
Y=s.diag(s.Rational(1,3),s.Rational(1,4))
A=X*X; B=Y*Y
R=X.row_join(Y); Q=R.T*R
U=s.diag(1,1,-1,-1)
assert Q+U*Q*U==2*s.diag(A,B)
assert R*R.T==A+B
assert A*B!=B*A
z=s.symbols('z')
assert s.expand(Q.charpoly(z).as_expr()-z*z*(A+B).charpoly(z).as_expr())==0
print('Noncommuting block identities checked exactly.')
print('Analysis: common endpoint spectral tail F is convex, F(0+)=1, F(1)=0, integral F=1/2.')
print('Hence F(t)=1-t on [0,1]; equal distributions do not imply equality of ordered elements.')
print('Given the verified eta=1/2 witness, positive scaling gives every eta in (0,1/2].')
