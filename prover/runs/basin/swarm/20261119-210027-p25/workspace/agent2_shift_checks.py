import itertools, numpy as np, random, json, math

def check_shift(k,m,trials):
    vs=list(itertools.combinations(range(m),k)); idx={v:i for i,v in enumerate(vs)}; n=len(vs)
    A=np.zeros((n,n),dtype='int64')
    for v,i in idx.items():
        for b in range(v[-1]+1,m):
            j=idx[v[1:]+(b,)]; A[i,j]=A[j,i]=1
    A2=A@A; A3=A2@A; A5=A3@A2
    assert np.trace(A3)==0 and np.trace(A5)==0
    Q=(A+A3)>0
    safe=[j for j in range(4,k-2) if j%2==0]
    rng=random.Random(20261123+k)
    counts=[0]*n
    for _ in range(trials):
        perm=list(range(m));rng.shuffle(perm)
        ranks=[0]*m
        for r,x in enumerate(perm):ranks[x]=r
        S=[i for i,v in enumerate(vs) if min(range(k),key=lambda j:ranks[v[j]])+1 in safe]
        assert not Q[np.ix_(S,S)].any()
        for i in S:counts[i]+=1
    # Exhaustively check ALL sign supports for this finite shift graph.
    counts_sign=np.zeros(n,dtype='int64')
    for signs in itertools.product((-1,1),repeat=m):
        scores=np.array([sum(((-1)**(j+1))*signs[a] for j,a in enumerate(v)) for v in vs])
        # Verify the edge identity and all odd-walk support disjointness.
        for i,j in zip(*np.where(np.triu(A)>0)):
            assert abs(scores[i]+scores[j])<=2
        S=np.flatnonzero(scores>3)
        assert not Q[np.ix_(S,S)].any()
        counts_sign[S]+=1
    numerator=sum(math.comb(k,j) for j in range((k+3)//2+1,k+1))
    assert all(x==numerator*(2**(m-k)) for x in counts_sign)
    return dict(k=k,m=m,vertices=n,edges=int(A.sum()//2),safe_positions=safe,support_fraction=len(safe)/k,trials=trials,min_empirical=min(counts)/trials,max_empirical=max(counts)/trials,all_sign_assignments=2**m,score_support_fraction=numerator/2**k)

out=[check_shift(8,11,2000),check_shift(10,12,2000),check_shift(12,14,2000)]
print(out)
open('workspace/agent2_shift_checks.json','w').write(json.dumps(out,indent=2))
# Export this actual executable checker.
code=open('scratchpad.py').read()
open('workspace/agent2_shift_checks.py','w').write(code)

# Exact integer reservoir bookkeeping, no floating point.
from fractions import Fraction
parameter_checks=[]
for k,m in [(12,14),(24,26),(66,68),(606,608)]:
    M=math.factorial(m)
    d=M//2-3*(M//k)
    assert Fraction(d,M)==Fraction(1,2)-Fraction(3,k)
    r=math.comb(m,k)
    T=1
    exact_delta=Fraction(d*T,3*((M+d)*T+r))
    limit=Fraction(d,3*(M+d))
    assert exact_delta<=limit<Fraction(1,9)
    parameter_checks.append(dict(k=k,m=m,branch_vertices=r,p=str(Fraction(d,M)),density=str(exact_delta),density_float=float(exact_delta),limit=str(limit)))
print(parameter_checks)
open('workspace/agent2_exact_density_checks.json','w').write(json.dumps(parameter_checks,indent=2))
