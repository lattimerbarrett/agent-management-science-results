from functools import lru_cache
from itertools import product
from math import factorial, comb
p, g, D = 1000000007, 25, 12

@lru_cache(None)
def partitions(n, m=100):
    if n == 0:
        return ((),)
    return tuple((i,) + q for i in range(min(m,n),0,-1)
                 for q in partitions(n-i,i))

A = [factorial(6*n)//factorial(3*n)//factorial(2*n)%p
     for n in range(D+1)]
B = [A[n]*(6*n+1)*pow(6*n-1,-1,p)%p for n in range(D+1)]

@lru_cache(None)
def K(t):
    if not t:
        return {():1}
    a, rest = t[0], t[1:]
    vals = sorted(set(rest))
    counts = [rest.count(v) for v in vals]
    out = {}
    for cs in product(*(range(c+1) for c in counts)):
        coeff, total, rem = factorial(sum(cs)), a, []
        for v,c,k in zip(vals,counts,cs):
            coeff *= comb(c,k)
            total += v*k
            rem += [v]*(c-k)
        for q,b in K(tuple(rem)).items():
            u = tuple(sorted(q+(total,)))
            out[u] = (out.get(u,0)+coeff*b)%p
    return out

def FZ(r, sigma):
    f = {}
    for d in range(r+1):
        for t in partitions(d):
            c = 1
            for n in set(t):
                m = t.count(n)
                c = c*pow(-A[n],m,p)*pow(factorial(m),-1,p)%p
            f[tuple(sorted(t))] = c
    for x in sigma:
        h, seq = x//3, (A if x%3==0 else B)
        out = {}
        for t,c in f.items():
            for n in range(r-sum(t)-h+1):
                u = tuple(sorted(t+(n+h,)))
                out[u] = (out.get(u,0)+c*seq[n])%p
        f = out
    out = {}
    for t,c in f.items():
        if sum(t) != r:
            continue
        z = t.count(0)
        u = tuple(v for v in t if v)
        for j in range(z):
            c = c*(2*g-2+len(u)+j)%p
        for q,b in K(u).items():
            out[q] = (out.get(q,0)+c*b)%p
    return out

def rank(rows, columns):
    pivots = {}
    for row in rows:
        v = [row.get(t,0)%p for t in columns]
        for i in range(len(v)):
            if not v[i]:
                continue
            if i in pivots:
                a = v[i]
                v = [(x-a*y)%p for x,y in zip(v,pivots[i])]
            else:
                a = pow(v[i],-1,p)
                pivots[i] = [a*x%p for x in v]
                break
    return len(pivots)

@lru_cache(None)
def df(n):
    return 1 if n<=1 else n*df(n-2)%p

@lru_cache(None)
def integral(t):
    v = factorial(2*g-3+len(t))%p
    for b in t:
        v = v*pow(df(2*b+1),-1,p)%p
    for q,c in K(t).items():
        if q != t:
            v = (v-c*integral(q))%p
    return v

columns = [tuple(sorted(t)) for t in partitions(D)]
relations = []
for r in range(1,D+1):
    for w in range(max(-1,3*r-g-1)+1):
        if (r+w-g)%2 != 1:
            continue
        for sigma in partitions(w):
            if any(x%3==2 for x in sigma):
                continue
            f = FZ(r,sigma)
            for t in partitions(D-r):
                relations.append({tuple(sorted(q+t)):c for q,c in f.items()})
pairing = [{q:integral(tuple(sorted(q+t))) for q in columns}
           for t in partitions(g-2-D)]
print('Number of degree-12 monomials:',len(columns))
print('FZ relation rank mod p:',rank(relations,columns))
print('Top pairing rank mod p:',rank(pairing,columns))
assert len(columns)==77
assert rank(relations,columns)==33
assert rank(pairing,columns)==43
# Check compatibility of every relation with every pairing row.
assert all(sum(c*row[q] for q,c in rel.items())%p==0
           for rel in relations for row in pairing)
print('All relations annihilate all pairing rows: checked')

# A separate characteristic-zero computation, without modular arithmetic.
import sympy as sp
from sympy.polys.matrices import DomainMatrix
from fractions import Fraction

@lru_cache(None)
def K_exact(t):
    if not t:
        return {():1}
    a, rest = t[0], t[1:]
    vals = sorted(set(rest))
    counts = [rest.count(v) for v in vals]
    out = {}
    for cs in product(*(range(c+1) for c in counts)):
        coeff, total, rem = factorial(sum(cs)), a, []
        for v,c,k in zip(vals,counts,cs):
            coeff *= comb(c,k)
            total += v*k
            rem += [v]*(c-k)
        for q,b in K_exact(tuple(rem)).items():
            u = tuple(sorted(q+(total,)))
            out[u] = out.get(u,0)+coeff*b
    return out

Ae = [factorial(6*n)//factorial(3*n)//factorial(2*n)
      for n in range(D+1)]
Be = [Ae[n]*(6*n+1)//(6*n-1) for n in range(D+1)]
def FZ_exact(r, sigma):
    f = {}
    for d in range(r+1):
        for t in partitions(d):
            c = Fraction(1)
            for n in set(t):
                m = t.count(n)
                c *= Fraction((-Ae[n])**m, factorial(m))
            f[tuple(sorted(t))] = c
    for x in sigma:
        h, seq = x//3, (Ae if x%3==0 else Be)
        out = {}
        for t,c in f.items():
            for n in range(r-sum(t)-h+1):
                u = tuple(sorted(t+(n+h,)))
                out[u] = out.get(u,0)+c*seq[n]
        f = out
    out = {}
    for t,c in f.items():
        if sum(t) != r:
            continue
        z = t.count(0)
        u = tuple(v for v in t if v)
        for j in range(z):
            c *= 2*g-2+len(u)+j
        for q,b in K_exact(u).items():
            out[q] = out.get(q,0)+c*b
    return out

@lru_cache(None)
def df_exact(n):
    return 1 if n<=1 else n*df_exact(n-2)

@lru_cache(None)
def integral_exact(t):
    denom = 1
    for b in t:
        denom *= df_exact(2*b+1)
    v, remainder = divmod(factorial(2*g-3+len(t)), denom)
    assert remainder == 0
    for q,c in K_exact(t).items():
        if q != t:
            v -= c*integral_exact(q)
    return v

exact_relations = []
for r in range(1,D+1):
    for w in range(max(-1,3*r-g-1)+1):
        if (r+w-g)%2 != 1:
            continue
        for sigma in partitions(w):
            if any(x%3==2 for x in sigma):
                continue
            f = FZ_exact(r,sigma)
            for t in partitions(D-r):
                exact_relations.append({tuple(sorted(q+t)):c for q,c in f.items()})
M = sp.Matrix([[sp.Rational(row.get(q,0)) for q in columns]
               for row in exact_relations])
print('Exact relation rank:',DomainMatrix.from_Matrix(M).rank(),flush=True)
N = sp.Matrix([[integral_exact(tuple(sorted(q+t))) for q in columns]
               for t in partitions(g-2-D)])
print('Exact pairing rank:',DomainMatrix.from_Matrix(N).rank(),flush=True)
assert M*N.T == sp.zeros(M.rows,N.rows)
print('Exact compatibility: checked')
import pickle
with open('exact_matrices.pkl','wb') as f:
    pickle.dump((columns,M,N),f)
_, piv = M.rref()
free = [i for i in range(len(columns)) if i not in piv]
rad = N[:,free].nullspace()
assert len(rad)==1
vec = rad[0]
den = sp.ilcm(*(x.q for x in vec))
v = [int(x*den) for x in vec]
from functools import reduce
from math import gcd
common = reduce(gcd,v)
v = [x//common for x in v]
print('Radical supported on',sum(bool(x) for x in v),'monomials')
for i,c in zip(free,v):
    if c:print(columns[i],c)
with open('radical.pkl','wb') as f:
    pickle.dump({columns[i]:c for i,c in zip(free,v) if c},f)
