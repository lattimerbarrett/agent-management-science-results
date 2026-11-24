"""Construct and exactly verify one-new-vertex completions in dimension three.
Requires agent3_check.py, agent1_filling.py in same directory.
"""
from itertools import combinations
from agent3_check import all_faces, submasks, k_certificate, maximal
from agent1_filling import check_certificate

def ridge_completion(facets,k):
    assert all(f.bit_count()==4 for f in facets)
    assert k>=1 and k_certificate(tuple(sorted(facets)),k) is not None
    vset=0
    for f in facets: vset|=f
    gamma=set(s for f in facets for s in submasks(f) if s.bit_count()==3)
    C=facets[0]
    out=[]
    while C!=vset:
        F=next(f for f in facets if (f&~C).bit_count()==1)
        v=F&~C; S=F&C; w=S&-S
        for u in (1<<i for i in range(vset.bit_length()) if C>>i&1):
            edge=v|u
            if edge not in all_faces(tuple(gamma)):
                triangle=edge|w
                assert triangle.bit_count()==3
                gamma.add(triangle);out.append(triangle)
                assert k_certificate(tuple(sorted(gamma)),k) is not None
        C|=v
        for xyz in combinations([i for i in range(C.bit_length()) if C>>i&1],3):
            triangle=sum(1<<i for i in xyz)
            if triangle not in gamma:
                assert all((triangle^b) in all_faces(tuple(gamma)) for b in submasks(triangle) if b.bit_count()==1)
                gamma.add(triangle);out.append(triangle)
                assert k_certificate(tuple(sorted(gamma)),k) is not None
    return out

def prefix_order(cert,include=0):
    if cert[0]=='simplex':return [include|cert[1]]
    _,s,dc,lc=cert
    return prefix_order(dc,include)+prefix_order(lc,include|s)

def completion(facets,k):
    facets=tuple(sorted(facets));vset=0
    for f in facets:vset|=f
    a=1<<vset.bit_length()
    gamma=tuple(sorted(set(s for f in facets for s in submasks(f) if s.bit_count()==3)))
    cert=k_certificate(gamma,k)
    assert cert is not None
    additions=[a|g for g in prefix_order(cert)]
    additions += [a|g for g in ridge_completion(facets,k)]
    vlist=[1<<i for i in range(vset.bit_length()) if vset>>i&1]
    additions += [sum(c) for c in combinations(vlist,4) if sum(c) not in facets]
    current=set(facets)
    for f in additions:
        assert f not in current
        current.add(f)
        cert=k_certificate(tuple(sorted(current)),k)
        assert cert is not None,(facets,k,f)
        assert check_certificate(tuple(sorted(current)),k,cert)
    expected={sum(c) for c in combinations(vlist+[a],4)}
    assert current==expected
    return additions

if __name__=='__main__':
    import random
    count=0
    for n in [4,5]:
        universe=[sum(1<<i for i in c) for c in combinations(range(n),4)]
        for mask in range(1,1<<len(universe)):
            facets=tuple(f for i,f in enumerate(universe) if mask>>i&1)
            for k in [1,2,3]:
                if k_certificate(facets,k) is not None:
                    completion(facets,k);count+=1
    print('all n<=5 exact certificates:',count,flush=True)
    n=6;universe=[sum(1<<i for i in c) for c in combinations(range(n),4)]
    from agent3_check import appendable
    for trial in range(30):
        current=(random.choice(universe),)
        for step in range(random.randint(1,14)):
            eligible=[f for f in universe if f not in current and appendable(current,f)]
            if not eligible:break
            current=tuple(sorted(current+(random.choice(eligible),)))
        completion(current,3);count+=1
    print('total verified completions:',count)
