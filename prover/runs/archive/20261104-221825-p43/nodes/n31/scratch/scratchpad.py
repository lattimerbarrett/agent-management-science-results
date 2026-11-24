import sympy as s
# Cohomology coordinates in the two sphere-factor classes.
omega=s.Matrix([4*s.pi,4*s.pi])
c1=s.Matrix([2,2])
print('Monotonicity: [omega] - 2*pi*c1 =',omega-2*s.pi*c1)
R=s.diag(-1,-1,1)
print('Half-turn fixed space:',(R-s.eye(3)).nullspace())
print('Half-turn tangent eigenvalues at each pole:',[-1,-1])
print('Number of fixed points on the product:',2*2)
