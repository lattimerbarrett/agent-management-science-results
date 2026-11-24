import itertools as it, math,json
from sage.all import matrix,ZZ

def verify(n):
    Ts=list(it.combinations(range(1,n+1),4))
    B=[A for j in range(min(4,n-4)+1) for A in it.combinations(range(1,n+1),j) if all(a>=2*(i+1) for i,a in enumerate(A))]
    BM=matrix(ZZ,[[int(set(A)<=set(T)) for A in B] for T in Ts])
    assert abs(BM.det())==1
    As=[A for j in (1,2) for A in it.combinations(range(1,n+1),j)]
    I=matrix(ZZ,[[int(set(A)<=set(T)) for A in As] for T in Ts])
    S=I.smith_form(transformation=False)
    ds=[int(S[i,i]) for i in range(min(S.dimensions())) if S[i,i]]
    assert ds.count(2)==1 and ds.count(1)==math.comb(n,2)-1
    assert len(ds)==math.comb(n,2)
    return dict(n=n,generators=len(Ts),relations=len(As),free=len(Ts)-len(ds),torsion=[x for x in ds if x!=1],basis_determinant=int(BM.det()))
if __name__=='__main__':
    out=[verify(n) for n in range(6,11)]
    print(json.dumps(out,indent=2))
    from pathlib import Path
    Path('workspace/agent4_incidence_checks.json').write_text(json.dumps(out,indent=2))
