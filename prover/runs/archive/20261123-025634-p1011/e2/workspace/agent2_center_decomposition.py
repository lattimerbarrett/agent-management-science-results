import sympy as s
from pathlib import Path

def sphere_mean(poly,ys):
 m=len(ys); out=0
 for exps,c in s.Poly(s.expand(poly),*ys).terms():
  if any(e%2 for e in exps):continue
  h=sum(exps)//2
  numer=s.prod(s.rf(s.Rational(1,2),e//2) for e in exps)
  out+=c*numer/s.rf(s.Rational(m,2),h)
 return s.simplify(out)
checks=0
for m in range(3,8):
 y=s.symbols('y:'+str(m)); R=sum(t*t for t in y)
 ds=list(range(1,m));ds.append(-sum(ds))
 A2=sum(a*a for a in ds);P=sum(ds[i]*y[i]**2 for i in range(m))
 norm=sphere_mean(P*P,y)
 for k in range(m):
  aa=s.Rational(ds[k]**2,A2); L=ds[k]*y[k]
  H=P*y[k]-s.Rational(2,m+2)*L*R
  assert s.simplify(sphere_mean(L*L,y)/norm-aa*(m+2)/2)==0
  assert s.simplify(sphere_mean(H*H,y)/norm-(s.Rational(1,m+4)+2*m*aa/((m+4)*(m+2))))==0
  checks+=2
  for j in range(1,4):
   f=P*R**j
   proj=sphere_mean(P*s.diff(f,y[k],2),y)/norm
   expected=2*j+8*j*aa+s.Rational(4*j*(j-1),m+4)*(1+4*aa)
   assert s.simplify(proj-expected)==0,(m,k,j,proj,expected)
   checks+=1
print('Verified',checks,'exact sphere-moment center-Hessian decomposition identities')
