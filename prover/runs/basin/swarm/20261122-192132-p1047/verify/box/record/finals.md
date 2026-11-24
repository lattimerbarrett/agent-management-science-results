# agent_1: last reply

The answer is
\[
\boxed{
(t(S),r(S))=
\begin{cases}
(1,3),&|S|=1,\\[2mm]
(2,4),&|S|=2.
\end{cases}}
\]
In particular, the two minima in the question are different.

Below, all constructions are explicit. The Python at the end constructs the matrices used in the proof and checks their determinants, Smith forms, local linking forms, and the relevant congruences.

## 1. Some algebra of odd-order linking forms

We first record the algebraic tools needed for both lower bounds.

### Gauss sums

For a nonsingular linking form \(\ell\) on an odd-order group \(A\), put
\[
\gamma(\ell)=|A|^{-1/2}\sum_{x\in A}\exp(2\pi i\ell(x,x)).
\]
We will use this separately on each primary component.

These elementary properties will be useful:

1. \(\gamma(\ell\oplus\ell')=\gamma(\ell)\gamma(\ell')\).
2. If \(M\) is isotropic, then
   \[
   \gamma(\ell)=\gamma(\ell|_{M^\perp/M}).
   \tag{1}
   \]
   Indeed, summing first over cosets of \(M\), the sum over a coset vanishes unless that coset lies in \(M^\perp\). Here the odd-order hypothesis makes multiplication by \(2\) invertible.
3. Consequently, a metabolic form has Gauss sum \(1\).

For an odd prime \(p\), let
\[
g_p=p^{-1/2}\sum_{x\bmod p}\exp(2\pi i x^2/p).
\]
The elementary quadratic Gauss-sum identities give
\[
\gamma\left(\left\langle\frac a{p^e}\right\rangle\right)
=
\begin{cases}
1,&e\text{ even},\\
\left(\frac ap\right)g_p,&e\text{ odd}.
\end{cases}
\tag{2}
\]
One obtains this by the recurrence for a quadratic sum modulo \(p^e\), reducing the exponent by \(2\). Also
\[
g_p^2=\left(\frac{-1}{p}\right).
\]
For completeness, the latter identity does not require choosing the sign of the classical Gauss sum: its absolute value is \(1\), and
\(\overline{g_p}=\left(\frac{-1}{p}\right)g_p\).

Thus, for every prime considered here,
\[
g_p^2=-1,\qquad g_p^3=-g_p.
\tag{3}
\]

### Jordan constituents and orthogonal summands

Every linking form on a finite abelian \(p\)-group, \(p\) odd, diagonalizes into cyclic forms
\(\langle a/p^e\rangle\), \(p\nmid a\). This follows by splitting off an element of maximal order with self-pairing of maximal order; if necessary, adding two elements produces such an element because \(2\) is invertible.

The dimension and square class at each exponent are intrinsic. One way to see this is to use
\[
D_k(A)=
\frac{A[p^k]}{A[p^{k-1}]+pA[p^{k+1}]}.
\]
The pairing \(p^{k-1}\ell\) induces a nonsingular symmetric \(\mathbb F_p\)-form on \(D_k(A)\). For a cyclic summand of order \(p^e\), it is zero unless \(k=e\), and at \(k=e\) its coefficient is \(a\bmod p\).

It follows that an orthogonal summand of
\[
\left\langle\frac1p\right\rangle
\oplus
\left\langle\frac1{p^3}\right\rangle
\oplus
\left\langle\frac1{p^5}\right\rangle
\tag{4}
\]
has, at each of the exponents \(1,3,5\), either no constituent or the single square-class constituent appearing in (4).

A nonzero such summand therefore has Gauss sum \(g_p^j\) for some \(j\in\{1,2,3\}\). None of these is \(1\). We have proved:

> **Lemma 1.** The form \(\lambda_S\) has no nonzero metabolic orthogonal direct summand.

Notice that this concerns *orthogonal direct summands*. Isotropic reductions, as in (1), are more flexible.

### A reciprocity observation

If \(p,q\equiv3\pmod4\) are distinct, then, for either \(\epsilon=1\) or \(-1\),
\[
\left(\frac{\epsilon q}{p}\right)
\left(\frac{\epsilon p}{q}\right)=-1.
\tag{5}
\]
Indeed, the two factors contributed by \(\epsilon\) have product \(1\), while quadratic reciprocity gives
\((q/p)(p/q)=-1\).

In particular, the two symbols in (5) cannot both be \(1\), and cannot both be \(-1\).

## 2. The topological facts we need

We give the relevant facts, including the distinction between isotropic reduction and orthogonal splitting.

### Branched covers and isotropic reduction

Let \(F\subset B^4\) be connected and locally flat, with one boundary component, and let \(W\) be its double branched cover. If \(b_1(F)=h\), then
\[
H_1(W;\mathbb F_2)=H_3(W;\mathbb F_2)=0,
\qquad
\dim_{\mathbb F_2}H_2(W;\mathbb F_2)=h.
\tag{6}
\]
For example, these identities follow from the mod-\(2\) Smith chain sequence for the branched cover: because the base is a ball, its positive-degree terms identify with the relative homology of \((B^4,F)\).

Suppose its boundary \(Y\) is a rational homology sphere of odd order. It follows that the free intersection lattice of \(W\) has rank \(h\), with a nonsingular integral matrix \(A\) of odd determinant.

Here is the precise boundary-linking statement. With the boundary-linking sign chosen to agree with \(\lambda_{V+V^T}\), there is an isotropic subgroup \(M\subset H_1(Y)\) such that
\[
(M^\perp/M,\ell_Y)\cong\lambda_A,
\qquad
|H_1(Y)|=|\det A|\,|M|^2.
\tag{7}
\]

These statements can be read directly from the long exact sequence of \((W,Y)\). In detail, take \(M\) to be the image of
\(\operatorname{Tor}H_2(W,Y)\) in \(H_1(Y)\). Then:

- \(M^\perp\) is the image of all of \(H_2(W,Y)\);
- on the free quotients, the map
  \(H_2(W)\to H_2(W,Y)\) is the intersection matrix \(A\);
- the induced pairing on \(M^\perp/M\) is \(A^{-1}\bmod\mathbb Z\).

These give (7), as well as isotropy of \(M\). In particular, (1) implies, prime by prime,
\[
\gamma((\ell_Y)_p)=\gamma((\lambda_A)_p).
\tag{8}
\]

For a branched cover of a knot, \(\ell_Y\) in this convention is precisely the form \(\lambda_K\) in the question. One checks the sign using the branched cover of a pushed-in orientable Seifert surface, whose intersection matrix is \(V+V^T\).

### A realization and compression lemma

We will use the following concrete disk-and-band construction.

> **Lemma 2.** Let \(m\ge3\), and let \(A\) be a symmetric integral matrix satisfying
> \[
> A_{11}=0,\qquad
> (A_{11},A_{12},\ldots,A_{1m})\equiv(0,1,0,\ldots,0)\pmod2,
> \]
> and whose submatrix in rows and columns \(3,\ldots,m\) is \(I_{m-2}\bmod2\).
> Then there is a knot \(K\) with \(\lambda_K\cong\lambda_A\) which bounds a smooth nonorientable surface in \(B^4\) with \(b_1=m-2\).

Here are construction details. They also explain why the assertion is about an actual embedded surface.

First make an integral change of basis fixing \(e_1\) so that
\[
A\bmod2=H\oplus I_{m-2},
\qquad
H=\begin{pmatrix}0&1\\1&0\end{pmatrix}.
\tag{9}
\]
Explicitly, put \(\tau=A_{22}\bmod2\), take \(f=e_2+\tau e_3\), and replace each \(e_j\), \(j\ge3\), by
\[
e_j+\bigl(e_j^TAf\bmod2\bigr)e_1.
\]
These vectors together with \(e_1,f\) form an integral unimodular basis and give (9).

Start with the standard disk-and-band surface consisting of one orientable handle and \(m-2\) crosscaps. Its mod-\(2\) intersection matrix is (9). Its first handle curve can be taken to be a zero-framed unknot.

Its integral Gordon–Litherland matrix can now be changed to the desired matrix:

- full twists change diagonal entries by \(2\);
- local clasps between bands change off-diagonal entries by \(2\).

The parities already agree. These operations can be made while keeping the first curve an unknot, and its framing remains zero because \(A_{11}=0\).

The double cover of the pushed-in disk-and-band surface has a handle description with intersection matrix \(A\): the disk lifts to a \(0\)-handle and the bands lift to \(2\)-handles. Hence its boundary form is \(\lambda_A\). Comparing with the orientable Seifert-surface construction fixes the sign as required in the question.

Finally, push the surface into a shallow collar of \(S^3\), and compress its first handle along a zero-framed disk bounded by the specified unknot, putting the disk interior deeper in \(B^4\). The compression is embedded, is nonseparating, and lowers \(b_1\) by \(2\). Its complement still contains the \(m-2\) crosscaps, so the resulting surface is nonorientable. This proves the lemma.

## 3. Explicit matrices

For each allowed prime \(s\), choose nonzero residues \(u_s,w_s\) such that
\[
u_s^2+w_s^2\equiv-1\pmod s.
\tag{10}
\]
Such residues always exist: since \(-1\) is nonsquare, the norm map
\(\mathbb F_{s^2}^{\,*}\to\mathbb F_s^{\,*}\) is the map
\(x+iy\mapsto x^2+y^2\), and it is surjective. A solution of norm \(-1\) cannot have either coordinate zero.

### One prime

For \(S=\{p\}\), use
\[
A_p=
\begin{pmatrix}
0&p^3&0\\
p^3&p&p^2u_p\\
0&p^2u_p&-p^3
\end{pmatrix}.
\tag{11}
\]
Its determinant is \(p^9\).

We verify its linking form. Work over \(\mathbb Z_p\). Pivot first on the middle entry \(p\). The resulting \(2\times2\) block is
\[
\begin{pmatrix}
-p^5&-p^4u_p\\
-p^4u_p&-p^3(1+u_p^2)
\end{pmatrix}.
\]
Its next pivot has exponent \(3\) and square unit coefficient, by (10). The final pivot has exponent \(5\) and square unit coefficient because the determinant, divided by \(p^9\), is a square. Thus the three local diagonal coefficients have exponents \(1,3,5\) and square units. Consequently
\[
\lambda_{A_p}\cong\lambda_{\{p\}}.
\tag{12}
\]

Matrix (11) satisfies Lemma 2 with \(m=3\). Therefore
\[
t(\{p\})\le1,\qquad r(\{p\})\le3.
\tag{13}
\]

### Two primes

Let \(S=\{p,q\}\), put \(n=pq\), and set
\[
C=u_q,\qquad D=u_p.
\]
Choose \(b\) by the Chinese remainder theorem so that
\[
\begin{aligned}
b+qC^2&\equiv p\pmod{p^2},\\
b+pD^2&\equiv q\pmod{q^2}.
\end{aligned}
\tag{14}
\]
Define
\[
A_{p,q}=
\begin{pmatrix}
0&n^3&0&0\\
n^3&b&q^2C&p^2D\\
0&q^2C&-q^3&0\\
0&p^2D&0&-p^3
\end{pmatrix}.
\tag{15}
\]
Expansion using the first row gives
\[
\det A_{p,q}=-n^9.
\tag{16}
\]

At \(p\), eliminate the unit entry \(-q^3\). The remaining block is
\[
\begin{pmatrix}
0&p^3q^3&0\\
p^3q^3&pz&p^2D\\
0&p^2D&-p^3
\end{pmatrix},
\qquad
z=\frac{b+qC^2}{p}\equiv1\pmod p.
\tag{17}
\]
Pivoting on \(pz\), the exponent-\(3\) coefficient has residue
\[
-\left(1+\frac{D^2}{z}\right)
\equiv-(1+D^2)\equiv w_p^2\pmod p.
\]
It is a nonzero square. The determinant of (17), divided by \(p^9\), is \(q^6\), also a square. The exponent-\(5\) coefficient is therefore square as well.

Thus, at \(p\), the discriminant form has exactly the three required constituents. The argument at \(q\) is identical, using the other congruence in (14). There is no torsion at another prime, by (16). Hence
\[
\lambda_{A_{p,q}}\cong\lambda_{\{p,q\}}.
\tag{18}
\]

The matrix is odd, and it satisfies Lemma 2 with \(m=4\). We obtain
\[
t(\{p,q\})\le2,\qquad r(\{p,q\})\le4.
\tag{19}
\]

## 4. Lower bounds for \(t(S)\)

Write
\[
N=\prod_{p\in S}p,
\qquad
|\lambda_S|=N^9.
\]

### A disc is impossible

If \(K\) bounded a disc, its branched cover would have intersection rank zero. Formula (7) would give
\[
N^9=|M|^2,
\]
which is impossible. Thus \(t(S)\ge1\).

Together with (13), this proves
\[
t(\{p\})=1.
\tag{20}
\]

### Two primes cannot have \(b_1=1\)

Suppose \(S=\{p,q\}\) and a permitted surface had \(b_1=1\). Its branched cover has a rank-one intersection matrix \([d]\). From (7),
\[
(pq)^9=|d|\,|M|^2.
\]
In particular,
\[
d=\epsilon pq\,a^2
\tag{21}
\]
for some integer \(a\) and \(\epsilon\in\{1,-1\}\).

At \(p\), formulas (2)–(3) give
\[
\gamma((\lambda_S)_p)=g_p^3=-g_p.
\]
On the other hand, (21) gives
\[
\gamma((\lambda_{[d]})_p)
=
\left(\frac{\epsilon q}{p}\right)g_p.
\]
Equality follows from the isotropic reduction (7), so
\[
\left(\frac{\epsilon q}{p}\right)=-1.
\]
Similarly,
\[
\left(\frac{\epsilon p}{q}\right)=-1.
\]
This contradicts (5). Therefore \(t(\{p,q\})\ge2\), and (19) proves
\[
t(\{p,q\})=2.
\tag{22}
\]

## 5. Lower bounds for \(r(S)\)

By Lemma 1, any decomposition in the definition of \(r(S)\) has \(\mu=0\). Thus a qualifying matrix must present all of \(\lambda_S\).

Each \(p\)-primary group requires three generators. Therefore its presentation matrix has size at least \(3\). With (13),
\[
r(\{p\})=3.
\tag{23}
\]

Now suppose \(S=\{p,q\}\) and that a \(3\times3\) matrix \(Q\) presented \(\lambda_S\). Then
\[
\det Q=\epsilon(pq)^9,\qquad \epsilon\in\{1,-1\}.
\]
Over \(\mathbb Z_p\), its three Jordan entries must have exponents \(1,3,5\) and square unit coefficients. There are no remaining unit entries because the matrix has size three. Consequently
\[
\left(\frac{\det Q/p^9}{p}\right)=1,
\quad\text{that is}\quad
\left(\frac{\epsilon q}{p}\right)=1.
\]
Likewise,
\[
\left(\frac{\epsilon p}{q}\right)=1.
\]
Again this contradicts (5). No size-three matrix exists. Combining this with (19) gives
\[
r(\{p,q\})=4.
\tag{24}
\]

This completes all the upper and lower bounds.

## 6. Executable exact checks

The following code uses exact rational arithmetic for the local diagonalizations. It does **not** infer local linking forms merely from determinants or Smith forms.

For any requested prime or pair, `matrix_single`, `matrix_double`, and `check_matrix` construct and certify the corresponding matrix. The self-test checks every allowed prime at most \(100\), every pair of those primes, and also enumerates small quadratic Gauss sums independently.

```python
from fractions import Fraction as F
from itertools import combinations
from sympy import Matrix, primerange, ZZ
from sympy.matrices.normalforms import smith_normal_form

def legendre(a, p):
    x = pow(int(a) % p, (p - 1)//2, p)
    return 0 if x == 0 else (1 if x == 1 else -1)

def minus_one_squares(p):
    assert p % 8 == 3
    for u in range(1, p):
        a = (-1-u*u) % p
        if a and legendre(a, p) == 1:
            w = pow(a, (p+1)//4, p)
            assert (u*u+w*w+1) % p == 0
            return u, w
    raise AssertionError("Finite-field isotropy failed")

def crt2(a, m, b, n):
    from math import gcd
    assert gcd(m, n) == 1
    return (a + m*((b-a)*pow(m, -1, n) % n)) % (m*n)

def matrix_single(p):
    u, _ = minus_one_squares(p)
    return [
        [0, p**3, 0],
        [p**3, p, p*p*u],
        [0, p*p*u, -p**3]
    ]

def matrix_double(p, q):
    assert p != q
    D, _ = minus_one_squares(p)
    C, _ = minus_one_squares(q)
    n = p*q
    b = crt2(p-q*C*C, p*p, q-p*D*D, q*q)
    assert (b+q*C*C-p) % (p*p) == 0
    assert (b+p*D*D-q) % (q*q) == 0
    return [
        [0, n**3, 0, 0],
        [n**3, b, q*q*C, p*p*D],
        [0, q*q*C, -q**3, 0],
        [0, p*p*D, 0, -p**3]
    ]

def vp(x, p):
    x = F(x)
    if x == 0:
        return float("inf")
    a, b = abs(x.numerator), x.denominator
    v = 0
    while a % p == 0:
        a //= p
        v += 1
    while b % p == 0:
        b //= p
        v -= 1
    return v

def unit_symbol(x, p):
    x = F(x)
    u = x / F(p)**vp(x, p)
    return legendre(u.numerator * pow(u.denominator, -1, p), p)

def local_jordan(A, p):
    """Exact Z_p diagonalization: (exponent, unit square class)."""
    A = [[F(x) for x in row] for row in A]
    out = []
    while A:
        n = len(A)
        v = min(vp(A[i][j], p)
                for i in range(n) for j in range(n))
        assert v != float("inf")
        pivot = next(
            (i for i in range(n) if vp(A[i][i], p) == v), None
        )
        if pivot is None:
            i, j = next(
                (i, j) for i in range(n) for j in range(i+1, n)
                if vp(A[i][j], p) == v
            )
            # Replace e_i by e_i+e_j: unimodular over Z.
            T = [[F(int(a == b)) for b in range(n)]
                 for a in range(n)]
            T[j][i] = 1
            A = [
                [sum(T[a][r]*A[a][b]*T[b][s]
                     for a in range(n) for b in range(n))
                 for s in range(n)]
                for r in range(n)
            ]
            pivot = i
            assert vp(A[i][i], p) == v

        A[0], A[pivot] = A[pivot], A[0]
        for row in A:
            row[0], row[pivot] = row[pivot], row[0]
        d = A[0][0]

        # Every elimination coefficient is p-integral.
        assert all(vp(A[0][i]/d, p) >= 0 for i in range(1, n))
        out.append((vp(d, p), unit_symbol(d, p)))
        A = [
            [A[i][j] - A[i][0]*A[0][j]/d
             for j in range(1, n)]
            for i in range(1, n)
        ]
    return sorted(out)

def check_matrix(A, primes):
    M = Matrix(A)
    n = 1
    for p in primes:
        n *= p
    expected_det = n**9 if len(primes) == 1 else -n**9
    assert M == M.T
    assert int(M.det()) == expected_det
    assert any(A[i][i] % 2 for i in range(len(A)))
    assert A[0][0] == 0

    for p in primes:
        data = local_jordan(A, p)
        assert all(v >= 0 for v, s in data)
        assert [(v, s) for v, s in data if v > 0] == [
            (1, 1), (3, 1), (5, 1)
        ], (primes, data)

    # Verify the integral basis change used in Lemma 2.
    m = len(A)
    e = [Matrix([int(i == j) for i in range(m)])
         for j in range(m)]
    f = e[1] + (A[1][1] % 2)*e[2]
    cols = [e[0], f]
    for j in range(2, m):
        cols.append(e[j] + int((e[j].T*M*f)[0] % 2)*e[0])
    T = Matrix.hstack(*cols)
    H = Matrix.eye(m)
    H[0, 0] = H[1, 1] = 0
    H[0, 1] = H[1, 0] = 1
    assert abs(T.det()) == 1
    assert all(int(x) % 2 == 0 for x in T.T*M*T-H)

    snf = smith_normal_form(M, domain=ZZ)
    smith = sorted(abs(int(snf[i, i])) for i in range(m))
    assert smith == (
        ([1] if len(primes) == 2 else []) + [n, n**3, n**5]
    )
    return M

def self_test(bound=100):
    ps = [int(p) for p in primerange(3, bound+1) if p % 8 == 3]
    single = double = 0

    for p in ps:
        check_matrix(matrix_single(p), [p])
        single += 1
        # Each nonempty selected set has nontrivial Gauss invariant.
        for mask in range(1, 8):
            assert mask.bit_count() % 4 != 0

    for p, q in combinations(ps, 2):
        check_matrix(matrix_double(p, q), [p, q])
        double += 1
        assert legendre(q, p)*legendre(p, q) == -1
        for sign in (-1, 1):
            # Rank-three integral-presentation obstruction.
            assert not (
                legendre(sign*q, p) == legendre(sign*p, q) == 1
            )
            # Rank-one branched-cover obstruction.
            assert not (
                legendre(sign*q, p) == legendre(sign*p, q) == -1
            )

    # Independently enumerate small cyclic Gauss sums.
    import cmath
    import math
    gauss_checks = 0
    for p in ps[:3]:
        g = sum(cmath.exp(2j*math.pi*(x*x % p)/p)
                for x in range(p))/math.sqrt(p)
        assert abs(g*g+1) < 1.e-9
        nonsquare = next(a for a in range(1, p)
                         if legendre(a, p) == -1)
        for k in (1, 2, 3):
            N = p**k
            for a in (1, nonsquare):
                z = sum(
                    cmath.exp(2j*math.pi*((a*x*x) % N)/N)
                    for x in range(N)
                )/math.sqrt(N)
                target = legendre(a, p)*g if k % 2 else 1
                assert abs(z-target) < 1.e-9
                gauss_checks += 1

    print("Enumerated cyclic Gauss sums checked:", gauss_checks)
    print("Primes checked:", ps)
    print("Exact matrix/local-Jordan/Smith checks:",
          single, "singletons and", double, "pairs")
    print("Example for {3}:")
    print(Matrix(matrix_single(3)))
    print("Example for {3,11}:")
    print(Matrix(matrix_double(3, 11)))

if __name__ == "__main__":
    self_test()
```

I ran this code. Its output was:

```text
Enumerated cyclic Gauss sums checked: 18
Primes checked: [3, 11, 19, 43, 59, 67, 83]
Exact matrix/local-Jordan/Smith checks: 7 singletons and 21 pairs
Example for {3}:
Matrix([[0, 27, 0], [27, 3, 9], [0, 9, -27]])
Example for {3,11}:
Matrix([[0, 35937, 0, 0], [35937, 613, 121, 9],
        [0, 121, -1331, 0], [0, 9, 0, -27]])
```

**What is proved:** both minima, for every allowed singleton and pair, with matching constructions and obstructions. **What remains:** nothing for the question as stated.