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

# Audit the normalized moving-domain energy independently of the spectral ansatz.
import sympy as sp
z=sp.symbols('z')
A0,A1,A2,F1,F2,k,q=sp.symbols('A0 A1 A2 F1 F2 k q', nonzero=True)
# E(z)=(k*A0+z*F1+z**2*F2)/(A0+z*A1+z**2*A2)**q.
# At the bubble, stationarity means F1=q*k*A1.
coeff=sp.expand(F2-q*F1*A1/A0-q*k*A2+q*(q+1)*k*A1**2/(2*A0))
print('A0**q times the quadratic coefficient:')
print(sp.simplify(coeff.subs(F1,q*k*A1)))

n,r2=sp.symbols('n r2', positive=True)
m=n-1; S=1+r2; a=(n-2)/(2*m)
# All the following quantities are multiplied by S**n.
gradU2=(n-2)**2*r2
lapU2=-2*(n-2)*m*S+4*(n-2)*(n-1)*r2
critical_term=(n-2)**2
print('First shape variation integrand times S**n:')
print(sp.simplify(-gradU2+a*lapU2+critical_term))
print('Thus shape stationarity holds, but the rank-one normalization term in the second variation must be retained.')
