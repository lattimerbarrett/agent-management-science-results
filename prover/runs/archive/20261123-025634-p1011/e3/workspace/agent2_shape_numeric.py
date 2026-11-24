import numpy as np
from scipy.special import roots_jacobi, eval_gegenbauer, gammaln
from scipy.linalg import eigh
from scipy.optimize import brentq

def Qblock(n,ell,J,N=1200,L=400):
 alpha=(n-2)/2+ell
 x,w=roots_jacobi(N,alpha-.5,alpha-.5)
 hs=np.array([(1+x)**j/(1-x)**(ell+j-1) for j in range(J+1)])
 Q=np.zeros((J+1,J+1))
 for m in range(L):
  lnH=np.log(np.pi)+(1-2*alpha)*np.log(2)+gammaln(m+2*alpha)-gammaln(m+1)-np.log(m+alpha)-2*gammaln(alpha)
  poly=eval_gegenbauer(m,alpha,x)*np.exp(-lnH/2)
  cs=(hs*(w*poly)).sum(axis=1)
  l=m+ell
  if l<2: continue
  mu=2*np.exp(gammaln((l+n+1)/2)+gammaln(l/2)-gammaln((l-1)/2)-gammaln((l+n)/2))
  lam=(l-1)*(l+n-1)
  Q+=np.outer(cs,cs)*lam**2/mu
 return Q

import sys
n=int(sys.argv[1]) if len(sys.argv)>1 else 19;d=n-1;J=3
Qs=[None]+[Qblock(n,ell,J) for ell in range(1,4)]
Q=Qs[2]; sq=np.sqrt(Q.diagonal());R=Q/np.outer(sq,sq)
M=R*np.fromfunction(lambda i,j:i+j+1,(4,4))
e,v=eigh(M); a=v[:,0]/sq
# graph f=Axx F(s); scale Q(t)=sum Qij ai aj t^(i+j+1)
p=np.zeros(7)
for i in range(4):
 for j in range(4):p[i+j]+=(i+j+1)*Q[i,j]*a[i]*a[j]
roots=np.polynomial.polynomial.polyroots(p)
print('a0',a,'roots',roots)
for t in roots:
 if abs(t.imag)>1e-7 or t.real<=0:continue
 t=t.real
 c=a*t**np.arange(4)
 slope2=sum((i+j)*(i+j+1)*Q[i,j]*c[i]*c[j] for i in range(4) for j in range(4))
 Fp=np.array([c[j+1]*(j+1) if j<3 else 0 for j in range(4)])
 sFpp=np.array([c[j+1]*(j+1)*j if j<3 else 0 for j in range(4)])
 Lrad=c*(1+2*np.arange(4)/(d+2))
 print('t',t,'F',c,'scaleH',slope2)
 for b in [0,1/d,2/d]:
  G=(2+8*b)*Fp+(4+16*b)/(d+4)*sFpp
  normL=b*(d+2)/2
  normT=1/(d+4)+2*d*b/((d+4)*(d+2))
  H=4*normL*(Lrad@Qs[1]@Lrad)+4*normT*(Fp@Qs[3]@Fp)+c@Qs[2]@G
  print(' b,Htrans',b,H)
np.savez('workspace/agent2_translation_blocks.npz',Q1=Qs[1],Q2=Qs[2],Q3=Qs[3],a=a)
