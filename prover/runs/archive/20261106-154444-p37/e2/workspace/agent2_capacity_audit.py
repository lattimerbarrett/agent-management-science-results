"""Exact audit of crossing-middle construction; no asymptotic or lambda guesses."""
from math import comb
from itertools import combinations
from functools import lru_cache

def mul(a,b):
    out=[0]*(len(a)+len(b)-1)
    for i,x in enumerate(a):
        if x:
            for j,y in enumerate(b):
                if y: out[i+j]+=x*y
    return out

def crosspoly(s): return [0]+[comb(s,j) for j in range(1,s)]+[0]

def capacity(c,r):
    t=c+r; q,rem=divmod(t,r)
    sizes=[q+1]*rem+[q]*(r-rem)
    assert min(sizes)>=2
    polys=[crosspoly(s) for s in sizes]
    p=[1]
    for a in polys:p=mul(p,a)
    m=t//2; N=p[m]
    if t%2==0:
        assert N%2==0
        return N//2,sizes,N
    # Pick coordinate giving most crossing m-sets containing it.
    best=0
    for s in set(sizes):
        rest=[1]; skipped=False
        for z,a in zip(sizes,polys):
            if z==s and not skipped:skipped=True;continue
            rest=mul(rest,a)
        marked=[0]+[comb(s-1,j-1) for j in range(1,s)]+[0]
        best=max(best,mul(rest,marked)[m])
    assert best*t>=m*N
    return best,sizes,N

def audit():
    for c in [5,10,20,50,100,200]:
        vals=[(capacity(c,r)[0],r) for r in range(3,c+1)]
        b,r=min(vals); middle=comb(c+1,(c+1)//2)
        print({'c':c,'worst_r':r,'min_freebits':str(b),'central_cplus1':str(middle),'ratio':b/middle},flush=True)

if __name__=='__main__':audit()
