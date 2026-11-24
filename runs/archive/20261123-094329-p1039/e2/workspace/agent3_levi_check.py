import sympy as s
lam,a=s.symbols("lam a",positive=True)
br,bi,c,A=s.symbols("br bi c A",real=True)
b=br+s.I*bi
H=s.Matrix([[lam,b],[s.conjugate(b),c+2*A*a*a]])
choice=((br*br+bi*bi)/lam-c+lam)/(2*a*a)
assert s.simplify(H.subs(A,choice).det()-lam*lam)==0
t=s.symbols("t",positive=True)
assert s.simplify(H.subs(A,choice+t).det()-(lam*lam+2*lam*a*a*t))==0
assert lam.is_positive and (lam*lam+2*lam*a*a*t).is_positive
x,y,u,v=s.symbols("x y u v",real=True)
r=s.Function('r')(x,y,u,v)
zo=[lambda f:(s.diff(f,x)-s.I*s.diff(f,y))/2,lambda f:(s.diff(f,u)-s.I*s.diff(f,v))/2]
bo=[lambda f:(s.diff(f,x)+s.I*s.diff(f,y))/2,lambda f:(s.diff(f,u)+s.I*s.diff(f,v))/2]
for j in range(2):
 for k in range(2):
  assert s.simplify(zo[j](bo[k](r+A*r*r))-(1+2*A*r)*zo[j](bo[k](r))-2*A*zo[j](r)*bo[k](r))==0
eps,R=s.symbols("eps R",positive=True)
assert s.simplify(eps*R**2/4-eps*R**2/8)==eps*R**2/8
assert (eps*R**2/8).is_positive
print("PASS: Levi determinant, defining-function Hessian, annular gluing margin")
