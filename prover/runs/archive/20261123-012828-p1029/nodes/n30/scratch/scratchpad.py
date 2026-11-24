import sympy as s
# A finite increasing sequence shows why joining spectral cuts is NOT
# the passage from projection completeness to an ordinary order supremum.
A=s.diag(1,0)
B=s.Matrix([[2,1],[1,1]])
print('B-A eigenvalues:', (B-A).eigenvals())
t=s.Rational(1,2)
lo=(3-s.sqrt(5))/2
hi=(3+s.sqrt(5))/2
Q=s.simplify((B-lo*s.eye(2))/(hi-lo))
P=A
print('spectral cut of A above 1/2:',P)
print('spectral cut of B above 1/2:',Q)
print('det(Q-P):',s.simplify((Q-P).det()))
print('rank(join of the cuts):',s.Matrix.hstack(P,Q).rank())
print('Yet the ordinary supremum of A,B,B,... is B.')
