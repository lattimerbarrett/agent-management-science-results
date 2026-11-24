import json,itertools

def exact_shelling(order):
    seen={frozenset()}
    dimension=len(order[0])-1
    for j,F0 in enumerate(order):
        F=frozenset(F0)
        assert len(F)==dimension+1 and F not in seen,(j,F)
        inter=[frozenset(s) for r in range(dimension+1) for s in itertools.combinations(F,r) if frozenset(s) in seen]
        maximal=[s for s in inter if not any(s<t for t in inter)]
        if j:assert all(len(s)==dimension for s in maximal),(j,F,maximal)
        for r in range(dimension+2):
            seen.update(frozenset(s) for s in itertools.combinations(F,r))
    return seen

def check():
    K=json.load(open('workspace/agent3_2core_order.json'))
    kfaces=exact_shelling(K)
    assert sum(len(f)==2 for f in kfaces)==36
    assert all(sum(frozenset(t) in kfaces for t in itertools.combinations(Q,3))!=3 for Q in itertools.combinations(range(9),4))
    order=json.load(open('workspace/agent3_base36_shelling.json'))
    seen=exact_shelling(order)
    vertices=set().union(*map(set,order))
    assert vertices==set(range(36))
    assert sum(len(f)==2 for f in seen)==630
    missing=0
    for F0 in itertools.combinations(range(36),4):
        F=frozenset(F0)
        if F in seen:continue
        missing+=1
        # Since the graph is complete, an attachment is pure2 iff >=3 boundary triangles exist.
        assert sum(frozenset(t) in seen for t in itertools.combinations(F0,3))<=2,F0
    return len(K),len(order),missing
if __name__=='__main__':print(check())
