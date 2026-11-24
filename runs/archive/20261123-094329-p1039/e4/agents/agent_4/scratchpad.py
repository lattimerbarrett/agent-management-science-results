import sympy as s
x=s.symbols('x', real=True)
r2=(s.sqrt(17)-1)/8
levi=s.simplify(1-7*r2)
assert s.simplify(r2+4*r2**2)==1
assert levi<0
# rho=sum |z_j|^2+4(sum |z_j|^2)^2-15|z1|^2|z2|^2-1.
# Quartic >= (sum |z_j|^2)^2 /4 by ab <= (a+b)^2/4.
# Radial derivative of rho(t*z) is 2tR+4t^3 P, positive if z != 0.
print({'r_squared':r2,'negative_tangential_levi':levi,'numerical_levi':float(levi)})
a,g=s.symbols('a g', positive=True)
bx,by,c,t=s.symbols('bx by c t', real=True)
A=( (bx**2+by**2)/a+t+1 )/(2*g**2)
H=s.Matrix([[a,bx+s.I*by],[bx-s.I*by,c+2*A*g**2]])
assert s.simplify(H.det()-a*(c+t+1))==0
# t=abs(c) ensures c+t>=0, so det(H)>=a>0.
# This checks normal rank-one correction of tangentially positive Levi matrix.
print('Rank-one Levi correction determinant:',s.simplify(H.det()))
open('workspace/agent4_nonpseudo_quartic.txt','w').write('Candidate all n>=2: rho=R+4R^2-15|z1|^2|z2|^2-1, R=sum |zj|^2. Quartic P>=R^2/4>0 away from 0; bounded smooth starshaped domain. At q=(sqrt((sqrt(17)-1)/8),0,...), v=e2 is complex tangent, Levi rho(v)=1-7*(sqrt(17)-1)/8<0. Oka complement not proved.\n')