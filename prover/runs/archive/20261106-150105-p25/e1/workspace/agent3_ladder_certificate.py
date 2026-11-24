"""Finite certificate used in the uniform ladder independence proof."""
from itertools import combinations
# roles a,p,q,r,b (0..4)
within={tuple(sorted(e)) for e in [(0,1),(1,2),(2,3),(3,4),(0,3),(1,4),(0,4)]}
cross={(0,1),(0,2),(0,4),(1,0),(1,3),(2,4),(3,4),(4,0),(4,3)}
def independent(S):return all(tuple(sorted(e)) not in within for e in combinations(S,2))
subsets=[set(S) for r in range(6) for S in combinations(range(5),r) if independent(S)]
assert max(map(len,subsets))==2
doubles=[S for S in subsets if len(S)==2]
assert doubles==[{0,2},{1,3},{2,4}]
# Any two double blocks conflict, regardless of their locations.
assert all(any((a,b) in cross for a in S for b in T) for S in doubles for T in doubles)
# If left endpoint selected, only a,r remain; they conflict.
assert not independent({0,3})
# If right endpoint selected, only p,b remain; they conflict.
assert not independent({1,4})
print('All finite independence-certificate assertions passed.')

def validate_walks(m):
    E=set()
    def add(u,v):E.add(tuple(sorted((u,v))))
    for i in range(m):
        for a in range(4):add((i,a),(i,a+1))
        for j in range(i+1,m):add((i,0),(j,4))
    def valid(w):
        assert len(w) in (2,4)
        assert all(tuple(sorted((u,v))) in E for u,v in zip(w,w[1:]))
    for i in range(1,m-1):
        valid([(i,0),(m-1,4),(0,0),(i,4)])
        for j in range(i+1,m-1):
            walks={(0,1):[(i,0),(m-1,4),(j,0),(j,1)],
                   (0,2):[(i,0),(j,4),(j,3),(j,2)],
                   (0,4):[(i,0),(j,4)],
                   (1,0):[(i,1),(i,0),(m-1,4),(j,0)],
                   (1,3):[(i,1),(i,0),(j,4),(j,3)],
                   (2,4):[(i,2),(i,1),(i,0),(j,4)],
                   (3,4):[(i,3),(i,4),(0,0),(j,4)],
                   (4,0):[(i,4),(0,0),(m-1,4),(j,0)],
                   (4,3):[(i,4),(0,0),(j,4),(j,3)]}
            assert set(walks)==cross
            for w in walks.values():valid(w)
for m in range(3,30):validate_walks(m)
print('Every symbolic cross-edge walk validated for 3<=m<30.')
