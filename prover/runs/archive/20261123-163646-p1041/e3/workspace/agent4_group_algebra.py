"""Checks group-algebra divided-square identity exhaustively in dimensions <=4.
Does not prove the remaining low-weight exclusions.
"""
from itertools import combinations

def mul(a,b,N):
 out=0
 for x in range(N):
  if a>>x&1:
   for y in range(N):
    if b>>y&1:out^=1<<(x^y)
 return out

def Q(a,N):
 S=[x for x in range(N) if a>>x&1]
 assert len(S)%2==0
 p=(len(S)//2)&1
 for x,y in combinations(S,2):p^=1<<(x^y)
 return p

def ymon(T,N):
 return sum(1<<x for x in range(N) if x&T==x)

def verify():
 for n in range(1,5):
  N=1<<n
  basis=[ymon(T,N) for T in range(1,N)]
  # Q polarizes to multiplication on augmentation ideal.
  for i,a in enumerate(basis):
   for b in basis[i+1:]:
    assert Q(a^b,N)^Q(a,N)^Q(b,N)==mul(a,b,N)
  # All monomials of degree >=2 have Q=0.
  for T in range(1,N):
   if T.bit_count()>=2:assert Q(ymon(T,N),N)==0
  # Exhaustively test Q(I^c) subset I^(2c) for c>=2.
  for c in range(2,n+1):
   Ts=[T for T in range(N) if T.bit_count()>=c]
   for mask in range(1<<len(Ts)):
    a=0;expected=0
    for i,T in enumerate(Ts):
     if mask>>i&1:
      a^=ymon(T,N)
      for j,U in enumerate(Ts[:i]):
       if mask>>j&1 and not T&U:expected^=ymon(T|U,N)
    assert Q(a,N)==expected
 print('Group-algebra identity verified exhaustively for n<=4')

if __name__=='__main__':verify()
