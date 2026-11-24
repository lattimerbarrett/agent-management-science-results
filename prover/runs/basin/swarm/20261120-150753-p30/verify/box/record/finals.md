# agent_1: last reply

\[
\boxed{D_s=3\cdot 2^{s-1}-2\qquad(s\geq3).}
\]

The lower bound is the subtler half: the usual parameter-counting lower bound is one dimension too small. We will construct Gaussian counterexamples in that smaller dimension.

## 1. The upper bound

We first recall a standard cohomological form of the product Borsuk–Ulam argument, including the details needed here.

### Equipartition criterion

For \(j\) absolutely continuous probability measures on \(\mathbb R^d\), two hyperplanes simultaneously equipartition all of them whenever
\[
x^j y^j(x+y)^j\ne0
\quad\text{in}\quad
\mathbb F_2[x,y]/(x^{d+1},y^{d+1}).
\tag{1}
\]

To prove this, parametrize oriented affine hyperplanes by
\[
a=(a_0,\ldots,a_d)\in S^d,\qquad
\ell_a(z)=a_0+\sum_{r=1}^d a_rz_r.
\]
The two poles represent constant positive and negative functions. Write
\(\epsilon_a(z)=\operatorname{sgn}\ell_a(z)\). For each measure \(\mu_i\), define
\[
f_i(a,b)=\int\epsilon_a\,d\mu_i,\quad
g_i(a,b)=\int\epsilon_b\,d\mu_i,\quad
h_i(a,b)=\int\epsilon_a\epsilon_b\,d\mu_i.
\]
These functions are continuous by dominated convergence, including at the poles.

Under \(a\mapsto-a\), the functions \(f_i,h_i\) change sign; under \(b\mapsto-b\), the functions \(g_i,h_i\) change sign. Consequently, together they define a section of
\[
E=L_x^{\oplus j}\oplus L_y^{\oplus j}
       \oplus(L_x\otimes L_y)^{\oplus j}
\]
over \(\mathbb RP^d\times\mathbb RP^d\), where \(L_x,L_y\) are the two tautological line bundles.

Here are the standard characteristic-class facts used in this argument:
\[
H^*(\mathbb RP^d\times\mathbb RP^d;\mathbb F_2)
=\mathbb F_2[x,y]/(x^{d+1},y^{d+1}),
\]
\[
w_1(L_x)=x,\quad w_1(L_y)=y,\quad
w_1(L_x\otimes L_y)=x+y.
\]
The Whitney product formula therefore gives
\[
w_{3j}(E)=x^jy^j(x+y)^j.
\]
A nowhere-zero section would split off a trivial line bundle, forcing this top Stiefel–Whitney class to vanish. Thus (1) forces a zero of the section.

At such a zero, the mass of the sign region \((\alpha,\beta)\in\{\pm1\}^2\) is
\[
\frac14\left(1+\alpha f_i+\beta g_i+\alpha\beta h_i\right)=\frac14.
\]
Neither parameter is a pole. All four sign regions are nonempty and convex, so they are exactly the four connected components required in the question. This proves the criterion.

### Applying the criterion

Put
\[
n=2^{s-1},\qquad j=2n-2,\qquad d=3n-2.
\]
In
\[
x^jy^j(x+y)^j
=\sum_k\binom jk x^{j+k}y^{2j-k},
\]
take \(k=n-2\). The resulting monomial is
\[
x^{3n-4}y^{3n-2}=x^{d-2}y^d.
\]
Its coefficient is odd. Indeed, over \(\mathbb F_2\),
\[
(1+t)^{2^s-2}=\prod_{r=1}^{s-1}(1+t^{2^r}),
\]
and \(n-2=2+4+\cdots+2^{s-2}\) occurs exactly once.

Thus this monomial survives in the quotient ring, proving
\[
D_s\le 3n-2.
\tag{2}
\]

## 2. Positive-definite bilinear forms with no common orthogonal pair

The following explicit construction supplies the stronger lower bound.

### Lemma

For every even \(n\ge4\), there exist \(2n-2\) real symmetric positive-definite \(n\times n\) matrices
\[
A_0,\ldots,A_{2n-3}
\]
such that
\[
u^{\mathsf T}A_i v=0\quad\text{for every }i
\quad\Longrightarrow\quad u=0\text{ or }v=0.
\tag{3}
\]

### Proof

Write \(n=2m\), where \(m\ge2\), and identify \(\mathbb R^n\) with the real vector space
\[
V=\mathbb C[t]_{\le m-1}.
\]

Choose the following \(2m-2\) distinct positive integers:
\[
R=\{3\}\cup\{\,4r+1:0\le r\le2m-4\,\},
\]
and put
\[
P(t)=\prod_{r\in R}(t+r).
\]
All roots are simple, and all coefficients of \(P\) are positive.

We need one useful property of its complementary factors. If
\[
P=FG,\qquad \deg F=\deg G=m-1,
\]
with \(F,G\) monic, then
\[
F(0)G(1)-F(1)G(0)\ne0.
\tag{4}
\]
To see this, let \(v_2\) denote the exponent of \(2\) in a nonzero rational number. Each \(4r+1\) contributes \(1\) to
\(v_2(P(1)/P(0))\), while the exceptional integer \(3\) contributes \(2\). Hence
\[
v_2\!\left(\frac{P(1)}{P(0)}\right)
=(2m-3)+2=2m-1,
\tag{5}
\]
which is odd. Equality in the negation of (4) would give
\[
\frac{F(1)}{F(0)}=\frac{G(1)}{G(0)},
\]
making (5) twice an integer, a contradiction.

We now define \(4m-2=2n-2\) real symmetric bilinear forms on \(V\):

* the coefficient inner product
  \[
  b_0(U,V)=\operatorname{Re}\sum_{k=0}^{m-1}\overline{u_k}v_k;
  \]
* the form
  \[
  b_1(U,V)=
  \operatorname{Re}\!\left(
    i\bigl(\overline{U(0)}V(1)-\overline{U(1)}V(0)\bigr)
  \right);
  \]
* the real and imaginary parts of each of the \(2m-2\) coefficients of the remainder of \(UV\) modulo \(P\).

The last forms are symmetric because polynomial multiplication is commutative. The form \(b_1\) is also real symmetric: its complex matrix is \(iK\), where \(K\) is real skew-symmetric.

We claim these forms have no common zero on a pair of nonzero vectors. Suppose otherwise. The remainder conditions give
\[
UV=cP.
\]
Since \(U,V\ne0\), we have \(c\ne0\). Degree considerations and unique factorization give
\[
U=aF,\qquad V=bG,
\]
where \(a,b\in\mathbb C\setminus\{0\}\), and \(F,G\) are complementary monic degree-\((m-1)\) factors of \(P\).

Their coefficients are positive, so
\[
C=\sum_k F_kG_k>0.
\]
Thus \(b_0(U,V)=0\) gives
\[
\operatorname{Re}(\overline ab)=0.
\]
By (4), the equation \(b_1(U,V)=0\) gives
\[
\operatorname{Im}(\overline ab)=0.
\]
This contradicts \(a,b\ne0\).

Finally, \(b_0\) is positive definite. Replace every other form \(b\) by
\[
b+M b_0
\]
with \(M\) sufficiently large that the replacement is positive definite. Keep \(b_0\) itself. Common vanishing is unchanged, since the equation \(b_0(U,V)=0\) is retained. The resulting matrices satisfy (3). ∎

## 3. Gaussian counterexamples

Take
\[
n=2^{s-1},\qquad j=2n-2,\qquad d_0=j+n-1=3n-3.
\]
Use the matrices from the lemma, indexed \(A_0,\ldots,A_{j-1}\).

Decompose
\[
\mathbb R^{d_0}=\mathbb R^{j-1}\oplus\mathbb R^n.
\]
Choose Gaussian probability measures \(\mu_0,\ldots,\mu_{j-1}\) with means
\[
c_0=0,\qquad c_r=(e_r,0)\quad(1\le r\le j-1)
\]
and covariance matrices
\[
\Sigma_i=
\begin{pmatrix}
I_{j-1}&0\\
0&A_i
\end{pmatrix}.
\tag{6}
\]
These are nondegenerate Gaussians, hence absolutely continuous.

Suppose two affine hyperplanes equipartition all these measures. Each hyperplane must bisect every measure.

A hyperplane bisects a nondegenerate Gaussian exactly when it passes through its mean: its defining affine functional is a one-dimensional normal random variable, whose unique median is its mean. Consequently, each of our hyperplanes contains all the \(c_i\). Its equation therefore has the form
\[
u^{\mathsf T}z=0,\qquad u\in\mathbb R^n\setminus\{0\}.
\]
Write the two normals as \(u,v\).

For centered jointly normal random variables \(Y,Z\) of correlation \(\rho\),
\[
\Pr(Y>0,Z>0)=\frac14+\frac{\arcsin\rho}{2\pi}.
\tag{7}
\]
For example, (7) follows by expressing \(Y,Z\) as two linear functionals of an isotropic planar Gaussian and measuring the angle of the intersection of their positive halfplanes. Thus all four sign probabilities equal \(1/4\) only if \(\rho=0\).

Applied to (6), this implies
\[
u^{\mathsf T}A_i v=0\qquad(0\le i\le j-1).
\]
The lemma says that \(u=0\) or \(v=0\), a contradiction.

Hence the desired property fails in dimension \(d_0=3n-3\).

The property is monotone in dimension: project measures in a larger-dimensional space onto a smaller-dimensional space, apply the property there, and lift the hyperplanes. The projected measures remain absolutely continuous by Fubini’s theorem. Therefore failure in dimension \(d_0\) implies
\[
D_s\ge d_0+1=3n-2.
\tag{8}
\]
Together, (2) and (8) prove the formula.

## 4. Exact Python checks

The following code constructs the matrices exactly, checks positive definiteness by strict diagonal dominance, checks the polynomial-remainder identities, and exhaustively checks all complementary factorizations for \(s=3,4,5\). It also constructs the Gaussian means and covariances.

These finite computations verify the explicit construction; the arguments above establish it for every \(s\).

```python
import itertools
from math import comb
import sympy as S


def v2(a):
    a = int(a)
    result = 0
    while a % 2 == 0:
        a //= 2
        result += 1
    return result


def matrices(s):
    assert s >= 3
    n = 2**(s - 1)
    m = n // 2
    j = 2*n - 2
    t = S.Symbol("t")

    roots = [3] + [4*i + 1 for i in range(2*m - 3)]
    P = S.Poly(S.prod(t + r for r in roots), t)

    assert len(set(roots)) == 2*m - 2
    assert P.degree() == 2*m - 2
    assert v2(P.eval(1)) - v2(P.eval(0)) == 2*m - 1

    Z = S.zeros(m)
    B, Ts = [], []

    # T_ell gives coefficient ell of UV modulo P.
    for ell in range(2*m - 2):
        T = S.Matrix(m, m, lambda a, b: int(a + b == ell))
        T[m-1, m-1] -= P.nth(ell)
        Ts.append(T)

        # Real and imaginary parts of the complex bilinear form.
        B.append(S.diag(T, -T))
        B.append(Z.row_join(T).col_join(T.row_join(Z)))

    e0 = S.zeros(m, 1)
    e0[0] = 1
    e1 = S.ones(m, 1)
    K = e0*e1.T - e1*e0.T
    B.append(Z.row_join(-K).col_join(K.row_join(Z)))

    I = S.eye(n)
    A = [I]
    for b in B:
        assert b == b.T
        shift = 1 + max(
            sum(abs(b[r, c]) for c in range(n))
            for r in range(n)
        )
        a = b + shift*I

        # Symmetric strict diagonal dominance with positive diagonal
        # proves positive definiteness.
        assert all(
            a[r, r] > sum(
                abs(a[r, c]) for c in range(n) if c != r
            )
            for r in range(n)
        )
        A.append(a)

    assert len(A) == j

    # Check all polynomial-remainder identities on a bilinear basis.
    for a in range(m):
        for b in range(m):
            remainder = S.rem(t**(a+b), P.as_expr(), t)
            reconstructed = sum(
                Ts[ell][a, b]*t**ell
                for ell in range(2*m - 2)
            )
            assert S.expand(remainder - reconstructed) == 0

    return roots, P, K, A


def check_factors(roots, P, K):
    m = K.rows
    t = P.gen
    count = 0

    for indices in itertools.combinations(range(len(roots)), m-1):
        # One representative of each complementary pair.
        if 0 not in indices:
            continue
        indices = set(indices)

        f = S.Poly(S.prod(t + roots[i] for i in indices), t)
        g = S.Poly(S.prod(
            t + roots[i]
            for i in range(len(roots)) if i not in indices
        ), t)

        u = S.Matrix([f.nth(i) for i in range(m)])
        v = S.Matrix([g.nth(i) for i in range(m)])

        assert f*g == P
        assert (u.T*v)[0] > 0

        w = (u.T*K*v)[0]
        assert w == f.eval(0)*g.eval(1) - f.eval(1)*g.eval(0)
        assert w != 0
        count += 1

    assert count == comb(2*m - 2, m-1)//2
    return count


def check_upper(s):
    n = 2**(s-1)
    j, d, k = 2*n - 2, 3*n - 2, n - 2
    assert j + k == d - 2
    assert 2*j - k == d

    # Binary criterion for an odd binomial coefficient.
    assert (k & ~j) == 0
    if s <= 12:
        assert comb(j, k) % 2 == 1
    return d


for s in range(3, 21):
    check_upper(s)
print("Upper-bound coefficient checked for s=3,...,20.")

for s in (3, 4, 5):
    roots, P, K, A = matrices(s)
    pairs = check_factors(roots, P, K)
    n, j = A[0].rows, len(A)
    print(
        f"s={s}: n={n}, {j} SPD matrices; "
        f"{pairs} complementary factor pairs checked; "
        f"D={check_upper(s)}"
    )

    # Construct and check the Gaussian data.
    d0 = j + n - 1
    means = [S.zeros(d0, 1)]
    for k in range(j-1):
        c = S.zeros(d0, 1)
        c[k] = 1
        means.append(c)

    assert S.Matrix.hstack(*means[1:]).rank() == j-1

    for a in A:
        covariance = S.diag(S.eye(j-1), a)
        assert covariance.shape == (d0, d0)
        assert covariance[j-1:, j-1:] == a
        assert all(
            covariance[r, r] > sum(
                abs(covariance[r, c])
                for c in range(d0) if c != r
            )
            for r in range(d0)
        )

print(
    "Gaussian counterexample data checked exactly "
    "in dimensions 9, 21, 45."
)
```

Actual output:
```text
Upper-bound coefficient checked for s=3,...,20.
s=3: n=4, 6 SPD matrices; 1 complementary factor pairs checked; D=10
s=4: n=8, 14 SPD matrices; 10 complementary factor pairs checked; D=22
s=5: n=16, 30 SPD matrices; 1716 complementary factor pairs checked; D=46
Gaussian counterexample data checked exactly in dimensions 9, 21, 45.
```

Thus both halves are proved: equipartitions always exist in dimension \(3\cdot2^{s-1}-2\), and explicit absolutely continuous Gaussian counterexamples exist one dimension below. **Nothing remains open in the stated problem.**