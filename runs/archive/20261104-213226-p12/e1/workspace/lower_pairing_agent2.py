import math,time,json,itertools
from functools import lru_cache
from pathlib import Path
P=1000003
assert all(P%d for d in range(2,math.isqrt(P)+1))

def partitions(n, maxpart=None):
    if n==0:
        yield ()
        return
    for a in range(min(n,maxpart or n),1-1,-1):
        for rest in partitions(n-a,a): yield (a,)+rest

invdf={s:pow(math.prod(range(1,2*s+2,2))%P,-1,P) for s in range(1,24)}
@lru_cache(None)
def bell(state):
    # coefficient of t^m sums products of inverse odd double factorials over labeled set partitions
    if not state:return (1,)
    counts={i:state.count(i) for i in sorted(set(state))}
    a=state[0];counts[a]-=1
    keys=list(counts)
    ans=[0]*(len(state)+1)
    for choice in itertools.product(*(range(counts[k]+1) for k in keys)):
        weight=1;s=a;rest=[]
        for k,c in zip(keys,choice):
            weight=weight*math.comb(counts[k],c)%P;s+=k*c
            rest.extend([k]*(counts[k]-c))
        weight=weight*invdf[s]%P
        sub=bell(tuple(sorted(rest,reverse=True)))
        for m,v in enumerate(sub): ans[m+1]=(ans[m+1]+weight*v)%P
    return tuple(ans)

fac=[math.factorial(i)%P for i in range(72)]
scale=math.prod(range(1,50,2))%P*pow(fac[49],-1,P)%P
@lru_cache(None)
def pairing(state):
    n=len(state)
    return scale*sum((-1)**(n-m)*fac[47+m]*v for m,v in enumerate(bell(state)) if m)%P

rows=list(partitions(12));cols=list(partitions(11))
t=time.time()
M=[[pairing(tuple(sorted(r+c,reverse=True))) for c in cols] for r in rows]
print('computed',len(rows),len(cols),'secs',time.time()-t,'states',bell.cache_info())
# exact Gaussian elimination mod P with row pivot tracking
A=[r.copy() for r in M]; ids=list(range(len(rows))); pivcols=[];pivrows=[];det=1
rank=0
for j in range(len(cols)):
    pivot=next((i for i in range(rank,len(rows)) if A[i][j]),None)
    if pivot is None:continue
    if pivot!=rank:A[pivot],A[rank]=A[rank],A[pivot];ids[pivot],ids[rank]=ids[rank],ids[pivot]
    v=A[rank][j];det=det*v%P
    pivrows.append(ids[rank]);pivcols.append(j)
    inv=pow(v,-1,P)
    A[rank]=[x*inv%P for x in A[rank]]
    for i in range(rank+1,len(rows)):
        v=A[i][j]
        if v:A[i]=[(x-v*y)%P for x,y in zip(A[i],A[rank])]
    rank+=1
print('rank',rank,'rows',pivrows,'cols',pivcols)
# direct determinant of original selected minor
minor=[[M[i][j] for j in pivcols] for i in pivrows]
det=1
for j in range(rank):
    k=next(k for k in range(j,rank) if minor[k][j])
    if k!=j:minor[k],minor[j]=minor[j],minor[k];det=-det
    v=minor[j][j];det=det*v%P
    for k in range(j+1,rank):
        mult=minor[k][j]*pow(v,-1,P)%P
        for h in range(j+1,rank):minor[k][h]=(minor[k][h]-mult*minor[j][h])%P
        minor[k][j]=0
assert (len(rows),len(cols),rank)==(77,56,43)
assert pivrows==list(range(41))+[43,44]
assert pivcols==list(range(42))+[45]
assert det==221905
assert pairing((23,))==1
assert pairing((22,1))==(49*47*pow(3,-1,P)-1)%P
print('minor determinant',det)
Path('workspace').mkdir(exist_ok=True)
json.dump(dict(prime=P,rows=rows,cols=cols,matrix=M,pivrows=pivrows,pivcols=pivcols,det=det),open('workspace/lower_pairing_agent2.json','w'))
