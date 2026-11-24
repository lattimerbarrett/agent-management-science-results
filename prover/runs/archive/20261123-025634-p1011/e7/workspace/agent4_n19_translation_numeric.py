import numpy as np
from scipy.special import gammaln, betaln
from pathlib import Path
from math import comb, factorial

def sector_gram(n,m,svals,N=100000):
 j=np.arange(N+1,dtype=float); l=j+m; alpha=m+(n-2)/2
 valid=l>=2; j=j[valid]; l=l[valid]
 logD=np.log(l-1)+gammaln(l/2)+gammaln((l+n+1)/2)-gammaln((l+1)/2)-gammaln((l+n)/2)
 logM=2*np.log(l-1)+2*np.log(l+n-1)-logD
 logh=np.log(np.pi)+(1-2*alpha)*np.log(2)+gammaln(j+2*alpha)-gammaln(j+1)-np.log(j+alpha)-2*gammaln(alpha)
 logI1=(2*alpha-1)*np.log(2)+betaln(alpha-.5,alpha+.5)
 w=np.exp(logM+2*logI1-logh)
 def Ipoly(k):
  if k==0: # zero because l>=2 means j>=1 in m1 case
   return np.zeros_like(j)
  pref=1.
  for h in range(1,k):pref*= (2*alpha-h)/(2*alpha-2*h-1)
  ans=np.ones_like(j)*pref
  for h in range(k-1):ans*= (j+1+h)*(j+2*alpha+1-k+h)/(2*alpha+1-k+h)/(h+1)
  return ans
 coeff=[]
 for ss in svals:
  coeff.append(sum(comb(ss,e)*2**e*(-1)**(ss-e)*Ipoly(m+e-1) for e in range(ss+1)))
 coeff=np.array(coeff)
 return (coeff*w)@coeff.T

n=19; d=n-1; T=2.; a=np.array([1.,-.46283557,.05655270,-.00140805]); K=len(a)-1
G=sector_gram(n,2,list(range(K+1))); G3=sector_gram(n,3,list(range(K))); G1=sector_gram(n,1,list(range(K+1)))
print('G=',G)
poly=np.zeros(2*K+2)
for k in range(K+1):
 for l in range(K+1):poly[k+l+1]+=a[k]*a[l]*G[k,l]
der=np.arange(1,len(poly))*poly[1:]
roots=np.polynomial.polynomial.polyroots(der)
print('scale roots',roots)
for zz in roots:
 if abs(zz.imag)>1e-7 or zz.real<=0:continue
 z=zz.real
 sec=np.polynomial.polynomial.polyval(z,np.arange(1,len(der))*der[1:])
 print('z=',z,'Qsecond=',sec)
 for ai2 in (0.,1.):
  hn=2*T/(d*(d+2)*(d+4))+4*ai2/((d+2)**2*(d+4))
  # h_i coefficients in H3 and trace H1 sectors
  b3=np.array([2*k*a[k]*z**k for k in range(1,K+1)])
  b1=np.array([2*(d+2+2*k)/(d+2)*a[k]*z**k if k else 0 for k in range(K+1)])
  square=hn*b3@G3@b3+ai2/d*(b1@G1@b1)
  cross=0.
  H2norm=2*T/(d*(d+2))
  for l in range(K+1):
   for k in range(1,K+1):
    ck=2*k*(d+2+2*k)*(T+4*ai2)/((d+4)*T)
    cross+=H2norm*a[l]*a[k]*z**(k+l)*ck*G[l,k-1]
  print(' ai2=',ai2,'square',square,'cross',cross,'Qtranslation',square+cross)
Path('workspace/agent4_n19_translation_numeric.py').write_text(Path(__file__).read_text())
