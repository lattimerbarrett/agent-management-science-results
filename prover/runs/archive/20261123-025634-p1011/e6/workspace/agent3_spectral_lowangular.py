"""Exploratory spectral reduced-energy matrices (not rigorous interval bounds)."""
import numpy as np
from scipy.special import gammaln, comb

def matrix(n,q,degree,terms=200000):
 a=(n-3)/2+q
 k=np.arange(max(0,2-q),terms,dtype=float); l=k+q
 integs=[]
 for i in range(max(0,2-q),degree+1):
  value=np.zeros(len(k))
  for j in range(i+1):
   s=q-1+j
   if s<=0:continue
   I=np.exp((2*a-s+1)*np.log(2)+gammaln(s+k)-gammaln(s)-gammaln(k+1)+gammaln(a+k+1)+gammaln(a-s+1)-gammaln(2*a+k-s+2))
   value+=comb(i,j)*2**j*(-1)**(i-j)*I
  integs.append(value)
 integs=np.array(integs)
 lognorm=(2*a+1)*np.log(2)-np.log(2*k+2*a+1)+2*gammaln(k+a+1)-gammaln(k+1)-gammaln(k+2*a+1)
 D=2*np.exp(gammaln(l/2)+gammaln((l+n+1)/2)-gammaln((l-1)/2)-gammaln((l+n)/2))
 weight=((l-1)*(l+n-1))**2/D/np.exp(lognorm)
 M=(integs*weight)@integs.T
 K=M*np.fromfunction(lambda i,j:i+j+q-1+2*max(0,2-q),M.shape)
 return M,K

if __name__=='__main__':
 for n in range(15,22):
  for q in range(0,2):
   degree=(n-1-2*q)//4
   if degree<max(0,2-q):continue
   M,K=matrix(n,q,degree)
   scale=np.sqrt(np.diag(K))
   print(n,q,degree,np.linalg.eigvalsh(K/np.outer(scale,scale)))
