from fractions import Fraction as Q
from functools import lru_cache
from math import factorial,comb
from collections import Counter
from itertools import product
from sage.all import matrix, QQ, GF

def parts(n,m=1):
    if n==0: yield ()
    for a in range(m,n+1):
        for p in parts(n-a,a): yield (a,)+p
@lru_cache(None)
def df(n): return 1 if n<=1 else n*df(n-2)
# Inverse of psi pushforward: coefficient (-1)^(n-number of blocks)
# Weighted set partition sum, retaining number of blocks.
@lru_cache(None)
def blocks(ds):
    if not ds: return (Q(1),)
    first,*rest=ds
    counts=Counter(rest); types=list(counts)
    ans=[Q(0)]*(len(ds)+1)
    for ns in product(*(range(counts[a]+1) for a in types)):
        size=1+sum(ns)
        total=first+sum(a*k for a,k in zip(types,ns))
        mult=(-1)**(size-1)
        for a,k in zip(types,ns): mult*=comb(counts[a],k)
        rem=tuple(sorted(a for a,k in zip(types,ns) for _ in range(counts[a]-k)))
        coeff=Q(mult,df(2*total+1))
        for j,v in enumerate(blocks(rem)): ans[j+1]+=coeff*v
    return tuple(ans)
@lru_cache(None)
def K(ds):
    # normalized by integral kappa_23 lambda_25 lambda_24
    return sum(v*factorial(47+k) for k,v in enumerate(blocks(ds)))*Q(df(47),factorial(48))
a=list(parts(11)); b=list(parts(12))
M=matrix(QQ,[[K(tuple(sorted(x+y))) for y in b] for x in a])
print('shape',M.nrows(),M.ncols(),flush=True)
print('rational rank',M.rank(),flush=True)
print('prime rank',M.change_ring(GF(1000000007)).rank(),flush=True)
print('K23',K((23,)), 'K1,22',K((1,22)),flush=True)
import pickle
with open('exactpair.pkl','wb') as f: pickle.dump((a,b,M),f)
