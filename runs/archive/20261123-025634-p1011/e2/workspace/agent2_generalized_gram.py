import numpy as np
from scipy.special import gammaln, betaln
import math

def g(n,l,J,K=1500):
 a=l+(n-2)/2;k=np.arange(K,dtype=float)
 def pl(b):return gammaln(b+k)-gammaln(b)
 logh=np.log(np.pi)+(1-2*a)*np.log(2)+gammaln(k+2*a)-gammaln(k+1)-np.log(k+a)-2*gammaln(a)
 vals=[]
 for j in range(J+1):
  v=np.zeros(K)
  for p in range(j+1):
   q=l+j-1-p;A=a+.5-q;B=a+.5
   if q==0:
    w=np.zeros(K);w[0]=np.exp((A+B-1)*np.log(2)+betaln(A,B)-.5*logh[0])
   else:
    w=np.exp((A+B-1)*np.log(2)+betaln(A,B)+pl(2*a)-gammaln(k+1)+pl(q)-pl(2*a+1-q)-.5*logh)
   v+=math.comb(j,p)*2**(j-p)*(-1)**p*w
  vals.append(v)
 L=k+l; W=np.zeros(K);mask=L>=2
 D=2*np.exp(gammaln((L[mask]+n+1)/2)+gammaln(L[mask]/2)-gammaln((L[mask]+n)/2)-gammaln((L[mask]-1)/2))
 W[mask]=((n-1)-L[mask]*(L[mask]+n-2))**2/D
 return (np.array(vals)*W)@np.array(vals).T

def matrices(n,J):
 G=g(n,2,J);G1=g(n,1,J);G3=g(n,3,J-1);m=n-1
 T=np.zeros_like(G)
 for i in range(J+1):
  for j in range(J+1):
   T[i,j]=(2+4*i/(m+2))*(2+4*j/(m+2))*(m+2)/(2*m)*G1[i,j]
   if i*j:T[i,j]+=4*i*j/(m+2)*G3[i-1,j-1]
   if j:T[i,j]+=(2*j+4*j*(j+1)/m)*G[i,j-1]
 T=(T+T.T)/2
 return G,T
rng=np.random.default_rng(2)
for n in [19,20,21,22,23,24,25,26,27]:
 J=2;G,T=matrices(n,J)
 best=1e9;bestb=None
 for z in range(10000):
  c=rng.normal(size=J+1)/np.sqrt(np.diag(G))
  p=np.zeros(2*J+1)
  for i in range(J+1):
   for j in range(J+1):p[i+j]+=(i+j+1)*G[i,j]*c[i]*c[j]
  for s in np.polynomial.polynomial.polyroots(p):
   if abs(s.imag)>1e-7 or s.real<=0:continue
   ss=s.real
   # P norm max iff derivative polynomial derivative negative.
   if np.polynomial.polynomial.polyval(ss,np.arange(1,len(p))*p[1:])>=0:continue
   b=c*ss**np.arange(J+1);val=b@T@b/(b@G@b)
   if val<best:best=val;bestb=b
 print(n,best,bestb)
from pathlib import Path
