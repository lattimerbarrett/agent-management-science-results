"""Exact small construction checks and numerical probability-bound checks.
The asymptotic existence proof is analytic; this file never treats sampling
as a proof of the universal incidence expansion condition.
"""
from itertools import combinations, product
from math import ceil, floor, sqrt, log, exp, e
import json, sys

def build(blocks,n,r,pad_size=None):
    blocks=[frozenset(B) for B in blocks]
    inc=[[a for a,B in enumerate(blocks) if i in B] for i in range(n)]
    lam=min(sum(i in B and j in B for B in blocks) for i,j in combinations(range(n),2))
    assert lam>0 and all(len(B)<=r for B in blocks)
    maxJ=0
    cores=[frozenset(('X',i,a) for a in range(n)) for i in range(n)]
    D=max(map(len,inc)); d=D+r; k=n+d
    pads=[frozenset(('Y',i,a) for a in range(d+n)) for i in range(n)]
    groups=[]
    for i in range(n):
        out=set()
        for z in range(min(r-1,len(inc[i]))+1):
            for EE in combinations(inc[i],z):
                E=set(EE)
                J=[j for j in range(n) if j!=i and 2*sum(j in blocks[a] for a in E)>=lam]
                maxJ=max(maxJ,len(J)); assert len(J)<r
                ext={('Z',a) for a in inc[i] if a not in E}
                for reps in product(*(cores[j] for j in J)):
                    base=set(cores[i])|ext|set(reps)
                    q=k-len(base)
                    assert 0<=q<=d
                    for P in combinations(pads[i],q):out.add(frozenset(base|set(P)))
        groups.append(out)
    return cores,groups,k,{'block_count':len(blocks),'block_size_bound':r,'lambda':lam,'D':D,'max_contact_count':maxJ}

def probability_check(n):
    assert n>=ceil(exp(8))
    x=log(n); r=ceil(sqrt(n)); m=ceil(64*n*x); lam=floor(16*x); D=ceil(512*r*x)
    p2=r*(r-1)/(n*(n-1)); mu=m*p2; mud=m*r/n
    assert r*(r-1)>=n/2
    assert mu>=32*x*(1-1e-13)
    assert lam<=mu/2 and lam>=15*x
    assert mud<=65*r*x
    assert e*mud/D<0.5
    h=ceil(lam*r/2)
    # The incidence-event probability is zero when h exceeds the possible r^2 incidences.
    if h<=r*r:
        log_one=h*log(e*r**3/(n*h))
        log_union=r*(log(m)+x)+log_one
        assert log_union<=-3.5*r*x+1e-8
    else:log_union=float('-inf')
    simplified=exp(-2*x)/2+exp((1-256*r)*x)+exp(-3.5*r*x)
    assert simplified<1
    assert n*(D+r)<=2000*n**1.5*x
    return {'n':n,'r':r,'m':m,'lambda':lam,'D':D,'log_expansion_failure_bound':log_union,'total_failure_upper':simplified}

if __name__=='__main__':
    sys.path.insert(0,'workspace')
    from agent3_verify import check_system
    cores,groups,k,meta=build(list(combinations(range(3),2)),3,2)
    exact=check_system(cores,groups,k,3)
    ns=sorted({ceil(exp(8)),3000,10000,100000,10**6,10**8,10**12}|{ceil(exp(8+j/10)) for j in range(121)})
    probs=[probability_check(n) for n in ns]
    result={'exact_small_construction':exact,'block_parameters':meta,'probability_checks':probs}
    with open('workspace/agent2_upper_checks.json','w') as f:json.dump(result,f,indent=2)
    print(exact,meta)
    print('All',len(probs),'probability-bound checks passed; first:',probs[0])
