import numpy as np
rng=np.random.default_rng(871)
def check(x,y,g):
 k=len(x); M=np.zeros((k+2,k+2))
 for i in range(k): M[i,i:i+3]=[1,-x[i]-y[i],x[i]*y[i]]
 M[k]=np.polynomial.polynomial.polymul([1,-g],np.polynomial.polynomial.polyfromroots(-x))
 M[k+1]=np.polynomial.polynomial.polymul([g,1],np.polynomial.polynomial.polyfromroots(-y))
 M/=np.max(np.abs(M),axis=1)[:,None]
 return np.linalg.slogdet(M)
for k in [2,3,4,5,8,12,20]:
 neg=0
 for j in range(10000):
  x=np.sort(np.exp(rng.uniform(-8,8,k)));y=np.sort(np.exp(rng.uniform(-8,8,k)));g=np.exp(rng.uniform(-6,6))
  a,b=check(x,y,g)
  if a<0:
   print('NEG',k,j,x,y,g,a,b);neg+=1;break
 print(k,'negative found',neg)
