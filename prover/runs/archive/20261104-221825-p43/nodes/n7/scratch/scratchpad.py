import sympy as s
Q=s.Matrix([[0,1],[1,0]])
print('Intersection form of S2 x S2:',Q)
print('determinant:',Q.det(),' eigenvalues:',Q.eigenvals())
print('Signature: 0; rank: 2; primitive isotropic classes: (1,0), (0,1).')
