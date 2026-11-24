from functools import lru_cache
from itertools import product
from math import comb
P=1000000007

def parts(n,lo=1):
    if n==0:
        yield ()
    for a in range(lo,n+1):
        for tail in parts(n-a,a):
            yield (a,)+tail

def counts(mu):
    return tuple(mu.count(a) for a in range(1,max(mu,default=0)+1))

def trim(c):
    while c and c[-1]==0:c=c[:-1]
    return c

invodd=[1]*24
odd=1
for n in range(24):
    if n:odd=odd*(2*n+1)%P
    invodd[n]=pow(odd,-1,P)

@lru_cache(None)
def poly(c):
    if not c:return (1,)
    # sum over unlabeled set partitions with block signs (-1)^(size-1)
    first=next(i for i,v in enumerate(c) if v)
    out=[0]*(sum(c)+1)
    opts=[range(x+1) if i!=first else range(1,x+1) for i,x in enumerate(c)]
    for b in product(*opts):
        multiplicity=1
        for i,(x,y) in enumerate(zip(c,b)):
            multiplicity*=comb(x-(i==first),y-(i==first))
        size=sum(b); weight=sum((i+1)*v for i,v in enumerate(b))
        fac=multiplicity*invodd[weight]*(-1 if size%2==0 else 1)%P
        rest=trim(tuple(x-y for x,y in zip(c,b)))
        for k,v in enumerate(poly(rest)):out[k+1]=(out[k+1]+fac*v)%P
    return tuple(out)

facts=[1]*71
for i in range(1,71):facts[i]=facts[i-1]*i%P
@lru_cache(None)
def kappa(mu):
    return sum(v*facts[47+k] for k,v in enumerate(poly(counts(mu))))%P
rows=list(parts(12)); cols=list(parts(11))
M=[[kappa(tuple(sorted(a+b))) for b in cols] for a in rows]
print('shape',len(rows),len(cols),'cache',poly.cache_info())
A=[r[:] for r in M]; rank=0;pivrows=[]; pivcols=[]; ids=list(range(len(rows)));det=1
for j in range(len(cols)):
    pivot=next((i for i in range(rank,len(rows)) if A[i][j]),None)
    if pivot is None:continue
    A[rank],A[pivot]=A[pivot],A[rank];ids[rank],ids[pivot]=ids[pivot],ids[rank]
    if pivot!=rank:det=-det%P
    x=A[rank][j];det=det*x%P;inv=pow(x,-1,P)
    A[rank]=[v*inv%P for v in A[rank]]
    for i in range(rank+1,len(rows)):
        x=A[i][j]
        if x:A[i]=[(a-x*b)%P for a,b in zip(A[i],A[rank])]
    pivrows.append(ids[rank]);pivcols.append(j);rank+=1
print('rank',rank,'pivrows',pivrows,'pivcols',pivcols)
# independent determinant of selected square matrix (do not use rectangular elimination swaps)
B=[[M[i][j] for j in pivcols] for i in pivrows];det=1
for j in range(rank):
    r=next(i for i in range(j,rank) if B[i][j])
    if r!=j:B[j],B[r]=B[r],B[j];det=-det%P
    x=B[j][j];det=det*x%P;inv=pow(x,-1,P)
    for i in range(j+1,rank):
        mul=B[i][j]*inv%P
        for k in range(j,rank):B[i][k]=(B[i][k]-mul*B[j][k])%P
print('minor determinant mod',P,'=',det)
import json
with open('workspace/agent3_lower_certificate.json','w') as f:json.dump({'prime':P,'rows':rows,'cols':cols,'matrix':M,'pivot_rows':pivrows,'pivot_cols':pivcols,'minor_det':det},f)
