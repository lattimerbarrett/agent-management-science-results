import sympy as s
# Quantum multiplication in basis (1,A,B,P), with A^2=B^2=q and P=AB.
q=s.symbols('q', nonzero=True)
LA=s.Matrix([[0,q,0,0],[1,0,0,0],[0,0,0,q],[0,0,1,0]])
LB=s.Matrix([[0,0,q,0],[0,0,0,q],[1,0,0,0],[0,1,0,0]])
print('A^2=qI:', LA**2==q*s.eye(4))
print('B^2=qI:', LB**2==q*s.eye(4))
print('commute:', LA*LB==LB*LA)
print('Global Floer rank:',4,'; hypothetical three local ranks:',[1,2,1])
print('Thus rank alone does not exclude three; the established lower bound needs more than this rank calculation.')
# Half turn on each sphere.
R=s.diag(-1,-1,1)
x,y,z=s.symbols('x y z', real=True)
print('fixed equations on one sphere:',list((R-s.eye(3))*s.Matrix([x,y,z])), x*x+y*y+z*z-1)
print('one-sphere fixed points:',[(0,0,-1),(0,0,1)])
print('product count:',2*2)
print('tangent fixed-point determinant:',(-2)**4)
