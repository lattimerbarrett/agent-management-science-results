from itertools import combinations, product
from pathlib import Path

# All maximal intersecting families: choose a side of every complementary pair,
# then retain choices pairwise meeting. This is exhaustive by self-duality.
def maximal_intersecting(t):
    full=(1<<t)-1
    pairs=[(a,full^a) for a in range(1<<t) if a < (full^a)]
    out=[]
    def search(k, chosen):
        if k==len(pairs):
            out.append(frozenset(chosen)); return
        for a in pairs[k]:
            if a and all(a & b for b in chosen):
                search(k+1,chosen+[a])
    search(0,[])
    return out

def family_orders(t,fams):
    full=(1<<t)-1
    pairs=[(a,full^a) for a in range(1<<t) if a < (full^a)]
    orders=[]
    for j in range(t):
        def key(F):
            return tuple(int((a if a in F else b)&(1<<j)!=0) for a,b in pairs)
        orders.append(sorted(range(len(fams)),key=lambda i:key(fams[i])))
    return orders

def verify_orders(t, fams, orders):
    n=len(fams)
    ranks=[{v:i for i,v in enumerate(L)} for L in orders]
    for x,y in combinations(range(n),2):
        assert any(r[x]<r[y] for r in ranks)
        assert any(r[y]<r[x] for r in ranks)
    for triple in combinations(range(n),3):
        for x in triple:
            assert any(all(r[y]<r[x] for y in triple if y!=x) for r in ranks)
    # Explicitly build poset linear extensions and check their intersection.
    els=[(i,) for i in range(n)]+list(combinations(range(n),2))
    exts=[]
    for L,r in zip(orders,ranks):
        ext=[]
        for v in L:
            ext.append((v,))
            ext.extend(e for e in combinations(range(n),2) if v in e and max(e,key=lambda x:r[x])==v)
        assert len(ext)==len(els)
        exts.append({a:i for i,a in enumerate(ext)})
    for a in els:
        for b in els:
            expected=set(a)<=set(b)
            assert all(r[a]<=r[b] for r in exts)==expected,(a,b)

def verify_lifts(t, fams, next_fams):
    full=(1<<t)-1
    next_set=set(next_fams)
    lifts=[frozenset(a for a in range(1<<(t+1)) if (a&full) in F) for F in fams]
    assert len(set(lifts))==len(fams)
    assert all(F in next_set for F in lifts)
    star=frozenset(a for a in range(1<<(t+1)) if a&(1<<t))
    assert star in next_set and star not in lifts

if __name__=='__main__':
    fs={t:maximal_intersecting(t) for t in range(1,7)}
    for t,fams in fs.items():
        print('lambda(%d)=%d'%(t,len(fams)),flush=True)
        if t<=4:
            verify_orders(t,fams,family_orders(t,fams))
            print('  all suitable-order and full incidence-realizer conditions checked',flush=True)
        if t<5:
            verify_lifts(t,fams,fs[t+1])
            print('  lift injection and extra star checked',flush=True)
    Path('workspace').mkdir(exist_ok=True)
    Path('workspace/agent2_lambda_check.py').write_text(Path(__file__).read_text())
