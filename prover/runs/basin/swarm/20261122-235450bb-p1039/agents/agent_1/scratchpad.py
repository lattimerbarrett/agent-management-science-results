import sympy as s
# Strictly pseudoconvex quadratic local model in C^2.
x,y,u,v,a,M=s.symbols('x y u v a M', real=True)
r=2*u+a*(x*x+y*y)
rtilde=r+M*r*r
vs=(x,y,u,v)
H=s.hessian(rtilde,vs).subs({x:0,y:0,u:0,v:0})
# Complex Levi matrix at zero; z=x+iy, w=u+iv.
L=s.Matrix([[ (H[0,0]+H[1,1])/4,
  (H[0,2]+H[1,3]+s.I*(H[0,3]-H[1,2]))/4],
 [(H[2,0]+H[3,1]+s.I*(H[2,1]-H[3,0]))/4,
 (H[2,2]+H[3,3])/4]])
assert L==s.diag(a,2*M)
# The Levi polynomial is h=w+M*w^2 for this model.
reh=u+M*(u*u-v*v)
assert s.expand(rtilde-2*reh-a*(x*x+y*y)-2*M*(u*u+v*v)) == s.expand(4*M*a*u*(x*x+y*y)+M*a*a*(x*x+y*y)**2)
# A polynomial defining function with negative tangential Levi for K.
rho=-r
assert s.diff(rho,x,2)/4+s.diff(rho,y,2)/4 == -a
b,d,c=s.symbols('b d c', real=True)
B=s.Matrix([[a,b+s.I*d],[b-s.I*d,c+2*M]])
assert s.expand(B.det()-(a*(c+2*M)-b*b-d*d)) == 0
assert s.simplify(B.det().subs(M,(b*b+d*d-a*c+a)/(2*a))) == a
print('Verified local Levi matrix:', L)
print('Verified exact Taylor remainder, orientation sign, and general Schur determinant.')
