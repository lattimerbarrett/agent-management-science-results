"""Faber lambda_g lambda_{g-1} pairing, exact modulo a prime.
The common nonzero factor (2g-3)!!/(2g-2)! is omitted.
"""
from functools import lru_cache
from itertools import product
from math import factorial, comb
from collections import Counter
P=1000000007

def partitions(n,m=None):
    if n==0:
        yield (); return
    if m is None: m=n
    for i in range(min(n,m),0,-1):
        for q in partitions(n-i,i): yield (i,)+q

def odd_df(n):
    z=1
    for i in range(n,0,-2): z=z*i%P
    return z

@lru_cache(None)
def partition_polynomial(a):
    # Sum over set partitions, recording block count as power of z.
    if not a: return (1,)
    first=a[0]; c=Counter(a[1:]); ks=tuple(c); cs=tuple(c[k] for k in ks)
    out=[0]*(len(a)+1)
    for vv in product(*(range(v+1) for v in cs)):
        size=1+sum(vv); ss=first+sum(k*v for k,v in zip(ks,vv))
        mult=1
        for c0,v in zip(cs,vv): mult=mult*comb(c0,v)%P
        coeff=mult*(-1)**(size-1)*pow(odd_df(2*ss+1),P-2,P)%P
        rem=tuple(sorted((k for k,c0,v in zip(ks,cs,vv) for _ in range(c0-v)),reverse=True))
        for j,z in enumerate(partition_polynomial(rem)): out[j+1]=(out[j+1]+coeff*z)%P
    return tuple(out)

@lru_cache(None)
def intersection(a,g=25):
    assert sum(a)==g-2
    return sum(z*factorial(2*g-3+j) for j,z in enumerate(partition_polynomial(a)))%P

def rank_certificate(M):
    A=[r[:] for r in M]; ids=list(range(len(A))); r=0; rows=[];cols=[];det=1
    for c in range(len(A[0])):
        j=next((j for j in range(r,len(A)) if A[j][c]),None)
        if j is None: continue
        A[r],A[j]=A[j],A[r];ids[r],ids[j]=ids[j],ids[r]
        rows.append(ids[r]);cols.append(c)
        v=A[r][c];det=det*v%P
        A[r]=[x*pow(v,P-2,P)%P for x in A[r]]
        for k in range(r+1,len(A)):
            v=A[k][c]
            if v: A[k]=[(x-v*y)%P for x,y in zip(A[k],A[r])]
        r+=1
        if r==len(A):break
    return r,rows,cols

def main():
    a=list(partitions(12));b=list(partitions(11))
    M=[[intersection(tuple(sorted(x+y,reverse=True))) for y in b] for x in a]
    rank, rows, cols=rank_certificate(M)
    assert rank==43
    print('Pairing shape',len(a),len(b),'rank mod',P,':',rank)
    print('43 by 43 nonzero minor rows:',rows,'columns:',cols)
    # Every supplied FZ relation must vanish on all 56 pairing columns.
    import json
    from fractions import Fraction
    fz=json.load(open('workspace/fz25_upper_data.json'))
    fb=[tuple(v) for v in fz['basis']]
    idx={v:i for i,v in enumerate(a)}
    for rel in fz['matrix']:
        rr=[]
        for x in rel:
            q=Fraction(str(x));rr.append(q.numerator*pow(q.denominator,P-2,P)%P)
        for j in range(len(b)):
            assert sum(x*M[idx[v]][j] for x,v in zip(rr,fb))%P==0
    print('All 59 FZ relation rows annihilate all pairing columns.')
if __name__=='__main__':main()
