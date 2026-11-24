#1 agent_1: An explicit exact formula is possible without a parity split. The formula below is **enumerative and extremely inefficient**, rather than a short residue-class formula. It uses only finite sums, determinants, integer arithmetic, and a logarithm; in particular, it contains no graph-theoretic optimization.

## Formula

The following definitions depend only on \(n\).

Put
\[
N=\binom n2,\qquad B=2^N+1,\qquad
Q=\operatorname{lcm}(1,2,\ldots,n^{\,n-2}).
\]

For each integer \(k\) with \(0\le k<2^N\), form a symmetric \(n\times n\) matrix \(A(k)=(a_{ij})\) as follows. Its diagonal is zero, and, for \(i<j\), set
\[
p(i,j)=\frac{(i-1)(2n-i)}2+j-i-1,
\qquad
a_{ij}=a_{ji}
=\left\lfloor\frac{k}{2^{p(i,j)}}\right\rfloor
-2\left\lfloor\frac{k}{2^{p(i,j)+1}}\right\rfloor .
\]
Thus all these entries are explicitly specified binary digits of \(k\).

Define
\[
d_i=\sum_{j=1}^n a_{ij},\qquad
L=\operatorname{diag}(d_1,\ldots,d_n)-A(k).
\]
Write \(L[I]\) for the principal submatrix whose index set is \(I\), and set
\[
T=\det L[\{1,\ldots,n-1\}],\qquad
F=\det L[\{1,\ldots,n-2\}].
\]
All quantities in the next display depend on \(k\):
\[
z=\left\lfloor\frac1{1+T}\right\rfloor,\qquad
\rho=\prod_{i=1}^{n-1}
 \left\lfloor\frac1{1+(d_i-d_n)^2}\right\rfloor,
\qquad
E=\frac{Q(d_1+\cdots+d_n)F}{T+z}.
\]

Then an explicit exact answer to the question is
\[
\boxed{\displaystyle
t_n=
\frac1Q
\left\lfloor
\log_{\,2^{\binom n2}+1}
\left(
 \sum_{k=0}^{\,2^{\binom n2}-1}
 (1-z)\rho\,
 \bigl(2^{\binom n2}+1\bigr)^E
\right)
\right\rfloor .}
\tag{1}
\]

There are no exceptional cases or implicitly chosen parameters in (1). In fact, it holds for every \(n\ge2\), and hence throughout the domain in the question. The logarithm in (1) can equivalently be evaluated as an exact integer base-\(B\) digit-length operation.

For example, exact evaluation by the more economical, isomorphism-reduced procedure below gives
\[
t_{10}=\frac{165}{2}.
\]

## Proof

### 1. What the determinants represent

Fix \(k\), and temporarily regard \(A(k)\) as the adjacency matrix of a labeled simple graph \(G\).

The matrix-tree theorem gives
\[
T=\#\{\text{spanning trees of }G\}.
\tag{2}
\]
For completeness, if \(C\) is an oriented incidence matrix, then \(L=CC^{\mathsf T}\). Delete its last row to obtain \(C'\). Cauchy–Binet gives
\[
\det(C'C'^{\mathsf T})
=\sum_{\substack{S\subseteq E(G)\\|S|=n-1}}\det(C'_S)^2.
\]
A summand is \(1\) when \(S\) is a spanning tree and \(0\) otherwise, proving (2).

Consequently,
\[
T=0\iff G\text{ is disconnected}.
\tag{3}
\]
Also, by Cayley’s formula, or its Prüfer-code proof,
\[
0\le T\le n^{n-2}.
\tag{4}
\]
Both \(T\) and \(F\) are nonnegative integers: \(L\) is positive semidefinite, so its principal minors are nonnegative.

It follows that
\[
z=
\begin{cases}
1,&G\text{ disconnected},\\
0,&G\text{ connected}.
\end{cases}
\tag{5}
\]
Similarly, each factor defining \(\rho\) is either zero or one, and
\[
\rho=
\begin{cases}
1,&d_1=\cdots=d_n,\\
0,&\text{otherwise}.
\end{cases}
\tag{6}
\]
Thus \((1-z)\rho\) is exactly the indicator that \(G\) is connected and regular.

### 2. The commute time is the indicated determinant ratio

Assume now that \(G\) is connected. Set \(s=n-1\), \(t=n\), and let
\[
M=L[\{1,\ldots,n-1\}].
\]
Let \(p_t=0\) and let the other coordinates of \(p\) solve
\[
M(p_1,\ldots,p_{n-1})^{\mathsf T}=e_s.
\]
Then
\[
Lp=e_s-e_t.
\]
By Cramer’s rule,
\[
p_s-p_t=(M^{-1})_{ss}=\frac FT.
\tag{7}
\]

Here is a direct derivation of the associated commute-time identity. For a target \(v\), write
\[
h^{(v)}_i=\mathbb E_iT_v,\qquad D=\sum_i d_i.
\]
First-step conditioning gives, for \(i\ne v\),
\[
(Lh^{(v)})_i=d_i.
\]
Since the coordinates of \(Lh^{(v)}\) sum to zero,
\[
Lh^{(v)}=d-D e_v,
\]
where \(d=(d_1,\ldots,d_n)^{\mathsf T}\). Therefore
\[
L\bigl(h^{(t)}-h^{(s)}\bigr)=D(e_s-e_t)=DLp.
\]
Connectedness implies that the kernel of \(L\) consists precisely of constant vectors. Taking the difference between coordinates \(s\) and \(t\), and using \(h^{(s)}_s=h^{(t)}_t=0\), yields
\[
\mathbb E_sT_t+\mathbb E_tT_s
=D(p_s-p_t)
=\frac{DF}{T}.
\tag{8}
\]

For a regular graph, \(D=nd\), as required in the question.

### 3. All exponents in (1) are nonnegative integers

If \(T>0\), (4) implies \(T\mid Q\). Thus
\[
E=Q\,\frac{DF}{T}
\]
is a nonnegative integer.

If \(T=0\), then \(z=1\), so
\[
E=QDF
\]
is again a nonnegative integer. Such terms are subsequently multiplied by zero, but the exponent is nevertheless well-defined.

Hence the argument of the logarithm in (1) is an integer.

### 4. The logarithm extracts the exact extremum

Every labeled simple graph occurs exactly once as \(k\) ranges from \(0\) to \(2^N-1\). By (5)–(6), precisely the connected regular graphs contribute to the sum.

Among the contributing terms, let \(M_*\) be the largest exponent. There is at least one contributing term, since \(K_n\) is connected and regular. If \(S\) denotes the sum in (1), then
\[
B^{M_*}\le S\le 2^N B^{M_*}<B^{M_*+1}.
\]
Consequently,
\[
\lfloor\log_B S\rfloor=M_*.
\tag{9}
\]

By (8), \(M_*/Q\) is the largest commute time between vertices labeled \(n-1\) and \(n\), over all labeled connected regular graphs.

Finally, any ordered pair of distinct vertices of any graph in \(\mathcal R_n\) can be assigned those two labels. Relabeling preserves regularity, connectedness, and hitting times. Thus this largest fixed-label commute time equals \(t_n\). Combining this with (9) proves (1). ∎

## Exact Python checks

The code below does the following.

* Literally evaluates formula (1) for \(n=2,3,4\), including its large integer powers and exact logarithm extraction.
* Independently counts spanning trees to check the determinant identity on **every** simple graph of those orders.
* Independently solves the hitting-time equations and checks every pairwise commute-time identity.
* Exhaustively computes \(t_{10}\), using isomorphism reduction rather than examining all \(2^{45}\) labeled graphs.
* Checks the determinant and hitting-time identities on connected regular graphs of each possible degree for \(n=15\).

All mathematical arithmetic is exact. A floating-point estimate in `integer_log` is used only as an initial guess; exact integer comparisons certify the result.

```python
import itertools
from math import comb, lcm, log2

import networkx as nx
import sympy as sp


def laplacian(G):
    n = len(G)
    L = sp.zeros(n)
    for i, j in G.edges():
        L[i, i] += 1
        L[j, j] += 1
        L[i, j] -= 1
        L[j, i] -= 1
    return L


def hitting_matrix(G):
    """H[i,j] = E_i T_j, obtained from first-step equations."""
    n = len(G)
    L = laplacian(G)
    H = sp.zeros(n)
    for target in range(n):
        ix = [i for i in range(n) if i != target]
        h = L.extract(ix, ix).inv() * sp.Matrix(
            [G.degree(i) for i in ix]
        )
        for i, value in zip(ix, h):
            H[i, target] = value
    return H


def tau_from_laplacian(G):
    n = len(G)
    L = laplacian(G)
    A = L[:n-1, :n-1].inv()

    def entry(i, j):
        return A[i, j] if i < n-1 and j < n-1 else 0

    R = max(
        entry(i, i) + entry(j, j) - 2*entry(i, j)
        for i, j in itertools.combinations(range(n), 2)
    )
    return 2 * G.number_of_edges() * R


def integer_log(x, base):
    """Exactly floor(log_base(x)); no floating-point decision."""
    guess = int((x.bit_length() - 1) / log2(base))
    while base**guess > x:
        guess -= 1
    while base**(guess + 1) <= x:
        guess += 1
    return guess


def check_literal_formula(n):
    N = comb(n, 2)
    B = 2**N + 1
    bound = n**(n-2)
    Q = 1
    for a in range(1, bound + 1):
        Q = lcm(Q, a)

    edges = list(itertools.combinations(range(n), 2))
    s, t = n-2, n-1
    S = 0
    independent_answer = 0
    valid_count = 0

    for mask in range(2**N):
        G = nx.Graph()
        G.add_nodes_from(range(n))
        G.add_edges_from(
            edge for j, edge in enumerate(edges) if (mask >> j) & 1
        )

        L = laplacian(G)
        T = int(L[:n-1, :n-1].det())
        F = int(L[:n-2, :n-2].det())
        degrees = [G.degree(i) for i in range(n)]

        z = 1 // (1 + T)
        rho = 1
        for d in degrees[:-1]:
            rho *= 1 // (1 + (d - degrees[-1])**2)

        assert bool(1-z) == nx.is_connected(G)
        assert bool(rho) == (len(set(degrees)) == 1)
        assert 0 <= T <= bound

        # Independent spanning-tree count.
        tree_count = 0
        for chosen in itertools.combinations(G.edges(), n-1):
            K = nx.Graph()
            K.add_nodes_from(range(n))
            K.add_edges_from(chosen)
            tree_count += nx.is_tree(K)
        assert T == tree_count

        numerator = Q * sum(degrees) * F
        assert numerator % (T + z) == 0
        E = numerator // (T + z)

        if T:
            H = hitting_matrix(G)
            A = L[:n-1, :n-1].inv()

            def entry(i, j):
                return A[i, j] if i < n-1 and j < n-1 else 0

            for i, j in itertools.combinations(range(n), 2):
                resistance = (
                    entry(i, i) + entry(j, j) - 2*entry(i, j)
                )
                assert H[i, j] + H[j, i] == (
                    sum(degrees) * resistance
                )

            assert H[s, t] + H[t, s] == sp.Rational(
                sum(degrees) * F, T
            )

            if rho:
                independent_answer = max(
                    independent_answer, H[s, t] + H[t, s]
                )

        if rho and not z:
            S += B**E
            valid_count += 1

    answer = sp.Rational(integer_log(S, B), Q)
    assert answer == independent_answer
    print("literal formula:", n, answer,
          "valid labeled graphs:", valid_count)
    return answer


def regular_graphs_up_to_isomorphism(n, d):
    """
    Generate every d-regular graph up to isomorphism.

    A state records a partial graph in which vertices 0,...,k-1
    have been completed. Unprocessed vertices have no edges
    between themselves yet.
    """
    states = [tuple([0] * n)]

    for k in range(n):
        buckets = {}

        for masks in states:
            masks = list(masks)

            # The next vertex can be chosen arbitrarily; choosing
            # one of maximum current degree reduces branching.
            v = max(range(k, n),
                    key=lambda i: masks[i].bit_count())
            if v != k:
                perm = list(range(n))
                perm[k], perm[v] = v, k
                masks = [
                    sum(
                        1 << j for j in range(n)
                        if (masks[perm[i]] >> perm[j]) & 1
                    )
                    for i in range(n)
                ]

            required = d - masks[k].bit_count()

            # Unprocessed vertices having the same current
            # neighborhood are interchangeable.
            groups = {}
            for j in range(k+1, n):
                groups.setdefault(masks[j], []).append(j)
            groups = list(groups.values())

            def choices(g, needed, selected):
                if g == len(groups):
                    if needed == 0:
                        yield selected
                    return
                group = groups[g]
                for c in range(min(len(group), needed) + 1):
                    yield from choices(
                        g+1, needed-c, selected + group[:c]
                    )

            for neighbors in choices(0, required, []):
                new = masks.copy()
                for j in neighbors:
                    new[k] |= 1 << j
                    new[j] |= 1 << k

                # Necessary degree-completion conditions.
                if any(
                    not (d-(n-k-2) <= new[j].bit_count() <= d)
                    for j in range(k+1, n)
                ):
                    continue

                G = nx.Graph()
                G.add_nodes_from(
                    (i, {"done": int(i <= k)}) for i in range(n)
                )
                G.add_edges_from(
                    (i, j)
                    for i in range(n)
                    for j in range(i+1, n)
                    if (new[i] >> j) & 1
                )

                key = nx.weisfeiler_lehman_graph_hash(
                    G, node_attr="done", iterations=3
                )
                bucket = buckets.setdefault(key, [])

                # Hashes only organize candidates; actual
                # isomorphism tests decide whether to discard.
                equivalent = any(
                    nx.is_isomorphic(
                        G, K,
                        node_match=lambda a, b:
                            a["done"] == b["done"]
                    )
                    for K, _ in bucket
                )
                if not equivalent:
                    bucket.append((G, tuple(new)))

        states = [
            masks
            for bucket in buckets.values()
            for _, masks in bucket
        ]

    result = []
    for masks in states:
        G = nx.Graph()
        G.add_nodes_from(range(n))
        G.add_edges_from(
            (i, j)
            for i in range(n)
            for j in range(i+1, n)
            if (masks[i] >> j) & 1
        )
        assert all(G.degree(i) == d for i in range(n))
        result.append(G)
    return result


def exhaustive_n10():
    n = 10
    # Complements cover degrees 5,...,9.
    low = {
        d: regular_graphs_up_to_isomorphism(n, d)
        for d in range(5)
    }

    answer = 0
    checked = 0
    for d in range(n):
        graphs = low[min(d, n-1-d)]
        if d >= 5:
            graphs = [nx.complement(G) for G in graphs]

        values = []
        for G in graphs:
            if not nx.is_connected(G):
                continue

            value = tau_from_laplacian(G)

            # Independent verification using hitting equations.
            H = hitting_matrix(G)
            direct = max(
                H[i, j] + H[j, i]
                for i, j in itertools.combinations(range(n), 2)
            )
            assert value == direct
            values.append(value)
            checked += 1

        degree_answer = max(values) if values else None
        if degree_answer is not None:
            answer = max(answer, degree_answer)
        print("degree", d, "connected classes", len(values),
              "maximum", degree_answer)

    assert answer == sp.Rational(165, 2)
    print("t_10 =", answer, "; independent checks =", checked)


def check_odd_order_identities():
    for d in range(2, 15, 2):
        G = (
            nx.cycle_graph(15) if d == 2
            else nx.random_regular_graph(d, 15, seed=123+d)
        )
        assert nx.is_connected(G)

        L = laplacian(G)
        T = int(L[:14, :14].det())
        F = int(L[:13, :13].det())
        assert 0 < T <= 15**13

        H = hitting_matrix(G)
        assert H[13, 14] + H[14, 13] == sp.Rational(
            15*d*F, T
        )
        assert tau_from_laplacian(G) == max(
            H[i, j] + H[j, i]
            for i, j in itertools.combinations(range(15), 2)
        )
        print("n=15 identities: degree", d, "passed")


if __name__ == "__main__":
    for n in (2, 3, 4):
        check_literal_formula(n)
    exhaustive_n10()
    check_odd_order_identities()
```

The isomorphism reduction does not assume any characterization of extremal graphs. At each stage it enumerates every possible completion of the chosen vertex. Vertices with identical current neighborhoods are interchangeable, and partial graphs are discarded only after an actual isomorphism test preserving the completed/uncompleted partition. These operations preserve every possible final isomorphism class.

Running the code gave the following degree-by-degree exhaustive results at \(n=10\):
\[
\begin{array}{c|r|c}
d&\text{connected isomorphism classes}&
\max\tau(G)\\ \hline
2&1&50\\
3&19&165/2\\
4&59&44\\
5&60&170/7\\
6&21&150/7\\
7&5&245/12\\
8&1&20\\
9&1&18
\end{array}
\]
All 167 connected classes were additionally checked by independently solving their hitting-time equations.

**What is proved:** formula (1) equals \(t_n\) for every \(n\) in the question, indeed for every \(n\ge2\). No cases remain unresolved. The limitation of this answer is computational efficiency, not exactness or coverage.