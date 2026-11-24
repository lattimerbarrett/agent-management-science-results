"""Independent finite checks of the lower-bound obstruction.
The dimension-independent proof only uses the assertions checked here:
complete graph, <=2 triangles on each four-set, and collapse to a tree.
The occupancy check tests the first-forbidden-facet invariant for d=3..12.
"""
from itertools import combinations, product
TRIANGLES = [[0, 1, 4], [0, 1, 6], [0, 1, 8], [0, 2, 3], [0, 2, 6], [0, 2, 9], [0, 3, 8], [0, 5, 6], [0, 5, 8], [0, 7, 9], [1, 2, 3], [1, 2, 5], [1, 2, 9], [1, 3, 6], [1, 3, 7], [1, 4, 7], [1, 4, 9], [1, 5, 7], [1, 6, 9], [2, 3, 4], [2, 4, 7], [2, 5, 8], [2, 6, 7], [2, 6, 8], [2, 8, 9], [3, 4, 6], [3, 4, 9], [3, 5, 6], [3, 7, 8], [3, 7, 9], [4, 5, 8], [4, 5, 9], [4, 6, 8], [5, 6, 7], [5, 7, 8], [5, 7, 9]]
T=set(map(frozenset,TRIANGLES))
V=set(range(10))

def seed_check():
    E={frozenset(e) for e in combinations(V,2)}
    assert {frozenset(e) for t in T for e in combinations(t,2)}==E
    assert all(sum(frozenset(t) in T for t in combinations(Q,3))<=2
               for Q in combinations(V,4))
    remaining=set(T); steps=[]
    while remaining:
        options=[(frozenset(e),t) for t in sorted(remaining,key=lambda t:sorted(t))
                 for e in combinations(sorted(t),2)
                 if sum(set(e)<=s for s in remaining)==1]
        assert options, 'collapse stuck'
        e,t=options[0]
        assert e in E
        remaining.remove(t);E.remove(e);steps.append((e,t))
    reached={0}
    while True:
        new=reached|set().union(*(e for e in E if e&reached))
        if new==reached:break
        reached=new
    assert reached==V and len(E)==len(V)-1
    return steps,E

def is_D_face(S):
    return len(S)<=2 or frozenset(S) in T

def occupancy_check(d):
    # A facet has d+1 vertices; r<=d-3 guarantees at least four OLD vertices.
    # Only support sizes3,4 need enumeration; support>=5 leaves >=4 blocks
    # after any single deletion and can supply no old ridge whatsoever.
    count=0
    for p in (3,4):
        for support in combinations(V,p):
            if is_D_face(support):continue
            for mult in product(range(1,d+1),repeat=p):
                old=sum(mult)
                if not 4<=old<=d+1:continue
                R=[support[i] for i,m in enumerate(mult)
                   if m==1 and is_D_face(set(support)-{support[i]})]
                assert len(R)<=2
                assert is_D_face(R)
                # With singleton multiplicities, R corresponds to <=2 old
                # vertices, so it is an original face in every clone expansion.
                count+=1
    return count

if __name__=='__main__':
    steps,E=seed_check()
    print('Seed checked:',len(T),'triangles;',len(steps),'free-edge collapses;',len(E),'tree edges')
    for d in range(3,13):
        print('d=',d,'forbidden old-support occupancy patterns checked:',occupancy_check(d))
