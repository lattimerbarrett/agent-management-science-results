"""Exact cycle counts for complete bipartite graphs with bounded internal components.
All integers exact. Running module checks formulas against exhaustive cycle enumeration.
"""
import math,itertools
from fractions import Fraction

def base(a,b):
 return sum(math.comb(a,k)*math.comb(b,k)*math.factorial(k)*math.factorial(k-1)//2 for k in range(2,min(a,b)+1))

def fall(a,k): return math.factorial(a)//math.factorial(a-k)

def universal(a,b):
 ans=base(a,b)
 for k in range(1,min(a,b)+1): ans+=fall(a,k)*fall(b,k)
 for k in range(1,min(a-1,b)+1): ans+=fall(a,k+1)*fall(b,k)//2
 for k in range(1,min(a,b-1)+1): ans+=fall(a,k)*fall(b,k+1)//2
 return ans

def matching_both(a,b,ma,mb):
 ans=ma*b+mb*a+2*ma*mb
 for j in range(ma+1):
  for l in range(mb+1):
   for k in range(max(2,j,l),min(a-j,b-l)+1):
    ans+=math.comb(ma,j)*math.comb(mb,l)*2**(j+l)*math.comb(a-2*j,k-j)*math.comb(b-2*l,k-l)*math.factorial(k)*math.factorial(k-1)//2
 return ans

def packing(a,b,size,opts,internal_cycles=0):
 # Remainder vertices are isolated internally.
 t=a//size;coeff={(0,0):1}
 for _ in range(t):
  ne={}
  for (j,p),v in coeff.items():
   for dj,dp,mul in opts:
    key=j+dj,p+dp;ne[key]=ne.get(key,0)+v*mul
  coeff=ne
 ans=Fraction(t*internal_cycles)
 for (j,p),v in coeff.items():
  for k in range(max(1,p),min(a-j,b)+1):
   if k==1 and j==0:continue
   if a-j-p<k-p:continue
   ans+=Fraction(v*math.comb(a-j-p,k-p)*math.comb(b,k)*2**p*math.factorial(k)*math.factorial(k-1),2)
 assert ans.denominator==1
 return ans.numerator

TRI=(3,[(0,0,1),(1,1,3),(2,1,3)],1)
C4=(4,[(0,0,1),(1,1,4),(2,1,4),(2,2,2),(3,1,4)],1)
P3=(3,[(0,0,1),(1,1,2),(2,1,1)],0)

def brute(n,edges):
 E={frozenset(e) for e in edges};ans=0
 for k in range(3,n+1):
  for S in itertools.combinations(range(n),k):
   for tail in itertools.permutations(S[1:]):
    seq=(S[0],)+tail
    if seq[1]>seq[-1]:continue
    if all(frozenset((seq[i],seq[(i+1)%k])) in E for i in range(k)):ans+=1
 return ans

def checks():
 for a,b in [(2,2),(3,3),(4,3)]:
  cross=[(i,a+j) for i in range(a) for j in range(b)]
  for ma in range(a//2+1):
   for mb in range(b//2+1):
    ed=cross+[(2*i,2*i+1) for i in range(ma)]+[(a+2*i,a+2*i+1) for i in range(mb)]
    assert brute(a+b,ed)==matching_both(a,b,ma,mb)
  ed=cross+[(i,a+b) for i in range(a+b)]
  assert brute(a+b+1,ed)==universal(a,b)
 for size,opts,ic,ied in [(3,TRI[1],1,[(0,1),(1,2),(0,2)]),(4,C4[1],1,[(0,1),(1,2),(2,3),(3,0)]),(3,P3[1],0,[(0,1),(1,2)])]:
  b=3;cross=[(i,size+j) for i in range(size) for j in range(b)]
  assert brute(size+b,cross+ied)==packing(size,b,size,opts,ic)
 print('All exact formulas passed exhaustive small-graph cycle checks.')
 # Rigorous finite rational certificate: first 3 terms of I0(2sqrt3)-2I0(2)-I1(2) are positive.
 partial=sum(Fraction(3**k-2,math.factorial(k)**2)-Fraction(1,math.factorial(k)*math.factorial(k+1)) for k in range(3))
 assert partial==Fraction(1,6)
 print('Bessel comparison positive partial sum:',partial,'; all remaining terms positive by 3**k > 2+1/(k+1).')
 for n in [24,48,96,192]:
  m=n//2;bas=base(m,m)
  print(n,'universal ratio',float(Fraction(universal(m-1,m),bas)),'triangle ratio',float(Fraction(packing(m,m,*TRI),bas)),'both matching',float(Fraction(matching_both(m,m,m//2,m//2),bas)))
if __name__=='__main__': checks()


def p3_shift_certificate():
 L=Fraction(7,3)
 N=4
 S=sum(L**(k+2)/Fraction(math.factorial(k)*math.factorial(k+2))-L**k/Fraction(math.factorial(k)**2) for k in range(N+1))
 tail=(L**(N+1)/math.factorial(N+1)**2)/(1-L/Fraction((N+2)**2))
 assert S-tail==Fraction(2916932707,6361545600)>0
 print('Rigorous P3 Bessel shift margin lower bound:',S-tail)
 for n in [60,120,240]:
  m=n//2
  balanced=packing(m,m,*P3)
  shifted=packing(m+1,m-1,*P3)
  assert shifted>balanced
  assert m*m+2*(m//3)> (m+1)*(m-1)+2*((m+1)//3)
  print('P3',n,'shifted/balanced',float(Fraction(shifted,balanced)))
if __name__=='__main__':p3_shift_certificate()
