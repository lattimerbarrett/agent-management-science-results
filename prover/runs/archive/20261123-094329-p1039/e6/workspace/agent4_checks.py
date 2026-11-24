import sympy as s
from fractions import Fraction
for n in range(2,9):
 x=s.symbols('x0:'+str(n),real=True); y=s.symbols('y0:'+str(n),real=True)
 lam=s.symbols('l0:'+str(n-1),real=True)
 rho=x[-1]+sum(lam[j]*(x[j]**2+y[j]**2) for j in range(n-1))
 zero={t:0 for t in x+y}
 def dz(f,j): return (s.diff(f,x[j])-s.I*s.diff(f,y[j]))/2
 def db(f,j): return (s.diff(f,x[j])+s.I*s.diff(f,y[j]))/2
 L=s.Matrix(n,n,lambda j,k:s.expand(db(dz(rho,j),k)).subs(zero))
 assert L==s.diag(*lam,0)
 assert s.Matrix([dz(rho,j).subs(zero) for j in range(n)])==s.Matrix([0]*(n-1)+[s.Rational(1,2)])
 h=2+sum((j+1)*x[j]+y[j]**2 for j in range(n))
 Lnew=s.Matrix(n,n,lambda j,k:s.expand(db(dz(h*rho,j),k)).subs(zero))
 assert Lnew[:n-1,:n-1]==2*L[:n-1,:n-1]
 assert s.Matrix(n,n,lambda j,k:s.expand(db(dz(-rho,j),k)).subs(zero))==-L
 t,u=s.symbols('t u',real=True)
 disc={x[0]:t,y[0]:u}
 disc.update({x[j]:0 for j in range(1,n)}); disc.update({y[j]:0 for j in range(1,n)})
 assert s.expand(rho.subs(disc)-lam[0]*(t*t+u*u))==0
 r=Fraction(1,3*n); epsilon=r/(4*n)
 assert n*epsilon<r
 print('n=',n,': exact Levi/orientation/tangent-disc checks PASS; n*eps/r=',n*epsilon/r)
