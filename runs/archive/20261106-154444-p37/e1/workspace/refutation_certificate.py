from functools import lru_cache
from itertools import combinations

def maximal_intersecting_count(k):
    # Maximal intersecting families on k points correspond bijectively
    # to intersecting upsets on k-1 points, hence intersecting antichains.
    sets = list(range(1, 1 << (k - 1)))
    adj = []
    for a in sets:
        adj.append(sum(1 << j for j, b in enumerate(sets)
                       if a & b and a & b != a and a & b != b))
    @lru_cache(None)
    def cliques(candidates):
        ans = 1  # empty clique
        while candidates:
            bit = candidates & -candidates
            candidates ^= bit
            ans += cliques(candidates & adj[bit.bit_length() - 1])
        return ans
    return cliques((1 << len(sets)) - 1)

def certificate(sizes):
    r = sum(sizes)
    blocks = []
    start = 0
    for size in sizes:
        blocks.append(sum(1 << j for j in range(start, start + size)))
        start += size
    full = (1 << r) - 1
    rows = []
    for subset in combinations(range(r), r // 2):
        a = sum(1 << j for j in subset)
        if a & 1 and all(a & b and (full ^ a) & b for b in blocks):
            rows.append(a)
    total = len(rows)
    assert total >= 21
    rows = rows[:21]
    for a, b in combinations(rows, 2):
        assert all(x & y for x in (a, full ^ a)
                         for y in (b, full ^ b))
    for a in rows:
        assert all(x & block for x in (a, full ^ a) for block in blocks)
    return r, total

if __name__ == '__main__':
    lam7 = maximal_intersecting_count(7)
    assert lam7 == 1422564
    assert lam7 + 1 < 2 ** 21
    print('lambda(7) =', lam7)
    for sizes in [(3,3,3), (3,3,2,2), (2,2,2,2,3), (2,2,2,2,2,2)]:
        r, total = certificate(sizes)
        print('groups:', sizes, 'orders:', r, 'available rows:', total,
              '21-row certificate verified')
