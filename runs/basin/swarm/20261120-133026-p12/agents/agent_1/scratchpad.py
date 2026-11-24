from functools import lru_cache
from collections import Counter, defaultdict
from math import factorial, comb
from fractions import Fraction as Q
from sympy import QQ
from sympy.polys.matrices import DomainMatrix

g, n, prime = 25, 12, 1000000007
@lru_cache(None)
def partitions(s, lo=1):
    if s == 0: return ((),)
    return tuple((a,) + b for a in range(lo, s+1)
                 for b in partitions(s-a, a))

def conv(a,b):
    return [sum(a[j]*b[i-j] for j in range(i+1)) for i in range(n+1)]
A = [Q(factorial(6*i),factorial(3*i)*factorial(2*i)) for i in range(n+1)]
B = [A[i]*Q(6*i+1,6*i-1) for i in range(n+1)]
Ai = [Q(1)]+[Q(0)]*n
for i in range(1,n+1): Ai[i] = -sum(A[j]*Ai[i-j] for j in range(1,i+1))
D = [ [Q(1)]+[Q(0)]*n ]
for i in range(10): D.append(conv(D[-1],conv(B,Ai)))
L = [0]+[sum(j*A[j]*Ai[i-j] for j in range(1,i+1))/i for i in range(1,n+1)]
# Keys (t-degree, kappa-partition); kappa_0 is replaced by 48.
def multiply(a,b):
    out=defaultdict(Q)
    for (i,p),x in a.items():
        for (j,q),y in b.items():
            if i+j<=n: out[i+j,tuple(sorted(p+q))] += x*y
    return {k:v for k,v in out.items() if v}
def accumulate(a,b,c=1):
    for k,v in b.items(): a[k]=a.get(k,0)+c*v

E={(0,()):Q(1)}
for i in range(1,n+1):
    E=multiply(E,{(i*m,(i,)*m):(-L[i])**m/factorial(m)
                  for m in range(n//i+1)})

# Enumerate a block containing the first element, with multiplicities.
def blocks(sig):
    counts=list(Counter(sig[1:]).items())
    def rec(j,chosen,mult):
        if j==len(counts):
            rest=list(sig[1:])
            for a in chosen: rest.remove(a)
            yield (sig[0],)+tuple(chosen),tuple(rest),mult
        else:
            a,c=counts[j]
            for k in range(c+1):
                yield from rec(j+1,chosen+[a]*k,mult*comb(c,k))
    yield from rec(0,[],1)

@lru_cache(None)
def marked(sig):
    if not sig: return {(0,()):Q(1)}
    out={}
    for block,rest,mult in blocks(sig):
        shift=sum(a//3 for a in block)
        b=sum(a%3==1 for a in block)
        factor=factorial(len(block)-1)
        pol={(i+shift, (i+shift,) if i+shift else ()):
             D[b][i]*factor*(1 if i+shift else 2*g-2)
             for i in range(n-shift+1) if D[b][i]}
        accumulate(out,multiply(pol,marked(rest)),mult)
    return out

basis=partitions(n)
rows=[]
for r in range(1,n+1):
    for w in range(max(-1,3*r-g-1)+1):
        if (g-r-w-1)%2: continue
        for sig in partitions(w):
            if any(a%3==2 for a in sig): continue
            rel={p:v for (i,p),v in multiply(E,marked(sig)).items() if i==r}
            for mu in partitions(n-r):
                rows.append({tuple(sorted(p+mu)):v for p,v in rel.items()})
M=DomainMatrix.from_list([[QQ(row.get(p,0)) for p in basis] for row in rows],QQ)
print('FZ rows, columns, rank:',len(rows),len(basis),M.rank())
assert len(basis)-M.rank()==44

# Faber's lambda_g lambda_{g-1} functional, up to a nonzero common scalar.
invdd=[]
for i in range(24):
    d=1
    for j in range(1,2*i+2,2): d=d*j%prime
    invdd.append(pow(d,-1,prime))
@lru_cache(None)
def block_sums(sig):
    if not sig: return (1,)
    out=[0]*(len(sig)+1)
    for block,rest,mult in blocks(sig):
        c=mult*(-1)**(len(block)-1)*invdd[sum(block)]
        for k,a in enumerate(block_sums(rest)):
            out[k+1]=(out[k+1]+c*a)%prime
    return tuple(out)
@lru_cache(None)
def integral(sig):
    return sum(a*factorial(2*g-3+k) for k,a in enumerate(block_sums(sig)))%prime
pair=[[integral(tuple(sorted(p+q))) for p in basis] for q in partitions(11)]

def rank_mod(a):
    a=[r[:] for r in a]; h=0
    for j in range(len(a[0])):
        v=next((i for i in range(h,len(a)) if a[i][j]),None)
        if v is None: continue
        a[h],a[v]=a[v],a[h]
        inv=pow(a[h][j],-1,prime)
        a[h]=[x*inv%prime for x in a[h]]
        for i in range(h+1,len(a)):
            c=a[i][j]
            a[i]=[(x-c*y)%prime for x,y in zip(a[i],a[h])]
        h+=1
        if h==len(a): break
    return h
print('Pairing rows, columns, modular rank:',len(pair),len(basis),rank_mod(pair))
assert rank_mod(pair)==43

def modq(x):
    x=Q(x)
    return x.numerator*pow(x.denominator,-1,prime)%prime
assert all(sum(a*modq(row.get(p,0)) for a,p in zip(v,basis))%prime==0
           for v in pair for row in rows)
print('All FZ relations annihilate the pairing matrix.')
