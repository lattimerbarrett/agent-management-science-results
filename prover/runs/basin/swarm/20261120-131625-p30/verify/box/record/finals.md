# agent_1: last reply

\[
\boxed{D_s=3\cdot 2^{s-1}-2\qquad(s\ge3).}
\]

The lower bound is important here: the usual moment-curve lower bound is **one dimension too small**. We will construct counterexamples using Gaussian measures.

Write
\[
n=2^{s-1},\qquad j=2n-2.
\]
We prove that dimension \(3n-2\) always works, while dimension \(3n-3\) does not.

## 1. The upper bound

We use the following standard vector-bundle form of the mod-\(2\) Euler-class obstruction.

**Zero lemma.** Suppose a continuous map
\[
F:S^d\times S^d\longrightarrow
\mathbb R^j\oplus\mathbb R^j\oplus\mathbb R^j
\]
has the transformation rules
\[
F(-u,v)=(-F_1,F_2,-F_3),\qquad
F(u,-v)=(F_1,-F_2,-F_3).
\]
If
\[
x^jy^j(x+y)^j\ne0
\quad\text{in}\quad
\mathbb F_2[x,y]/(x^{d+1},y^{d+1}),
\tag{1}
\]
then \(F\) has a zero.

Indeed, over \(\mathbb {RP}^d\times\mathbb {RP}^d\), let \(L_1,L_2\) be the two tautological line bundles. The map defines a section of
\[
E=L_1^{\oplus j}\oplus L_2^{\oplus j}
       \oplus(L_1\otimes L_2)^{\oplus j}.
\]
The mod-\(2\) cohomology ring of the base is the ring in (1), with
\(w_1(L_1)=x\) and \(w_1(L_2)=y\). The Whitney product formula gives
\[
w_{3j}(E)=x^jy^j(x+y)^j.
\]
A nowhere-zero section would split off a trivial line bundle and force this top Stiefel–Whitney class to vanish. This proves the lemma.

Now let \(\mu_1,\ldots,\mu_j\) be the given measures on \(\mathbb R^d\). For
\(u=(u_0,u_1,\ldots,u_d)\in S^d\), set
\[
\ell_u(z)=u_0+\sum_{r=1}^d u_rz_r.
\]
Define
\[
\begin{aligned}
F_{1,i}(u,v)&=\int\operatorname{sgn}(\ell_u)\,d\mu_i,\\
F_{2,i}(u,v)&=\int\operatorname{sgn}(\ell_v)\,d\mu_i,\\
F_{3,i}(u,v)&=\int\operatorname{sgn}(\ell_u)
                         \operatorname{sgn}(\ell_v)\,d\mu_i .
\end{aligned}
\]
Absolute continuity and dominated convergence give continuity, including at the two parameters representing constant affine functions. The transformation rules are exactly those of the zero lemma.

At a zero of \(F\), each sign region has measure
\[
\frac14\left(1+\varepsilon F_{1,i}
                 +\eta F_{2,i}+\varepsilon\eta F_{3,i}\right)=\frac14.
\tag{2}
\]

Take \(d=3n-2\). Since \(n\) is a power of two,
\[
(x+y)^{2n-2}
=\prod_{r=1}^{\log_2 n}(x^{2^r}+y^{2^r})
\quad\text{over }\mathbb F_2.
\]
The coefficient of \(x^ny^{n-2}\) is \(1\). Consequently,
\[
x^jy^j(x+y)^j
\]
contains
\[
x^{3n-2}y^{3n-4}
\]
with coefficient \(1\). Both exponents are at most \(d\), so (1) holds.

The resulting affine functions cannot be constant, since they bisect probability measures. Their hyperplanes cannot be parallel or coincident, since then at least one of the four sign regions would be empty, contradicting (2). Thus their complement has exactly four connected components.

Therefore
\[
D_s\le 3n-2.
\tag{3}
\]

## 2. An algebraic construction for the lower bound

We first construct positive-definite quadratic forms having no common orthogonal pair.

**Lemma.** For every even \(n\ge4\), there are \(2n-2\) positive-definite real symmetric \(n\times n\) matrices \(A_r\) such that
\[
x^TA_ry=0\quad\text{for every }r
\quad\Longrightarrow\quad x=0\ \text{or}\ y=0.
\tag{4}
\]

### Proof

Put \(n=2m\), where \(m\ge2\), and identify \(\mathbb R^{2m}\) with the complex polynomials of degree at most \(m-1\), using coefficient vectors.

Let
\[
p(t)=\prod_{r=1}^{2m-2}(t+r).
\]
For each partition of its roots into two sets of size \(m-1\), write
\[
p=u\,v
\]
with \(u,v\) monic. Their coefficient vectors are positive, and \(u,v\) are linearly independent.

Choose a real skew-symmetric matrix \(K\) such that
\[
u^TKv\ne0
\tag{5}
\]
for every such complementary pair. Such a \(K\) exists: for each pair, \(u^TKv=0\) is a proper linear hyperplane in the space of skew-symmetric matrices, because \(u,v\) are independent. A finite union of proper hyperplanes cannot cover that space.

Here is also an explicit integer choice, useful for computation. All factor coefficients are at most
\[
C=(2m-1)!.
\]
Enumerate the pairs \(a<b\) by distinct exponents \(e(a,b)=0,1,\ldots\), choose
\[
T=4C^2+2,\qquad K_{ab}=T^{e(a,b)},\quad K_{ba}=-K_{ab}.
\]
Then \(u^TKv\) is a nonzero integer polynomial evaluated at \(T\), with coefficients bounded in absolute value by \(2C^2\). Its leading term dominates all the others, proving (5).

For complex coefficient vectors \(f,g\), consider the following real bilinear forms:

* the real and imaginary parts of all \(2m-2\) coefficients of
  \(fg\bmod p\);
* \(\operatorname{Re}(f^*g)\);
* \(\operatorname{Re}(i f^*Kg)\).

There are
\[
2(2m-2)+2=4m-2=2n-2
\]
forms. They are symmetric as real bilinear forms; for the last one, this follows because \(iK\) is Hermitian.

We claim that they have no common zero with \(f,g\ne0\).

If all remainder coefficients vanish, then \(p\mid fg\). The degree bounds force
\[
fg=c\,p,\qquad
f=\alpha u,\quad g=\beta v,
\]
for one of the complementary monic factor pairs above and nonzero complex numbers \(\alpha,\beta\).

Set \(\gamma=\overline\alpha\beta\). The last two equations become
\[
(u^Tv)\operatorname{Re}\gamma=0,\qquad
-(u^TKv)\operatorname{Im}\gamma=0.
\]
Here \(u^Tv>0\), and (5) holds. Thus \(\gamma=0\), a contradiction.

Write these real symmetric forms as \(x^TS_ry\). One of the \(S_r\) is \(I\). Keep that matrix, and replace every other \(S_r\) by
\[
A_r=S_r+\lambda I
\]
with \(\lambda\) sufficiently large to make it positive definite. A common zero of the new forms has \(x^Ty=0\), and hence is also a common zero of all the original forms. This proves (4). ∎

## 3. Gaussian counterexamples in dimension \(3n-3\)

Apply the lemma, with
\[
j=2n-2,\qquad d_0=(j-1)+n=3n-3.
\]

Decompose
\[
\mathbb R^{d_0}=\mathbb R^{j-1}\oplus\mathbb R^n.
\]
Choose \(j\) Gaussian probability measures with respective means
\[
0,e_1,\ldots,e_{j-1}
\]
and covariance matrices
\[
\Sigma_r=
\begin{pmatrix}
I_{j-1}&0\\
0&A_r
\end{pmatrix}.
\]
All these measures have everywhere-positive Lebesgue densities.

Suppose two hyperplanes quarter every one of these measures. Each hyperplane must bisect every measure. A hyperplane bisects a nondegenerate Gaussian exactly when it contains its mean. Thus both hyperplanes contain
\[
\mathbb R^{j-1}\oplus\{0\}.
\]
Their equations therefore have the form
\[
x^Tz=0,\qquad y^Tz=0
\]
for nonzero \(x,y\in\mathbb R^n\).

For the \(r\)-th Gaussian, the two defining linear functions are jointly centered Gaussian, with covariance
\[
x^TA_ry.
\]
For centered jointly Gaussian variables of correlation \(\rho\),
\[
\Pr(X>0,Y>0)=\frac14+\frac{\arcsin\rho}{2\pi}.
\tag{6}
\]
This follows, for example, by representing them as two linear functions of a rotationally invariant planar Gaussian and measuring the corresponding angular sector. In particular, quartering forces their covariance to be zero.

We obtain
\[
x^TA_ry=0\qquad(r=1,\ldots,j),
\]
contradicting (4). So dimension \(3n-3\) does not work.

Finally, the desired property is monotone in dimension: push measures forward under a coordinate projection, find the hyperplanes in the smaller space, and lift them. Absolute continuity of the pushforwards follows from Fubini's theorem. Thus failure in dimension \(3n-3\) rules out every smaller dimension as well, giving
\[
D_s\ge3n-2.
\tag{7}
\]
Combining (3) and (7) proves the answer.

## 4. Exact computational checks

The following Python uses integer and symbolic arithmetic, not numerical sampling. It constructs the matrices and checks:

* the polynomial-remainder identities defining every bilinear form;
* positive definiteness by strict diagonal dominance;
* the change from the original forms to positive-definite forms;
* all complementary factor pairs for the tested cases;
* the affine-bisector constraints on the Gaussian means;
* the complete surviving mod-\(2\) obstruction polynomial.

The argument above proves all parameters; the computations give exact certificates for \(s=3,4,5\).

```python
from math import factorial, comb
from itertools import combinations
import sympy as S


def mul(a, b):
    c = [0] * (len(a) + len(b) - 1)
    for i, x in enumerate(a):
        for k, y in enumerate(b):
            c[i + k] += x * y
    return c


def factor_vector(roots):
    a = [1]
    for r in roots:
        a = mul(a, [r, 1])
    return a


def check(s, exhaustive=True):
    assert s >= 3
    m = 2**(s - 2)
    n, j = 2*m, 4*m - 2
    d0, d = 6*m - 3, 6*m - 2

    roots = tuple(range(1, 2*m - 1))
    p = factor_vector(roots)
    C = factorial(2*m - 1)
    T = 4*C*C + 2

    K = S.zeros(m)
    exponent = 0
    for a in range(m):
        for b in range(a + 1, m):
            K[a, b] = T**exponent
            K[b, a] = -T**exponent
            exponent += 1
    assert K.T == -K and T - 1 > 2*C*C

    # R[k] gives coefficient k of f*g modulo p.
    R = []
    for k in range(2*m - 2):
        R.append(S.Matrix(
            m, m,
            lambda a, b:
                int(a + b == k) if a + b < 2*m - 2 else -p[k]
        ))

    t = S.Symbol("t")
    P = sum(c*t**a for a, c in enumerate(p))

    # Checking on basis monomials certifies the full bilinear identity.
    for a in range(m):
        for b in range(m):
            rhs = sum(R[k][a, b]*t**k for k in range(2*m - 2))
            assert S.rem(t**(a + b) - rhs, P, t) == 0

    Z = S.zeros(m)
    B = []
    for r in R:
        B.extend([
            S.BlockMatrix([[r, Z], [Z, -r]]).as_explicit(),
            S.BlockMatrix([[Z, r], [r, Z]]).as_explicit()
        ])

    I = S.eye(n)
    B.extend([
        I,
        S.BlockMatrix([[Z, -K], [K, Z]]).as_explicit()
    ])
    assert len(B) == j
    assert all(b == b.T for b in B)

    identity_index = j - 2
    M = 1 + max(
        sum(abs(b[a, c]) for c in range(n))
        for b in B for a in range(n)
    )
    A = [
        I if k == identity_index else M*I + b
        for k, b in enumerate(B)
    ]

    for k, a in enumerate(A):
        assert a == a.T
        # Positive diagonal + strict diagonal dominance => positive definite.
        assert all(
            a[r, r] >
            sum(abs(a[r, c]) for c in range(n) if c != r)
            for r in range(n)
        )
        if k == identity_index:
            assert a == I
        else:
            assert a - M*A[identity_index] == B[k]

    # Bisector equations for means 0,e_1,...,e_{j-1}.
    # Columns: offset, first j-1 normal entries, final n entries.
    E = S.zeros(j, d0 + 1)
    for r in range(j):
        E[r, 0] = -1
    for r in range(1, j):
        E[r, r] = 1
    assert E[:, :j].det() != 0
    assert E[:, j:] == S.zeros(j, n)

    checked = 0
    if exhaustive:
        for subset in combinations(roots, m - 1):
            # One representative per unordered factor pair.
            if 1 not in subset:
                continue
            complement = tuple(r for r in roots if r not in subset)
            u = S.Matrix(factor_vector(subset))
            v = S.Matrix(factor_vector(complement))

            assert mul(list(u), list(v)) == p
            assert all(0 < a <= C for a in list(u) + list(v))
            assert u.dot(v) > 0

            wedge = [
                u[a]*v[b] - u[b]*v[a]
                for a in range(m) for b in range(a + 1, m)
            ]
            assert any(wedge)
            assert max(map(abs, wedge)) <= 2*C*C
            assert (u.T*K*v)[0] != 0
            assert all((u.T*r*v)[0] == 0 for r in R)

            # Determinant of the two equations on Re(gamma), Im(gamma).
            assert u.dot(v) * (u.T*K*v)[0] != 0
            checked += 1

        assert checked == comb(2*m - 2, m - 1)//2

    # Compute all terms of x^j*y^j*(x+y)^j modulo 2,
    # then quotient by x^(d+1), y^(d+1).
    monomials = {
        (j + k, 2*j - k)
        for k in range(j + 1) if comb(j, k) % 2
    }
    surviving = {
        (a, b) for a, b in monomials if a <= d and b <= d
    }
    assert (3*n - 2, 3*n - 4) in surviving

    print(
        f"s={s}: lower counterexample dimension {d0}; upper {d}; "
        f"factor pairs certified {checked}; "
        f"surviving monomials {sorted(surviving)}"
    )


if __name__ == "__main__":
    for s in (3, 4, 5):
        check(s)
```

Actual output:

```text
s=3: lower counterexample dimension 9; upper 10; factor pairs certified 1; surviving monomials [(8, 10), (10, 8)]
s=4: lower counterexample dimension 21; upper 22; factor pairs certified 10; surviving monomials [(20, 22), (22, 20)]
s=5: lower counterexample dimension 45; upper 46; factor pairs certified 1716; surviving monomials [(44, 46), (46, 44)]
```

Thus both halves are established: universal equipartition in dimension \(3\cdot2^{s-1}-2\), and absolutely continuous Gaussian counterexamples one dimension below. **Nothing remains to determine \(D_s\).**