import sympy as s
import numpy as np
from mpmath import iv
from math import comb
from pathlib import Path
iv.dps=40
source=Path('workspace/agent1_exactmoments.py').read_text()
exec(source.split('for n in [17,18,19]:')[0])

def Cinterval(n,l,d,N=2000):
 p0=l; start=1 if l==1 else 0
 a=iv.mpf(n+2*l-3)/2;alpha=a+iv.mpf('.5');T=n+2*l-2;DD=n+2*l-p0-1
 def B(j):return iv.gamma(j+p0)**2*iv.gamma(j+T)*(j+alpha)/(iv.gamma(j+1)*iv.gamma(j+DD)**2)
 def beta(j):
  k=j+l
  return 2*iv.gamma(iv.mpf(k+n+1)/2)*iv.gamma(iv.mpf(k)/2)/(iv.gamma(iv.mpf(k+n)/2)*iv.gamma(iv.mpf(k-1)/2))
 K=2**(6*a-2*p0+2)/iv.pi*iv.gamma(a+1)**2*iv.gamma(a-p0+1)**2*iv.gamma(alpha)**2/(iv.gamma(p0)**2*iv.gamma(2*a+1)**2)
 ws=[iv.mpf(0),iv.mpf(0)]
 ws[start%2]=K*B(start)/beta(start);ws[(start+1)%2]=K*B(start+1)/beta(start+1)
 C=[[iv.mpf(0) for q in range(d+1)] for p in range(d+1)]
 for j0 in range(start,N):
  R={p0:iv.mpf(1)}
  for p in range(p0,l+d):R[p+1]=R[p]*(j0+p)*(j0+n+2*l-2-p)/(2*p*(a-p))
  gs=[]
  for q in range(d+1):
   c=iv.mpf(q*(2*q+n+2*l-3))/(n-1);g=iv.mpf(0)
   for e,coef in [(q-1,c),(q,c+1-l-2*q)]:
    if e>=0:
     for p in range(e+1):g+=coef*comb(e,p)*2**p*(-1)**(e-p)*R[l+p]
   gs.append(g)
  for u in range(d+1):
   for v in range(u,d+1):C[u][v]+=ws[j0%2]*gs[u]*gs[v]
  Brat=iv.mpf(((j0+p0)*(j0+p0+1))**2*(j0+T)*(j0+T+1))/((j0+1)*(j0+2)*((j0+DD)*(j0+DD+1))**2)*(j0+alpha+2)/(j0+alpha)
  betarat=iv.mpf((j0+l+n+1)*(j0+l))/((j0+l+n)*(j0+l-1))
  ws[j0%2]*=Brat/betarat
 Kw=2*K*(1+iv.mpf(n+2*l)/N)**(3*p0-2)
 Kr={p0:iv.mpf(1)}
 for p in range(p0,l+d):Kr[p+1]=Kr[p]*(1+iv.mpf(p)/N)*(1+iv.mpf(n+2*l-2-p)/N)/(2*p*(a-p))
 Kgs=[]
 for q in range(d+1):
  c=iv.mpf(q*(2*q+n+2*l-3))/(n-1);bound=iv.mpf(0)
  for e,coef in [(q-1,c),(q,c+1-l-2*q)]:
   if e>=0:
    for p in range(e+1):bound+=abs(coef)*comb(e,p)*2**p*Kr[l+p]/N**(2*(q-p))
  Kgs.append(bound)
 for u in range(d+1):
  for v in range(u,d+1):
   exponent=n-2*l-2*u-2*v
   err=Kw*Kgs[u]*Kgs[v]/(exponent*(N-1)**exponent)
   C[u][v]+=iv.mpf([-1,1])*err;C[v][u]=C[u][v]
 return C

def evalpoly(cs,z):
 ans=iv.mpf(0)
 for c in reversed(cs):ans=ans*z+c
 return ans

def qform(a,C,b):return sum(a[i]*C[i][j]*b[j] for i in range(len(a)) for j in range(len(b)))

aexact=[s.Integer(1),-s.Rational(46284,100000),s.Rational(5655,100000),-s.Rational(1408,1000000)]
results=[]
for n in range(19,33):
 C=Cexact(n)
 wexact=s.simplify(8*s.Rational(n+4,(n+1)**2)/s.pi*s.gamma(s.Rational(n+3,2))**2/(s.gamma(s.Rational(n+2,2))*s.gamma(s.Rational(n+4,2))))
 CC=C.subs(w,wexact)
 # convert exact rational/pi expressions into outward intervals
 def cv(v):
  v=s.cancel(v)
  if v.is_Rational:return iv.mpf(int(v.p))/int(v.q)
  if v==s.pi:return iv.pi
  if v.is_Add:return sum(cv(t) for t in v.args)
  if v.is_Mul:
   ans=iv.mpf(1)
   for t in v.args:ans*=cv(t)
   return ans
  if v.is_Pow:return cv(v.base)**int(v.exp)
  raise ValueError(v)
 # CC uses the universal weights with normalization w0=1. Absolute C2
 # has C2_00 divided by the universal moment M0; derive W2 at j=0.
 aa=iv.mpf(n+1)/2;al=aa+iv.mpf('.5')
 I0=2**(2*aa-1)*iv.gamma(aa+1)*iv.gamma(aa-1)/iv.gamma(2*aa)
 h0=iv.sqrt(iv.pi)*iv.gamma(aa+1)/iv.gamma(aa+iv.mpf('1.5'))
 beta0=2*iv.gamma(iv.mpf(n+3)/2)/(iv.gamma(iv.mpf(n+2)/2)*iv.sqrt(iv.pi))
 W0=I0**2/h0/beta0
 C2=[[cv(CC[i,j])*W0 for j in range(4)] for i in range(4)]
 pol=[iv.mpf(0) for _ in range(7)]
 for i in range(4):
  for j0 in range(4):pol[i+j0]+=(2+2*i+2*j0)*C2[i][j0]*cv(aexact[i])*cv(aexact[j0])
 pn=[float(x.a) for x in pol]
 roots=np.polynomial.polynomial.polyroots(pn)
 z0=min(r.real for r in roots if abs(r.imag)<1e-8 and r.real>0)
 zlo=np.floor(z0*1e7)/1e7;zhi=zlo+1e-7
 lo=iv.mpf(str(zlo));hi=iv.mpf(str(zhi));z=iv.mpf([str(zlo),str(zhi)])
 assert evalpoly(pol,lo)>0 and evalpoly(pol,hi)<0
 assert evalpoly([i*pol[i] for i in range(1,7)],z)<0
 P=[cv(aexact[i])*z**i for i in range(4)]
 C1=Cinterval(n,1,3);C3=Cinterval(n,3,2)
 for rho in [iv.mpf(0),iv.mpf(1)]:
  R1=[P[q]*(2+iv.mpf(4*q)/(n+1)) for q in range(4)]
  R3=[2*q*P[q] for q in range(1,4)]
  R2=[q*P[q]*(2+8*rho+iv.mpf(4)*(1+4*rho)*(q-1)/(n+3)) for q in range(1,4)]
  norm1=iv.mpf(n+1)/2*rho;norm3=(1+iv.mpf(2*(n-1))/(n+1)*rho)/(n+3)
  H=-(norm1*qform(R1,C1,R1)+norm3*qform(R3,C3,R3)+qform(P,C2,R2))
  assert H>0,(n,rho,H)
  results.append((n,str(rho),str(H)))
 print(n,'scale critical z in',z,'all translation directions positive',flush=True)
Path('workspace/agent3_transcert_results.txt').write_text(str(results))
