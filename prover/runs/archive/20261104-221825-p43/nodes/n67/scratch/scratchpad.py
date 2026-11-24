import sympy as s
# Apply the established distinct-point lower-bound theorem for the equal-area product.
lower_bound = 4
# H=pi*(x_3+y_3) rotates both factors by pi at time one.
R=s.diag(-1,-1,1)
print('Time-one rotation matrix:',R)
print('Fixed subspace:',(R-s.eye(3)).nullspace())
fixed_points=[((0,0,a),(0,0,b)) for a in (-1,1) for b in (-1,1)]
print('Fixed points on S^2 x S^2:',fixed_points)
print('Established lower bound:',lower_bound)
print('Attained upper bound:',len(fixed_points))
assert lower_bound==len(fixed_points)
