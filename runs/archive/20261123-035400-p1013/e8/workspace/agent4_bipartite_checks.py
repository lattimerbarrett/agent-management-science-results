from fractions import Fraction as F
from math import factorial,comb

def bip_cycles(a,b):
 return sum(F(comb(a,k)*comb(b,k)*factorial(k)*factorial(k-1),2) for k in range(2,min(a,b)+1))
def one_internal(a,b):
 # internal edge in first class; choose further first vertices and second vertices,
 # contract edge and orient it. k denotes number of second vertices.
 return sum(comb(a-2,k-1)*comb(b,k)*factorial(k)*factorial(k-1) for k in range(1,min(a-1,b)+1))
def cross_edge_cycles(a,b):
 return F(2,a*b)*sum(F(k*comb(a,k)*comb(b,k)*factorial(k)*factorial(k-1),2) for k in range(2,min(a,b)+1))

if __name__=='__main__':
 # Rational interval for alpha = I1(2)/I0(2), no reliance on floating point.
 N=20
 den=sum(F(1,factorial(j)**2) for j in range(N+1))
 num=sum(F(1,factorial(j)*factorial(j+1)) for j in range(N+1))
 den_tail=F(1,factorial(N+1)**2)/(1-F(1,(N+2)**2))
 num_tail=F(1,factorial(N+1)*factorial(N+2))/(1-F(1,(N+2)*(N+3)))
 lo=num/(den+den_tail);hi=(num+num_tail)/den
 assert F(2,3)<lo<hi<F(3,4)
 print('Certified 2/3 < I1(2)/I0(2) < 3/4; alpha≈',float(lo))
 for m in [10,20,50,100]:
  c=bip_cycles(m,m)
  a=F(m,2)*one_internal(m,m)/c
  b=F(m,2)*cross_edge_cycles(m,m)/c
  print(m,'internal coefficient',float(a),'cross coefficient',float(b),'trade 4internal−3cross',float(4*a-3*b))
