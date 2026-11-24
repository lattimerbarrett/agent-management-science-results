from sage.all import ZZ, QQ, matrix, vector, graphs
from itertools import combinations
from collections import Counter
from math import lcm, log2
from time import monotonic


def det_minor(L, removed):
    ix = [i for i in range(L.nrows()) if i not in removed]
    return ZZ(1) if not ix else L.matrix_from_rows_and_columns(ix, ix).det()


def laplacian_from_mask(n, m):
    L = matrix(ZZ, n)
    for k, (i, j) in enumerate(combinations(range(n), 2)):
        if (m >> k) & 1:
            L[i,i] += 1; L[j,j] += 1
            L[i,j] -= 1; L[j,i] -= 1
    return L


def arithmetic_score(L):
    n = L.nrows()
    d = list(L.diagonal())
    D = det_minor(L, {0})
    F = det_minor(L, {0,1})
    z = 1 // (int(D) + 1)
    c = 1 // (1 + sum(int(x-d[0])**2 for x in d))
    assert 0 <= D <= n**(n-2)
    return QQ(c*(1-z)*n*d[0]*F) / (D+z)


def independent_commutes(L):
    # Solve the first-step hitting equations, NOT a resistance formula.
    n = L.nrows()
    H = matrix(QQ, n)
    for v in range(n):
        ix = [i for i in range(n) if i != v]
        A = L.matrix_from_rows_and_columns(ix,ix)
        b = vector(QQ, [L[i,i] for i in ix])
        h = A.solve_right(b)
        for j, u in enumerate(ix):
            H[u,v] = h[j]
    return H + H.transpose()


def exact_ilog(S, B):
    # The float is only a guess. The comparisons certify the answer.
    k = max(0, int(S.bit_length()/log2(B)))
    while pow(B,k) > S:
        k -= 1
    while pow(B,k+1) <= S:
        k += 1
    assert pow(B,k) <= S < pow(B,k+1)
    return k


def evaluate_literal_formula(n):
    N = 1 << (n*(n-1)//2)
    B = N+1
    P = n**(n-2)
    Q = lcm(*range(1,P+1))
    exponents = Counter()
    for m in range(N):
        e = Q*arithmetic_score(laplacian_from_mask(n,m))
        assert e.denominator() == 1
        exponents[int(e)] += 1
    S = sum(c*pow(B,e) for e,c in exponents.items())
    ans = QQ(exact_ilog(S,B))/Q
    return ans, Q, S.bit_length(), exponents


def check_all_small_graphs():
    checked = 0
    for n in range(2,6):
        for m in range(1 << (n*(n-1)//2)):
            L = laplacian_from_mask(n,m)
            D = det_minor(L,{0})
            score = arithmetic_score(L)
            if D == 0:
                assert score == 0
                continue
            C = independent_commutes(L)
            # Check the forest determinant formula even for irregular graphs.
            vol = sum(L.diagonal())
            for u,v in combinations(range(n),2):
                F = det_minor(L,{u,v})
                assert C[u,v] == vol*F/D
            regular = len(set(L.diagonal())) == 1
            assert score == (C[0,1] if regular else 0)
            checked += 1
    return checked


def check_n10():
    # Supplying degree_sequence forces Sage's in-process canonical
    # augmentation; this does not invoke nauty_geng or another process.
    n=10
    best = {d:QQ(0) for d in range(1,n)}
    counts = {}
    for d in range(5):
        count=0
        for g in graphs(n, degree_sequence=[d]*n):
            count += 1
            for h in (g, g.complement()):
                if not h.is_connected():
                    continue
                L = h.kirchhoff_matrix()
                C = independent_commutes(L)
                k=h.degree(0)
                assert arithmetic_score(L) == C[0,1]
                T=det_minor(L,{0})
                assert 1 <= T <= n**(n-2)
                for u,v in combinations(range(n),2):
                    assert C[u,v] == n*k*det_minor(L,{u,v})/T
                best[k] = max(best[k],max(C.list()))
        counts[d] = count
    assert max(best.values()) == QQ(165)/2
    return counts,best

if __name__ == '__main__':
    st=monotonic()
    print('connected labeled small graphs checked:',check_all_small_graphs(),flush=True)
    for n in range(2,5):
        a,q,bits,es=evaluate_literal_formula(n)
        assert a == {2:2,3:4,4:8}[n]
        print('literal formula:',n,'t =',a,'Q =',q,'bits in S =',bits,'terms =',dict(es),flush=True)
    counts,best=check_n10()
    print('n=10 isomorphism class counts:',counts,flush=True)
    print('n=10 exact maxima by degree:',best,flush=True)
    print('seconds',monotonic()-st,flush=True)
