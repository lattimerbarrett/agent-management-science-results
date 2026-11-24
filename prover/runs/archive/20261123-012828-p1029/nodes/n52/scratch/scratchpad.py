import sympy as s
# Full graphs of the scalar contractions 0 and 1.
g0=s.Matrix([1,0]);g1=s.Matrix([1,1])
p0=g0*g0.T/(g0.T*g0)[0]
p1=g1*g1.T/(g1.T*g1)[0]
J=s.diag(1,-1)
print('graph projection 0:',p0)
print('graph projection 1:',p1)
print('angle compression for graph 0:',p0*J*p0)
print('angle compression for graph 1:',p1*J*p1)
print('rank of their combined ranges:',s.Matrix.hstack(g0,g1).rank())
print('join angle eigenvalues:',J.eigenvals())
