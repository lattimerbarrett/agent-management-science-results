import numpy as np
from scipy.special import gammaln

def gram(n,l,K=1,N=20000):
 s=np.arange(N,dtype=float); A=l+(n-3)/2
 logh=(2*A+1)*np.log(2)-np.log(2*s+2*A+1)+2*gammaln(s+A+1)-gammaln(s+1)-gammaln(s+2*A+1)
 j=s+l
 logN=gammaln((j+n)/2)+gammaln((j-1)/2)-np.log(2)-gammaln((j+n+1)/2)-gammaln(j/2)
 q=(j-1)**2*(j+n-1)**2*np.exp(logN)
 rows=[]
 import math
 for k in range(K+1):
  row=np.zeros(N)
  for h in range(k+1):
   a=l+k-1-h
   if a==0:
    val=np.zeros(N); val[0]=np.exp((2*A+1)*np.log(2)+2*gammaln(A+1)-gammaln(2*A+2)-logh[0]/2)
   else:
    logI=(2*A-a+1)*np.log(2)+gammaln(a+s)-gammaln(a)-gammaln(s+1)+gammaln(s+A+1)+gammaln(A-a+1)-gammaln(s+2*A-a+2)
    val=np.exp(logI-logh/2)
   row+=.5*math.comb(k,h)*2**(k-h)*(-1)**h*val
  rows.append(row*np.sqrt(q))
 rows=np.array(rows)
 return rows@rows.T

for n in range(9,41):
 K=(n-5)//4
 G=gram(n,2,K)
 G=G/np.sqrt(np.outer(G.diagonal(),G.diagonal()))
 p=1+2*np.arange(K+1)
 D=(p[:,None]+p[None,:])*G
 eig=np.linalg.eigvalsh(D)
 print(n,K,'min dilation eigenvalue',eig[0])
