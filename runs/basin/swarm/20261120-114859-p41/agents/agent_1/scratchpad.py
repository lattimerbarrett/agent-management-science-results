from itertools import combinations
from functools import lru_cache

# Exact checks for pure 2-dimensional complexes on five labelled vertices.
n, q = 5, 3
facets = tuple(frozenset(c) for c in combinations(range(n), q))
N = len(facets)

def attachment_ok(mask, j):
    F = facets[j]
    intersections = [F & facets[i] for i in range(N) if mask >> i & 1]
    maximal = [G for G in set(intersections)
               if not any(G < H for H in intersections)]
    return bool(maximal) and all(len(G) == q-1 for G in maximal)

@lru_cache(None)
def shellable(mask):
    if mask.bit_count() == 1:
        return True
    if mask == 0:
        return False
    return any(shellable(mask ^ (1 << j)) and attachment_ok(mask ^ (1 << j), j)
               for j in range(N) if mask >> j & 1)

# General definition of k-decomposability, implemented on maximal faces.
def canonical(fs):
    fs = set(fs)
    return tuple(sorted((tuple(sorted(F)) for F in fs
                        if not any(F < G for G in fs))))

@lru_cache(None)
def kd(fs, k):
    Fs = [frozenset(F) for F in fs]
    if len(Fs) == 1:
        return True
    if not Fs or len(set(map(len, Fs))) != 1:
        return False
    size = len(Fs[0])
    faces = set()
    for F in Fs:
        for s in range(1, min(k+1, size)+1):
            faces.update(frozenset(S) for S in combinations(sorted(F), s))
    for S in faces:
        # The deletion consists of unchanged facets and the faces obtained
        # from facets containing S by dropping one element of S.
        deletion = []
        link = []
        for F in Fs:
            if S <= F:
                deletion.extend(F - {x} for x in S)
                link.append(F - S)
            else:
                deletion.append(F)
        D, L = canonical(deletion), canonical(link)
        if all(len(F) == size for F in D) and kd(D, k) and kd(L, k):
            return True
    return False

pairs = 0
shellable_count = 0
for mask in range(1, 1 << N):
    fs = tuple(tuple(sorted(facets[i])) for i in range(N) if mask >> i & 1)
    assert kd(tuple(sorted(fs)), q-1) == shellable(mask)
    if shellable(mask):
        shellable_count += 1
        for j in range(N):
            if not (mask >> j & 1):
                assert shellable(mask | (1 << j)) == attachment_ok(mask, j)
                pairs += 1
print(f'Checked {2**N-1} nonempty pure complexes.')
print(f'Checked shellable iff dimension-decomposable for all of them.')
print(f'{shellable_count} shellable complexes; {pairs} one-facet extensions checked.')
