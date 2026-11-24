import math,itertools,os
from fractions import Fraction

def compositions(n,r):
    if r==1:
        yield(n,);return
    for x in range(n+1):
        for ys in compositions(n-x,r-1):yield(x,)+ys

def turan(n,r):
    q,s=divmod(n,r)
    return (n*n-s*(q+1)**2-(r-s)*q*q)//2
checks=0
# Exact continuous quadratic bound used by the gap proof:
# e(K_parts)+s_i/2 <= t_r(n)+n/(2r)+(r+1)/8.
for r in range(2,6):
    for n in range(26):
        for ss in compositions(n,r):
            cross=(n*n-sum(s*s for s in ss))//2
            for s in ss:
                assert Fraction(cross)+Fraction(s,2)<=Fraction(turan(n,r))+Fraction(n,2*r)+Fraction(r+1,8)
                checks+=1
print('Weighted partition quadratic bound:',checks,'exact checks passed')
checks2=0
for m in range(1,4):
 for n in range(1,4):
  for h in range(1,min(m,n)+1):
   for mask in range(1<<(m*n)):
    # Entry 1 signifies a complete adjacency between two internal matching blocks.
    has=any(all((mask>>(i*n+j))&1 for i in Is for j in Js)
      for Is in itertools.combinations(range(m),h) for Js in itertools.combinations(range(n),h))
    if not has:
     missing=m*n-mask.bit_count()
     assert h*h*missing>=m*n
     checks2+=1
print('Matching-block missing-edge double count:',checks2,'exact checks passed')
