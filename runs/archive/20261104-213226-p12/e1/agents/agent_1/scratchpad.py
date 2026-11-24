from pathlib import Path
code=r'''from fractions import Fraction as Q
from functools import lru_cache
from itertools import product
from math import factorial as fac, comb, prod, isqrt

p = 1000000007
assert all(p % d for d in range(2, isqrt(p)+1))

def parts(n, lo=1):
    if n == 0:
        yield ()
    for a in range(lo, n+1):
        for t in parts(n-a, a):
            yield (a,)+t

basis = list(parts(12))
A = [fac(6*n)//(fac(3*n)*fac(2*n)) for n in range(13)]
B = [Q(A[n]*(6*n+1), 6*n-1) for n in range(13)]

@lru_cache(None)
def kap(t):
    z = t.count(0)
    if z:
        u = tuple(x for x in t if x)
        c = prod(range(48+len(u), 48+len(u)+z))
        return {m:c*v for m,v in kap(u).items()}
    if not t:
        return {():1}
    a, rest = t[0], t[1:]
    out = {}
    # Select the other labels in the cycle containing the first label.
    for mask in range(1 << len(rest)):
        chosen = [x for i,x in enumerate(rest) if mask >> i & 1]
        left = tuple(x for i,x in enumerate(rest) if not (mask >> i & 1))
        s, c = a+sum(chosen), fac(len(chosen))
        for m,v in kap(left).items():
            key = tuple(sorted((s,)+m))
            out[key] = out.get(key,0)+c*v
    return out

@lru_cache(None)
def exponential(r):
    out = {}
    for n in range(r+1):
        for t in parts(n):
            out[t] = prod(Q((-A[j])**t.count(j), fac(t.count(j)))
                          for j in set(t))
    return out

def relation(r, sigma):
    terms = dict(exponential(r))
    for s in sigma:
        shift, series = s//3, (A if s%3 == 0 else B)
        new = {}
        for t,c in terms.items():
            for n in range(shift, r-sum(t)+1):
                key = tuple(sorted(t+(n,)))
                new[key] = new.get(key,0)+c*series[n-shift]
        terms = new
    out = {}
    for t,c in terms.items():
        if sum(t) == r:
            for m,v in kap(t).items():
                out[m] = out.get(m,0)+c*v
    return out

relations = []
for r in range(1,13):
    for w in range(max(0,3*r-25)):
        if (25-r-w-1) % 2:
            continue
        for sigma in parts(w):
            if any(s%3 == 2 for s in sigma):
                continue
            f = relation(r,sigma)
            for t in parts(12-r):
                row = {tuple(sorted(m+t)):c for m,c in f.items()}
                relations.append([row.get(m,0) for m in basis])

def rank_mod(rows):
    pivots = {}
    for row in rows:
        v = [Q(x).numerator*pow(Q(x).denominator,-1,p)%p for x in row]
        for j,w in sorted(pivots.items()):
            c = v[j]
            if c:
                v = [(a-c*b)%p for a,b in zip(v,w)]
        if any(v):
            j = next(j for j,x in enumerate(v) if x)
            c = pow(v[j],-1,p)
            pivots[j] = [x*c%p for x in v]
    return len(pivots)

# Coefficients of the weighted set-partition polynomial.
invodd = {s:pow(prod(range(1,2*s+2,2)),-1,p) for s in range(1,24)}
@lru_cache(None)
def bell(t):
    if not t:
        return (1,)
    a, rest = t[0], t[1:]
    vals = sorted(set(rest))
    ns = [rest.count(v) for v in vals]
    out = [0]*(len(t)+1)
    for cs in product(*(range(n+1) for n in ns)):
        c = prod(comb(n,k) for n,k in zip(ns,cs))
        s = a+sum(v*k for v,k in zip(vals,cs))
        left = tuple(v for v,n,k in zip(vals,ns,cs) for _ in range(n-k))
        for j,x in enumerate(bell(left)):
            out[j+1] = (out[j+1]+c*invodd[s]*x)%p
    return tuple(out)

@lru_cache(None)
def integral(t):
    return sum((-1)**(len(t)-j)*fac(47+j)*x
               for j,x in enumerate(bell(t)))%p

columns = list(parts(11))
pairing = [[integral(tuple(sorted(a+b))) for b in columns] for a in basis]
u, l = rank_mod(relations), rank_mod(pairing)
assert (len(basis),len(relations),len(columns),u,l) == (77,59,56,33,43)
print('monomials =',len(basis))
print('FZ relations =',len(relations),' rank mod p =',u)
print('pairing size =',len(basis),'x',len(columns),' rank mod p =',l)
print('43 <= dim R^12(M_25) <= 44')
'''
Path('workspace/final_checker_agent1.py').write_text(code)
exec(compile(code,'workspace/final_checker_agent1.py','exec'))
