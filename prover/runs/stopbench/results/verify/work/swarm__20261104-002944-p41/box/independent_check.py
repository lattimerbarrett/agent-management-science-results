import sys, time
from itertools import combinations
sys.path.insert(0,'workspace')
import agent2_independent_lower as team
import agent2_checker as original
from agent2_fast_verify import verify_uniform
# Recheck all seed face intervals (not merely edge counts).
old={frozenset()}; restrictions=[]
for i, tri in enumerate(team.T0):
    faces={frozenset(c) for j in range(4) for c in combinations(tri,j)}
    new=faces-old
    if i:
        minima=[x for x in new if not any(y<x for y in new)]
        assert len(minima)==1 and 1<=len(minima[0])<=2
        R=minima[0]
        assert new=={x for x in faces if R<=x}
        restrictions.append(tuple(sorted(R)))
    old |= faces
print('Exact seed restriction intervals:',restrictions)
assert sum(len(x)==2 for x in old)==28
# Use full face sets for a verifier, independent of both ridge hash verifiers.
def to_sets(fs):
    return [frozenset(i for i in range(f.bit_length()) if f>>i&1) for f in fs]
def face_family(fs):
    return {frozenset(g) for f in fs for r in range(len(f)+1) for g in combinations(f,r)}
def full_verify(C,cert,k=1):
    stack=[(C,cert)];nodes=0
    while stack:
        C,c=stack.pop();nodes+=1
        maxs=[f for f in C if not any(f<g for g in C)]
        assert len({len(f) for f in maxs})==1
        if c[0]=='simplex':
            expected=frozenset(i for i in range(c[1].bit_length()) if c[1]>>i&1)
            assert maxs==[expected]
            continue
        assert c[0]=='shed'
        s=frozenset(i for i in range(c[1].bit_length()) if c[1]>>i&1)
        assert s in C and 1<=len(s)<=k+1
        D={f for f in C if not s<=f}
        L={f-s for f in C if s<=f}
        de_maxs=[f for f in D if not any(f<g for g in D)]
        assert {len(f) for f in de_maxs}=={len(maxs[0])}
        stack.append((D,c[2]));stack.append((L,c[3]))
    return nodes
fs,c,phases=team.construct(4,2)
t=time.time()
assert original.verify(fs,1,c)
print('Original verifier: PASS 16-vertex,',len(fs),'facets,',phases,'phases')
print('Own full-face verifier:',full_verify(face_family(to_sets(fs)),c),'nodes; elapsed',time.time()-t)
# Verify full expanded obstruction by enumerating all 4-sets and actual old face intersections.
C=face_family(to_sets(fs));S=set(team.S)
def allow(f):
    p=tuple(sorted(set(v//2 for v in f)))
    return len(p)<=2 or p in S
barrier={frozenset(t) for t in combinations(range(16),3) if allow(t)}
assert {t for t in C if len(t)==3}<=barrier
assert len(barrier)==288 and len([t for t in C if len(t)==2])==120
assert all(sum(frozenset(t) in barrier for t in combinations(Q,3))!=3 for Q in combinations(range(16),4))
# Each allowable ridge attachment preserves triangle barrier, including non-clique missing tetrahedra.
admissible=0
for Q in map(frozenset,combinations(range(16),4)):
    if Q in C:continue
    I={g for g in C if g<=Q}
    mx=[g for g in I if not any(g<h for h in I)]
    if all(len(g)==3 for g in mx):
        admissible+=1
        assert all(t in barrier for t in map(frozenset,combinations(Q,3)))
print('All 1540 missing tetrahedra checked; ridge-attachment candidates',admissible,'cannot escape barrier')
# Additional general family case.
t=time.time();fs,c,phases=team.construct(6)
print('q=6:',len(fs),'facets;',verify_uniform(fs,1,c),'; barrier',team.verify_barrier(fs,6,6),'; elapsed',time.time()-t)
