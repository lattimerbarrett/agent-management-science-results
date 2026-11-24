import sympy as S
# Rational spectral example of a nonmaximal s=2 two-cycle.
x=list(map(S.Integer,[-3,-1,1,3]))
w=list(map(S.Rational,[S.Rational(3,16),S.Rational(5,16),S.Rational(5,16),S.Rational(3,16)]))
y=S.Matrix([S.sqrt(v) for v in w]); V=S.Matrix([[yi,yi*xi] for xi,yi in zip(x,y)])
q=S.diag(*[xi**2-4 for xi in x]); Q=S.diag(*[xi**2-6 for xi in x]); H2=S.Integer(15)
assert q*Q==H2*S.eye(4)
assert V.T*q*y==S.zeros(2,1)
K=V*(V.T*V).inv()*V.T
DK=q*V
A=DK*(DK.T*DK).inv()*DK.T
B=q.inv()*K*q
assert A*B==A and B*A==B
N=A-B
assert S.simplify(N*N)==S.zeros(4)
assert S.simplify(N*y)==S.zeros(4,1)
P=S.eye(4)-y*y.T
shear=S.simplify(P*N)
assert S.simplify(shear*shear)==S.zeros(4)
assert shear.rank()==1
print('Exact nonmaximal two-cycle: H²=15, tangent Jacobian I+2N; N²=0, rank N=1.')
