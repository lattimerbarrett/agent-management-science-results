from sage.all import *
from functools import lru_cache
import time
P=PolynomialRing(QQ, names=('q','A')); E=P.fraction_field(); q,A=map(E,P.gens())
h=q-1/q
prod0=prod
def prod(xs):return prod0(xs,E(1))
@lru_cache(None)
def br(n):return (q**n-q**(-n))/h
@lru_cache(None)
def fac(n):return prod(br(i) for i in range(1,n+1))
def D(i):return A*q**i-1/A/q**i
@lru_cache(None)
def g(n):return prod(D(i)/h for i in range(-1,n-1))/fac(n)
@lru_cache(None)
def dim(r):return prod(D(i)/h for i in range(r))/fac(r)
@lru_cache(None)
def delta(r,m):return br(2*m+1)*prod(D(i)/h for i in range(r+m))*prod(D(i)/h for i in range(-1,r-m-1))/(fac(r+m+1)*fac(r-m))
@lru_cache(None)
def bd(k):return E(1) if k==0 else D(2*k-1)*D(-1)*prod(D(i)**2 for i in range(k-1))/(h**(2*k)*fac(k)**2)
@lru_cache(None)
def a(r,k,m):
 pref=(-1)**(r+k+m)*br(2*m+1)*(fac(k)*fac(m))**2*fac(r-k)*fac(r-m)/(fac(r+k+1)*fac(r+m+1))
 ans=E(0)
 for j in range(max(r+m,r+k),min(r+k+m,2*r)+1):
  ans+=(-1)**j*fac(j+1)/(fac(2*r-j)*(fac(j-r-k)*fac(j-r-m)*fac(r+k+m-j))**2)*g(r-m)*g(j+1)/(g(r+k+1)*g(j-r-m))
 return pref*ans
@lru_cache(None)
def b(r,k,m):return bd(m)*a(r,m,k)/delta(r,k)
def H(r):return sum(delta(r,k)*prod(sum(b(r,k,m)*(-A*q**(m-1))**(m*p) for m in range(r+1)) for p in [-3,-3,3,5,7]) for k in range(r+1))/dim(r)
def laurent(x): return len(x.denominator().monomials())==1
FF=GF(1009)
def witness(x,k):
 vals=(FF(2),FF(2)**(-k))
 return x.numerator().change_ring(FF)(*vals)/x.denominator().change_ring(FF)(*vals)

def coefficient(r,j):return fac(r)/fac(j)/fac(r-j)*D(-1)*prod(D(r+i-1) for i in range(1,j+1))

Gs={}
for r in range(1,7):
 t=time.time(); hr=H(r)
 v=hr-1
 for j in range(1,r):v-=fac(r)/fac(j)/fac(r-j)*D(-1)*prod(D(r+i-1) for i in range(1,j+1))*Gs[j]
 Gs[r]=v/(D(-1)*prod(D(r+i-1) for i in range(1,r+1)))
 save(hr,'hr%s'%r); save(Gs[r],'gr%s'%r)
 zz=Gs[r]; k=0
 while zz.numerator()(q=q,A=q**(-k))==0 and zz.numerator()(q=q,A=-q**(-k))==0:
  zz/=D(k); k+=1
 assert laurent(hr) and laurent(Gs[r]) and laurent(zz)
 assert witness(zz,k)!=0
 assert hr==1+sum(coefficient(r,j)*Gs[j] for j in range(1,r+1))
 print(r,k,len(Gs[r].numerator().monomials()),str(Gs[r].denominator()),len(zz.numerator().monomials()),str(zz.denominator()),witness(zz,k),flush=True)
 # Verify the recoupling normalizations and the single-crossing fingers.
 assert sum(delta(r,k) for k in range(r+1))==dim(r)**2
 assert sum(bd(k) for k in range(r+1))==dim(r)**2
 for k in range(r+1):
  assert a(r,0,k)==delta(r,k)/dim(r)
  for p in [-1,1]:
   finger=sum(b(r,k,m)*(-A*q**(m-1))**(m*p) for m in range(r+1))
   assert finger==((-1)**(r-k)*A**r*q**(r*r-k*(k+1)))**p
 for k in range(r+1):
  for l in range(r+1):
   assert sum(a(r,k,m)*b(r,m,l) for m in range(r+1))==int(k==l)
 print('normalization checks passed',r,'time',time.time()-t,flush=True)

alex=H(1)(A=1)
assert alex==5-2*(q**2+q**(-2))
print('Alexander:',alex)
