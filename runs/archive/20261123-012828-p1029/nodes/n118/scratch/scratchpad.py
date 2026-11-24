import sympy as s
# Audit a tempting projection-join proof. Graphs of distinct scalar
# operators already span the whole two-dimensional space, so their
# joins cannot serve as graph projections of the desired supremum.
u=s.Matrix([1,0]); v=s.Matrix([1,1])
P=u*u.T/(u.T*u)[0]
Q=v*v.T/(v.T*v)[0]
print('Graph projection for 0:',P)
print('Graph projection for 1:',Q)
print('Rank of their joined ranges:',s.Matrix.hstack(u,v).rank())
print('Thus one must invoke the actual finite-AW* monotone sequential completeness theorem, not a bare graph-projection join.')
