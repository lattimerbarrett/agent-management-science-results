"""Exact zero-codimension-two-slice pair-parity identity.
No unproved RM spectrum or KTA classification is assumed by this checker.
"""
from itertools import product

def convolution(A,B,n):
 c=[0]*n
 for a in A:
  for b in B:c[a^b]^=1
 return c

def pairparities(S,n):
 q=[0]*n;ss=list(S)
 for i,a in enumerate(ss):
  for b in ss[i+1:]:q[a^b]^=1
 return q

def check():
 checked=0
 for d in range(3):
  n=1<<d
  subsets=[{i for i in range(n) if mask>>i&1} for mask in range(1<<n)]
  for G,H,J in product(subsets,repeat=3):
   # Empty00; the three other fibers have quotient labels1,2,3.
   S={n+x for x in G}|{2*n+x for x in H}|{3*n+x for x in J}
   q=pairparities(S,4*n)
   for a,b,label in [(G,H,3),(G,J,2),(H,J,1)]:
    assert q[label*n:(label+1)*n]==convolution(a,b,n)
   if all(q[v] for v in range(1,4*n)):
    assert len(G)*len(H)>=n
    assert len(G)*len(J)>=n
    assert len(H)*len(J)>=n
   checked+=1
 print('Exact identities checked on',checked,'three-fiber point sets.')

if __name__=='__main__':check()
