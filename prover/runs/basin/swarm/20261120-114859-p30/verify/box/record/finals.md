# agent_1: last reply

\[
\boxed{D_s=3\cdot 2^{s-1}-2\qquad(s\ge3).}
\]

The important point is that the usual dimension-counting lower bound is **not sharp** here. We will construct Gaussian counterexamples in dimension \(3\cdot2^{s-1}-3\), and then prove the matching universal upper bound.

Put
\[
n=2^{s-1},\qquad j=2n-2.
\]

## 1. The upper bound: \(D_s\le 3n-2\)

We first recall the bundle version of the product Borsuk–Ulam argument.

### A zero-forcing lemma

Suppose a continuous map
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

Indeed, quotienting by the two antipodal actions makes \(F\) a section of
\[
E=L_x^{\oplus j}\oplus L_y^{\oplus j}
  \oplus(L_x\otimes L_y)^{\oplus j}
\]
over \(\mathbb {RP}^d\times\mathbb {RP}^d\). Here \(L_x,L_y\) are the tautological line bundles from the two factors. Its top Stiefel–Whitney class is
\[
w_{3j}(E)=x^jy^j(x+y)^j.
\]
A nowhere-zero section would split off a trivial line bundle, forcing this class to vanish. This proves the lemma.

### Applying the lemma to measures

An element \(u=(a,b)\in S^d\subset\mathbb R^d\oplus\mathbb R\) represents the signed affine function
\[
\ell_u(z)=a\cdot z+b.
\]
The two points with \(a=0\) are allowed temporarily as constant signed functions.

Given the \(j\) measures \(\mu_i\), define
\[
\begin{aligned}
F_{1,i}(u,v)&=\int \operatorname{sgn}\ell_u\,d\mu_i,\\
F_{2,i}(u,v)&=\int \operatorname{sgn}\ell_v\,d\mu_i,\\
F_{3,i}(u,v)&=\int
 \operatorname{sgn}\ell_u\,\operatorname{sgn}\ell_v\,d\mu_i .
\end{aligned}
\tag{2}
\]
These functions are continuous. For proper hyperplanes this follows from absolute continuity and dominated convergence; continuity at the constant signed functions follows from the same argument. They have exactly the transformation rules in the lemma.

At a common zero, each signed quadrant has measure
\[
\frac14\int
 (1+\varepsilon\operatorname{sgn}\ell_u)
 (1+\delta\operatorname{sgn}\ell_v)\,d\mu_i
=\frac14.
\tag{3}
\]
The hyperplanes must be proper and nonparallel: otherwise four signed quadrants could not all have positive measure. Their complement therefore has exactly four connected components.

Take \(d=3n-2\). Since \(n\) is a power of two, over \(\mathbb F_2\),
\[
(X+Y)^{2n-2}
=\sum_{r=0}^{n-1}X^{2r}Y^{2n-2-2r}.
\tag{4}
\]
In particular, the coefficient of \(X^{n-2}Y^n\) is \(1\). Consequently,
\[
x^jy^j(x+y)^j
\]
contains the nonzero surviving monomial
\[
x^{j+n-2}y^{j+n}
=x^{3n-4}y^{3n-2}
\]
in the ring in (1). The zero-forcing lemma applies, proving
\[
D_s\le3n-2.
\tag{5}
\]

## 2. A quadratic-form construction

The lower bound rests on the following explicit lemma.

### Lemma

For every even \(n\ge4\), there are \(2n-2\) real symmetric positive-definite \(n\times n\) matrices
\[
A_0,\ldots,A_{2n-3}
\]
such that
\[
u^{T}A_i v=0\quad\text{for every }i
\quad\Longrightarrow\quad u=0\ \text{or}\ v=0.
\tag{6}
\]

### Proof

Write \(n=2k\), identify \(\mathbb R^n\) with \(\mathbb C^k\), and associate to \(z\in\mathbb C^k\) the polynomial
\[
P_z(t)=z_0+z_1t+\cdots+z_{k-1}t^{k-1}.
\]

Choose the following \(2k-2\) distinct positive real numbers:
\[
R=\{1,2,4,6,\ldots,4k-6\}.
\tag{7}
\]
Their sum is odd.

Let \(K\) be the real skew-symmetric \(k\times k\) matrix whose only nonzero entries are
\[
K_{k-2,k-1}=1,\qquad K_{k-1,k-2}=-1.
\]
Consider these \(4k-2=2n-2\) real symmetric bilinear forms:
\[
\begin{aligned}
B_0(z,w)&=\operatorname{Re}(z^*w),\\
B_1(z,w)&=\operatorname{Re}(z^*iKw),\\
B_{r,\mathrm{Re}}(z,w)&=\operatorname{Re}\bigl(P_z(r)P_w(r)\bigr),\\
B_{r,\mathrm{Im}}(z,w)&=\operatorname{Im}\bigl(P_z(r)P_w(r)\bigr),
\qquad r\in R.
\end{aligned}
\tag{8}
\]
They are symmetric over \(\mathbb R\); in particular \(iK\) is Hermitian.

We claim that these forms have no common zero with \(z,w\ne0\).

Suppose otherwise. The evaluation forms imply that \(P_zP_w\) vanishes at all \(2k-2\) points of \(R\). Its degree is at most \(2k-2\), so necessarily
\[
P_z=\alpha p_S,\qquad P_w=\beta p_T,
\tag{9}
\]
where \(S,T\) partition \(R\), both have size \(k-1\),
\[
p_S(t)=\prod_{r\in S}(t-r),\qquad
p_T(t)=\prod_{r\in T}(t-r),
\]
and \(\alpha,\beta\ne0\).

Let \(a,b\) be the real coefficient vectors of \(p_S,p_T\), in ascending order. Because all their roots are positive, corresponding coefficients have the same alternating signs. Thus
\[
D=a^Tb>0.
\tag{10}
\]
Their leading coefficients are \(1\), and their next coefficients are minus their root sums. Hence
\[
\kappa=a^TKb=\sum_{r\in T}r-\sum_{r\in S}r.
\tag{11}
\]
This integer is odd, because the total root sum is odd. In particular, \(\kappa\ne0\).

Now the first two forms in (8) give
\[
0=D\operatorname{Re}(\bar\alpha\beta),\qquad
0=-\kappa\operatorname{Im}(\bar\alpha\beta).
\]
Therefore \(\bar\alpha\beta=0\), a contradiction.

Let \(M_0=I,M_1,\ldots,M_{2n-3}\) be the real symmetric matrices of these bilinear forms. For \(i\ge1\), put
\[
\lambda_i=1+\max_a\sum_b |(M_i)_{ab}|,\qquad
A_i=M_i+\lambda_i I,
\]
and put \(A_0=I\). Each \(A_i\) is positive definite, for example by strict diagonal dominance.

If all \(u^TA_iv\) vanish, \(A_0=I\) first gives \(u^Tv=0\), after which all \(u^TM_iv\) vanish. The claim just proved establishes (6). ∎

## 3. The lower bound: Gaussian counterexamples in dimension \(3n-3\)

Let
\[
d_0=3n-3=(j-1)+n,
\]
and decompose
\[
\mathbb R^{d_0}=\mathbb R^{j-1}\oplus\mathbb R^n.
\]

Use the \(j\) matrices from the lemma. Define \(j\) nondegenerate Gaussian probability measures with means
\[
m_0=0,\qquad m_i=(e_i,0)\quad(1\le i\le j-1)
\tag{12}
\]
and covariance matrices
\[
\Sigma_i=
\begin{pmatrix}
I_{j-1}&0\\
0&A_i
\end{pmatrix}.
\tag{13}
\]
These measures have smooth, everywhere-positive densities.

Suppose two affine hyperplanes quarter every one of them.

A hyperplane bisects a nondegenerate Gaussian exactly when it passes through its mean. Thus both hyperplanes must pass through every point in (12). Their offsets are zero, and their normals have the form
\[
(0,u),\qquad(0,v),\qquad u,v\in\mathbb R^n\setminus\{0\}.
\tag{14}
\]

For the \(i\)-th Gaussian, the two defining linear functions are centered jointly Gaussian, with covariance
\[
u^TA_iv.
\]
Two centered Gaussian variables put probability \(1/4\) in every signed quadrant exactly when their covariance is zero. Indeed, if their correlation is \(\rho\),
\[
\Pr(X>0,Y>0)=\frac14+\frac{\arcsin\rho}{2\pi}.
\tag{15}
\]
This follows by whitening to a rotationally invariant planar Gaussian and measuring the corresponding angular sector.

Consequently,
\[
u^TA_iv=0\qquad\text{for all }i,
\]
contradicting the lemma.

So the required property fails in dimension \(3n-3\).

Finally, the property is monotone upward in dimension: project measures onto a lower-dimensional coordinate space, equipartition their absolutely continuous pushforwards, and pull the hyperplanes back. Therefore failure in dimension \(3n-3\) rules out every smaller dimension as well. We have proved
\[
D_s\ge3n-2.
\tag{16}
\]

Combining (5) and (16) proves the asserted formula.

## 4. Exact computational checks

The following runnable Python uses only exact integer/rational arithmetic through SymPy. It checks:

- **every complementary root split** in the selected instances;
- positivity of \(a^Tb\) and the odd nonzero value of \(a^TKb\);
- all real quadratic-form matrices;
- positive definiteness of every Gaussian covariance by strict diagonal dominance;
- the common-bisector normal space;
- the entire truncated mod-\(2\) Euler polynomial.

The general proof above handles all \(s\); these computations verify the finite certificates for \(s=3,4,5\), not merely numerical samples.

```python
from itertools import combinations
from math import comb
import sympy as sp


def coefficients(roots):
    """Coefficients of prod(t-r), ascending powers, exactly."""
    a = [1]
    for r in roots:
        b = [0] * (len(a) + 1)
        for i, x in enumerate(a):
            b[i] -= r * x
            b[i + 1] += x
        a = b
    return sp.Matrix(a)


def check(s):
    assert s >= 3
    n = 2 ** (s - 1)
    k = n // 2
    j = 2 * n - 2
    d0 = 3 * n - 3
    d = d0 + 1

    roots = [1] + [2 * r for r in range(1, 2 * k - 2)]
    assert len(roots) == len(set(roots)) == 2 * k - 2
    assert all(r > 0 for r in roots)
    assert sum(roots) % 2 == 1

    K = sp.zeros(k)
    K[k - 2, k - 1] = 1
    K[k - 1, k - 2] = -1

    # Exhaust all complementary root splits, modulo swapping.
    splits = 0
    for S in combinations(roots, k - 1):
        if 1 not in S:
            continue
        T = set(roots) - set(S)
        a, b = coefficients(S), coefficients(T)

        assert a[-1] == b[-1] == 1
        assert all(a[i] * b[i] > 0 for i in range(k))
        assert (a.T * b)[0] > 0

        wedge = (a.T * K * b)[0]
        assert wedge == sum(T) - sum(S)
        assert wedge % 2 == 1
        splits += 1

    assert splits == comb(2 * k - 2, k - 1) // 2

    # Real coordinates are z=x+i*y.
    Z, I = sp.zeros(k), sp.eye(n)
    M = [I, sp.BlockMatrix([[Z, -K], [K, Z]]).as_explicit()]

    for r in roots:
        v = sp.Matrix([r ** a for a in range(k)])
        V = v * v.T
        M += [
            sp.diag(V, -V),  # Re(P_z(r) P_w(r))
            sp.BlockMatrix([[Z, V], [V, Z]]).as_explicit()
        ]

    assert len(M) == j
    A = [I]
    for B in M[1:]:
        assert B == B.T
        shift = 1 + max(
            sum(abs(B[a, b]) for b in range(n))
            for a in range(n)
        )
        C = B + shift * I
        assert C - shift * A[0] == B
        assert all(
            C[a, a] > sum(abs(C[a, b])
                          for b in range(n) if a != b)
            for a in range(n)
        )
        A.append(C)

    # Exact common-bisector constraints: normal dot mean - offset = 0.
    means = [sp.zeros(d0, 1)]
    for i in range(j - 1):
        e = sp.zeros(d0, 1)
        e[i] = 1
        means.append(e)

    constraints = sp.Matrix([list(mu) + [-1] for mu in means])
    N = constraints.nullspace()
    assert len(N) == n
    assert all(
        all(v[a] == 0 for a in range(j - 1)) and v[-1] == 0
        for v in N
    )

    # Full Gaussian covariance matrices, with exact SPD certificates.
    for C in A:
        Sigma = sp.diag(sp.eye(j - 1), C)
        assert Sigma.shape == (d0, d0)
        assert Sigma[j - 1:, j - 1:] == C
        assert all(
            Sigma[a, a] > sum(abs(Sigma[a, b])
                              for b in range(d0) if a != b)
            for a in range(d0)
        )

    # Entire Euler polynomial modulo (x^(d+1), y^(d+1), 2).
    euler = {
        (j + a, 2 * j - a): 1
        for a in range(j + 1)
        if j + a <= d
        and 2 * j - a <= d
        and comb(j, a) % 2
    }
    assert euler.get((3 * n - 4, 3 * n - 2)) == 1

    print(
        f"s={s}: {splits} root splits certified; "
        f"{j} SPD covariances in dimension {d0}; "
        f"Euler monomials {sorted(euler)}"
    )


for s in (3, 4, 5):
    check(s)

for s in range(3, 16):
    n = 2 ** (s - 1)
    assert comb(2 * n - 2, n - 2) % 2 == 1

print("All exact checks passed.")
```

Output:

```text
s=3: 1 root splits certified; 6 SPD covariances in dimension 9; Euler monomials [(8, 10), (10, 8)]
s=4: 10 root splits certified; 14 SPD covariances in dimension 21; Euler monomials [(20, 22), (22, 20)]
s=5: 1716 root splits certified; 30 SPD covariances in dimension 45; Euler monomials [(44, 46), (46, 44)]
All exact checks passed.
```

**Proved:** a universal equipartition theorem in dimension \(3\cdot2^{s-1}-2\), and explicit absolutely continuous Gaussian counterexamples one dimension below. Thus the exact value is established for every \(s\ge3\). **Nothing remains to be proved.**