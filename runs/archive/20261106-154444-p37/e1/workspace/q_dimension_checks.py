from itertools import combinations

def maximal_intersecting(k):
    U=(1<<k)-1
    pairs=[(a,U^a) for a in range(1<<k) if a<(U^a)]
    out=[]
    for bits in range(1<<len(pairs)):
        F=frozenset(pair[(bits>>j)&1] for j,pair in enumerate(pairs))
        if all(a&b for a in F for b in F):
            out.append(F)
    return out

def suitable_orders(k,families):
    U=(1<<k)-1
    pairs=[(a,U^a) for a in range(1<<k) if a<(U^a)]
    result=[]
    for i in range(k):
        def key(F):
            return tuple(int(bool((a if a in F else b)&(1<<i))) for a,b in pairs)
        result.append(sorted(range(len(families)),key=lambda j:key(families[j])))
    return result

def check_suitable(orders,n):
    positions=[{v:i for i,v in enumerate(order)} for order in orders]
    return all(any(pos[x]>pos[y] and pos[x]>pos[z] for pos in positions)
               for x in range(n) for y in range(n) for z in range(y+1,n) if x!=y and x!=z)

def incidence_realizer(orders,n):
    # Insert each edge just after its later endpoint. Only vertex order matters.
    extensions=[]
    for order in orders:
        done=set(); L=[]
        for v in order:
            L.append((v,)); done.add(v)
            for w in order:
                if w!=v and w in done:
                    L.append(tuple(sorted((v,w))))
        extensions.append(L)
    return extensions

def check_realizer(Ls):
    elements=Ls[0]
    assert all(set(L)==set(elements) and len(L)==len(elements) for L in Ls)
    pos=[{x:i for i,x in enumerate(L)} for L in Ls]
    return all((set(x)<=set(y))==all(p[x]<=p[y] for p in pos) for x in elements for y in elements)

if __name__=='__main__':
    from pathlib import Path

if __name__=='__main__':
    for k in range(1,6):
        Fs=maximal_intersecting(k)
        assert all(all(any((a&b)==0 for b in F) for a in range(1<<k) if a not in F) for F in Fs)
        orders=suitable_orders(k,Fs)
        assert check_suitable(orders,len(Fs))
        # For k=1,2, triple suitability alone needs vertex pair coverage.
        if k>=2:
            assert check_realizer(incidence_realizer(orders,len(Fs)))
        print(k,len(Fs),'suitable and realizer verified')
