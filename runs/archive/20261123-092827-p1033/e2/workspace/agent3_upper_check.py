from itertools import combinations
from math import comb
import json, os, time

def verify_construction(n):
    r=2
    blocks=[frozenset(e) for e in combinations(range(n),2) for _ in range(3)]
    m=len(blocks)
    inc=[frozenset(b for b,B in enumerate(blocks) if i in B) for i in range(n)]
    codeg={(i,j):len(inc[i]&inc[j]) for i in range(n) for j in range(n) if i!=j}
    D=max(map(len,inc)); d=D+r; k=n+d
    # Disjoint actual vertex sets: cores, block labels, private padding reservoirs.
    at=0; cores=[]
    for i in range(n): cores.append(frozenset(range(at,at+n))); at+=n
    z=list(range(at,at+m)); at+=m
    reservoirs=[]
    for i in range(n): reservoirs.append(frozenset(range(at,at+d+n))); at+=d+n
    all_modes=[]; lookup={}
    for i in range(n):
        for sz in range(r+1):
            for EE in combinations(sorted(inc[i]),sz):
                E=frozenset(EE)
                J=frozenset(j for j in range(n) if j!=i and 2*len(E&inc[j])>=codeg[i,j])
                assert len(J)<r
                Z=frozenset(z[b] for b in inc[i]-E)
                assert len(Z)+len(J)<=d
                mode=(i,E,J,Z)
                all_modes.append(mode); lookup[i,E]=mode
    # This condition certifies intersections for ALL contact/padding choices.
    pairs=0
    for (i,E,J,Z),(a,F,L,W) in combinations(all_modes,2):
        if i!=a:
            assert a in J or i in L or Z&W
            pairs+=1
    # Every possible (n-1)-cover of the entire actual ground set gets a concrete avoiding edge.
    tested=0; contact_uses=0
    for CC in combinations(range(at),n-1):
        C=frozenset(CC)
        U=[i for i in range(n) if not cores[i]&C]
        selected=frozenset(b for b in range(m) if z[b] in C)
        assert len(U)>len(selected)
        assert sum(len(inc[i]&selected) for i in U)<=r*len(selected)<r*len(U)
        i=next(i for i in U if len(inc[i]&selected)<r)
        E=inc[i]&selected
        _,_,J,Z=lookup[i,E]
        F=set(cores[i])|set(Z)
        for j in J:
            F.add(next(v for v in cores[j] if v not in C)); contact_uses+=1
        needed=k-len(F)
        pad=[v for v in reservoirs[i] if v not in C][:needed]
        assert len(pad)==needed
        F.update(pad)
        assert len(F)==k and not F&C and cores[i]<=F
        assert all(len(F&cores[j])<=1 for j in range(n) if j!=i)
        tested+=1
    assert tested==comb(at,n-1)
    return {'n':n,'r':r,'blocks':m,'D':D,'d':d,'k':k,'vertices':at,'modes':len(all_modes),'modes_with_nonempty_contacts':sum(bool(M[2]) for M in all_modes),'cross_mode_pairs_checked':pairs,'all_small_covers_checked':tested,'contact_witnesses_used':contact_uses,'total_deficit':n*d}

if __name__=='__main__':
    os.makedirs('workspace',exist_ok=True)
    # Copy this exact standalone executable, not just results.
    source=open(__file__).read()
    open('workspace/agent3_upper_check.py','w').write(source)
    ans=[verify_construction(n) for n in (3,4)]
    print(json.dumps(ans,indent=2))
    json.dump(ans,open('workspace/agent3_upper_checks.json','w'),indent=2)
