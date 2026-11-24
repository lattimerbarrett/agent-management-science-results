from itertools import combinations
from math import comb
import sympy as sp


def root_polynomial_coefficients(roots):
    # Ascending powers; exact integer arithmetic.
    a = [1]
    for r in roots:
        b = [0] * (len(a) + 1)
        for i, x in enumerate(a):
            b[i] -= r * x
            b[i + 1] += x
        a = b
    return sp.Matrix(a)


def check_construction(s):
    assert s >= 3
    n = 2 ** (s - 1)
    k = n // 2
    j = 2 * n - 2
    d0 = 3 * n - 3
    d = d0 + 1
    roots = [1] + [2 * r for r in range(1, 2 * k - 2)]
    assert len(roots) == 2 * k - 2
    assert len(set(roots)) == len(roots)
    assert all(r > 0 for r in roots) and sum(roots) % 2 == 1

    K = sp.zeros(k)
    K[k - 2, k - 1] = 1
    K[k - 1, k - 2] = -1
    splits = 0
    for S in combinations(roots, k - 1):
        if 1 not in S:  # One representative of each complementary pair.
            continue
        T = set(roots) - set(S)
        a = root_polynomial_coefficients(S)
        b = root_polynomial_coefficients(T)
        assert a[k - 1] == b[k - 1] == 1
        assert all(a[i] * b[i] > 0 for i in range(k))
        assert (a.T * b)[0] > 0
        wedge = (a.T * K * b)[0]
        assert wedge == sum(T) - sum(S)
        assert wedge % 2 == 1
        splits += 1
    assert splits == comb(2 * k - 2, k - 1) // 2

    Z = sp.zeros(k)
    I = sp.eye(n)
    M = [I, sp.BlockMatrix([[Z, -K], [K, Z]]).as_explicit()]
    for r in roots:
        v = sp.Matrix([r ** a for a in range(k)])
        V = v * v.T
        M += [sp.diag(V, -V),
              sp.BlockMatrix([[Z, V], [V, Z]]).as_explicit()]
    assert len(M) == j

    A = [I]
    for B in M[1:]:
        assert B == B.T
        shift = 1 + max(sum(abs(B[a, b]) for b in range(n))
                        for a in range(n))
        C = B + shift * I
        assert C - shift * A[0] == B
        assert all(C[a, a] > sum(abs(C[a, b])
                                for b in range(n) if a != b)
                   for a in range(n))
        A.append(C)
    assert len(A) == j

    # All common bisecting hyperplanes of the constructed Gaussians
    # have zero offset and normals in the last n coordinates.
    means = [sp.zeros(d0, 1)]
    for i in range(j - 1):
        e = sp.zeros(d0, 1)
        e[i] = 1
        means.append(e)
    equations = sp.Matrix([list(mu) + [-1] for mu in means])
    nullspace = equations.nullspace()
    assert len(nullspace) == n
    assert all(all(v[a] == 0 for a in range(j - 1)) and v[-1] == 0
               for v in nullspace)
    for C in A:
        Sigma = sp.diag(sp.eye(j - 1), C)
        assert Sigma.shape == (d0, d0)
        assert Sigma[j - 1:, j - 1:] == C
        assert all(Sigma[a, a] > sum(abs(Sigma[a, b])
                                    for b in range(d0) if b != a)
                   for a in range(d0))

    # Compute the entire truncated mod-2 Euler polynomial.
    euler = {(j + a, 2 * j - a): comb(j, a) % 2
             for a in range(j + 1)
             if j + a <= d and 2 * j - a <= d and comb(j, a) % 2}
    assert euler.get((3 * n - 4, 3 * n - 2)) == 1
    print(f's={s}: {splits} complementary root splits certified; '
          f'{j} SPD Gaussian covariance matrices in dimension {d0}; '
          f'Euler monomials {sorted(euler)}')


for s in (3, 4, 5):
    check_construction(s)

# Further exact checks of the general upper-bound coefficient identity.
for s in range(3, 16):
    n = 2 ** (s - 1)
    j = 2 * n - 2
    assert ((n - 2) & j) == n - 2  # Lucas's parity criterion.
    assert comb(j, n - 2) % 2 == 1
print('All exact checks passed.')
