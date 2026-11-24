"""Exact cycle counting in complete multipartite graphs with internal graphs.
No floating-point arithmetic is used. Independent DFS verifier is included.
"""
from functools import lru_cache
from fractions import Fraction
from itertools import product

@lru_cache(None)
def multipartite_hamilton(parts):
    """Number of unoriented Hamilton cycles; generalized value 1/2 on K_1,1."""
    parts=tuple(parts)
    n=sum(parts)
    if n<2 or max(parts,default=0)*2>n:return Fraction(0)
    first=next(i for i,b in enumerate(parts) if b)
    # Fix one distinguished vertex in the first nonempty part.
    rem=list(parts);rem[first]-=1
    @lru_cache(None)
    def paths(rem,last):
        if not sum(rem):return int(last!=first)
        ans=0
        for j,b in enumerate(rem):
            if b and j!=last:
                nxt=list(rem);nxt[j]-=1
                ans+=b*paths(tuple(nxt),j)
        return ans
    return Fraction(paths(tuple(rem),first),2)

def convolve(a,b):
    c=[0]*(len(a)+len(b)-1)
    for i,x in enumerate(a):
        for j,y in enumerate(b):c[i+j]+=x*y
    return c

def path_polynomial(adj):
    """Coefficient k counts oriented disjoint paths on selected subset, k blocks."""
    n=len(adj)
    # Oriented simple paths, indexed by used vertex set. Singleton has one orientation.
    weights={}
    def dfs(path,mask):
        weights[mask]=weights.get(mask,0)+1
        for w in adj[path[-1]]:
            if not (mask>>w)&1:dfs(path+[w],mask|(1<<w))
    for v in range(n):dfs([v],1<<v)
    @lru_cache(None)
    def rec(mask):
        if not mask:return (1,)
        bit=mask&-mask
        # Smallest remaining vertex can be omitted or belongs to unique path block.
        out=list(rec(mask^bit))+[0]
        sub=mask
        while sub:
            if sub&bit and sub in weights:
                vals=rec(mask^sub)
                for k,v in enumerate(vals):out[k+1]+=weights[sub]*v
            sub=(sub-1)&mask
        return tuple(out)
    return rec((1<<n)-1)

def brute_cycles(adj):
    n=len(adj);ans=0
    def dfs(start,path,used):
        nonlocal ans
        for w in adj[path[-1]]:
            if w==start:
                if len(path)>=3 and path[1]<path[-1]:ans+=1
            elif w>start and not (used>>w)&1:
                dfs(start,path+[w],used|(1<<w))
    for v in range(n):dfs(v,[v],1<<v)
    return ans

def count_cycles(internals):
    polynomials=[path_polynomial(g) for g in internals]
    ans=Fraction(0)
    for bs in product(*(range(len(p)) for p in polynomials)):
        w=1
        for p,b in zip(polynomials,bs):w*=p[b]
        if w:ans+=w*multipartite_hamilton(bs)
    ans-=sum(Fraction(len(internals[i])*len(internals[j]),2)
             for i in range(len(internals)) for j in range(i))
    ans+=sum(brute_cycles(g) for g in internals)
    assert ans.denominator==1
    return int(ans)

def join_graph(internals):
    sizes=[len(g) for g in internals]
    n=sum(sizes);out=[set() for _ in range(n)]
    offset=0
    for i,g in enumerate(internals):
        for v,nei in enumerate(g):
            out[offset+v].update(offset+w for w in nei)
            out[offset+v].update(range(offset))
            out[offset+v].update(range(offset+len(g),n))
        offset+=len(g)
    return out

import math

def multipartite_hamilton_ie(parts):
    """Independent inclusion-exclusion formula; supports large part sizes."""
    if sum(b>0 for b in parts)<2:return Fraction(0)
    p=[1]
    for b in parts:
        if not b:continue
        p=convolve(p,[0]+[(-1)**(b-k)*math.comb(b-1,k-1)*math.factorial(b)//math.factorial(k) for k in range(1,b+1)])
    return Fraction(sum(p[k]*math.factorial(k-1) for k in range(1,len(p))),2)
