from itertools import combinations

def directed_cut_counts(edges,S,X):
    a=b=0
    for u,v in edges:
        if u not in X: u,v=v,u
        assert u in X and v not in X
        a+=int(u not in S and v in S)
        b+=int(u in S and v not in S)
    return a,b

def verify(nmax=6):
    checks=0
    # Every bipartite graph with a prescribed bipartition, no isomorphism shortcut.
    for n in range(1,nmax+1):
        X=set(range(n//2)); Y=set(range(n//2,n))
        possible=[(u,v) for u in X for v in Y]
        cuts=[{v for v in range(n) if mask>>v&1} for mask in range(1<<n)]
        for mask in range(1<<len(possible)):
            edges=[e for j,e in enumerate(possible) if mask>>j&1]
            cs=[directed_cut_counts(edges,S,X) for S in cuts]
            for i,S in enumerate(cuts):
                for j,T in enumerate(cuts):
                    h=directed_cut_counts(edges,S&T,X)
                    k=directed_cut_counts(edges,S|T,X)
                    crossing=sum((u in S-T and v in T-S) or (v in S-T and u in T-S) for u,v in edges)
                    assert h[0]+k[0]==cs[i][0]+cs[j][0]-crossing
                    assert h[1]+k[1]==cs[i][1]+cs[j][1]-crossing
                    checks+=1
    return checks

if __name__=='__main__':
    print('Exact directed-cut uncrossing identities checked on',verify(5),'graph/cut-pair instances.')
