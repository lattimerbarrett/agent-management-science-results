from sage.all import ZZ, matrix, vector, ChainComplex, gcd
from itertools import combinations, product

def core(q,b):
    faces=[]
    for k in range(q+1):
        faces.append([tuple(zip(S,R)) for S in combinations(range(q),k)
                      for R in product(range(3),repeat=k)
                      if all(R.count(i)<=b[i] for i in range(3))])
    ids=[{f:i for i,f in enumerate(F)} for F in faces]
    D={}
    for k in range(1,q+1):
        D[k]=matrix(ZZ,len(faces[k-1]),len(faces[k]),
                    {(ids[k-1][f[:p]+f[p+1:]],j):(-1)**p
                     for j,f in enumerate(faces[k]) for p in range(k)})
    for k in range(2,q+1): assert D[k-1]*D[k]==0
    return faces,D

cases=[(4,(2,2,2),{3:1,4:2}),(3,(1,2,2),{3:2}),
       (2,(0,2,2),{2:1}),(2,(1,1,2),{2:2}),
       (1,(0,1,2),{1:1}),(1,(1,1,1),{1:2})]
for q,b,expected in cases:
    faces,D=core(q,b)
    H=ChainComplex(dict(D),degree=-1).homology()
    assert {k:tuple(G.invariants()) for k,G in H.items() if G.invariants()}=={
        k:(0,)*r for k,r in expected.items()}
    print(q,b,'boundary ranks',[D[k].rank() for k in D],
          'homology',{k:G for k,G in H.items() if G.invariants()})

faces,D=core(4,(2,2,2));values=[]
for f in faces[3]:
    missing=next(j for j in range(4) if j not in {c for c,r in f})
    counts=[sum(r==i for c,r in f) for i in range(3)]
    v=0
    if 2 in counts:
        r,s=counts.index(2),counts.index(1)
        v=1 if (r,s) in ((0,1),(1,2),(2,0)) else -1
    values.append((-1)**missing*v)
phi=vector(ZZ,values)
assert phi*D[4]==0
assert gcd(D[3].right_kernel_matrix()*phi)==6
print('Primitive local coordinate phi/6 verified over the full integer cycle lattice.')
with open('workspace/agent2_compact_core_certificate.py','w') as f:f.write(open(__file__).read())
