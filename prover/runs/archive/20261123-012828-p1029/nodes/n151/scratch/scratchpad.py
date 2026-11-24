import sympy as s
# Audit a tempting 2x2-block proof of a stronger quasitrace bound.
# Positivity of [[S^2, sqrt(S) C sqrt(S)], [...,C^2]] would be useful,
# but it is false even for rational positive 2x2 matrices.
S=s.diag(1,4)
R=s.diag(1,2)
C=s.Matrix([[2,1],[1,2]])
H=R*C*R
B=(S*S).row_join(H).col_join(H.row_join(C*C))
print('S =',S)
print('C =',C)
print('det(block matrix) =',B.det())
print('eigenvalues approximately =',[complex(v) for v in B.evalf().eigenvals()])
assert B.det()<0
print('Thus this proposed block-positivity shortcut cannot justify a Schwarz inequality.')
