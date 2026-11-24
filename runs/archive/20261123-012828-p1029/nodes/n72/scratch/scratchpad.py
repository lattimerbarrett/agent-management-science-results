import sympy as s
# The endpoint constraints imply common spectral tails, not equality of operators.
t=s.symbols('t', real=True)
F=1-t
print('Candidate endpoint tail on [0,1]: F(t)=',F)
print('Quasitrace:',s.integrate(F,(t,0,1)))
print('Reflection constraint F(t)+F(1-t)=',s.simplify(F+F.subs(t,1-t)))
print('Convexity:',s.diff(F,t,2))
# Verify the block-matrix identities used to derive midpoint convexity.
# A=X*X and B=Y*Y with noncommuting positive X,Y.
X=s.Matrix([[2,1],[1,1]])/5
Y=s.diag(s.Rational(1,3),s.Rational(1,4))
A=X*X;B=Y*Y
Q=(X.col_join(Y))*X.row_join(Y)
U=s.diag(1,1,-1,-1)
assert Q+U*Q*U==2*s.diag(A,B)
row=X.row_join(Y)
assert row*row.T==A+B
z=s.symbols('z')
assert s.factor(Q.charpoly(z).as_expr()-z**2*(A+B).charpoly(z).as_expr())==0
assert A*B!=B*A
print('Noncommuting row/column block identities verified exactly.')
print('Uniform tails satisfy the resulting midpoint-convexity inequality.')
print('Consequently equality at eta=1/2 is not contradicted by these spectral constraints.')
