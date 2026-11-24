import numpy as np
from scipy.special import gammaln, comb
from scipy.optimize import brentq

def gram(n,l,js,K=20000):
 k=np.arange(K,dtype=float); alpha=l+(n-3)/2
 loghn=(2*alpha+1)*np.log(2)-np.log(2*k+2*alpha+1)+2*gammaln(k+alpha+1)-gammaln(k+1)-gammaln(k+2*alpha+1)
 def moment(beta):
  c=(2*alpha+beta+1)*np.log(2)+gammaln(alpha+beta+1)
  if beta<0:
   return np.exp(c+gammaln(alpha+k+1)+gammaln(k-beta)-gammaln(-beta)-gammaln(k+1)-gammaln(2*alpha+beta+k+2)-loghn/2)
  out=np.zeros(K)
  for kk in range(beta+1):
   out[kk]=(-1)**kk*np.exp(c+gammaln(alpha+kk+1)+gammaln(beta+1)-gammaln(beta-kk+1)-gammaln(kk+1)-gammaln(2*alpha+beta+kk+2)-loghn[kk]/2)
  return out
 C=np.array([sum(comb(j,h)*2**(j-h)*(-1)**h*moment(1-l-j+h) for h in range(j+1)) for j in js])
 L=k+l; eig=np.zeros(K); valid=L>=2; z=L[valid]
 mu=2*np.exp(gammaln(z/2)+gammaln((z+n+1)/2)-gammaln((z-1)/2)-gammaln((z+n)/2))
 eig[valid]=((z-1)*(z+n-1))**2/mu
 return (C*eig)@C.T

n=19;m=n-1;js=np.arange(4); ds=2+2*js
A2=gram(n,2,js); A1=gram(n,1,js); A3=gram(n,3,np.arange(3))
c=np.array([1,-461/1000,7/125,-693/500000])
B=A2*(ds[:,None]+ds[None,:]-2)
def vec(lam):return c*lam**(ds-1)
def der(lam):
 v=vec(lam);return v@B@v/lam
prev=.001; roots=[]
for lam in np.geomspace(.001,100,2000):
 if der(prev)*der(lam)<0:roots.append(brentq(der,prev,lam,xtol=1e-13))
 prev=lam
N1=1/m
N2=2*(m-1)/(m*m*(m+2))
N3=6*(m-1)/(m*(m+2)**2*(m+4))
print('roots',roots)
for lam in roots:
 v=vec(lam)
 b=2*(m-1)/m+4*js*(m-1)/(m*(m+2))
 w1=v*b;w3=(2*js*v)[1:]
 first_parallel=N1*(w1@A1@w1)+N3*(w3@A3@w3)
 # l2 projection of second parallel derivative, indexed j->j-1
 a3=3*m/((m+4)*(m+2))
 k2=2*js*b+2*js*3*m/(m+2)+4*js*(js-1)*a3
 secvec=np.r_[v[1:]*k2[1:],0.]
 second_parallel=N2*(v@A2@secvec)
 hpar=2*(first_parallel+second_parallel)
 # trace of translation Hessian
 w1sum=v*(1+2*js/(m+2))
 first_sum=N2*(2*(m+2)*(w1sum@A1@w1sum)+m/(m+2)*(w3@A3@w3))
 lapcoef=2*js*(2*2+m+2*js-2)
 lapvec=np.r_[v[1:]*lapcoef[1:],0.]
 second_sum=N2*(v@A2@lapvec)
 htrace=2*(first_sum+second_sum)
 hper=(htrace-hpar)/(m-1)
 hscale=(der(lam+1e-5)-der(lam-1e-5))/(2e-5)*N2
 print('lambda',lam,'Q',N2*(v@A2@v),'Hscale',hscale,'Hpar',hpar,'Hper',hper)
