from fractions import Fraction
from itertools import product

def tr(n,r):
 q,s=divmod(n,r)
 return (n*n-(r-s)*q*q-s*(q+1)*(q+1))//2
cnt=0
for r in range(2,5):
 for k in range(2,9):
  rho=Fraction(k-2,k-1)
  # Relative to the continuous Turan value, the optimal correction is at most rho^2(r-1)/(2r).
  for sizes in product(range(10), repeat=r):
   n=sum(sizes)
   cross=(n*n-sum(s*s for s in sizes))//2
   cont=Fraction((r-1)*n*n,2*r)
   bound=cont+rho*Fraction(n,r)+rho*rho*Fraction(r-1,2*r)
   assert cross+rho*max(sizes)<=bound
   cnt+=1
print('Verified generalized quadratic bound in',cnt,'integer cases.')
for r in (2,3,4,5):
 print('r =',r,'discrete candidate coefficients below 1/r:',[str(Fraction(j-1,j*r)) for j in range(1,9)],'limit',Fraction(1,r))
