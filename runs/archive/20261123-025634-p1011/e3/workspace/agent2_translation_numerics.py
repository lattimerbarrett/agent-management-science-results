import numpy as np, sys
from scipy.linalg import eigh
src=open('workspace/agent2_shape_numeric.py').read().split('import sys\n')[0]
exec(src,{'__name__':'utility'}) # need functions local
ns={'__name__':'utility'};exec(src,ns);Qblock=ns['Qblock']
for n in list(range(19,41))+[50,75,100,200]:
 d=n-1;J=3
 Qs=[None]+[Qblock(n,ell,J,N=700,L=200) for ell in range(1,4)]
 Q=Qs[2];sq=np.sqrt(Q.diagonal());R=Q/np.outer(sq,sq)
 M=R*np.fromfunction(lambda i,j:i+j+1,(4,4));e,v=eigh(M);a=v[:,0]/sq
 p=np.zeros(7)
 for i in range(4):
  for j in range(4):p[i+j]+=(i+j+1)*Q[i,j]*a[i]*a[j]
 roots=np.polynomial.polynomial.polyroots(p)
 vals=[]
 for t in roots:
  if abs(t.imag)>1e-6 or t.real<=0:continue
  t=t.real;c=a*t**np.arange(4)
  Hs=sum((i+j)*(i+j+1)*Q[i,j]*c[i]*c[j] for i in range(4) for j in range(4))
  if Hs>=0:continue
  Fp=np.array([c[j+1]*(j+1) if j<3 else 0 for j in range(4)])
  sFpp=np.array([c[j+1]*(j+1)*j if j<3 else 0 for j in range(4)])
  Lrad=c*(1+2*np.arange(4)/(d+2))
  ht=[]
  for b in [0,1]:
   G=(2+8*b)*Fp+(4+16*b)/(d+4)*sFpp
   normL=b*(d+2)/2;normT=1/(d+4)+2*d*b/((d+4)*(d+2))
   H=4*normL*(Lrad@Qs[1]@Lrad)+4*normT*(Fp@Qs[3]@Fp)+c@Qs[2]@G
   ht.append(H)
  vals.append((t,Hs,ht))
 print(n,'eig',e[0],vals,flush=True)
