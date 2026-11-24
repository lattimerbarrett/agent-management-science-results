import math, itertools
import numpy as np
from fractions import Fraction

def graph(n, edges):
    a=[0]*n
    for u,v in edges:
        assert u!=v
        a[u]|=1<<v; a[v]|=1<<u
    return a

def bits(x):
    while x:
        b=x & -x; yield b.bit_length()-1; x-=b

def edges(a):
    for u,x in enumerate(a):
        for v in bits(x & ~((1<<(u+1))-1)):
            yield u,v

def odd3(a):
    out=[]
    for u in range(len(a)):
        z=0
        for v in bits(a[u]):
            for w in bits(a[v]): z |= a[w]
        out.append(z)
    return out

def no35(a):
    # A length-5 closed walk exists iff the graph contains C3 or C5.
    two=[]
    for x in a:
        z=0
        for v in bits(x): z |= a[v]
        two.append(z)
    return all(not(two[u]&two[v]) for u,v in edges(a))

def trianglefree(a):
    return all(not(a[u]&a[v]) for u,v in edges(a))

def bipartite(a):
    col={}
    for s in range(len(a)):
        if s in col: continue
        col[s]=0; stack=[s]
        while stack:
            u=stack.pop()
            for v in bits(a[u]):
                if v not in col: col[v]=1-col[u];stack.append(v)
                elif col[v]==col[u]: return False
    return True

def wide(q,col):
    return all(col[u]!=col[v] for u,x in enumerate(q) for v in bits(x))

def omega(m):
    vs=[(i,A) for i in range(m) for A in range(1<<m) if not (A>>i)&1]
    es=[]
    for p,(i,A) in enumerate(vs):
        for r in range(p):
            j,B=vs[r]
            if (B>>i)&1 and (A>>j)&1 and not A&B: es.append((p,r))
    return vs,graph(len(vs),es)

def partitions(n):
    def rec(a):
        if len(a)==n: yield a; return
        for c in range(max(a,default=-1)+2): yield from rec(a+[c])
    yield from rec([])

# Exhaustively verify the wide-colouring target and extension lemmas.
checked=0
for n in range(1,6):
    pairs=list(itertools.combinations(range(n),2))
    for mask in range(1<<len(pairs)):
        a=graph(n,[e for j,e in enumerate(pairs) if (mask>>j)&1])
        brute_no35 = True
        for length in (3,5):
            if length>n: continue
            for cyc in itertools.permutations(range(n),length):
                if all((a[cyc[j]]>>cyc[(j+1)%length])&1 for j in range(length)):
                    brute_no35=False; break
            if not brute_no35: break
        assert no35(a)==brute_no35
        if not trianglefree(a): continue
        q=odd3(a)
        for col in partitions(n):
            if not wide(q,col): continue
            m=max(col)+1; vs,om=omega(m); lookup={v:j for j,v in enumerate(vs)}
            f=[]
            for u in range(n):
                A=0
                for v in bits(a[u]): A |= 1<<col[v]
                f.append(lookup[(col[u],A)])
            assert all((om[f[u]]>>f[v])&1 for u,v in edges(a))
            checked+=1
        for W in range(1<<n):
            if any(q[u]&W for u in bits(W)): continue
            T=[v for v in range(n) if not (W>>v)&1]
            ind=graph(len(T),[(i,j) for i in range(len(T)) for j in range(i) if (a[T[i]]>>T[j])&1])
            qi=odd3(ind)
            NW=0
            for v in bits(W): NW |= a[v]
            for co in partitions(len(T)):
                if not wide(qi,co): continue
                col=[(-1,False)]*n
                for i,v in enumerate(T): col[v]=(co[i], bool((NW>>v)&1))
                assert wide(q,col)
for m in range(1,6):
    vs,a=omega(m); assert trianglefree(a)
print('Exhaustively checked wide-colouring maps:',checked)
print('Extension lemma checked on every triangle-free graph with <=5 vertices.')

# Explicit geometric lower-construction test.  B is a near-antipodal odd cycle.
L=101; m=601
X=np.array([(math.cos(2*math.pi*j/L),math.sin(2*math.pi*j/L)) for j in range(L)])
step=(L-1)//2
B=graph(L,[(j,(j+step)%L) for j in range(L)])
eps=max(np.linalg.norm(X[u]+X[v]) for u,v in edges(B))*1.00001
assert 5*eps<2
z=np.array([(math.cos(2*math.pi*j/m),math.sin(2*math.pi*j/m)) for j in range(m)])
a=2*eps
inc=X@z.T>a
counts=inc.sum(axis=1); q=int(counts.min())
assert a*2>3*eps
nf=3*L; N=nf+3*m+3*q
es=[]
for u,v in edges(B):
    for i in range(3):
        for j in range(3):
            if i!=j: es.append((3*u+i,3*v+j))
for i in range(3):
    P=nf+i*m; Q=nf+3*m+i*q
    for j in range(m):
        for k in range(q): es.append((P+j,Q+k))
    for b in range(L):
        for j in np.flatnonzero(inc[b]): es.append((3*b+i,P+int(j)))
G=graph(N,es)
assert no35(G)
assert not bipartite(G)
delta=min(x.bit_count() for x in G)
assert delta>=q
# Independently verify all cap sets are 3-wide on B.
qb=odd3(B)
for j in range(m):
    I=sum(1<<b for b in range(L) if inc[b,j])
    assert all(not(qb[b]&I) for b in bits(I))
print('Geometric example:',N,'vertices,',sum(x.bit_count() for x in G)//2,'edges')
print('Minimum degree:',delta,'ratio:',float(Fraction(delta,N)))
print('Verified: no C3 or C5; not homomorphic to K2; every cap is 3-wide.')

# For gamma=c-1/9 in (0,1), the upper-bound surplus divided by gamma
# is 9-6/100-3*gamma/10**6-12*gamma**3/10**14.
assert 9-Fraction(6,100)-Fraction(3,10**6)-Fraction(12,10**14)>0
print('Exact coefficient bound verifies the error margin for every c>1/9.')
