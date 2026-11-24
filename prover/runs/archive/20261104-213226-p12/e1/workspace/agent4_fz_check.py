from fractions import Fraction as Q
from math import factorial, comb
from functools import lru_cache
from collections import Counter
import json, time
N=12
def partitions(n, lo=1):
    if n==0: yield (); return
    for i in range(lo,n+1):
        for p in partitions(n-i,i): yield (i,)+p

def conv(a,b):
    return [sum(a[i]*b[n-i] for i in range(n+1)) for n in range(N+1)]
A=[Q(factorial(6*n),factorial(3*n)*factorial(2*n)) for n in range(N+1)]
B=[A[n]*Q(6*n+1,6*n-1) for n in range(N+1)]
inv=[Q(1)]+[Q(0)]*N
for n in range(1,N+1): inv[n]=-sum(A[i]*inv[n-i] for i in range(1,n+1))
R=conv(B,inv)
logA=[Q(0)]*(N+1)
for n in range(1,N+1): logA[n]=A[n]-sum(Q(i,n)*logA[i]*A[n-i] for i in range(1,n))
Rpows=[[Q(1)]+[Q(0)]*N]
for i in range(10): Rpows.append(conv(Rpows[-1],R))
@lru_cache(None)
def block(q,m):
    return {(() if n==0 else (n,)):Rpows[m][n-q]*(48 if n==0 else 1) for n in range(q,N+1) if Rpows[m][n-q]}

def mul(a,b):
    out={}
    for p,x in a.items():
        for q,y in b.items():
            if sum(p)+sum(q)<=N:
                z=tuple(sorted(p+q));out[z]=out.get(z,Q(0))+x*y
    return {p:x for p,x in out.items() if x}

def subchoices(counts):
    if not counts: yield ();return
    for j in range(counts[0]+1):
        for rest in subchoices(counts[1:]):yield (j,)+rest

@lru_cache(None)
def marked(sig):
    if not sig:return {():Q(1)}
    first=sig[0]; cs=Counter(sig[1:]);vals=tuple(sorted(cs));cts=tuple(cs[v] for v in vals)
    out={}
    for chosen in subchoices(cts):
        subset=(first,)+tuple(v for v,c in zip(vals,chosen) for _ in range(c))
        rem=tuple(v for v,c,k in zip(vals,cts,chosen) for _ in range(c-k))
        coeff=factorial(len(subset)-1)
        for c,k in zip(cts,chosen):coeff*=comb(c,k)
        q=sum(v//3 for v in subset);m=sum(v%3==1 for v in subset)
        for p,x in mul(block(q,m),marked(rem)).items():out[p]=out.get(p,Q(0))+coeff*x
    return {p:x for p,x in out.items() if x}
E={}
for n in range(N+1):
    for p in partitions(n):
        x=Q(1)
        for k,m in Counter(p).items():x*=(-logA[k])**m/Q(factorial(m))
        E[p]=x
rows=[];labels=[];cols=list(partitions(N));
t0=time.time()
for r in range(9,N+1):
    for s in range(3*r-25):
        if (25-r-s-1)%2:continue
        for sig in partitions(s):
            if any(x%3==2 for x in sig):continue
            f=mul(E,marked(sig));f={p:x for p,x in f.items() if sum(p)==r}
            for m in partitions(N-r):
                row={tuple(sorted(p+m)):x for p,x in f.items()}
                rows.append([row.get(p,Q(0)) for p in cols]);labels.append((r,sig,m))
    print('r',r,'rows',len(rows),'time',time.time()-t0,flush=True)
# fraction-free integer row elimination via primitive normalization
from math import gcd,lcm
basis={}
def primitive(v):
    den=lcm(*(x.denominator for x in v));v=[int(x*den) for x in v];g=gcd(*v)
    return [x//g for x in v] if g else v
pivots=[]
for idx,row in enumerate(rows):
    v=primitive(row)
    for j,w in sorted(basis.items()):
        if v[j]:
            a=v[j];b=w[j];v=[b*x-a*y for x,y in zip(v,w)];g=gcd(*v)
            if g:v=[x//g for x in v]
    j=next((j for j,x in enumerate(v) if x),None)
    if j is not None:basis[j]=v;pivots.append(idx)
print('COLUMNS',len(cols),'ROWS',len(rows),'EXACT RANK',len(basis),'PIVOT ROWS',pivots,'PIVOT COLS',sorted(basis),flush=True)
with open('workspace/agent4_fz_data.json','w') as f:json.dump({'columns':cols,'labels':labels,'matrix':[[str(x) for x in row] for row in rows],'rank':len(basis),'pivot_rows':pivots,'pivot_columns':sorted(basis)},f)
