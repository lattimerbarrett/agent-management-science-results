import importlib.util
from itertools import product
from math import comb
spec=importlib.util.spec_from_file_location('team','agents/agent_1/scratchpad.py')
t=importlib.util.module_from_spec(spec);spec.loader.exec_module(t)
# Independently count antichains of T3 x T3, by bottom/top choices.
E=list(product(range(1,7),repeat=2))
levs=[[x for x in E if sum(a.bit_count() for a in x)==r] for r in [2,3,4]]
lo,mi,hi=levs
def le(x,y):return all(a&b==a for a,b in zip(x,y))
def unions(vals):
    ans=[0]*(1<<len(vals))
    for m in range(1,len(ans)):
        b=m&-m;ans[m]=ans[m^b]|vals[b.bit_length()-1]
    return ans
LM=unions([sum(1<<j for j,y in enumerate(mi) if le(x,y)) for x in lo])
LH=unions([sum(1<<j for j,y in enumerate(hi) if le(x,y)) for x in lo])
HM=unions([sum(1<<j for j,y in enumerate(mi) if le(y,x)) for x in hi])
cnt=sum(1<<(len(mi)-(LM[a]|HM[b]).bit_count()) for a in range(1<<len(lo)) for b in range(1<<len(hi)) if not LH[a]&b)
assert cnt==t.base8()==783558
print('Independent rank-by-rank antichain count:',cnt)
# Larger checks of chain property; written induction is what proves all n.
for n in range(11,16):t.check_chains(n)
print('Diamond chain property also checked through n=15.')
# Direct counts of intersecting upsets check ideal/complement-image condition.
for n in range(1,5):
    mask=(1<<(1<<n))-1
    direct=encoded=0
    for D in t.ideals(n):
        U=[x for x in range(1<<n) if not(D>>x&1)]
        direct+=all(x&y for x in U for y in U)
        rev=sum((D>>x&1)<<(((1<<n)-1)^x) for x in range(1<<n))
        encoded+=(D|rev)==mask
    assert direct==encoded
    print('Intersecting upsets B_%d:'%n,direct)
