"""Exact cycle counts for complete joins of small internally decorated parts.
Pure Python, integer/rational arithmetic. Block path polynomials count arbitrary
vertex subsets partitioned into oriented paths; singleton orientations are not doubled.
"""
from math import comb, factorial
from fractions import Fraction
from itertools import product

def pmul(a,b):
    c=[0]*(len(a)+len(b)-1)
    for i,x in enumerate(a):
        for j,y in enumerate(b): c[i+j]+=x*y
    return c

def path_polynomial(n,edges):
    # Enumerate edge subsets and vertex supersets, valid for arbitrary small blocks.
    ans=[0]*(n+1)
    for mask in range(1<<len(edges)):
        deg=[0]*n; parent=list(range(n)); good=True; e=0
        def root(v):
            while parent[v]!=v: v=parent[v]
            return v
        for j,(u,v) in enumerate(edges):
            if not(mask>>j&1): continue
            deg[u]+=1; deg[v]+=1; e+=1
            a,b=root(u),root(v)
            if deg[u]>2 or deg[v]>2 or a==b: good=False; break
            parent[a]=b
        if not good: continue
        used=sum(d>0 for d in deg)
        nonsingle=used-e
        for single in range(n-used+1):
            ans[nonsingle+single]+=2**nonsingle*comb(n-used,single)
    return ans

def star_polynomial(leaves):
    # Center unused/singleton, degree one, or degree two.
    out=[0]*(leaves+2)
    for k in range(leaves+1):
        out[k]+=comb(leaves,k)
        out[k+1]+=comb(leaves,k)
    if leaves:
        for k in range(leaves): out[k+1]+=2*leaves*comb(leaves-1,k)
    if leaves>=2:
        for k in range(leaves-1): out[k+1]+=2*comb(leaves,2)*comb(leaves-2,k)
    return out

def multipartite_hamilton_directed(ks):
    # Directed cycles up to rotation, on distinguishable vertices with part counts ks.
    # Inclusion-exclusion over forbidden same-color adjacency bonds.
    if sum(ks)<2: return 0
    terms=[]
    for k in ks:
        if k==0: terms.append([(0,1)])
        else: terms.append([(j,(-1)**(k-j)*comb(k-1,j-1)*Fraction(factorial(k),factorial(j))) for j in range(1,k+1)])
    total=Fraction(0)
    for row in product(*terms):
        J=sum(x[0] for x in row)
        term=Fraction(factorial(J-1))
        for _,v in row: term*=v
        total+=term
    assert total.denominator==1
    return total.numerator

def joined_cycles(polys,internal_cycles=0):
    # polys[i] is product of block path polynomials in part i.
    out=Fraction(internal_cycles)
    for ks in product(*(range(len(p)) for p in polys)):
        if sum(k>0 for k in ks)<2: continue
        m=multipartite_hamilton_directed(ks)
        if not m: continue
        val=Fraction(m,2)
        for p,k in zip(polys,ks): val*=p[k]
        out+=val
    # Every pair of singleton vertices in different parts produced half a 2-cycle.
    sizes=[len(p)-1 for p in polys]
    out-=Fraction(sum(sizes[i]*sizes[j] for i in range(len(sizes)) for j in range(i)),2)
    assert out.denominator==1
    return out.numerator

def brute_cycles(n,edges):
    adj=[set() for _ in range(n)]
    for a,b in edges: adj[a].add(b); adj[b].add(a)
    ans=0
    for start in range(n):
        def walk(path,seen):
            nonlocal ans
            for v in adj[path[-1]]:
                if v==start and len(path)>=3: ans+=1
                elif v>start and v not in seen: walk(path+[v],seen|{v})
        walk([start],{start})
    return ans//2
