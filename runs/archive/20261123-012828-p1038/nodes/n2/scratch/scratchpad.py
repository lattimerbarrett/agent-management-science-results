import numpy as np
from scipy.special import roots_legendre

def mul(*ps):
 p=np.array([1.])
 for q in ps:p=np.convolve(p,q)
 return p

def cross(m,r,R,h):
 z=np.exp(2j*np.pi*np.arange(m)/m)
 D=h+np.sqrt(h*h+abs(R*z-r)**2)
 C=mul(*[[1,-np.conj(v)] for v in (R*z-r)/D])
 E=mul(*[[v,1] for v in (R-r*z)/D])
 return C.real,E.real

def blocks(m,al,ga,be,de,C,E):
 a,b=len(al),len(be);n=a+b+2*m
 H=mul(*[[1,np.exp(1j*np.pi*(.5-k/m))] for k in range(1,m)]).real
 A=mul(H,C,*[[x,1] for x in al],*[[1,x] for x in be])
 B=mul(H,E,*[[x,1] for x in ga],*[[1,x] for x in de])
 blocks=[]
 for s in range(m):
  inds=list(range(s,n,m));q=len(inds)-2
  X=np.zeros((q+2,q+2))
  for k in range(q):
   j=s+k*m
   if j<a:X[k,k:k+3]=[1,-al[j]**m-ga[j]**m,(al[j]*ga[j])**m]
   else:
    j-=a;X[k,k:k+3]=[(be[j]*de[j])**m,-(-1)**m*(be[j]**m+de[j]**m),1]
  X[-2]=A[s::m];X[-1]=B[s::m]
  blocks.append(X)
 return blocks
rng=np.random.default_rng(11)
for m in range(1,8):
 bad=0
 for it in range(2000):
  a,b=rng.integers(1,9,2)
  al=np.sort(rng.uniform(.01,.99,a));ga=np.sort(rng.uniform(.01,.99,a))
  be=-np.sort(-rng.uniform(.01,.99,b));de=-np.sort(-rng.uniform(.01,.99,b))
  C,E=cross(m,*[1,2],10**rng.uniform(-1,1))
  ds=[np.linalg.det(X) for X in blocks(m,al,ga,be,de,C,E)]
  # first qL lower and qU upper then A B ; move rings middle = even shift, determinant same
  if min(ds)<-1e-8:
   print('BAD',m,a,b,ds,al,ga,be,de,C,E);bad+=1;break
 print(m,'done',bad)
