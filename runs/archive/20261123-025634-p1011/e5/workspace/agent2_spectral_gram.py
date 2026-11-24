import numpy as np
from scipy.special import gammaln, comb
from scipy.linalg import eigh

def gram_exact_coeff(n,d=4,L=100000):
 a=(n+1)/2
 l=np.arange(L+1,dtype=float)
 lognorm=(2*a+1)*np.log(2)-np.log(2*l+2*a+1)+2*gammaln(l+a+1)-gammaln(l+1)-gammaln(l+2*a+1)
 logkap=-np.log(2)+gammaln((l+1)/2)+gammaln((l+n+2)/2)-gammaln((l+n+3)/2)-gammaln((l+2)/2)
 logfac=logkap+2*np.log((l+1)*(l+n+1))-lognorm
 Js={}
 for p in range(1,d+2):
  logj=(2*a-p+1)*np.log(2)+gammaln(p+l)-gammaln(p)-gammaln(l+1)+gammaln(l+a+1)+gammaln(a-p+1)-gammaln(l+2*a-p+2)
  Js[p]=np.exp(logj+logfac/2) # sign (-1)^l cancels in all Gram products
 B=[]
 for j in range(d+1):
  B.append(sum(comb(j,s,exact=True)*2**(j-s)*(-1)**s*Js[j+1-s] for s in range(j+1)))
 B=np.array(B)
 return B@B.T

if __name__=='__main__':
 for n in [20,21,22,25,30,40,100]:
  for L in [100,1000,10000,100000]:
   G=gram_exact_coeff(n,L=L)
   p=2+2*np.arange(5)[:,None]+2*np.arange(5)[None,:]
   D=G*p
   vals,vec=eigh(D,G)
   print(n,L,vals[0],G[4,4])
   if n==21 and L==100000:
    v=vec[:,0];v/=v[0]
    print('NEGATIVE DIRECTION:',v,'quadratic D',v@D@v)
    np.savez('workspace/agent2_gram21_exact_coeff.npz',G=G,D=D,negative=v)
 import pathlib
