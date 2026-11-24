from sage.all import *
from functools import lru_cache
from collections import Counter, defaultdict
p=1000000007
K=GF(p)
N=12; W=11; g=25
R=PolynomialRing(K,['k'+str(i) for i in range(1,N+1)])
ks=[R(2*g-2)]+list(R.gens())
@lru_cache(None)
def parts(n,lo=1):
    if n==0:return ((),)
    return tuple((i,)+q for i in range(lo,n+1) for q in parts(n-i,i))
sigs=[s for w in range(W+1) for s in parts(w) if all(x%3!=2 for x in s)]
T=PowerSeriesRing(K,'t',default_prec=N+1);t=T.gen()
A=T([K(QQ(factorial(6*n))/factorial(3*n)/factorial(2*n)) for n in range(N+1)])
B=T([K(QQ(factorial(6*n))/factorial(3*n)/factorial(2*n)*(QQ(6*n+1)/(6*n-1))) for n in range(N+1)])
L=A.log(); D=B/A
# E=-{log Psi}_kappa, indexed sigma and t degree
E={}
for s in sigs:
    if not s:
        cs=L
    else:
        l=len(s);shift=sum(x//3 for x in s);b=sum(x%3==1 for x in s)
        coeff=K(QQ((-1)**(l-1)*factorial(l-1))/prod(factorial(v) for v in Counter(s).values()))
        cs=coeff*t**shift*D**b
    for n in range(1,N+1):
        if cs[n]:E[n,s]=-R(cs[n])*ks[n]
# F0=(1-p1)^(-48)
F={(0,(1,)*l):R(binomial(2*g-3+l,l)) for l in range(W+1)}
@lru_cache(None)
def split(s):
    c=Counter(s);items=list(c.items());ans=[]
    def go(j,a,b):
        if j==len(items):ans.append((tuple(a),tuple(b)));return
        x,m=items[j]
        for k in range(m+1):go(j+1,a+[x]*k,b+[x]*(m-k))
    go(0,[],[])
    return ans
for n in range(1,N+1):
    for s in sigs:
        z=R.zero()
        for a,b in split(s):
            for i in range(1,n+1):
                if (i,a) in E and (n-i,b) in F:z+=i*E[i,a]*F[n-i,b]
        if z:F[n,s]=z/K(n)
    print('F',n,flush=True)
def relation_matrix(degree):
    basis=parts(degree); cols={s:j for j,s in enumerate(basis)}
    rows=[]
    for r in range(1,degree+1):
        for s in sigs:
            if sum(s)>3*r-g or (g-r-sum(s)-1)%2:continue
            f=F.get((r,s),R.zero())
            if not f:continue
            for q in parts(degree-r):
                h=f*prod(ks[x] for x in q)
                row=[K(0)]*len(basis)
                for e,c in h.dict().items():
                    pp=tuple(i+1 for i,m in enumerate(e) for _ in range(m))
                    row[cols[pp]]=c
                rows.append(row)
    return matrix(K,rows)
M=relation_matrix(12)
M11=relation_matrix(11)
print('FZ degree 12',M.dimensions(),M.rank(),'upper',len(parts(12))-M.rank(),flush=True)
print('FZ degree 11',M11.dimensions(),M11.rank(),'upper',len(parts(11))-M11.rank(),flush=True)
save(M,'fz.sobj')
# Intersection functional, normalized by a nonzero common scalar.
@lru_cache(None)
def H(s):
    # coefficient of x^j: sum partitions into j blocks of product 1/(2 sum(block)+1)!!
    if not s:return (K(1),)
    out=[K(0)]*(len(s)+1)
    a=s[0]; tail=s[1:];ct=Counter(tail)
    for block,rest in split(tail):
        ways=prod(binomial(ct[v],m) for v,m in Counter(block).items())
        fac=K(ways)/K(prod(range(1,2*(a+sum(block))+2,2)))
        h=H(rest)
        for j,c in enumerate(h):out[j+1]+=fac*c
    return tuple(out)
@lru_cache(None)
def integ(s):
    return sum((-1)**(len(s)-j)*K(factorial(2*g-3+j))*c for j,c in enumerate(H(s)))
Bmat=matrix(K,[[integ(tuple(sorted(a+b))) for b in parts(12)] for a in parts(11)])
print('pairing',Bmat.dimensions(),Bmat.rank(),flush=True)
save(Bmat,'pairing.sobj')
print('relations pair to zero:', (M*Bmat.transpose()).is_zero())
