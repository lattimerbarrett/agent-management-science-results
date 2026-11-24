import math,itertools,pickle,os
from functools import lru_cache
from collections import Counter,defaultdict
P=1000000007
D=12
g=25

def partitions(n,allowed=None,lo=1):
    if n==0:
        yield ()
        return
    for x in range(lo,n+1):
        if allowed is None or allowed(x):
            for tail in partitions(n-x,allowed,x): yield (x,)+tail

def inv(x): return pow(int(x)%P,-1,P)
def addterm(poly,m,c):
    v=(poly.get(m,0)+c)%P
    if v: poly[m]=v
    elif m in poly: del poly[m]
def kmul(m,i): return tuple(sorted(m+(i,))) if i else m

def seriesmul(a,b):
    return [sum(a[j]*b[i-j] for j in range(i+1))%P for i in range(D+1)]
A=[math.factorial(6*i)//(math.factorial(3*i)*math.factorial(2*i))%P for i in range(D+1)]
B=[A[i]*(6*i+1)*inv(6*i-1)%P for i in range(D+1)]
Ai=[1]+[0]*D
for i in range(1,D+1): Ai[i]=-sum(A[j]*Ai[i-j] for j in range(1,i+1))%P
BA=seriesmul(B,Ai)
Bpow=[[1]+[0]*D]
for k in range(1,11): Bpow.append(seriesmul(Bpow[-1],BA))
logA=[0]+[sum(j*A[j]*Ai[i-j] for j in range(1,i+1))*inv(i)%P for i in range(1,D+1)]

@lru_cache(None)
def L(sigma):
    if not sigma:return tuple(-x%P for x in logA)
    c=Counter(sigma);l=len(sigma);base=sum(x//3 for x in sigma);k=sum(x%3==1 for x in sigma)
    fact=(-1)**l*math.factorial(l-1)
    for m in c.values(): fact=fact*inv(math.factorial(m))%P
    return tuple(0 if r<base else fact*Bpow[k][r-base]%P for r in range(D+1))

@lru_cache(None)
def subparts(sigma):
    cc=list(Counter(sigma).items())
    return tuple(tuple(x for (x,m),n in zip(cc,ns) for _ in range(n)) for ns in itertools.product(*(range(m+1) for x,m in cc)))

@lru_cache(None)
def F(sigma):
    result=[{} for _ in range(D+1)]
    if not sigma:
        result[0][()]=1
        for r in range(1,D+1):
            for i in range(1,r+1):
                c=i*L(())[i]*inv(r)%P
                for m,v in result[r-i].items(): addterm(result[r],kmul(m,i),c*v)
    else:
        j=sigma[0];den=inv(sigma.count(j))
        for nu in subparts(sigma):
            if j not in nu:continue
            rem=list(sigma)
            for x in nu:rem.remove(x)
            rem=tuple(rem);f=F(rem);ls=L(nu)
            coeff=nu.count(j)*den%P
            for i,c in enumerate(ls):
                if not c:continue
                c=c*coeff*(2*g-2 if i==0 else 1)%P
                for r in range(i,D+1):
                    for m,v in f[r-i].items():addterm(result[r],kmul(m,i),c*v)
    return result

def rank_mod(rows,n):
    piv={}
    for rr in rows:
        row=[x%P for x in rr]
        for j in range(n):
            if not row[j]:continue
            if j in piv:
                a=row[j]; row=[(x-a*y)%P for x,y in zip(row,piv[j])]
            else:
                a=inv(row[j]);piv[j]=[x*a%P for x in row];break
    return len(piv)

def fz():
    bases={r:list(partitions(r)) for r in range(D+1)}
    rels={r:[] for r in range(D+1)}
    for r in range(1,D+1):
        for w in range(3*r-g):
            if (g-r-w-1)%2:continue
            for s in partitions(w,lambda x:x%3!=2):
                rels[r].append(F(s)[r])
        rows=[]
        for e in range(1,r+1):
            for rel in rels[e]:
                for m in bases[r-e]:
                    row={tuple(sorted(m+k)):v for k,v in rel.items()}
                    rows.append([row.get(k,0) for k in bases[r]])
        rank=rank_mod(rows,len(bases[r]));print('FZ',r,'vars',len(bases[r]),'rank',rank,'dim',len(bases[r])-rank,flush=True)
    with open('fz.pkl','wb') as f:pickle.dump((P,bases,rels),f)
@lru_cache(None)
def oddfac(n):
    return math.prod(range(1,2*n+2,2))%P

@lru_cache(None)
def integrand(m):
    # Coefficients of z^l in the signed block sum.
    if not m:return (1,)
    x=m[0];rest=m[1:];out=[0]*(len(m)+1)
    cc=Counter(rest)
    for sub in subparts(rest):
        c=Counter(sub);mul=(-1)**len(sub)*inv(oddfac(x+sum(sub)))%P
        for a,b in c.items():mul=mul*math.comb(cc[a],b)%P
        rem=list(rest)
        for a in sub:rem.remove(a)
        v=integrand(tuple(rem))
        for ell,val in enumerate(v):out[ell+1]=(out[ell+1]+mul*val)%P
    return tuple(out)

@lru_cache(None)
def integral(m):
    vals=integrand(m);rise=1;v=0
    for ell,c in enumerate(vals):
        if ell:rise=rise*(2*g-3+ell)%P
        v=(v+c*rise)%P
    return v

def pairing():
    a=list(partitions(11));b=list(partitions(12))
    rows=[[integral(tuple(sorted(x+y))) for y in b] for x in a]
    print('pairing rank',rank_mod(rows,len(b)),flush=True)
    with open('pair.pkl','wb') as f:pickle.dump(rows,f)
def compatibility():
    with open('fz.pkl','rb') as f:prime,bases,rels=pickle.load(f)
    with open('pair.pkl','rb') as f:pair=pickle.load(f)
    cols=bases[12];rows=[]
    for e in range(1,13):
        for rel in rels[e]:
            for m in bases[12-e]:
                row={tuple(sorted(m+k)):v for k,v in rel.items()}
                rows.append([row.get(k,0) for k in cols])
    assert all(sum(a*b for a,b in zip(r,s))%P==0 for r in rows for s in pair)
    print('all',len(rows),'degree-12 FZ rows annihilate all',len(pair),'pairing rows')
def exact_fz_rank():
    from fractions import Fraction
    class Exact:
        def __rmod__(self,x):return Fraction(x)
    source=open(__file__).read().split('def exact_fz_rank():')[0]
    source=source.replace('P=1000000007','P=EXACT')
    source=source.replace('def inv(x): return pow(int(x)%P,-1,P)','def inv(x): return Fraction(1)/x')
    ns={'__name__':'exact','EXACT':Exact(),'Fraction':Fraction}
    exec(source,ns)
    bases={r:list(partitions(r)) for r in range(13)};rels={r:[] for r in range(13)}
    for r in range(1,13):
        for w in range(3*r-g):
            if (g-r-w-1)%2:continue
            for s in partitions(w,lambda x:x%3!=2):rels[r].append(ns['F'](s)[r])
    rows=[]
    for e in range(1,13):
        for rel in rels[e]:
            for m in bases[12-e]:
                row={tuple(sorted(m+k)):v for k,v in rel.items()}
                rows.append([row.get(k,0) for k in bases[12]])
    print('exact rational FZ relation rank:',ns['rank_mod'](rows,77),flush=True)
if __name__=='__main__':
    fz();pairing();compatibility();exact_fz_rank()
