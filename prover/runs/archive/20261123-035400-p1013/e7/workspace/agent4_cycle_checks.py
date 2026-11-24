"""Exact cycle checks supporting W7 counterexample; no floating point evidence."""
from math import factorial
from fractions import Fraction as F

def mul(a,b):
 c=[0]*(len(a)+len(b)-1)
 for i,x in enumerate(a):
  for j,y in enumerate(b):c[i+j]+=x*y
 return c

def power(a,k):
 c=[1]
 for _ in range(k):c=mul(c,a)
 return c

def cycle_triangle(a,b):
 assert a%3==0
 q=power([1,15,9,1],a//3)
 z=F(a,3)+F(b*(q[1]-a),2)
 for k in range(2,min(a,b)+1):
  z+=F(q[k]*factorial(b)//factorial(b-k)*factorial(k-1),2)
 assert z.denominator==1
 return z.numerator

def cycle_matchings(m):
 assert m%2==0
 q=power([1,4,1],m//2)
 z=F(q[1]**2-m*m,2)
 for k in range(2,m+1):z+=F(q[k]**2*factorial(k)*factorial(k-1),2)
 assert z.denominator==1
 return z.numerator

def brute_cycles(n,edges):
 adj=[set() for _ in range(n)]
 for a,b in edges:adj[a].add(b);adj[b].add(a)
 twice=0
 for start in range(n):
  def dfs(v,seen):
   nonlocal twice
   if len(seen)>=3 and start in adj[v]:twice+=1
   for w in adj[v]:
    if w>start and w not in seen:dfs(w,seen|{w})
  dfs(start,{start})
 assert twice%2==0
 return twice//2

def graph(a,b,tri=False,match=False):
 E=[(i,a+j) for i in range(a) for j in range(b)]
 if tri:
  for i in range(0,a,3):E.extend([(i,i+1),(i,i+2),(i+1,i+2)])
 if match:
  E.extend((i,i+1) for i in range(0,a,2))
  E.extend((a+i,a+i+1) for i in range(0,b,2))
 return E

def certify_series():
 # A = I_0(4)=sum 4^j/(j!)^2.
 # B = 3 I_2(2sqrt3)=sum 3^(j+2)/(j!(j+2)!).
 J=16
 A=sum((F(4**j,factorial(j)**2) for j in range(J+1)),F(0))
 B=sum((F(3**(j+2),factorial(j)*factorial(j+2)) for j in range(J+1)),F(0))
 # First omitted term and uniform geometric bound on later ratios.
 tail_B=F(3**(J+3),factorial(J+1)*factorial(J+3))/(1-F(3,(J+2)*(J+4)))
 assert A>B+tail_B
 # I_0(2sqrt3) < I_0(4) holds termwise, strict at j=1.
 return A-B-tail_B

if __name__=='__main__':
 for a,b in [(3,3),(3,4),(6,2)]:
  exact=cycle_triangle(a,b)
  brute=brute_cycles(a+b,graph(a,b,tri=True))
  assert exact==brute,(a,b,exact,brute)
 for m in [2,4]:
  exact=cycle_matchings(m)
  brute=brute_cycles(2*m,graph(m,m,match=True))
  assert exact==brute,(m,exact,brute)
 gap=certify_series()
 print('Exact generating-polynomial cycle formulas match independent DFS tests.')
 print('Certified rational lower bound for I0(4)-3I2(2sqrt3):',gap)
 print('In particular gap > 23/100:',gap>F(23,100))
 for m in [12,24,48,96]:
  base=F(factorial(m)*factorial(m-1),2)
  print('m=',m,'triangle-balanced ratio=',float(F(cycle_triangle(m,m),base)),
        'matching-balanced ratio=',float(F(cycle_matchings(m),base)))
