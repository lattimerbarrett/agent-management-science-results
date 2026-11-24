import json,pickle
from itertools import combinations,product
from agent2_decomp import subs, link, deletion, rank, witness

def check_base18():
    order=json.load(open('workspace/agent3_2core_order.json'))
    blocks={v:[1<<(2*v),1<<(2*v+1)] for v in range(9)}
    prefix=[];acc=set()
    for t in order:
        cluster=[x for v in t for x in blocks[v]]
        acc.update(sum(c) for c in combinations(cluster,4))
        prefix.append(frozenset(acc))
    current=prefix[-1];proof=[]
    for j in range(len(order)-1,0,-1):
        t=order[j]
        oldedges={frozenset(e) for f in order[:j] for e in combinations(f,2)}
        R=[v for v in t if frozenset(set(t)-{v}) in oldedges]
        assert len(R) in (1,2)
        for choices in product(*(blocks[v] for v in R)):
            s=sum(choices)
            assert any(f&s==s for f in current)
            lk=link(current,s);de=deletion(current,s)
            assert rank(de)==4
            verts=set(v for f in lk for v in subs(f) if v.bit_count()==1)
            if len(R)==1:
                assert lk==frozenset(sum(c) for c in combinations(verts,3))
            else:
                assert rank(lk)==2
                seen={next(iter(verts))}
                while True:
                    new=seen|{v for e in lk if any(e&u for u in seen) for v in verts if v&e}
                    if new==seen:break
                    seen=new
                assert seen==verts
            proof.append((s,sorted(lk)));current=de
        assert current==prefix[j-1]
    assert witness(current,0) is not None
    # Independently verify completeness of graph and closure of triangles.
    from agent2_decomp import skeleton
    T=skeleton(prefix[-1],3)
    assert len(skeleton(prefix[-1],2))==153
    assert len(T)<816
    missing=0
    for F in (sum(c) for c in combinations([1<<v for v in range(18)],4)):
        if F in prefix[-1]:continue
        assert sum((F^v) in T for v in subs(F) if v.bit_count()==1)<=2
        missing+=1
    return len(prefix[-1]),len(proof),len(current),missing

if __name__=='__main__':print(check_base18())
