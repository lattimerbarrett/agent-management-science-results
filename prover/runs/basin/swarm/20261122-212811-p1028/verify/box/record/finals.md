# agent_1: last reply

Here is one explicit exact formula. It is computationally enormous, rather than a compact formula by residue classes, but it involves **only \(n\)** and ordinary arithmetic operations, determinants, factorials, floors, and a finite sum. In particular, there is no optimization over graphs in the formula.

## The formula

Use vertex indices \(0,\ldots,n-1\). Put
\[
m=\binom n2,\qquad B=2^m+1,\qquad H=(n-1)^{n-1},\qquad Q=H!.
\]

For \(0\le a<2^m\) and \(0\le i<j<n\), define
\[
s(i,j)=\frac{i(2n-i-1)}2+j-i-1,
\]
and
\[
b_{ij}(a)=
\left\lfloor\frac{a}{2^{s(i,j)}}\right\rfloor
-2\left\lfloor\frac{a}{2^{s(i,j)+1}}\right\rfloor.
\]
Set \(b_{ji}(a)=b_{ij}(a)\), \(b_{ii}(a)=0\), and
\[
d_i(a)=\sum_{j=0}^{n-1}b_{ij}(a).
\]
Let \(L_a\) be the explicitly specified integer matrix
\[
(L_a)_{ij}=
\begin{cases}
d_i(a),&i=j,\\
-b_{ij}(a),&i\ne j.
\end{cases}
\]

For a matrix \(L\), write \(L_{\widehat S}\) for the principal submatrix obtained by deleting the indices in \(S\). Define
\[
D_a=\det (L_a)_{\widehat{\{1\}}},
\qquad
F_a=\det (L_a)_{\widehat{\{0,1\}}},
\]
\[
c_a=1-\left\lfloor\frac1{D_a+1}\right\rfloor,
\qquad
r_a=\prod_{i=1}^{n-1}
 \left\lfloor\frac1{1+(d_i(a)-d_0(a))^2}\right\rfloor,
\]
and
\[
E_a=
\frac{Q\,n\,d_0(a)\,c_a r_a F_a}{D_a+1-c_a}.
\]

Then the answer throughout the requested domain is
\[
\boxed{\displaystyle
t_n=
\frac1{((n-1)^{n-1})!}
\left\lfloor
\log_{\,2^{\binom n2}+1}
\left(
\sum_{a=0}^{\,2^{\binom n2}-1}
\left(2^{\binom n2}+1\right)^{E_a}
\right)
\right\rfloor .}
\tag{1}
\]

All denominators appearing here are positive, and every \(E_a\) is a nonnegative integer. These assertions are proved below. Determinants in (1) can also be expanded by the Leibniz formula if a formula using only scalar operations is preferred.

In fact, (1) works for every \(n\ge2\).

## Proof

### 1. The determinant tests and their bounds

The numbers \(b_{ij}(a)\) are precisely the successive binary digits of \(a\). Consequently, as \(a\) ranges from \(0\) to \(2^m-1\), these arrays run through every symmetric zero-diagonal \(0\)-\(1\) array exactly once.

For the proof, interpret one such array as the adjacency matrix of a graph. Its Laplacian is \(L_a\). For every real vector \(x\),
\[
x^{\mathsf T}L_a x
=\sum_{\{i,j\}:\,b_{ij}(a)=1}(x_i-x_j)^2.
\tag{2}
\]
In particular, \(L_a\) and all its principal submatrices are positive semidefinite.

Consider \(A=(L_a)_{\widehat{\{1\}}}\). Extend a vector indexed by \(V\setminus\{1\}\) by putting its coordinate at \(1\) equal to zero. Equation (2) shows that \(A\) is positive definite exactly when the graph is connected:

* In a connected graph, zero energy forces all coordinates to be equal, hence zero.
* In a disconnected graph, the indicator of a component not containing \(1\) gives a nonzero zero-energy vector.

Thus
\[
D_a>0\quad\Longleftrightarrow\quad\text{the graph is connected}.
\tag{3}
\]
Also \(D_a\) is a nonnegative integer. Hadamard’s determinant inequality gives
\[
0\le D_a
\le \prod_{i\ne1}d_i(a)
\le(n-1)^{n-1}=H.
\tag{4}
\]
Positive semidefiniteness also gives \(F_a\ge0\).

It follows immediately that
\[
c_a=
\begin{cases}
1,&\text{the graph is connected},\\
0,&\text{otherwise}.
\end{cases}
\tag{5}
\]
Likewise, since the degrees are integers,
\[
r_a=
\begin{cases}
1,&d_0(a)=d_1(a)=\cdots=d_{n-1}(a),\\
0,&\text{otherwise}.
\end{cases}
\tag{6}
\]

In particular, \(D_a+1-c_a\) equals \(D_a\) in the connected case and \(1\) otherwise, so it is always positive.

### 2. An exact determinant formula for the commute time

Let \(G\) be connected and \(d\)-regular, with Laplacian \(L\). For a vertex \(v\), let
\[
h^{(v)}_i=\mathbb E_iT_v.
\]
These expectations are finite: from every vertex there is a path of at most \(n-1\) steps to \(v\), and connectedness gives a uniform positive probability of following such a path in any block of \(n-1\) steps.

The first-step equations say
\[
h^{(v)}_i=1+\frac1d\sum_{j\sim i}h^{(v)}_j
\qquad(i\ne v).
\]
Since \(h^{(v)}_v=0\) and the rows and columns of \(L\) sum to zero, these equations are equivalent to
\[
Lh^{(v)}=d\mathbf1-nd\,e_v.
\tag{7}
\]
Subtracting the equations for \(v=1\) and \(v=0\) yields
\[
L\bigl(h^{(1)}-h^{(0)}\bigr)
=nd(e_0-e_1).
\tag{8}
\]

Let \(x\) be the unique solution of
\[
Lx=e_0-e_1,\qquad x_1=0.
\]
It exists and is unique because \(L_{\widehat{\{1\}}}\) is positive definite. Equation (8) shows that
\[
h^{(1)}-h^{(0)}-nd\,x
\]
is constant. Comparing coordinates \(0\) and \(1\), therefore,
\[
\mathbb E_0T_1+\mathbb E_1T_0=nd\,x_0.
\tag{9}
\]

Cramer’s rule applied to the grounded system gives
\[
x_0=
\frac{\det L_{\widehat{\{0,1\}}}}
     {\det L_{\widehat{\{1\}}}}.
\]
Consequently,
\[
\boxed{\displaystyle
\mathbb E_0T_1+\mathbb E_1T_0
=nd\,
\frac{\det L_{\widehat{\{0,1\}}}}
     {\det L_{\widehat{\{1\}}}}.}
\tag{10}
\]

### 3. What the exponents encode

By (5), (6), and (10), the quantity \(E_a/Q\) is:

* the commute time between \(0\) and \(1\), if the encoded graph is connected and regular;
* zero otherwise.

Moreover, in the connected case \(D_a\) is an integer between \(1\) and \(H\). Hence \(D_a\mid H!=Q\). The definition of \(E_a\) therefore proves that
\[
E_a\in\mathbb Z_{\ge0}.
\tag{11}
\]

Every graph under consideration can be labeled by \(0,\ldots,n-1\). Furthermore, any chosen pair of distinct vertices can be relabeled as \(0,1\). Thus, as a statement used in the proof,
\[
\max_{0\le a<2^m}E_a=Q\,t_n.
\tag{12}
\]
There is no restriction lost through fixing the two labels.

### 4. Extracting the largest exponent

Let \(M\) denote the left side of (12), and set
\[
Z=\sum_{a=0}^{2^m-1}B^{E_a}.
\]
At least one summand is \(B^M\), while there are exactly \(2^m=B-1\) summands. Therefore
\[
B^M\le Z\le(B-1)B^M<B^{M+1}.
\]
It follows that
\[
\lfloor\log_B Z\rfloor=M=Qt_n,
\]
which proves (1).

This establishes both attainment and the upper bound: the binary arrays include every eligible graph and every vertex pair after relabeling, and the digit-extraction argument returns exactly their greatest commute time.

## Executable exact checks

The following is Python using SageMath. It uses rational arithmetic throughout; no floating-point logarithms are used.

It performs two kinds of checks:

1. For every adjacency array on \(2,3,4,5\) vertices, it checks the determinant bounds, the two filters, integrality of the exponents, and the determinant commute-time identity against independently solved hitting-time equations. For \(n=2,3\), it also constructs the integer sum in (1) literally.
2. It exhaustively checks \(n=10\), an instance in the question’s domain. It generates regular graphs up to isomorphism and uses complementation to cover every degree. Fixing the neighbors of vertex \(0\) loses no isomorphism classes.

For larger inputs, one should not expand the integer in (1). Its leading exponent can instead be computed exactly, keeping rational exponents divided by the common symbolic factor \(Q\).

```python
from itertools import combinations
from sage.all import Graph, matrix, vector, ZZ, QQ, factorial


def arithmetic_data(n, a):
    """The quantities in formula (1), with score = E_a / Q."""
    L = matrix(ZZ, n, n)
    k = 0
    for i in range(n):
        for j in range(i + 1, n):
            b = a // (2**k) - 2 * (a // (2**(k + 1)))
            k += 1
            L[i, i] += b
            L[j, j] += b
            L[i, j] -= b
            L[j, i] -= b

    ids = [i for i in range(n) if i != 1]
    D = L.matrix_from_rows_and_columns(ids, ids).det()
    F = L[2:, 2:].det()  # determinant of empty matrix is 1

    c = 1 - 1 // (D + 1)
    r = 1
    for i in range(1, n):
        r *= 1 // (1 + (L[i, i] - L[0, 0])**2)

    score = QQ(n * L[0, 0] * c * r * F) / (D + 1 - c)
    return L, D, F, c, r, score


def hit(L, target, start):
    """Independent first-step-equation calculation."""
    ids = [i for i in range(L.nrows()) if i != target]
    A = L.matrix_from_rows_and_columns(ids, ids).change_ring(QQ)
    rhs = vector(QQ, [L[i, i] for i in ids])
    h = A.solve_right(rhs)
    return h[ids.index(start)]


def check_small():
    for n in range(2, 6):
        H = (n - 1)**(n - 1)
        Q = factorial(H)
        scores = []

        for a in range(1 << (n * (n - 1) // 2)):
            L, D, F, c, r, score = arithmetic_data(n, a)

            assert 0 <= D <= H
            assert F >= 0
            assert c == int(D > 0)
            assert r == int(len(set(L.diagonal())) == 1)
            assert (Q * score).denominator() == 1

            if c:
                commute = hit(L, 1, 0) + hit(L, 0, 1)
                # The more general, not necessarily regular identity:
                assert commute == sum(L.diagonal()) * F / D
                if r:
                    assert commute == score

            if not (c and r):
                assert score == 0
            scores.append(score)

        answer = max(scores)

        if n <= 3:
            B = (1 << (n * (n - 1) // 2)) + 1
            Z = sum(B**int(Q * score) for score in scores)

            # Exact floor(log_B Z), with integer arithmetic.
            leading_exponent = 0
            while Z >= B:
                Z //= B
                leading_exponent += 1
            assert QQ(leading_exponent) / Q == answer

        print("all-mask check:", n, len(scores), answer)


def regular_representatives(n, d):
    """
    Generate all isomorphism classes of d-regular graphs.
    The neighbors of vertex 0 are fixed as 1,...,d.
    """
    rem = [d] * n
    adj = [0] * n
    for j in range(1, d + 1):
        adj[0] |= 1 << j
        adj[j] |= 1
        rem[j] -= 1
    rem[0] = 0

    representatives = {}
    leaves = 0

    def rec(i):
        nonlocal leaves

        while i < n and rem[i] == 0:
            i += 1

        if i == n:
            leaves += 1
            edges = [
                (u, v)
                for u in range(n)
                for v in range(u + 1, n)
                if (adj[u] >> v) & 1
            ]
            G = Graph([list(range(n)), edges],
                      format="vertices_and_edges")
            key = G.canonical_label().graph6_string()
            representatives.setdefault(key, edges)
            return

        choices = [j for j in range(i + 1, n) if rem[j] > 0]
        need = rem[i]
        if len(choices) < need:
            return

        rem[i] = 0
        for ns in combinations(choices, need):
            for j in ns:
                rem[j] -= 1
                adj[i] |= 1 << j
                adj[j] |= 1 << i

            positive = sum(x > 0 for x in rem[i + 1:])
            # A residual positive degree must be <= positive - 1.
            if all(x < positive for x in rem[i + 1:] if x):
                rec(i + 1)

            for j in ns:
                rem[j] += 1
                adj[i] ^= 1 << j
                adj[j] ^= 1 << i
        rem[i] = need

    rec(1)
    print("generated:", d, leaves, len(representatives))
    return list(representatives.values())


def check_n10():
    n = 10
    reps = {d: regular_representatives(n, d) for d in range(5)}
    answers = []

    for d in range(n):
        best = QQ(0)
        connected_classes = 0

        for edges in reps[min(d, n - 1 - d)]:
            G = Graph([list(range(n)), edges],
                      format="vertices_and_edges")
            if d >= 5:
                G = G.complement()
            if not G.is_connected():
                continue

            connected_classes += 1
            L = G.laplacian_matrix().change_ring(QQ)

            # Ground vertex 9. This inverse gives every pair's
            # effective resistance, hence its commute time.
            A = L[:9, :9].inverse()
            resistance_diameter = max(
                A[u, u] if v == 9
                else A[u, u] + A[v, v] - 2 * A[u, v]
                for u in range(9)
                for v in range(u + 1, 10)
            )
            best = max(best, n * d * resistance_diameter)

        answers.append(best)
        print("degree maximum:", d, connected_classes, best)

    assert max(answers) == QQ(165) / 2


if __name__ == "__main__":
    check_small()
    check_n10()
```

The executed small checks returned
```text
all-mask check: 2 2 2
all-mask check: 3 8 4
all-mask check: 4 64 8
all-mask check: 5 1024 12
```

The complete \(n=10\) enumeration gave:

| Degree | Connected isomorphism classes | Greatest commute time |
|---:|---:|---:|
| 0 | 0 | — |
| 1 | 0 | — |
| 2 | 1 | \(50\) |
| 3 | 19 | \(165/2\) |
| 4 | 59 | \(44\) |
| 5 | 60 | \(170/7\) |
| 6 | 21 | \(150/7\) |
| 7 | 5 | \(245/12\) |
| 8 | 1 | \(20\) |
| 9 | 1 | \(18\) |

Thus, for example, the formula gives \(t_{10}=165/2\).

**What is proved:** formula (1) equals \(t_n\) for every \(n\) in the question, and indeed for all \(n\ge2\). No case or unproved extremal-graph assertion remains. The formula’s drawback is its size, not a conditional step in its correctness.