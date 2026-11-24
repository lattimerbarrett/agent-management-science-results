from itertools import combinations

def verify_modes(modes):
    """Return exact intersection and cover certificates for finite abstract modes.
    modes[i] consists of pairs (external labels, contacted owner indices).
    """
    t=len(modes)
    assert t>=1 and all(modes)
    modes=[[(frozenset(E),frozenset(S)) for E,S in row] for row in modes]
    d=max(len(E)+len(S) for row in modes for E,S in row)
    for i,row in enumerate(modes):
        for E,S in row: assert i not in S and S <= set(range(t))
    for i in range(t):
        for j in range(i):
            for E,S in modes[i]:
                for F,U in modes[j]:
                    if not(E&F) and j not in S and i not in U:
                        return {'valid':False,'reason':'disjoint modes','owners':[i,j], 'modes':[(sorted(E),sorted(S)),(sorted(F),sorted(U))]}
    ext=sorted(set().union(*(E for row in modes for E,S in row)))
    tau=t
    cert=None
    for n in range(min(t,len(ext)+1)):
        for zz in combinations(ext,n):
            Z=set(zz)
            covered=[i for i,row in enumerate(modes) if all(E&Z for E,S in row)]
            cost=n+t-len(covered)
            if cost<tau: tau=cost;cert={'external':zz,'externally_covered_groups':covered}
    return {'valid':tau==t,'deficit':d,'tau':tau,'cover':cert,'groups':t,'externals':len(ext)}

if __name__=='__main__':
    cycle=[[(set(),{(i+1)%3})] for i in range(3)]
    out=verify_modes(cycle)
    assert out['valid'] and out['tau']==3 and out['deficit']==1
    # Transitive orientation on 3 owners is also intersecting, with deficit 2.
    tournament=[[(set(),set(range(i+1,3)))] for i in range(3)]
    assert verify_modes(tournament)['valid']
    # A common external label violates the cover property, as it should.
    assert not verify_modes([[({'x'},set())] for i in range(3)])['valid']
    print(out)
