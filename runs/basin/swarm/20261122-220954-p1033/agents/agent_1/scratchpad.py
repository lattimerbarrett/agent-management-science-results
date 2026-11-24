from itertools import combinations, product
from math import isqrt

def construction(t):
    k = 2*t-1
    cores=[]
    start=0
    for i in range(t):
        size=t+i
        cores.append(tuple(range(start,start+size)))
        start+=size
    groups=[]
    for i in range(t):
        group=[]
        for tail in product(*cores[i+1:]):
            group.append(frozenset(cores[i])|frozenset(tail))
        groups.append(group)
    return k, cores, groups, start

for t in range(2,5):
    k,cores,groups,n=construction(t)
    fam=[f for g in groups for f in g]
    assert len(set(fam))==len(fam)
    assert all(len(f)==k for f in fam)
    assert all(frozenset(cores[i]) <= f for i,g in enumerate(groups) for f in g)
    assert all(set(cores[i]).isdisjoint(cores[j]) for i in range(t) for j in range(i))
    masks=[sum(1<<v for v in f) for f in fam]
    assert all(a&b for a,b in combinations(masks,2))
    checked=0
    for c in combinations(range(n),t-1):
        cm=sum(1<<v for v in c)
        assert any(not (cm&f) for f in masks)
        checked+=1
    witness=sum(1<<x[0] for x in cores)
    assert all(witness&f for f in masks)
    B=sum(k-len(x) for x in cores)
    assert B==t*(t-1)//2
    print(dict(t=t,k=k,n=n,edges=len(fam),covers_ruled_out=checked,B=B))

# Check the numerical form of the derived lower bound against the
# construction, using integer arithmetic: m <= (floor(B/(t-m+1))+1)^2.
for t in range(2,1001):
    B=t*(t-1)//2
    assert all(m <= (B//(t-m+1)+1)**2 for m in range(1,t+1))
print('All finite checks passed.')
