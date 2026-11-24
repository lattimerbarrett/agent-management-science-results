import numpy as np
from scipy.special import gammaln,betaln
from math import comb

def Cmat(n,ell,d,N=100000):
 a=(n+2*ell-3)/2; alpha=a+.5; js=np.arange(N,dtype=float)
 logI0=(2*a-ell+1)*np.log(2)+betaln(a+1,a-ell+1)
 logI=logI0+gammaln(js+ell)-gammaln(ell)-gammaln(js+1)+gammaln(js+2*a+1)-gammaln(2*a+1)+gammaln(2*a-ell+2)-gammaln(js+2*a-ell+2)
 logh=np.log(np.pi)+(1-2*alpha)*np.log(2)+gammaln(js+2*alpha)-gammaln(js+1)-np.log(js+alpha)-2*gammaln(alpha)
 k=js+ell
 logb=np.log(2)+gammaln((k+n+1)/2)+gammaln(k/2)-gammaln((k+n)/2)-gammaln((k-1)/2)
 if ell==1:logb[0]=np.inf
 w=np.exp(2*logI-logh-logb)
 ratios=[np.ones_like(js)]
 for p in range(ell,ell+d):ratios.append(ratios[-1]*(js+p)*(2*a-p+1+js)/(p*2*(a-p)))
 gs=[]
 for q in range(d+1):
  c=q*(2*q+n+2*ell-3)/(n-1);vec=np.zeros_like(js)
  for e,coef in [(q-1,c),(q,c+1-ell-2*q)]:
   if e<0:continue
   for p in range(e+1):vec+=coef*comb(e,p)*2**p*(-1)**(e-p)*ratios[p]
  if ell==1:vec[0]=0
  gs.append(vec)
 C=(np.array(gs)*w)@np.array(gs).T
 return C
n=19;m=n-1;lam=.9499314709891288
P=np.array([1,-.46283557,.05655270,-.00140805])*lam**(2*np.arange(4))
C1=Cmat(n,1,3);C2=Cmat(n,2,3);C3=Cmat(n,3,2)
print('C00s',C1[0,0],C2[0,0],C3[0,0])
for rho in [0,1/18,1/2,1]:
 R1=P*(2+4*np.arange(4)/(m+2))
 R3=2*np.arange(1,4)*P[1:]
 R2=np.arange(1,4)*P[1:]*((2+8*rho)+4*(1+4*rho)*(np.arange(1,4)-1)/(m+4))
 norm1=(m+2)/2*rho;norm3=(1+2*m*rho/(m+2))/(m+4)
 terms=[norm1*(R1@C1@R1),norm3*(R3@C3@R3),P@C2[:,:3]@R2]
 print('rho',rho,'terms',terms,'Hessian',-sum(terms),'relative C200',-sum(terms)/C2[0,0])
