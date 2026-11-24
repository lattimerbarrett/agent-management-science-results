from functools import lru_cache
from collections import Counter
from itertools import product
from math import comb, factorial
import json, os, time
P=1000000007

def partitions(n,m=None):
    if n==0:
        yield (); return
    if m is None or m>n:m=n
    for a in range(m,0,-1):
        for q in partitions(n-a,a):yield (a,)+q

weights={a:pow(__import__('math').prod(range(1,2*a+2,2)),P-2,P) for a in range(24)}
@lru_cache(None)
def bell(mu):
    if not mu:return (1,)
    a=mu[0]; co=Counter(mu[1:]); keys=sorted(co,reverse=True)
    out=[0]*(len(mu)+1)
    for nums in product(*(range(co[k]+1) for k in keys)):
        rem=tuple(x for k,c in zip(keys,nums) for x in [k]*(co[k]-c))
        s=a+sum(k*c for k,c in zip(keys,nums))
        mult=1
        for k,c in zip(keys,nums):mult*=comb(co[k],c)
        coeff=mult*weights[s]%P
        for j,v in enumerate(bell(rem)):out[j+1]=(out[j+1]+coeff*v)%P
    return tuple(out)

@lru_cache(None)
def integral(mu):
    n=len(mu)
    return sum((-1)**(n-k)*factorial(47+k)*v for k,v in enumerate(bell(mu)))%P

def rank(A):
    A=[r[:] for r in A]; r=0; piv=[]
    for j in range(len(A[0])):
        p=next((i for i in range(r,len(A)) if A[i][j]),None)
        if p is None:continue
        A[p],A[r]=A[r],A[p]
        c=pow(A[r][j],P-2,P); A[r]=[x*c%P for x in A[r]]
        for i in range(r+1,len(A)):
            c=A[i][j]
            if c:A[i]=[(x-c*y)%P for x,y in zip(A[i],A[r])]
        piv.append(j);r+=1
    return r,piv

rows=list(partitions(12)); cols=list(partitions(11))
t=time.time(); A=[[integral(tuple(sorted(a+b,reverse=True))) for b in cols] for a in rows]
print('dimensions',len(rows),len(cols),'time',time.time()-t,'cache',bell.cache_info())
print('rank',rank(A))
os.makedirs('workspace',exist_ok=True)
json.dump({'prime':P,'rows':rows,'cols':cols,'matrix':A},open('workspace/agent3_pairing_mod.json','w'))
from fractions import Fraction
from math import prod, lcm
weights={a:Fraction(1,prod(range(1,2*a+2,2))) for a in range(24)}
@lru_cache(None)
def exact_bell(mu):
    if not mu:return (Fraction(1),)
    a=mu[0]; co=Counter(mu[1:]); keys=sorted(co,reverse=True)
    out=[Fraction(0)]*(len(mu)+1)
    for nums in product(*(range(co[k]+1) for k in keys)):
        rem=tuple(x for k,c in zip(keys,nums) for x in [k]*(co[k]-c))
        s=a+sum(k*c for k,c in zip(keys,nums))
        mult=1
        for k,c in zip(keys,nums):mult*=comb(co[k],c)
        coeff=mult*weights[s]
        for j,v in enumerate(exact_bell(rem)):out[j+1]+=coeff*v
    return tuple(out)
@lru_cache(None)
def exact_integral(mu):
    n=len(mu)
    return sum((-1)**(n-k)*factorial(47+k)*v for k,v in enumerate(exact_bell(mu)))
t=time.time(); E=[[exact_integral(tuple(sorted(a+b,reverse=True))) for b in cols] for a in rows]
print('Exact entries done',time.time()-t)
EI=[]
for row in E:
    d=lcm(*(x.denominator for x in row))
    EI.append([int(x*d) for x in row])
from sage.all import matrix,ZZ
M=matrix(ZZ,EI)
print('Exact Q rank',M.rank(), 'total time',time.time()-t)
json.dump({'rows':rows,'cols':cols,'matrix':EI},open('workspace/agent3_pairing_Z.json','w'))
