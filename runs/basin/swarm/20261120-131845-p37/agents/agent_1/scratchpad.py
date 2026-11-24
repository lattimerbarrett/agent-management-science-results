from itertools import combinations
from math import comb
from fractions import Fraction
from time import perf_counter
import numpy as np


def lambda_exact(k):
    full = (1 << k) - 1
    pairs = [(a, full ^ a) for a in range(1, full)
             if a < (full ^ a)]
    pairs.sort(key=lambda ab: min(ab[0].bit_count(), ab[1].bit_count()))
    bad = {a: sum(1 << b for b in range(1, full) if not (a & b))
           for a in range(1, full)}

    def rec(j, chosen):
        if j == len(pairs):
            return 1
        a, b = pairs[j]
        ans = 0
        if not (chosen & bad[a]):
            ans += rec(j + 1, chosen | (1 << a))
        if not (chosen & bad[b]):
            ans += rec(j + 1, chosen | (1 << b))
        return ans

    return rec(0, 0)


def partitions_three(d):
    out = []
    def rec(p, largest):
        if len(p) == d:
            if largest == 2:
                out.append(tuple(p))
            return
        for c in range(min(largest + 1, 2) + 1):
            rec(p + [c], max(largest, c))
    rec([0], 0)
    return out


def certify_d8(target):
    d = 8
    full = (1 << d) - 1
    ps = partitions_three(d)
    assert len(ps) == 966
    ss = [a for a in range(1, full) if 3 <= a.bit_count() <= 5]
    pairs = [(a, full ^ a) for a in ss if a < (full ^ a)]
    pairs.sort(key=lambda ab: (-min(ab[0].bit_count(),
                                    ab[1].bit_count()), ab))
    bad = {a: sum(1 << b for b in ss if not (a & b)) for a in ss}
    rainbow = {
        a: sum(1 << j for j, p in enumerate(ps)
               if len({p[i] for i in range(d) if (a >> i) & 1}) == 3)
        for a in ss
    }
    leaves = 0
    nodes = 0

    def rec(j, chosen, viable):
        nonlocal leaves, nodes
        nodes += 1
        assert viable
        if leaves >= target:
            return
        if j == len(pairs):
            leaves += 1
            return
        a, b = pairs[j]
        va = (viable & rainbow[a]) if not (chosen & bad[a]) else 0
        vb = (viable & rainbow[b]) if not (chosen & bad[b]) else 0
        if va and vb:
            rec(j + 1, chosen | (1 << a), va)
            rec(j + 1, chosen | (1 << b), vb)
        else:
            # A skipped cut adds no constraint to the path.
            rec(j + 1, chosen, viable)

    rec(0, 0, (1 << len(ps)) - 1)
    assert leaves == target
    return leaves, nodes


def ideals_boolean(r):
    n = 1 << r
    lower = [sum(1 << b for b in range(n) if b != a and (a & b) == b)
             for a in range(n)]
    out = []
    def rec(a, chosen):
        if a == n:
            out.append(chosen)
            return
        rec(a + 1, chosen)
        if (chosen & lower[a]) == lower[a]:
            rec(a + 1, chosen | (1 << a))
    rec(0, 0)
    return out


def dedekind_seven():
    ids = ideals_boolean(4)
    n = len(ids)
    assert n == 168 and n ** 6 < 2 ** 63
    z = np.array([[int((a & b) == a) for b in ids] for a in ids],
                 dtype=np.int64)
    answer = 0
    intervals = 0
    for i in range(n):
        for j in range(n):
            if not z[i, j]:
                continue
            K = np.flatnonzero(z[i, :] & z[:, j])
            q = z[np.ix_(K, K)]
            U = q @ q.T
            answer += int(np.sum((U @ U) * U))
            intervals += 1
    assert intervals == 7581
    return answer


def certify_d9(D7):
    # Three blocks of size 3, and balanced subsets of size 4.
    vertices = [a for a in range(512) if a.bit_count() == 4
                and all(0 < (a & (7 << (3 * j))).bit_count() < 3
                        for j in range(3))]
    S = [a for a in vertices if a & 1]
    T = [a for a in vertices if not (a & 1)]
    assert (len(vertices), len(S), len(T)) == (81, 36, 45)
    neigh = [sum(1 << j for j, a in enumerate(S) if not (a & b))
             for b in T]
    total = 0
    summands = []
    for r in range(4):
        subtotal = 0
        for R in combinations(range(len(T)), r):
            if any(not (T[i] & T[j]) for i, j in combinations(R, 2)):
                continue
            forbidden = 0
            for i in R:
                forbidden |= neigh[i]
            subtotal += 1 << (len(S) - forbidden.bit_count())
        summands.append(subtotal)
        total += subtotal
    assert total > D7
    return total, summands


def cut_count(parts):
    a, b, c = parts
    d = a + b + c
    k = d // 2
    ans = 0
    for i in range(1, a):
        for j in range(1, b):
            h = k - i - j
            if 1 <= h < c:
                first = comb(a, i) if d % 2 == 0 else comb(a - 1, i - 1)
                ans += first * comb(b, j) * comb(c, h)
    if d % 2 == 0:
        assert ans % 2 == 0
        ans //= 2
    return ans


def certify_d10_and_up(D7):
    parts = {
        10: (4, 3, 3), 11: (3, 4, 4), 12: (4, 4, 4),
        13: (4, 5, 4), 14: (5, 5, 4), 15: (5, 5, 5),
        16: (6, 5, 5), 17: (5, 6, 6), 18: (6, 6, 6),
        19: (6, 7, 6)
    }
    upper = D7
    table = []
    for d in range(10, 20):
        b = cut_count(parts[d])
        w = comb(d - 2, (d - 2) // 2)
        if d <= 13:
            upper = upper * (upper + 1) // 2
            assert (1 << b) > upper
        else:
            assert 5 * b >= 8 * w
        table.append((d, parts[d], b))
    # Constants in the two infinite-tail estimates.
    assert Fraction(19, 10) * (1 - Fraction(6, 64)) > Fraction(8, 5)
    assert (Fraction(20, 11) *
            (1 - Fraction(4, 128) - 2 * Fraction(11, 20) ** 7)
            > Fraction(8, 5))
    assert 3 ** 5 < 2 ** 8
    return table


def check_ordered_symmetric_chains(max_n=9):
    chains = [(0,)]
    for n in range(max_n + 1):
        assert len(chains) == comb(n, n // 2)
        flat = [a for C in chains for a in C]
        assert sorted(flat) == list(range(1 << n))
        earlier = set()
        for C in chains:
            assert C[0].bit_count() + C[-1].bit_count() == n
            assert all((a & b) == a and b.bit_count() == a.bit_count() + 1
                       for a, b in zip(C, C[1:]))
            for a, b in zip(C, C[2:]):
                assert any(a != z != b and (a & z) == a and (z & b) == z
                           for z in earlier)
            earlier.update(C)
        bit = 1 << n
        new = []
        for C in chains:
            if len(C) > 1:
                new.append(tuple(a | bit for a in C[:-1]))
            new.append(C + (C[-1] | bit,))
        chains = new


if __name__ == '__main__':
    start = perf_counter()
    check_ordered_symmetric_chains()
    small_lambda = [lambda_exact(k) for k in range(1, 8)]
    assert small_lambda == [1, 2, 4, 12, 81, 2646, 1422564]
    print('lambda(1..7):', small_lambda, flush=True)
    print('d=8 leaves, visited states:', certify_d8(small_lambda[-1] + 1), flush=True)
    D7 = dedekind_seven()
    assert D7 == 2414682040998
    print('D(7):', D7, flush=True)
    print('d=9 lower count and its four summands:', certify_d9(D7), flush=True)
    print('cut counts:', certify_d10_and_up(D7), flush=True)
    print('All finite certificates passed; elapsed seconds:', perf_counter() - start)
