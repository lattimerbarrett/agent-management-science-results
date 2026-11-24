"""Exact Faber-Zagier calculation for R^12(M_25), Python stdlib only."""
from fractions import Fraction
from math import factorial, comb, prod
from functools import lru_cache
import json

G=25
D=12

def partitions(n, lo=1):
    if n==0:
        yield ()
    for a in range(lo,n+1):
        for t in partitions(n-a,a):
            yield (a,)+t

BASIS=list(partitions(D))
A=[factorial(6*n)//(factorial(3*n)*factorial(2*n)) for n in range(D+1)]
B=[Fraction(A[n]*(6*n+1),6*n-1) for n in range(D+1)]

@lru_cache(None)
def kap(t):
    """Sum over permutations by cycles, returned as kappa polynomial.
    Remove zero indices using kappa(K0^z M)=(48+len(M))_z kappa(M).
    For positive indices, choose cycle containing a fixed first label.
    """
    z=t.count(0)
    if z:
        u=tuple(x for x in t if x)
        factor=prod(range(2*G-2+len(u),2*G-2+len(u)+z))
        return {m:c*factor for m,c in kap(u).items()}
    if not t:
        return {():1}
    x=t[0]
    rest=t[1:]
    vals=sorted(set(rest))
    counts=[rest.count(v) for v in vals]
    out={}
    def rec(i,chosen,left,ways):
        if i==len(vals):
            s=x+sum(chosen)
            fac=ways*factorial(len(chosen))
            for m,c in kap(tuple(left)).items():
                key=tuple(sorted((s,)+m))
                out[key]=out.get(key,0)+fac*c
            return
        v=vals[i]; n=counts[i]
        for k in range(n+1):
            rec(i+1,chosen+[v]*k,left+[v]*(n-k),ways*comb(n,k))
    rec(0,[],[],1)
    return out

@lru_cache(None)
def exp_terms(r):
    out={}
    for n in range(r+1):
        for t in partitions(n):
            c=Fraction(1)
            for j in set(t):
                e=t.count(j)
                c*=Fraction((-A[j])**e,factorial(e))
            out[t]=c
    return out

def relation(r,sigma):
    terms=dict(exp_terms(r))
    for part in sigma:
        shift=part//3
        series=A if part%3==0 else B
        new={}
        for t,c in terms.items():
            for n in range(shift,r-sum(t)+1):
                key=tuple(sorted(t+(n,)))
                new[key]=new.get(key,0)+c*series[n-shift]
        terms=new
    ans={}
    for t,c in terms.items():
        if sum(t)!=r: continue
        for m,v in kap(t).items():
            ans[m]=ans.get(m,0)+c*v
    return {m:c for m,c in ans.items() if c}

def all_rows():
    rows=[]; labels=[]
    for r in range(1,D+1):
        for w in range(max(0,3*r-G)):
            if (G-r-w-1)%2: continue
            for sigma in partitions(w):
                if any(s%3==2 for s in sigma): continue
                rel=relation(r,sigma)
                for mul in partitions(D-r):
                    row={tuple(sorted(m+mul)):c for m,c in rel.items()}
                    rows.append([row.get(m,0) for m in BASIS])
                    labels.append((r,sigma,mul))
    return rows,labels

def modular_certificate(rows,p=1000000007):
    pivots={}; indices=[]
    for i,row in enumerate(rows):
        v=[(x.numerator*pow(x.denominator,-1,p))%p if isinstance(x,Fraction) else x%p for x in row]
        for col,w in sorted(pivots.items()):
            if v[col]:
                c=v[col]
                v=[(a-c*b)%p for a,b in zip(v,w)]
        if any(v):
            col=next(j for j,x in enumerate(v) if x)
            inv=pow(v[col],-1,p)
            pivots[col]=[(a*inv)%p for a in v]
            indices.append(i)
    return indices,list(pivots)

if __name__=='__main__':
    rows,labels=all_rows()
    assert len(BASIS)==77
    ids,cols=modular_certificate(rows)
    print('basis',len(BASIS),'relations',len(rows),'modular rank',len(ids))
    print('independent labels:',[labels[i] for i in ids])
    assert len(ids)==33
    # Modular rank already suffices: 33 independent rational relations.
    payload={'basis':BASIS,'labels':labels,'matrix':[[str(x) for x in row] for row in rows], 'independent_rows':ids,'pivot_columns':cols,'prime':1000000007}
    with open('workspace/agent1_fz_certificate.json','w') as f: json.dump(payload,f)
