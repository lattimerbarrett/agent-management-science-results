import sympy as s
R = s.Matrix([[0,-1,0],[1,0,0],[0,0,1]])
print('Fixed subspace of a quarter-turn:', (R-s.eye(3)).nullspace())
print('Each fixed subspace meets S^2 in 2 points; product fixed-point count:', 2*2)
