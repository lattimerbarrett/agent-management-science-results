from functools import lru_cache
from itertools import product
from math import comb, prod
from fractions import Fraction
import numpy as np

# D(n): order ideals of the Boolean lattice B_n.
def ideals(n):
    if n == 0:
        return [0, 1]
    old = ideals(n-1)
    h = 1 << (n-1)
    return [a | (b << h) for a in old for b in old if (a & b) == b]

# Count D(7) as monotone maps B_3 -> J(B_4).
def dedekind7():
    m = np.array(ideals(4), dtype=np.int64)
    assert len(m) == 168
    n = len(m)
    index = np.zeros(1 << 16, dtype=np.int64)
    index[m] = np.arange(n)
    le = (m[:, None] & m[None, :]) == m[:, None]
    lower = le.sum(axis=0)
    join = index[m[:, None] | m[None, :]]
    ans = 0
    for top in range(n):
        J = np.flatnonzero(le[:, top])
        M = m[J]
        interval = le[:, J].sum(axis=1)
        B = interval[join[np.ix_(J, J)]]
        for i in J:
            A = interval[join[i, J]]
            bottom = lower[index[m[i] & M[:, None] & M[None, :]]]
            ans += int((B * A[:, None] * A[None, :] * bottom).sum())
    return ans

# lambda(7) = intersecting upsets of B_6.
def lambda7():
    I = np.array(ideals(5), dtype=np.uint32)
    def reverse32(x):
        x = ((x >> 1) & 0x55555555) | ((x & 0x55555555) << 1)
        x = ((x >> 2) & 0x33333333) | ((x & 0x33333333) << 2)
        x = ((x >> 4) & 0x0f0f0f0f) | ((x & 0x0f0f0f0f) << 4)
        x = ((x >> 8) & 0x00ff00ff) | ((x & 0x00ff00ff) << 8)
        return (x >> 16) | (x << 16)
    R = reverse32(I)
    ans = D6 = 0
    for a in I:
        comparable = (I & a) == I
        D6 += int(comparable.sum())
        ans += int((comparable & ((a | R) == 0xffffffff)).sum())
    assert D6 == 7828354
    return ans

# Ideals of B_3 with its minimum and maximum deleted.
def proper3_ideals():
    E = list(range(1, 7))
    return [m for m in range(64)
            if all(not (m >> i & 1) or
                   all((a & b) != b or (m >> j & 1)
                       for j, b in enumerate(E))
                   for i, a in enumerate(E))]

def base8():
    I = proper3_ideals()
    assert len(I) == 18
    C = [[sum(((a | b) & z) == (a | b) for z in I)
          for b in I] for a in I]
    return sum(C[i][j] * C[i][k] * C[j][k]
               for i in range(18) for j in range(18) for k in range(18))

# Independent sets in an explicitly specified 63-vertex graph.
def base9():
    V = [x for x in product(range(1, 7), repeat=3)
         if sum(a.bit_count() for a in x) == 4 and (x[0] & 3)]
    assert len(V) == 63
    adj = [sum(1 << j for j, y in enumerate(V)
               if all((a & b) == 0 for a, b in zip(x, y))) for x in V]
    @lru_cache(None)
    def count(mask):
        if mask == 0:
            return 1
        seen = front = mask & -mask
        while front:
            b = front & -front
            front -= b
            new = adj[b.bit_length()-1] & mask & ~seen
            seen |= new
            front |= new
        if seen != mask:
            return count(seen) * count(mask ^ seen)
        remaining = mask
        vertex, degree = -1, -1
        while remaining:
            b = remaining & -remaining
            remaining -= b
            v = b.bit_length()-1
            d = (adj[v] & mask).bit_count()
            if d > degree:
                vertex, degree = v, d
        b = 1 << vertex
        return count(mask ^ b) + count(mask & ~(b | adj[vertex]))
    return count((1 << len(V))-1)

def exponent(d):
    sizes = [d//3 + (j < d % 3) for j in range(3)]
    r = d//2
    if d % 2 == 0:
        N = sum(prod(comb(a, b) for a, b in zip(sizes, x))
                for x in product(*(range(1, a) for a in sizes)) if sum(x) == r)
        assert N % 2 == 0
        return N//2
    return max(sum(prod(comb(a-(i == j), b-(i == j))
                        for i, (a, b) in enumerate(zip(sizes, x)))
                   for x in product(*(range(1, a) for a in sizes)) if sum(x) == r)
               for j in range(3))

# Verify the ordered symmetric-chain construction used in the proof.
def chains(n):
    if n == 0:
        return [[0]]
    out = []
    bit = 1 << (n-1)
    for C in chains(n-1):
        out.append(C + [C[-1] | bit])
        if len(C) > 1:
            out.append([x | bit for x in C[:-1]])
    return sorted(out, key=len)  # stable: parent order breaks ties

def check_chains(n):
    C = chains(n)
    assert len(C) == comb(n, n//2)
    owner = {}
    for i, chain in enumerate(C):
        assert chain[0].bit_count() + chain[-1].bit_count() == n
        for x in chain:
            assert x not in owner
            owner[x] = i
        for a, b in zip(chain, chain[1:]):
            assert a & b == a and (a ^ b).bit_count() == 1
    assert len(owner) == 1 << n
    for i, chain in enumerate(C):
        for a, b, c in zip(chain, chain[1:], chain[2:]):
            other = a | (c ^ b)
            assert other != b and owner[other] < i

if __name__ == '__main__':
    D7, lam7, N8, N9 = dedekind7(), lambda7(), base8(), base9()
    assert D7 == 2414682040998
    assert lam7 == 1422564
    assert N8 == 783558
    assert N9 == 5556381987840
    assert 2*N8 >= lam7+1
    assert N9 >= D7+1
    assert (D7*D7+D7)//2 < 2**82
    for d in range(10, 14):
        assert exponent(d) >= 82 * 2**(d-10)
    for d in range(14, 21):
        assert 5*exponent(d) > 8*comb(d-2, (d-2)//2)
    assert Fraction(493, 288) > Fraction(8, 5)
    odd_lower = Fraction(20, 11)*(1-Fraction(1,32)-2*Fraction(11,20)**7)
    assert odd_lower > Fraction(8, 5)
    assert 3**5 < 2**8
    for n in range(11):
        check_chains(n)
    # Check the two-block concatenation used for d=8.
    groups = [{0,1}, {2,3,4}, {5,6,7}]
    A = {0,1,2,5}
    permutation = dict(zip([0,1,2,5,3,4,6,7], [3,4,6,7,0,1,2,5]))
    other_groups = [{permutation[x] for x in g} for g in groups]
    Ac = set(range(8))-A
    assert all(A & g for g in groups) and any(g <= A for g in groups)
    assert all(Ac & g for g in other_groups) and any(g <= Ac for g in other_groups)
    print('D(7) =', D7)
    print('lambda(7) =', lam7)
    print('d=8, one block =', N8, '; two blocks =', 2*N8)
    print('d=9, independent-set lower construction =', N9)
    print('exponents d=10,...,20:', [exponent(d) for d in range(10,21)])
    print('All checks passed.')
