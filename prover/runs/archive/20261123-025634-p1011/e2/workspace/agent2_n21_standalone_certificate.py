import sympy as s
from pathlib import Path
x,z,q=s.symbols('x z q')

def symbolic_gram(l,J):
 a=x+l
 def R(v):
  if v==0:return s.Integer(0)
  return 2**s.Integer(1-v)*s.prod(z-(a-1-t)**2 for t in range(v-1))/(s.factorial(v-1)*s.rf(a+s.Rational(1,2)-v,v-1))
 b=[s.expand(sum((-1)**(j-r)*s.binomial(j,r)*2**r*R(l-1+r) for r in range(j+1))) for j in range(J+1)]
 maxr=2*J+l-2
 U=[s.prod(z-(a-l-1-2*t)**2 for t in range(r)) for r in range(maxr+1)]
 # Output is exact shape Gram / pi, with q=Gamma(x+3/2)^2/(pi Gamma(x+1)^2).
 preE={1:2*q*x*x/(x+s.Rational(1,2))**2,2:2*(x+s.Rational(1,2))**2,3:32*(x+s.Rational(3,2))**2*q}[l]
 preO={1:s.Rational(1,2),2:8*q,3:18*(x+s.Rational(3,2))**2}[l]
 beta=s.Rational(l+1,2)
 moments=[s.factor(4**r*(preE*s.rf(beta,r)*s.rf(a-beta-r,r)+preO*s.rf(beta+s.Rational(1,2),r)*s.rf(a+s.Rational(1,2)-beta-r,r))/(a-l-1-r)) for r in range(maxr+1)]
 G=s.zeros(J+1)
 for i in range(J+1):
  for j in range(i,J+1):
   p=b[i]*b[j]
   if l==1:p*=z-a*a
   if l==3:p=s.cancel(p/(z-(a-1)**2))
   p=s.Poly(s.expand(p),z);v=0
   for r in range(p.degree() if not p.is_zero else -1,-1,-1):
    c=p.nth(r);v+=c*moments[r];p=s.Poly(p.as_expr()-c*U[r],z)
   assert p.is_zero
   G[i,j]=G[j,i]=s.factor(v)
 return G

def atan_bounds(inv,N):
 sums=sum((-1)**k*s.Rational(1,(2*k+1)*inv**(2*k+1)) for k in range(N))
 nxt=(-1)**N*s.Rational(1,(2*N+1)*inv**(2*N+1))
 return min(sums,sums+nxt),max(sums,sums+nxt)
# Exact rational tangent check for Machin: 4 atan(1/5)-atan(1/239)=pi/4.
# The angle is in (0,pi/2), so tangent=1 identifies it uniquely.
tan2=2*s.Rational(1,5)/(1-s.Rational(1,25))
tan4=2*tan2/(1-tan2**2)
assert s.cancel((tan4-s.Rational(1,239))/(1+tan4/s.Integer(239)))==1
a,b=atan_bounds(5,15);c,d=atan_bounds(239,5)
pilo,pihi=16*a-4*d,16*b-4*c
assert pilo>s.Rational(333,106) and pihi<s.Rational(22,7)
xx=s.Rational(19,2);m=20
qq=s.simplify(s.gamma(xx+s.Rational(3,2))**2/s.gamma(xx+1)**2/s.pi)
C=s.simplify(qq*s.pi**2);assert C.is_Rational
qlo=C/pihi**2;qhi=C/pilo**2
G=symbolic_gram(2,2).subs(x,xx);G1=symbolic_gram(1,2).subs(x,xx);G3=symbolic_gram(3,1).subs(x,xx)
z,v=s.symbols('z v');co=[1,z,s.Rational(7,150)]
H=sum(2*(i+j+1)*G[i,j]*co[i]*co[j] for i in range(3) for j in range(3))
K=sum(2*(i+j+1)*(2*i+2*j+1)*G[i,j]*co[i]*co[j] for i in range(3) for j in range(3))
T=s.zeros(3)
for i in range(3):
 for j in range(3):
  T[i,j]=(2+s.Rational(4*i,m+2))*(2+s.Rational(4*j,m+2))*s.Rational(m+2,2*m)*G1[i,j]
  if i*j:T[i,j]+=s.Rational(4*i*j,m+2)*G3[i-1,j-1]
  if j:T[i,j]+=(2*j+s.Rational(4*j*(j+1),m))*G[i,j-1]
Center=sum(T[i,j]*co[i]*co[j] for i in range(3) for j in range(3))
left=-s.Rational(425186,10**6);right=-s.Rational(425185,10**6)

def bern(e):
 p=s.Poly(s.expand(e.subs(z,left+(right-left)*v)),v);dd=p.degree()
 bs=[sum(p.nth(j)*s.binomial(k,j)/s.binomial(dd,j) for j in range(k+1)) for k in range(dd+1)]
 assert all(t>0 for t in bs)
 return bs
cert=[]
for qt in [qlo,qhi]:
 h=H.subs(q,qt)
 assert h.subs(z,left)<0 and h.subs(z,right)>0
 cert.extend(bern(-K.subs(q,qt)))
 cert.extend(bern(-Center.subs(q,qt)))
print('EXACT rational certificates: scale root in',left,right,'; scale and every center direction negative.')
print('Verified',len(cert),'strict-positive rational Bernstein coefficients, with exact Machin pi bounds.')
