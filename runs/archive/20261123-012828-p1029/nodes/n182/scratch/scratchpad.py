import sympy as s
x=s.Matrix([[s.Rational(1,3),0],[0,0]])
y=s.Matrix([[s.Rational(1,4),s.Rational(1,4)],[s.Rational(1,4),s.Rational(1,4)]])
b0=x*x; b1=y*y
R=x.row_join(y)
G=R.T*R
S=R*R.T
Z=s.zeros(2)
V=R.col_join(s.zeros(2,4))
assert V.T*V == G
assert V*V.T == S.row_join(Z).col_join(Z.row_join(Z))
assert S == b0+b1
print('Exact row identities verified:')
print('V* V = R* R; V V* = diag(b0+b1,0).')
print('I - (b0+b1) positive definite:', (s.eye(2)-S).is_positive_definite)
print('Gram diagonal blocks:', G[:2,:2], G[2:,2:])
print('Off-diagonal Gram block:',G[:2,2:])
print('Quasitrace conclusion: q2(G)=q(b0+b1)<=q(1).')
print('NOT established by this identity: q2(G)=q(b0)+q(b1).')
