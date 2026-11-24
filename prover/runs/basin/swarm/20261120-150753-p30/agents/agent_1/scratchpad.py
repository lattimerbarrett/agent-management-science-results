import itertools
from math import comb
import sympy as S


def matrices(s):
    assert s >= 3
    n = 2**(s-1)
    m = n//2
    j = 2*n-2
    t = S.Symbol('t')
    roots = [3] + [4*i+1 for i in range(2*m-3)]
    P = S.Poly(S.prod(t+r for r in roots), t)
    assert len(set(roots)) == 2*m-2
    assert P.degree() == 2*m-2
    # v_2(P(1)/P(0)) = 2m-1, an odd integer.
    def v2_int(a):
        a = int(a); ans = 0
        while a % 2 == 0:
            a //= 2; ans += 1
        return ans
    assert v2_int(P.eval(1))-v2_int(P.eval(0)) == 2*m-1
    Z = S.zeros(m)
    B = []
    Ts = []
    for ell in range(2*m-2):
        T = S.Matrix(m, m, lambda a,b: int(a+b == ell))
        T[m-1,m-1] -= P.nth(ell)
        Ts.append(T)
        B.extend([S.diag(T,-T), Z.row_join(T).col_join(T.row_join(Z))])
    e0 = S.zeros(m,1); e0[0] = 1
    e1 = S.ones(m,1)
    K = e0*e1.T-e1*e0.T
    J = Z.row_join(-K).col_join(K.row_join(Z))
    B.append(J)
    I = S.eye(n)
    A = [I]
    for b in B:
        assert b == b.T
        shift = 1 + max(sum(abs(b[r,c]) for c in range(n)) for r in range(n))
        a = b + shift*I
        assert all(a[r,r] > sum(abs(a[r,c]) for c in range(n) if c != r)
                   for r in range(n))
        A.append(a)
    assert len(A) == j
    # Exact polynomial-remainder identities underlying the construction.
    for a in range(m):
        for b in range(m):
            rem = S.rem(t**(a+b),P.as_expr(),t)
            reconstructed = sum(Ts[ell][a,b]*t**ell for ell in range(2*m-2))
            assert S.expand(rem-reconstructed) == 0
    return roots,P,K,Ts,A


def check_factors(roots, P, K):
    m = K.rows
    t = P.gen
    count = 0
    for inds in itertools.combinations(range(len(roots)),m-1):
        # One representative of every complementary pair.
        if 0 not in inds: continue
        inds = set(inds)
        f = S.Poly(S.prod(t+roots[i] for i in inds),t)
        g = S.Poly(S.prod(t+roots[i] for i in range(len(roots)) if i not in inds),t)
        u = S.Matrix([f.nth(i) for i in range(m)])
        v = S.Matrix([g.nth(i) for i in range(m)])
        assert f*g == P
        assert (u.T*v)[0] > 0
        w = (u.T*K*v)[0]
        assert w == f.eval(0)*g.eval(1)-f.eval(1)*g.eval(0)
        assert w != 0
        count += 1
    assert count == comb(2*m-2,m-1)//2
    return count


def check_upper(s):
    n = 2**(s-1); j = 2*n-2; d = 3*n-2; k = n-2
    assert j+k == d-2 and 2*j-k == d
    # Lucas' binary criterion, also compare with the actual integer for small s.
    assert k & ~j == 0
    if s <= 12: assert comb(j,k) % 2 == 1
    return d

for s in range(3,21):
    check_upper(s)
print('Upper-bound coefficient checked for s=3,...,20.')
for s in (3,4,5):
    roots,P,K,Ts,A = matrices(s)
    pairs = check_factors(roots,P,K)
    print(f's={s}: n={A[0].rows}, {len(A)} SPD matrices; '
          f'{pairs} complementary factor pairs checked; D={check_upper(s)}')
    # Build the actual Gaussian means and covariance matrices.
    j = len(A); n = A[0].rows; d0 = j+n-1
    means = [S.zeros(d0,1)]
    for k in range(j-1):
        c = S.zeros(d0,1); c[k] = 1; means.append(c)
    assert S.Matrix.hstack(*means[1:]).rank() == j-1
    for a in A:
        covariance = S.diag(S.eye(j-1),a)
        assert covariance.shape == (d0,d0)
        assert covariance[j-1:,j-1:] == a
        assert all(covariance[r,r] > sum(abs(covariance[r,c])
                   for c in range(d0) if c != r) for r in range(d0))
print('Gaussian counterexample data checked exactly in dimensions 9, 21, 45.')
