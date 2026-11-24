import sympy as s
x,y,u,v,a,b=s.symbols('x y u v a b',real=True)
C=[x,y,u,v,a,b]
r=x*x+y*y+u*u+v*v+(a*a+b*b-1)**2-4
psi=-s.log(-r)
def dz(f,j): return (s.diff(f,C[2*j])-s.I*s.diff(f,C[2*j+1]))/2
def db(f,j): return (s.diff(f,C[2*j])+s.I*s.diff(f,C[2*j+1]))/2
for j in range(3):
 for k in range(3):
  H=dz(db(psi,k),j)
  rhs=-dz(db(r,k),j)/r+dz(r,j)*db(r,k)/r**2
  assert s.factor(H-rhs)==0
# Exact positive (n-1)-dimensional restriction has form alpha I+beta cc*.
# Its quadratic form is alpha ||v||²+beta |c*v|² with alpha,beta>0.
assert s.factor(dz(db(r,0),0))==1
assert s.factor(dz(db(r,1),1))==1
assert s.factor(dz(db(r,0),1))==0
assert s.simplify(dz(db(r,2),2)-(4*(a*a+b*b)-2))==0
print('PASS: all nine complex Hessian chain-rule entries; positive horizontal block.')
