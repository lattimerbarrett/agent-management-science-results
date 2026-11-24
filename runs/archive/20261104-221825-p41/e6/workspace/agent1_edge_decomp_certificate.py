import json,itertools,math
from collections import Counter

def check(m=4,r=4):
    old=json.load(open('workspace/agent3_2core_order.json'))
    oldseen={frozenset()}; restrictions=[]
    for j,f in enumerate(old):
        f=frozenset(f)
        new=[frozenset(s) for q in range(1,4) for s in itertools.combinations(f,q) if frozenset(s) not in oldseen]
        minimal=[s for s in new if not any(t<s for t in new)]
        assert j==0 or len(minimal)==1,(j,minimal)
        restrictions.append(f if j==0 else minimal[0])
        for q in range(4):oldseen.update(frozenset(s) for s in itertools.combinations(f,q))
    fs={frozenset(s) for f in old for s in itertools.combinations([m*v+i for v in f for i in range(m)],r)}
    ridgecounts=Counter(t for f in fs for t in map(frozenset,itertools.combinations(f,r-1)))
    initial=len(fs);cert=[]
    for f,sigma in reversed(list(zip(old,restrictions))[1:]):
        assert 1<=len(sigma)<=2
        blockchoices=[range(m*v,m*(v+1)) for v in sorted(sigma)]
        for tup in itertools.product(*blockchoices):
            s=frozenset(tup)
            removed={f for f in fs if s<=f}
            assert removed
            # Link is exactly a uniform skeleton, hence vertex-decomposable.
            lk={f-s for f in removed}
            vs=set().union(*lk)
            assert all(len(g)==r-len(s) for g in lk)
            assert len(lk)==math.comb(len(vs),r-len(s)),(f,s,len(lk),len(vs))
            # Verify literal deletion has no lower-dimensional maximal faces.
            for g in removed:
                for x in s:
                    assert ridgecounts[g-{x}]>=2,(f,s,g,x)
            fs-=removed
            for g in removed:
                for t in map(frozenset,itertools.combinations(g,r-1)):
                    ridgecounts[t]-=1
            cert.append(tuple(tup))
    vs=set().union(*fs)
    assert len(fs)==math.comb(len(vs),r)
    return initial,len(cert),len(fs)

if __name__=='__main__':print(check())
