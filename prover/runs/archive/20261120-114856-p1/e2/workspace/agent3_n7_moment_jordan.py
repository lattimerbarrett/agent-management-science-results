import sympy as S
from pathlib import Path
x=S.symbols('x');be=S.Rational(1,100);chi=(x*x-1)**2*(x*x-be)-be;P=x*chi
p=(x*x-1)*(x-S.Rational(1,10));q=(x*x-1)*(x+S.Rational(1,10));r=x*x-S.Rational(1,2)
def L6(f): return S.rem(S.Poly(f,x),S.Poly(chi,x)).nth(5)
m=S.Matrix([L6(q*r*x**k) for k in range(7)])
print('moments',list(m))
rem=[S.Poly(S.rem(x**k,P,x),x) for k in range(13)]
def ev(f,m):
 rr=S.Poly(S.rem(S.expand(f),P,x),x)
 return S.expand(sum(co*m[mon[0]] for mon,co in rr.terms()))
def step(m):
 M=S.Matrix([[m[i+j] for j in range(3)] for i in range(3)]);c=-M.inv()*S.Matrix([m[j+3] for j in range(3)]);qp=x**3+sum(c[j]*x**j for j in range(3));F=ev(qp**2,m)
 out=S.Matrix([ev(x**k*qp**2,m)/F for k in range(7)])
 jac=S.zeros(6,6)
 for j in range(1,7):
  dm=S.zeros(7,1);dm[j]=1
  dc=-M.inv()*S.Matrix([ev(qp*x**k,dm) for k in range(3)])
  dq=sum(dc[k]*x**k for k in range(3));dF=ev(qp**2,dm)
  for k in range(1,7):jac[k-1,j-1]=(ev(x**k*qp**2,dm)+2*ev(x**k*qp*dq,m)-out[k]*dF)/F
 return out,qp,F,jac
mp,pp,F,J=step(m);mpp,qq,Fp,Jp=step(mp);G=Jp*J;N=G-S.eye(6)
print('p,q,F',S.factor(pp),S.factor(qq),F,Fp,'cycle',mpp==m)
print('rankN,N2,N3,N4',*[ (N**j).rank() for j in range(1,5)])
print('charpoly',G.charpoly().as_expr().factor())
import pickle
with open('workspace/agent3_n7_jordan.pkl','wb') as f:pickle.dump(dict(P=P,m=m,mp=mp,G=G,N=N,p=pp,q=qq,F=F),f)
