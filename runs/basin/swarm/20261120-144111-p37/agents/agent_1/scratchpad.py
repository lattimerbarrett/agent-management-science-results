from functools import lru_cache
from itertools import product, combinations
from math import comb
from fractions import Fraction
import gc, time

# Independent sets are antichains; adding disjointness edges requires intersection.
def count_antichains(n, intersecting=False):
    N = 1 << n
    adj = []
    for a in range(N):
        adj.append(sum(1 << b for b in range(N) if a != b and
                       ((a & b) == a or (a & b) == b or
                        (intersecting and (a & b) == 0))))
    @lru_cache(None)
    def independent(mask):
        if not mask:
            return 1
        # Factor over connected components.
        component, frontier = 0, mask & -mask
        while frontier:
            component |= frontier
            neighbors = 0
            while frontier:
                bit = frontier & -frontier
                frontier -= bit
                neighbors |= adj[bit.bit_length()-1]
            frontier = neighbors & mask & ~component
        if component != mask:
            return independent(component) * independent(mask ^ component)
        degree, vertex, todo = -1, -1, mask
        while todo:
            bit = todo & -todo
            todo -= bit
            j = bit.bit_length()-1
            deg = (adj[j] & mask).bit_count()
            if deg > degree:
                degree, vertex = deg, j
        if degree == 0:
            return 1 << mask.bit_count()
        rest = mask & ~(1 << vertex)
        return independent(rest) + independent(rest & ~adj[vertex])
    mask = (1 << N)-1
    if intersecting:
        mask &= ~1                 # The empty set cannot be a member.
    answer = independent(mask)
    independent.cache_clear()
    return answer

start = time.time()
lam7 = count_antichains(6, True)   # Bijection proved in the text.
lam8 = count_antichains(7, True)
D7 = count_antichains(7)
assert (lam7, lam8, D7) == (1422564, 229809982112, 2414682040998)
assert D7 * (D7 + 1) < 1 << 83
print('lambda(7), lambda(8), D(7):', lam7, lam8, D7, flush=True)
gc.collect()

# All partitions of [8] into three nonempty unlabeled classes.
partitions = []
for colors in product(range(3), repeat=8):
    if colors[0] != 0 or set(colors) != {0, 1, 2}:
        continue
    groups = tuple(sum(1 << j for j in range(8) if colors[j] == h)
                   for h in range(3))
    if groups[1] < groups[2]:
        partitions.append(groups)
assert len(partitions) == 966
rain = [sum(1 << j for j, groups in enumerate(partitions)
            if all(s & g for g in groups)) for s in range(256)]
good = [sum(1 << s for s in range(256) if all(s & g for g in groups))
        for groups in partitions]
up = [sum(1 << t for t in range(256) if (s & t) == s)
      for s in range(256)]
queries = sorted((s for s in range(256)
                  if s < (255 ^ s) and 3 <= s.bit_count() <= 5),
                 key=lambda s: (abs(4-s.bit_count()), s))
assert len(queries) == 91
all_colors = (1 << len(partitions))-1
reverse_byte = bytes(int(f'{x:08b}'[::-1], 2) for x in range(256))

def reflect(H):
    return int.from_bytes(H.to_bytes(32, 'little')
                          .translate(reverse_byte)[::-1], 'little')

def tree_leaves(cap, collect=False):
    # H is the upward closure of the selected branch sets.
    # cs records precisely the color partitions rainbow on those sets.
    stack = [(0, 0, all_colors, ())]
    number, nodes, samples = 0, 0, []
    while stack:
        k, H, cs, path = stack.pop()
        nodes += 1
        assert cs
        while k < len(queries):
            s = queries[k]
            sc = 255 ^ s
            k += 1
            if (H >> s) & 1 or (H >> sc) & 1:
                continue
            c1, c0 = cs & rain[s], cs & rain[sc]
            if not c1 or not c0:
                continue
            stack.append((k, H | up[s], c1,
                          path + (s,) if collect else ()))
            stack.append((k, H | up[sc], c0,
                          path + (sc,) if collect else ()))
            break
        else:
            j = (cs & -cs).bit_length()-1
            assert H & ~good[j] == 0     # Every set of H is rainbow.
            assert H & reflect(H) == 0   # H is intersecting.
            number += 1
            if collect:
                samples.append((path, partitions[j]))
            if number == cap:
                return number, nodes, samples
    return number, nodes, samples

leaves, nodes, _ = tree_leaves(lam7 + 1)
assert leaves == lam7 + 1
print('d=8 certificate: leaves =', leaves, 'visited nodes =', nodes, flush=True)

# d=9 construction: zero or one of 45 allowed 4-sets.
A, B, Cprime = 0b00000111, 0b00111000, 0b11000000
blocks9 = (A, B, Cprime | (1 << 8))
def bipanchromatic(s, blocks, full):
    return all(s & g and (full ^ s) & g for g in blocks)
var4 = [s for s in range(256) if s.bit_count() == 4
        and bipanchromatic(s, blocks9, 511)]
var5 = [s for s in range(256) if s.bit_count() == 5
        and bipanchromatic(s, blocks9, 511)]
assert len(var4) == 45 and len(var5) == 36
r = [sum((s & t) == s for t in var5) for s in var4]
assert r.count(4) == 9 and r.count(3) == 36
N9 = (1 << 36) + sum(1 << (36-v) for v in r)
assert N9 == 97 * (1 << 32) and N9 > lam8
print('d=9 construction size:', N9, flush=True)

# Exponents in the even/odd middle-layer constructions.
def exponent(d):
    sizes = sorted([d//3 + (j < d % 3) for j in range(3)])
    m = d//2
    total = 0
    for a in range(1, sizes[0]):
        for b in range(1, sizes[1]):
            c = m-a-b
            if 1 <= c < sizes[2]:
                first = comb(sizes[0]-1, a-1) if d % 2 else comb(sizes[0], a)
                total += first * comb(sizes[1], b) * comb(sizes[2], c)
    if d % 2:
        return total
    assert total % 2 == 0
    return total//2

upper = {7: D7}
for n in range(8, 12):
    upper[n] = upper[n-1] * (upper[n-1]+1)//2
assert [exponent(d) for d in range(10, 14)] == [90, 164, 396, 690]
for d in range(10, 14):
    assert (1 << exponent(d)) > upper[d-2]
for d in (14, 15, 16, 17, 19):
    assert 5 * exponent(d) >= 8 * comb(d-2, (d-2)//2)
# Uniform rational estimates handle all remaining dimensions.
assert Fraction(17, 9) * Fraction(29, 32) > Fraction(8, 5)
assert Fraction(20, 11) * (1-Fraction(1, 32)-2*Fraction(11, 20)**7) > Fraction(8, 5)
assert 2**8 > 3**5
print('All finite and uniform numerical inequalities verified.', flush=True)

# Exhaustive check of the tree-to-permutations and grid-embedding lemmas.
_, _, samples = tree_leaves(8, collect=True)
pos = []
for c in range(8):
    order = sorted(range(8), key=lambda i: tuple((s >> c) & 1 for s in samples[i][0]))
    pos.append({i: j for j, i in enumerate(order)})
kappa = [[next(h for h, g in enumerate(groups) if (g >> c) & 1)
          for c in range(8)] for path, groups in samples]
for i in range(8):
    for j in range(8):
        if j == i:
            continue
        wins = {c for c in range(8) if pos[c][i] > pos[c][j]}
        assert {kappa[i][c] for c in wins} == {0, 1, 2}
        for k in range(8):
            if k not in (i, j):
                assert any(pos[c][i] > max(pos[c][j], pos[c][k]) for c in range(8))
Q = [(i,) for i in range(8)] + list(combinations(range(8), 2))
elements = [(p, q) for p in product(range(2), repeat=3) for q in Q]
images = [tuple(max(2*pos[c][i] + p[kappa[i][c]] for i in q)
                for c in range(8)) for p, q in elements]
for (p, q), v in zip(elements, images):
    for (pp, qq), vv in zip(elements, images):
        actual = all(x <= y for x, y in zip(p, pp)) and set(q) <= set(qq)
        assert actual == all(x <= y for x, y in zip(v, vv))
print('Exhaustively checked', len(elements)**2, 'ordered pairs of a grid embedding.')
print('Elapsed seconds:', round(time.time()-start, 2))
