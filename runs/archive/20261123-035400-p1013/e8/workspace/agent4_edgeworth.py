import sympy as S
from functools import lru_cache
t=S.symbols('t0:3');r=S.Integer(4);xx=list(t)+[0]
u=S.symbols('u');f=1/(1+(r-1)*S.exp(u));fd=[S.diff(f,u,j).subs(u,0)/S.factorial(j) for j in range(5)]
L=sum(xx)/r;Ls={1:L}
for j in range(2,5):
 expr=sum(fd[k]*sum((L-x)**k for x in xx) for k in range(1,j+1))
 coeff=S.Poly(S.expand(expr),*t)
 hj=sum(c*S.prod(a**b for a,b in zip(t,ex)) for ex,c in coeff.terms() if sum(ex)==j)
 lj=S.expand(-hj/(r*fd[1]));Ls[j]=lj;L+=lj
# Compact centered derivative table, checked as an exact polynomial identity.
mean=sum(xx)/r;center=[x-mean for x in xx]
S2=sum(x*x for x in center);S3=sum(x**3 for x in center);S4=sum(x**4 for x in center)
assert S.expand(Ls[2]-S2/16)==0
assert S.expand(Ls[3]+S3/192)==0
assert S.expand(Ls[4]+S.Rational(5,768)*S4-S2**2/512)==0
V=S.hessian(Ls[2],t);Cov=V.inv()
@lru_cache(None)
def moment(ex):
 if sum(ex)==0:return S.Integer(1)
 if sum(ex)%2:return S.Integer(0)
 i=next(i for i,a in enumerate(ex) if a);a=list(ex);a[i]-=1;val=0
 for j in range(3):
  if a[j]:
   b=a.copy();b[j]-=1;val+=a[j]*Cov[i,j]*moment(tuple(b))
 return val
def expectation(p):return S.simplify(sum(c*moment(ex) for ex,c in S.Poly(S.expand(p),*t).terms()))
kw=expectation(Ls[4]-Ls[3]**2/2);kh=kw+S.Rational(15,12);kc=kh-S.Rational(2,3)
assert (kw,kh,kc)==(-1,S.Rational(1,4),-S.Rational(5,12))
# Compute the entropy-prefactor curvature. Vary y in a contrast direction.
x=S.symbols('x');y=S.Matrix([S.Rational(1,4)+x,S.Rational(1,4)-x,S.Rational(1,4),S.Rational(1,4)])
a=y.applyfunc(lambda z:z*(1-z));b=y.applyfunc(lambda z:1-2*z);den=sum(a);p=a/den;ab=a.multiply_elementwise(b)
var=(S.diag(*list(ab))-ab*p.T-p*ab.T+sum(ab)*p*p.T)/den
vdet=S.factor(var[:-1,:-1].det());curv=S.diff(vdet,x,2).subs(x,0)/vdet.subs(x,0)/2
Bh=-r*r/4-curv*S.Rational(9,16)
Bc=Bh+S.Rational(16,3)
assert Bh==S.Rational(3,2) and Bc==S.Rational(41,6)
if __name__=='__main__':print('Edgeworth word/Hamilton/total kappas',kw,kh,kc,'B_H/B_c',Bh,Bc)
