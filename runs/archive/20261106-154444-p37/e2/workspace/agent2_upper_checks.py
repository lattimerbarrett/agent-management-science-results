from itertools import combinations, product

def upsets(k):
    N=1<<k
    return [frozenset(A for A in range(N) if mask>>A&1)
            for mask in range(1<<N)
            if all(not(mask>>A&1) or all(mask>>B&1 for B in range(N) if A&B==A) for A in range(N))]

def check(k):
    us=upsets(k); full=(1<<k)-1; bits=list(range(1,full))
    patterns=sorted(set(tuple(int(B in U) for B in bits) for U in us))
    assert len(patterns)==len(us)-2
    intersecting=[U for U in us if all(A&B for A in U for B in U)]
    if k>=3: assert len(us)-len(intersecting)>=3
    d=k+2; n=len(patterns)
    # Bit1 preferred exactly on A_B={coordinate0} union B in coordinates2..d-1.
    def pref(i,B): return i==0 or (i>=2 and bool(B>>(i-2)&1))
    perms=[]
    for i in range(d):
        perms.append(sorted(range(n),key=lambda v:tuple(patterns[v][j] if pref(i,B) else 1-patterns[v][j] for j,B in enumerate(bits))))
    rank=[{v:j for j,v in enumerate(p)} for p in perms]
    for a,b in combinations(range(n),2):
        for group in [range(2),range(2,d)]:
            assert any(rank[i][a]<rank[i][b] for i in group)
            assert any(rank[i][b]<rank[i][a] for i in group)
    for a,b,c in combinations(range(n),3):
        for v,other in [(a,(b,c)),(b,(a,c)),(c,(a,b))]:
            assert any(all(rank[i][v]>rank[i][w] for w in other) for i in range(d))
    # Test proposed coordinate embedding on [2]^2 x Q_n exhaustively.
    Q=[frozenset([a]) for a in range(n)]+[frozenset(e) for e in combinations(range(n),2)]
    elems=[(x,y,A) for x in range(2) for y in range(2) for A in Q]
    coords=[tuple((max(rank[i][a] for a in A), x if i<2 else y) for i in range(d)) for x,y,A in elems]
    for j,(x,y,A) in enumerate(elems):
        for h,(xx,yy,B) in enumerate(elems):
            actual=x<=xx and y<=yy and A<=B
            embedded=all(coords[j][i]<=coords[h][i] for i in range(d))
            assert actual==embedded,(k,elems[j],elems[h])
    print(dict(k=k,upsets=len(us),intersecting_upsets=len(intersecting),vertices=n,product_elements=len(elems),checked_ordered_pairs=len(elems)**2))

if __name__=='__main__':
    for k in [2,3]: check(k)
