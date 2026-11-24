"""Exact checks for the d=8 rainbow-lex upper bound (no huge enumeration).
Each row A_j is a subset of r coordinates. Every two rows are qualitatively
independent: all four Boolean intersections are nonempty. Thus lex orders
with these preference columns are 3-suitable on all 2^L bitstrings.
Moreover every row and its complement meets each group of coordinates,
so each group supplies both orientations of every pair of bitstrings.
"""
from itertools import combinations, product
from functools import lru_cache

def lambda7():
    m=6;subsets=list(range(1,1<<m));adj=[]
    for a in subsets:
        adj.append(sum(1<<j for j,b in enumerate(subsets)
                       if a&b and a&b!=a and a&b!=b))
    @lru_cache(None)
    def rec(mask):
        total=1
        while mask:
            bit=mask&-mask;mask^=bit;j=bit.bit_length()-1
            total+=rec(mask&adj[j])
        return total
    return rec((1<<len(subsets))-1)

def code_for(groupsizes):
    r=sum(groupsizes);groups=[];start=0
    for size in groupsizes:
        groups.append(set(range(start,start+size)));start+=size
    # distinguished coordinate 0 belongs to a group of size 2 when possible
    distinguished=next(iter(min(groups,key=len)))
    U=set(range(r));weight=r//2
    rows=[set(A) for A in combinations(range(r),weight)
          if distinguished in A and all(set(A)&g and (U-set(A))&g for g in groups)]
    assert rows
    for A in rows:
        assert all(A&g and (U-A)&g for g in groups)
    for A,B in combinations(rows,2):
        assert A&B and A&(U-B) and (U-A)&B and (U-A)&(U-B)
    return r,groups,rows

def small_lex_check(r,groups,rows):
    # Exhaust all triples on 32 sample bitstrings using five rows.
    rows=rows[:5];words=list(product((0,1),repeat=len(rows)))
    orders=[]
    for coordinate in range(r):
        orders.append(sorted(range(len(words)),key=lambda w:tuple(
            words[w][j] if coordinate in rows[j] else 1-words[w][j]
            for j in range(len(rows)))))
    ranks=[{x:i for i,x in enumerate(o)} for o in orders]
    for x,y in combinations(range(len(words)),2):
        for g in groups:
            assert any(ranks[i][x]>ranks[i][y] for i in g)
            assert any(ranks[i][y]>ranks[i][x] for i in g)
    for triple in combinations(range(len(words)),3):
        for x in triple:
            assert any(all(ranks[i][x]>ranks[i][y] for y in triple if y!=x)
                       for i in range(r))

if __name__=='__main__':
    lam=lambda7();assert lam==1422564
    print('lambda(7), computed:',lam)
    for t,sizes in [(3,[3,3,3]),(4,[2,2,3,3]),(5,[2,2,2,2,3]),(6,[2]*6)]:
        r,groups,rows=code_for(sizes)
        small_lex_check(r,groups,rows)
        assert r-t==6 and 2**len(rows)>=lam+1
        print('t,r,rows,capacity:',t,r,len(rows),2**len(rows))
    print('All four Boolean intersections, group traces, and sampled lex triples checked.')


def explicit_product_check(t,sizes,n=8):
    r,groups,rows=code_for(sizes)
    rows=rows[:3]
    words=list(product((0,1),repeat=3))[:n]
    sigmas=[]
    for coordinate in range(r):
        sigmas.append(sorted(range(n),key=lambda w:tuple(
            words[w][j] if coordinate in rows[j] else 1-words[w][j]
            for j in range(3))))
    # Standard example S_t: a_i=2i, b_i=2i+1.
    P=list(range(2*t))
    def ple(p,q):
        return p==q or (p%2==0 and q%2==1 and p//2!=q//2)
    PL=[]
    for i in range(t):
        order=[2*j for j in range(t) if j!=i]+[2*i+1,2*i]+[2*j+1 for j in range(t) if j!=i]
        ranks={v:j for j,v in enumerate(order)}
        assert all(not ple(a,b) or ranks[a]<=ranks[b] for a in P for b in P)
        PL.append(ranks)
    assert all(ple(a,b)==all(L[a]<=L[b] for L in PL) for a in P for b in P)
    Q=[frozenset([v]) for v in range(n)]+[frozenset(e) for e in combinations(range(n),2)]
    X=[(p,q) for p in P for q in Q]
    exts=[]
    for c,sigma in enumerate(sigmas):
        g=next(i for i,G in enumerate(groups) if c in G)
        vrank={v:i for i,v in enumerate(sigma)}
        qnumber={q:i for i,q in enumerate(Q)}
        order=sorted(X,key=lambda x:(max(vrank[v] for v in x[1]),PL[g][x[0]],len(x[1]),qnumber[x[1]]))
        exts.append({x:i for i,x in enumerate(order)})
    for x in X:
        for y in X:
            expected=ple(x[0],y[0]) and x[1]<=y[1]
            actual=all(L[x]<=L[y] for L in exts)
            assert actual==expected,(t,x,y,actual,expected)
    return len(X)

if __name__=='__main__':
    for t,sizes in [(3,[3,3,3]),(4,[2,2,3,3]),(5,[2,2,2,2,3]),(6,[2]*6)]:
        print('Explicit realizer checked t=',t,'product size=',explicit_product_check(t,sizes))
