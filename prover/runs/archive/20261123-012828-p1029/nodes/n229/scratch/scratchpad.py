import sympy as s
# Finite-matrix certificates for graph gluing formulas.
Y=s.Matrix([[s.Rational(1,2),s.Rational(1,3)],[0,s.Rational(1,2)]])
I=s.eye(2); Z=s.zeros(2)
C=I.col_join(Y)
G=C*(I+Y.T*Y).inv()*C.T
P=s.diag(1,1,0,0)
print('graph projection:',G*G==G, G.T==G)
# Inverse in G-corner computed by adjoining the complement.
R=(G*P*G+s.eye(4)-G).inv()*G
X=(s.eye(4)-P)*G*R*G*P
print('reconstructed graph operator:',X[2:4,0:2]==Y)
print('full horizontal range:',s.simplify(P*G*R*G*P)==P)
print('compressed angle eigenvalues for K=1:',(C.T*s.diag(1,1,-1,-1)*C).eigenvals())
print('This checks finite identities, not the AW*-dimension continuity theorem.')
