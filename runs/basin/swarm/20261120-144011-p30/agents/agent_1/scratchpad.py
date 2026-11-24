from itertools import combinations
from math import comb
import sympy as sp

def check(s):
    assert isinstance(s, int) and s >= 3
    n = 2**(s-1)
    k = n//2
    j = 2*n-2
    d = 3*n-2
    # Upper-bound Euler-class coefficient, checked in two independent ways.
    a, b = d-2, d
    assert a+b == 3*j
    c = comb(j, a-j)
    assert (a-j) == n-2 and c % 2 == 1
    bits = 1
    for _ in range(j):
        bits ^= bits << 1  # coefficients of (1+t)^j over F_2
    assert ((bits >> (n-2)) & 1) == 1
    assert bits == sum(1 << r for r in range(0, 2*n-1, 2))

    # Explicit data for the lower-bound covariance matrices.
    t = sp.Symbol('t')
    M = 2*k-2
    p = sp.Poly(sp.prod(t-r for r in range(1, M+1)), t)
    Cbound = (M+1)**(k-1)
    Bbound = 2*Cbound**2
    T = Bbound+2
    K = sp.zeros(k)
    h = 0
    for u in range(k):
        for v in range(u+1, k):
            K[u,v], K[v,u] = T**h, -T**h
            h += 1
    S = sum(T**e for e in range(h))
    eps = sp.Rational(1, 2*(S+1))
    I = sp.eye(n)
    H = sp.BlockMatrix([[sp.eye(k), -eps*K], [eps*K, sp.eye(k)]]).as_explicit()
    assert K.T == -K
    assert eps*S < sp.Rational(1, 2)

    # Encode the real/imaginary coefficients of ab mod p as real symmetric matrices.
    rem = [sp.rem(sp.Poly(t**r, t), p) for r in range(2*k-1)]
    raw = []
    for ell in range(M):
        R = sp.Matrix(k, k, lambda u,v: rem[u+v].nth(ell))
        Z = sp.zeros(k)
        raw.append(sp.BlockMatrix([[R,Z],[Z,-R]]).as_explicit())
        raw.append(sp.BlockMatrix([[Z,R],[R,Z]]).as_explicit())
    assert len(raw)+2 == j
    Q = [I,H]
    for R in raw:
        assert R.T == R
        L = 1 + max(sum(abs(R[u,v]) for v in range(n)) for u in range(n))
        Q.append(R+L*I)
        assert Q[-1]-L*I == R
    # Strict diagonal dominance certifies positive definiteness, exactly over Q.
    for A in Q:
        assert A.T == A
        assert all(A[u,u] > sum(abs(A[u,v]) for v in range(n) if v != u)
                   for u in range(n))

    # All possible polynomial factorizations: check the finite nonsingularity certificate.
    count = 0
    roots = set(range(1, M+1))
    for A in combinations(range(1, M+1), k-1):
        Ac = roots-set(A)
        f = sp.Poly(sp.prod(t-r for r in A), t)
        g = sp.Poly(sp.prod(t-r for r in Ac), t)
        assert f*g == p
        fv = sp.Matrix([f.nth(r) for r in range(k)])
        gv = sp.Matrix([g.nth(r) for r in range(k)])
        assert max(abs(v) for v in list(fv)+list(gv)) <= Cbound
        wedges = [fv[u]*gv[v]-fv[v]*gv[u]
                  for u in range(k) for v in range(u+1,k)]
        assert any(wedges)
        assert max(abs(w) for w in wedges) <= Bbound
        P = (fv.T*K*gv)[0]
        assert P == sum(w*T**e for e,w in enumerate(wedges)) and P != 0
        C = (fv.T*gv)[0]
        assert C > 0
        # Restrict the two Hermitian forms to (alpha*f, beta*g).
        Ef = sp.zeros(n,2); Eg = sp.zeros(n,2)
        for u in range(k):
            Ef[u,0]=fv[u]; Ef[k+u,1]=fv[u]
            Eg[u,0]=gv[u]; Eg[k+u,1]=gv[u]
        assert Ef.T*I*Eg == C*sp.eye(2)
        assert Ef.T*H*Eg == sp.Matrix([[C,-eps*P],[eps*P,C]])
        # The coefficient determinant for beta is nonzero for alpha != 0.
        x,y = sp.symbols('x y', real=True)
        equations = sp.Matrix([[C*x, C*y],
                               [C*x+eps*P*y, C*y-eps*P*x]])
        assert sp.expand(equations.det()+C*eps*P*(x*x+y*y)) == 0
        count += 1
    assert count == comb(M,k-1)
    print(f's={s}: D={d}; upper coefficient={c} (odd); '
          f'{len(Q)} SPD matrices of order {n}; '
          f'{count} factorization certificates checked.')
    return Q

if __name__ == '__main__':
    import sys
    for s in map(int, sys.argv[1:] or ['3','4','5']):
        check(s)
