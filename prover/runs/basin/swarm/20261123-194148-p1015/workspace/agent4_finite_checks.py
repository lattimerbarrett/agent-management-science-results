import itertools, json, os

def subset(a,b): return a & ~b == 0

def monotone_maps(n):
    size=1<<n
    comparable=[(a,b) for a in range(size) for b in range(size) if subset(a,b)]
    return [f for f in itertools.product(range(size),repeat=size) if all(subset(f[a],f[b]) for a,b in comparable)]

def checks():
    n=2; full=(1<<n)-1
    maps=monotone_maps(n)
    assert len(maps)==36
    tested_pairs=0
    fixed_sets=0
    for theta in maps:
        for psi in maps:
            f=[psi[full^theta[x]] for x in range(1<<n)]
            assert all(subset(f[y],f[x]) for x in range(1<<n) for y in range(1<<n) if subset(x,y))
            fixed=[x for x in range(1<<n) if f[x]==x]
            assert all(not subset(x,y) for x in fixed for y in fixed if x!=y)
            tested_pairs+=1; fixed_sets+=len(fixed)
    # Every monotone Boolean map has exactly its canonical finite-positive rule representation.
    canonical_checks=0
    for f in maps:
        rules=[(out,inp) for out in range(n) for inp in range(1<<n) if (f[inp]>>out)&1]
        for oracle in range(1<<n):
            got=0
            for out,inp in rules:
                if subset(inp,oracle): got |= 1<<out
            assert got==f[oracle]
            canonical_checks+=1
    return {'universe_size':n,'monotone_operators':len(maps),'operator_pairs_checked':tested_pairs,'fixed_points_checked':fixed_sets,'finite_positive_rule_checks':canonical_checks}

def large_checks():
    import numpy as np
    n=3; size=1<<n; full=size-1
    scalar=[]
    comparable=[(a,b) for a in range(size) for b in range(size) if subset(a,b)]
    for f in itertools.product(range(2),repeat=size):
        if all(f[a]<=f[b] for a,b in comparable): scalar.append(f)
    assert len(scalar)==20
    maps=np.array([[sum(scalar[c][x]<<bit for bit,c in enumerate(parts)) for x in range(size)] for parts in itertools.product(range(20),repeat=3)],dtype=np.uint8)
    assert maps.shape==(8000,8)
    strict=[(a,b) for a,b in comparable if a!=b]
    pair_count=0; fixed_count=0
    for theta in maps:
        # Row r contains Psi_r(complement Theta(x)), all eight x.
        outputs=maps[:,full^theta]
        fixed=outputs==np.arange(size,dtype=np.uint8)[None,:]
        for a,b in strict:
            assert not np.any(fixed[:,a]&fixed[:,b])
        fixed_count+=int(fixed.sum()); pair_count+=len(maps)
    assert pair_count==64000000
    return {'universe_size':3,'scalar_monotone_predicates':20,'monotone_operators':8000,'operator_pairs_checked':pair_count,'fixed_points_checked':fixed_count}

if __name__=='__main__':
    result={'small':checks(),'large':large_checks()}
    os.makedirs('workspace',exist_ok=True)
    with open('workspace/agent4_finite_checks.json','w') as f: json.dump(result,f,indent=2)
    with open('workspace/agent4_finite_checks.py','w') as f: f.write(open(__file__).read())
    print(json.dumps(result,indent=2))
    proof=r'''Additional checked structural lemma: weakly cototal degrees are closed under skip.

Let B represent the weakly cototal degree and let D=complement(B) have total
enumeration degree. Choose a literal self-total set T with D equivalent_e T.
Then D is c.e. in T, so B is Pi_1^T. Thus S=skip(B) is Pi_2^T.
Moreover T <=_e D <=_e S, since complements of all enumeration images of B
many-one reduce to skip(B).

Let H_T be the ordinary Turing halting set relative to the oracle T. Since T
is self-total, H_T <=_e T <=_e S. Put C=S join H_T; then C equivalent_e S.
Its complement is complement(S) join complement(H_T). Because S is Pi_2^T,
complement(S) is Sigma_2^T and hence enumerable in the total Turing jump T'.
The set complement(H_T) has total enumeration degree T': it computes T by
its usual negative-halting coding and enumerates H_T using T. Consequently
complement(C) has total degree T'. This witnesses weak cototality of S.

This closure lemma does not imply cototality of S, and does not resolve the
central existence problem. Separately checked finite operator algebra is
in agent4_finite_checks.py and its JSON output; 64,000,000 three-coordinate
operator pairs were tested exhaustively.
'''
    with open('workspace/agent4_skip_closure.txt','w') as f: f.write(proof)
