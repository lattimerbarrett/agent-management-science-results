from itertools import combinations

def check(n=6,d=3):
    facets=[sum(1<<v for v in f) for f in combinations(range(n),d+1)]
    m=len(facets)
    # For each candidate last facet, tabulate the trace of each other facet.
    traces=[[F&G for G in facets] for F in facets]
    proper=[[(F ^ (1<<v)) for v in range(n) if F>>v&1] for F in facets]
    shell=[False]*(1<<m)
    shell[0]=True
    shelling_extensions=[False]*(1<<m)
    shelling_extensions[-1]=True
    def attachment_ok(S,j):
        if S==0: return True
        F=facets[j]
        intersections=[traces[j][i] for i in range(m) if S>>i&1]
        ridges=[R for R in proper[j] if any(R&T==R for T in intersections)]
        # Intersection must be nonempty and pure of dimension d-1.
        return bool(ridges) and all(any(T&R==T for R in ridges) for T in intersections)
    for S in range(1,1<<m):
        for j in range(m):
            if S>>j&1 and shell[S^(1<<j)] and attachment_ok(S^(1<<j),j):
                shell[S]=True
                break
    # Fixed shelling prefixes can be extended precisely by these attachments.
    for S in range((1<<m)-2,-1,-1):
        shelling_extensions[S]=any(not(S>>j&1) and attachment_ok(S,j) and shelling_extensions[S|(1<<j)] for j in range(m))
    bad=[S for S in range(1,1<<m) if shell[S] and not shelling_extensions[S]]
    result={'n':n,'dimension':d,'facets':m,'subsets':1<<m,'shellable_nonempty':sum(shell)-1,'nonextendable_shellable':len(bad)}
    assert not bad, result
    return result

if __name__=='__main__':
    print(check())
