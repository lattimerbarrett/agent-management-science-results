import sympy as s
# The autonomous Hamiltonian pi*(x_3+y_3) rotates both spheres by pi.
R=s.diag(-1,-1,1)
print('Kernel of R-I:', (R-s.eye(3)).nullspace())
poles=[s.Matrix([0,0,1]),s.Matrix([0,0,-1])]
fixed=[(tuple(x),tuple(y)) for x in poles for y in poles if R*x==x and R*y==y]
print('Fixed points:',fixed)
print('Number:',len(fixed))
# At these points, Dphi-I is -2 I in each two-dimensional tangent space.
print('Tangent determinant:',(-2)**4)
