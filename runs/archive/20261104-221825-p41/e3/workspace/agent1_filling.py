"""Exact checks for the cone-filling lemma. Run using Python 3."""
from itertools import combinations
from functools import lru_cache
from agent3_check import all_faces, maximal, submasks, k_certificate

def check_certificate(facets,k,cert):
    facets=tuple(sorted(facets))
    if cert is None: return False
    if cert[0]=='simplex': return len(facets)==1 and cert[1]==facets[0]
    _,s,dc,lc=cert
    if s<=0 or s.bit_count()>k+1: return False
    faces=all_faces(facets)
    if s not in faces: return False
    d=facets[0].bit_count()
    dele=maximal(f for f in faces if f&s!=s)
    link=maximal(f^s for f in facets if f&s==s)
    if any(f.bit_count()!=d for f in dele): return False
    return check_certificate(dele,k,dc) and check_certificate(link,k,lc)

def lift_filling_certificate(gamma,fillings,a,k,cert):
    gamma=tuple(sorted(gamma));fillings=tuple(sorted(fillings))
    faces=all_faces(gamma)
    q=gamma[0].bit_count()
    assert all(f.bit_count()==q for f in gamma)
    assert a and a&(a-1)==0 and all(not(f&a) for f in gamma+fillings)
    assert all(f.bit_count()==q+1 and all((f^b) in faces for b in submasks(f) if b.bit_count()==1) for f in fillings)
    if cert[0]=='simplex':
        if not fillings: return ('simplex',a|gamma[0])
        assert gamma==(0,) and all(f.bit_count()==1 for f in fillings)
        result=('simplex',a)
        for f in fillings: result=('shed',f,result,('simplex',0))
        return result
    _,s,dc,lc=cert
    deletion=maximal(f for f in faces if f&s!=s)
    link=maximal(f^s for f in gamma if f&s==s)
    fd=tuple(f for f in fillings if f&s!=s)
    fl=tuple(f^s for f in fillings if f&s==s)
    return ('shed',s,lift_filling_certificate(deletion,fd,a,k,dc),lift_filling_certificate(link,fl,a,k,lc))

def exhaustive(n,q,k):
    bases=[sum(1<<i for i in c) for c in combinations(range(n),q)]
    fills=[sum(1<<i for i in c) for c in combinations(range(n),q+1)]
    checked=0
    for mask in range(1,1<<len(bases)):
        gamma=tuple(f for i,f in enumerate(bases) if mask>>i&1)
        cert=k_certificate(gamma,k)
        if cert is None: continue
        faces=all_faces(gamma)
        possible=[f for f in fills if all((f^(1<<i)) in faces for i in range(n) if f>>i&1)]
        for m in range(1<<len(possible)):
            ff=tuple(f for i,f in enumerate(possible) if m>>i&1)
            target=tuple(sorted(tuple(f|(1<<n) for f in gamma)+ff))
            lifted=lift_filling_certificate(gamma,ff,1<<n,k,cert)
            assert check_certificate(target,k,lifted),(gamma,ff,k)
            checked+=1
    return checked

if __name__=='__main__':
    for args in [(4,2,0),(5,2,0),(5,3,0),(5,3,1)]:
        print(args,exhaustive(*args),flush=True)
