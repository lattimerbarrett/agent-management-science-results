import sympy as s
# Model complement in C^3:
# D = {Re(w)+|z|^2-|u|^2 < 0}; its obstacle has defining
# function rho_K=-Re(w)-|z|^2+|u|^2 and mixed tangent Levi form.
L_D=s.diag(1,-1)
print('Complement tangential Levi matrix:', L_D)
print('Obstacle tangential Levi matrix:', -L_D)
# Test a full-dimensional polynomial map that attempts to use the
# negative square to dominate all positive terms.
a,b,c,M=s.symbols('a b c M', real=True)
w=-1+a
z=b
u=c+M*(a*a+b*b)
r=w+z*z-u*u
P=s.Matrix([w,z,u])
print('Jacobian determinant of candidate:',s.det(P.jacobian([a,b,c])))
print('Defining function on the cancellation locus u=0:',s.expand(r.subs(c,-M*(a*a+b*b))))
print('At a=0,b=2,c=-4*M:',s.simplify(r.subs({a:0,b:2,c:-4*M})))
print('Thus this full-rank polynomial candidate does not map into D.')