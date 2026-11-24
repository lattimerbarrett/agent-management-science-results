import sympy as s
A=s.Matrix([[1,0],[0,0]])
C=s.Matrix([[1,1],[1,1]])/2
assert A*A==A and C*C==C
assert (A*C+C*A).det()==-s.Rational(1,4)
print("verified anticommutator obstruction")
