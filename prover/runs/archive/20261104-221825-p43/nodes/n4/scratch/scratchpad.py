import sympy as s
# Fixed-point equations for a coupling flow followed by half turns about
# perpendicular axes: x=(u,0,z), y=(0,v,-z), v=+-u.
u,z=s.symbols('u z', real=True)
x=s.Matrix([u,0,z]); y=s.Matrix([0,u,-z]); S=x+y
print('sum:',S.T)
print('S cross x:',S.cross(x).T)
print('target:',s.diag(1,-1,-1)*x)
print('squared sum:',s.expand(S.dot(S)))
