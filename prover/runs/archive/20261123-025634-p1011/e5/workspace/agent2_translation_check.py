import numpy as np
from scipy.special import roots_jacobi,eval_jacobi,gammaln
from scipy.linalg import eigh
from pathlib import Path

def gram_l(n,ang,d,N=1200,L=300):
 a=(n-3)/2+ang
 z,w=roots_jacobi(N,a,a)
 q=np.array([(1-z)**j/(1+z)**(j+ang-1) for j in range(d+1)])
 G=np.zeros((d+1,d+1))
 for l in range(L+1):
  k=l+ang
  if k<2:continue
  p=eval_jacobi(l,a,a,z)
  norm=np.exp((2*a+1)*np.log(2)-np.log(2*l+2*a+1)+2*gammaln(l+a+1)-gammaln(l+1)-gammaln(l+2*a+1))
  b=(q*(w*p)).sum(axis=1)/np.sqrt(norm)
  kap=.5*np.exp(gammaln((k-1)/2)+gammaln((k+n)/2)-gammaln((k+n+1)/2)-gammaln(k/2))
  G+=kap*((k-1)*(k+n-1))**2*np.outer(b,b)
 return G

def study(n,d):
 m=n-1;G=gram_l(n,2,d);G1=gram_l(n,1,d);G3=gram_l(n,3,d-1)
 p=2+2*np.arange(d+1)[:,None]+2*np.arange(d+1)[None,:]
 vals,vs=eigh(G*p,G)
 v=vs[:,0];v/=v[0]
 coeff=np.zeros(2*d+2)
 for i in range(d+1):
  for j in range(d+1):coeff[i+j]+=p[i,j]*G[i,j]*v[i]*v[j]
 roots=np.polynomial.polynomial.polyroots(coeff)
 roots=sorted(r.real for r in roots if abs(r.imag)<1e-6 and r.real>0)
 print('n,d,vals,v,roots',n,d,vals,v,roots)
 # E(eps)=-sum Gij ai aj eps^(2+2i+2j); derivative roots eps²
 for t in roots:
  aa=v*t**np.arange(d+1)
  g=aa*(1+2*np.arange(d+1)/(m+2))
  b=np.array([2*(j+1)*aa[j+1] for j in range(d)])
  c=np.zeros(d+1);c[:d]=[2*(j+1)*(1+2*j/(m+4))*aa[j+1] for j in range(d)]
  PN=4/(m*(m+2))
  C=PN*aa@G@c
  deriv1=4/m*(g@G1@g)+8*(m+1)/(m*(m+2)**2*(m+4))*(b@G3@b)
  deriv3=4/(m*(m+2)*(m+4))*(b@G3@b)
  H1=2*(deriv1+3*C);H3=2*(deriv3+C)
  # N''eps at stationary sign
  Heps=aa@(G*p*(p-1))@aa
  print('t,Hnorm tang1,tang3,scale',t,H1,H3,Heps)
for n,d in [(19,3),(20,3),(21,2),(21,3),(22,2),(25,2)]:study(n,d)
