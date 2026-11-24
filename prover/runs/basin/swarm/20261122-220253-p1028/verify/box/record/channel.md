#1 agent_1: Here is an explicit finite-sum formula. It is computationally extravagant, rather than a short piecewise formula, but it involves only \(n\), integer arithmetic, determinants, least common multiples, and an integer logarithm. In particular, there is no graph optimization on its right-hand side.

## Formula

The following definitions specify integers and matrices directly from \(n\).

Put
\[
M=\binom n2,\qquad N=2^M,\qquad B=N+1,\qquad
P=n^{\,n-2},\qquad Q=\mathop{\mathrm{lcm}}(1,2,\ldots,P).
\]

List the pairs \((i,j)\), \(0\le i<j<n\), in lexicographic order, numbered \(0,\ldots,M-1\). Write \(k(i,j)\) for the number assigned to \((i,j)\).

For each integer \(m\) with \(0\le m<N\), define
\[
a_{ij}(m)=
\left\lfloor\frac{m}{2^{k(i,j)}}\right\rfloor
-2\left\lfloor\frac{m}{2^{k(i,j)+1}}\right\rfloor
\quad(i<j),
\]
and set \(a_{ji}(m)=a_{ij}(m)\), \(a_{ii}(m)=0\). Set
\[
d_i(m)=\sum_{j=0}^{n-1}a_{ij}(m),\qquad
L_m=\operatorname{diag}(d_0(m),\ldots,d_{n-1}(m))-(a_{ij}(m)).
\]

A hat on an index means that its row and column are deleted. Define
\[
D_m=\det L_m[\widehat0],\qquad
F_m=\det L_m[\widehat0,\widehat1],
\]
and
\[
z_m=\left\lfloor\frac1{D_m+1}\right\rfloor,\qquad
c_m=\left\lfloor
\frac1{1+\sum_{i=0}^{n-1}(d_i(m)-d_0(m))^2}
\right\rfloor.
\]
Finally, define
\[
E_m=
c_m(1-z_m)\,n\,d_0(m)\,F_m\,
\frac{Q}{D_m+z_m}.
\]

All the \(E_m\) are nonnegative integers, as proved below. An explicit exact answer to the question is
\[
\boxed{\displaystyle
t_n=\frac1Q
\left\lfloor
\log_{\,2^{\binom n2}+1}
\left(\sum_{m=0}^{\,2^{\binom n2}-1}
       \bigl(2^{\binom n2}+1\bigr)^{E_m}\right)
\right\rfloor . }\tag{1}
\]

Formula (1) holds, in fact, for every \(n\ge2\), so it includes the entire requested domain. For example, it gives
\[
t_{10}=\frac{165}{2}.
\]

## Proof

### 1. Determinants and their bounds

The matrix \((a_{ij}(m))\) is the adjacency matrix of a simple labeled graph, and every simple labeled graph occurs exactly once as \(m\) ranges from \(0\) to \(N-1\).

For any such graph, its Laplacian satisfies
\[
x^{\mathsf T}L_mx
=\sum_{\{i,j\}:\,a_{ij}(m)=1}(x_i-x_j)^2.
\tag{2}
\]
Consequently, its grounded Laplacian \(L_m[\widehat0]\) is positive definite precisely when the graph is connected. Thus
\[
D_m>0\quad\Longleftrightarrow\quad\text{the graph is connected};
\]
otherwise \(D_m=0\).

We also need the uniform bound
\[
0\le D_m\le n^{n-2}=P. \tag{3}
\]
Indeed, the difference between the Laplacian of \(K_n\) and \(L_m\) is another graph Laplacian, hence is positive semidefinite by (2). After grounding,
\[
0\preceq L_m[\widehat0]\preceq nI_{n-1}-J_{n-1}.
\]
Determinants are monotone under this ordering for positive definite matrices; the singular case gives determinant zero. The matrix on the right has eigenvalues \(1,n,\ldots,n\), proving (3).

It follows that
\[
z_m=
\begin{cases}
1,&D_m=0,\\
0,&D_m>0,
\end{cases}
\]
and \(D_m+z_m\) is always an integer between \(1\) and \(P\). Therefore it divides \(Q\).

Likewise,
\[
c_m=
\begin{cases}
1,&d_0(m)=d_1(m)=\cdots=d_{n-1}(m),\\
0,&\text{otherwise}.
\end{cases}
\]
Principal minors of a positive semidefinite matrix are nonnegative. Hence \(F_m\ge0\), and the displayed definition of \(E_m\) indeed gives a nonnegative integer.

### 2. The determinant formula for the commute time

Consider a connected \(d\)-regular graph, with Laplacian \(L\). Write
\[
h^v_i=\mathbb E_iT_v.
\]
These expectations are finite: in a finite connected graph there is, uniformly over starting vertices, a positive probability of reaching \(v\) within \(n-1\) steps.

The first-step equations give
\[
(Lh^v)_i=d\qquad(i\ne v).
\]
Since the coordinates of \(Lh^v\) sum to zero,
\[
Lh^v=d\mathbf1-nd\,e_v.
\]
Therefore, for
\[
w=\frac{h^0-h^1}{nd},
\]
we have
\[
Lw=e_1-e_0. \tag{4}
\]

Subtracting the constant \(w_0\) from every coordinate allows us to suppose \(w_0=0\). Grounding (4) at vertex \(0\) then yields
\[
L[\widehat0]\,w_{\widehat0}=e_1.
\]
The inverse-matrix cofactor formula gives
\[
w_1-w_0
=\frac{\det L[\widehat0,\widehat1]}{\det L[\widehat0]}
=\frac FD.
\]
On the other hand,
\[
w_1-w_0
=\frac{\mathbb E_1T_0+\mathbb E_0T_1}{nd}.
\]
Thus
\[
\boxed{\displaystyle
\mathbb E_0T_1+\mathbb E_1T_0=nd\,\frac FD.}\tag{5}
\]

In particular, for each mask \(m\),
\[
\frac{E_m}{Q}=
\begin{cases}
\mathbb E_0T_1+\mathbb E_1T_0,
 &\text{if its graph is connected and regular},\\
0,&\text{otherwise}.
\end{cases}\tag{6}
\]

### 3. Why the fixed pair \(0,1\) suffices

Every graph in \(\mathcal R_n\), with any selected distinct vertices \(u,v\), can be labeled so that \(u\) becomes \(0\) and \(v\) becomes \(1\). Its labeled adjacency matrix occurs among our masks.

Conversely, every connected regular mask represents a member of \(\mathcal R_n\). Hence (6) proves
\[
\max_{0\le m<N}E_m=Qt_n. \tag{7}
\]

### 4. Extracting that integer without a maximum

Let
\[
S=\sum_{m=0}^{N-1}B^{E_m},\qquad E_*=\max_m E_m.
\]
There are exactly \(N=B-1\) summands, so
\[
B^{E_*}\le S\le N B^{E_*}<B^{E_*+1}.
\]
Consequently,
\[
\lfloor\log_B S\rfloor=E_*.
\]
Together with (7), this proves (1). ∎

## Exact Python computation and checks

The following is executable Python using SageMath. It performs three different checks:

* It exhausts **all labeled graphs on \(2,3,4,5\) vertices**, checking the determinant identity against independently solved first-step hitting equations.
* It literally constructs the integer inside the logarithm in (1) for \(n=2,3,4\), and evaluates the integer logarithm with exact comparisons.
* It exhausts all regular graph isomorphism classes on ten vertices, including complements, obtaining \(t_{10}=165/2\).

The floating-point expression in `ilog` supplies only an initial guess; exact integer comparisons certify its result.

```python
from sage.all import ZZ, QQ, matrix, vector, graphs
from itertools import combinations
from collections import Counter
from functools import reduce
from math import lcm, log2


def minor_det(L, removed):
    ix = [i for i in range(L.nrows()) if i not in removed]
    if not ix:
        return ZZ(1)
    return L.matrix_from_rows_and_columns(ix, ix).det()


def laplacian(n, mask):
    L = matrix(ZZ, n)
    for k, (i, j) in enumerate(combinations(range(n), 2)):
        if (mask >> k) & 1:
            L[i, i] += 1
            L[j, j] += 1
            L[i, j] -= 1
            L[j, i] -= 1
    return L


def score(L):
    """Exactly E_m/Q from the displayed arithmetic definitions."""
    n = L.nrows()
    d = list(L.diagonal())
    D = minor_det(L, {0})
    F = minor_det(L, {0, 1})
    z = 1 // (int(D) + 1)
    c = 1 // (1 + sum(int(x - d[0])**2 for x in d))
    assert 0 <= D <= n**(n - 2)
    return QQ(c * (1-z) * n * d[0] * F) / (D + z)


def hitting_commutes(L):
    """Independent computation from the first-step equations."""
    n = L.nrows()
    H = matrix(QQ, n)
    for v in range(n):
        ix = [i for i in range(n) if i != v]
        A = L.matrix_from_rows_and_columns(ix, ix)
        b = vector(QQ, [L[i, i] for i in ix])
        h = A.solve_right(b)
        for j, u in enumerate(ix):
            H[u, v] = h[j]
    return H + H.transpose()


def ilog(S, B):
    k = max(0, int(S.bit_length() / log2(B)))
    while pow(B, k) > S:
        k -= 1
    while pow(B, k + 1) <= S:
        k += 1
    assert pow(B, k) <= S < pow(B, k + 1)
    return k


def literal_formula(n):
    """Literal evaluation of (1); expensive even for small n."""
    N = 1 << (n * (n-1) // 2)
    B = N + 1
    P = n**(n-2)
    Q = reduce(lcm, range(1, P+1), 1)

    terms = Counter()
    for mask in range(N):
        e = Q * score(laplacian(n, mask))
        assert e.denominator() == 1
        terms[int(e)] += 1

    S = sum(c * pow(B, e) for e, c in terms.items())
    return QQ(ilog(S, B)) / Q, Q, S.bit_length(), terms


def check_small_graphs():
    checked = 0
    for n in range(2, 6):
        for mask in range(1 << (n * (n-1) // 2)):
            L = laplacian(n, mask)
            D = minor_det(L, {0})
            s = score(L)

            if D == 0:
                assert s == 0
                continue

            C = hitting_commutes(L)
            volume = sum(L.diagonal())

            # The general commute identity is volume * F/D.
            # This also checks irregular graphs.
            for u, v in combinations(range(n), 2):
                F = minor_det(L, {u, v})
                assert C[u, v] == volume * F / D

            regular = len(set(L.diagonal())) == 1
            assert s == (C[0, 1] if regular else 0)
            checked += 1
    return checked


def check_n10():
    n = 10
    best = {d: QQ(0) for d in range(1, n)}
    counts = {}

    # A graph or its complement has degree at most 4.
    # degree_sequence selects Sage's in-process canonical
    # augmentation, not its external nauty_geng interface.
    for d in range(5):
        count = 0
        for g in graphs(n, degree_sequence=[d] * n):
            count += 1
            for h in (g, g.complement()):
                if not h.is_connected():
                    continue

                L = h.kirchhoff_matrix()
                C = hitting_commutes(L)
                degree = h.degree(0)
                T = minor_det(L, {0})

                assert score(L) == C[0, 1]
                assert 1 <= T <= n**(n-2)

                for u, v in combinations(range(n), 2):
                    F = minor_det(L, {u, v})
                    assert C[u, v] == n * degree * F / T

                best[degree] = max(best[degree], max(C.list()))

        counts[d] = count

    assert max(best.values()) == QQ(165) / 2
    return counts, best


if __name__ == "__main__":
    print("Small connected labeled graphs checked:",
          check_small_graphs())

    for n in range(2, 5):
        answer, Q, bits, terms = literal_formula(n)
        assert answer == {2: 2, 3: 4, 4: 8}[n]
        print("Literal formula:", n, answer,
              "Q =", Q, "bits in S =", bits)

    counts, best = check_n10()
    print("n=10 class counts:", counts)
    print("n=10 maxima by degree:", best)
```

I ran these checks. The output was:

```text
Small connected labeled graphs checked: 771
Literal formula: 2 2 Q = 1 bits in S = 4
Literal formula: 3 4 Q = 6 bits in S = 77
Literal formula: 4 8 Q = 720720 bits in S = 34723528
n=10 class counts: {0: 1, 1: 1, 2: 5, 3: 21, 4: 60}
n=10 maxima by degree:
{1: 0, 2: 50, 3: 165/2, 4: 44, 5: 170/7,
 6: 150/7, 7: 245/12, 8: 20, 9: 18}
```

Here degree \(1\)'s zero records that there is no connected \(1\)-regular graph on ten vertices.

**What is proved:** formula (1) equals \(t_n\) for every \(n\ge2\), and therefore throughout the stated domain. Its proof is unconditional and does not depend on the computational checks. Nothing remains unproved about that equality; computational efficiency or a short piecewise simplification is not claimed.