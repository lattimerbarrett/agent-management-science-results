# agent_1: last reply

\[
\boxed{D_s=3\cdot 2^{s-1}-2\qquad(s\geq 3).}
\]

In particular, \(D_3=10\), not \(9\). The lower bound is the subtler half: a parameter-counting lower bound alone would give only \(9\).

I give a proof below. It includes an exact, reproducible computer-assisted calculation in dimension \(4\); all the other dimensions follow by a doubling argument. The Python uses rational arithmetic, Gröbner bases, and Sturm's theorem—not numerical optimization.

## 1. The upper bound

Put
\[
n=2^{s-1},\qquad j=2n-2,\qquad d=3n-2.
\]

We use the following standard vector-bundle form of the mod-\(2\) Borsuk–Ulam argument.

**Equivariant zero lemma.** Suppose a continuous map
\[
F:S^d\times S^d\longrightarrow
(\mathbb R_x\oplus\mathbb R_y\oplus\mathbb R_{x+y})^{\oplus j}
\]
is equivariant for the two antipodal actions. The subscripts mean that the first, second, or both antipodal actions change the sign of that coordinate. If
\[
\bigl(xy(x+y)\bigr)^j\ne0
\quad\text{in}\quad
\mathbb F_2[x,y]/(x^{d+1},y^{d+1}),
\]
then \(F\) has a zero.

Indeed, the map defines a section of
\[
(\lambda_1\oplus\lambda_2\oplus(\lambda_1\otimes\lambda_2))^{\oplus j}
\longrightarrow \mathbb {RP}^d\times\mathbb {RP}^d.
\]
Its top Stiefel–Whitney class is \((xy(x+y))^j\). A nowhere-zero section would split off a trivial line, making that top class zero.

For each given measure \(\mu_i\), and two oriented affine hyperplanes, let
\[
f_{i,1}=\int \operatorname{sgn}(h_1)\,d\mu_i,\quad
f_{i,2}=\int \operatorname{sgn}(h_2)\,d\mu_i,\quad
f_{i,12}=\int \operatorname{sgn}(h_1)\operatorname{sgn}(h_2)\,d\mu_i .
\]
Here an oriented affine hyperplane is parametrized by
\[
(a,b)\in S^d,\qquad h(z)=a\cdot z+b.
\]
The two parameters with \(a=0\) are allowed as formal constant halfspaces. Absolute continuity and dominated convergence make the test map continuous, including at these parameters.

Reversing the first orientation changes the signs of \(f_{i,1},f_{i,12}\); reversing the second changes those of \(f_{i,2},f_{i,12}\). Thus the lemma applies.

We check its hypothesis. In
\[
(xy(x+y))^j
=\sum_{k=0}^j\binom jk x^{j+k}y^{2j-k},
\]
take \(k=n-2\). Then
\[
j+k=d-2,\qquad 2j-k=d.
\]
Furthermore,
\[
\binom{2n-2}{n-2}\equiv1\pmod2.
\]
For example, this follows immediately from
\[
(1+t)^{2^s-2}
=\prod_{r=1}^{s-1}(1+t^{2^r})
\quad\text{over }\mathbb F_2.
\]
Consequently, the monomial \(x^{d-2}y^d\) survives in the quotient ring.

At a zero of the test map, every sign combination has mass
\[
\frac14\left(1+\varepsilon f_{i,1}
+\eta f_{i,2}+\varepsilon\eta f_{i,12}\right)=\frac14.
\]
Neither parameter can be a constant halfspace. Nor can the hyperplanes be parallel or coincident, since then at least one of the four sign combinations is empty. Thus their complement has exactly four connected components.

This proves
\[
D_s\le 3n-2.
\]

## 2. The algebra needed for the lower bound

Call a symmetric bilinear map
\[
B:\mathbb R^n\times\mathbb R^n\longrightarrow\mathbb R^{2n-2}
\]
**positive and nonsingular** if:

* \(B(u,v)=0\) implies \(u=0\) or \(v=0\);
* one coordinate of \(B(u,u)\) is a positive-definite quadratic form.

We shall prove:

> **Algebraic lemma.** Such a map exists for every \(n=2^r\), \(r\ge2\).

### 2.1. An exact base case: \(n=4\)

Let \(K\) be the span of the following four symmetric, trace-zero matrices:
\[
K_1=\begin{pmatrix}
12&6&-15&4\\
6&-15&-6&-11\\
-15&-6&3&3\\
4&-11&3&0
\end{pmatrix},\quad
K_2=\begin{pmatrix}
-3&5&7&5\\
5&-13&5&3\\
7&5&7&3\\
5&3&3&9
\end{pmatrix},
\]
\[
K_3=\begin{pmatrix}
-15&10&3&-4\\
10&14&-8&2\\
3&-8&1&-3\\
-4&2&-3&0
\end{pmatrix},\quad
K_4=\begin{pmatrix}
6&-2&-5&7\\
-2&-4&0&-9\\
-5&0&9&-5\\
7&-9&-5&-11
\end{pmatrix}.
\]

The exact calculation supplied below proves
\[
\boxed{\text{Every nonzero matrix in }K\text{ has rank at least }3.} \tag{1}
\]

Here is precisely how the calculation certifies (1).

A matrix
\[
aK_1+bK_2+cK_3+eK_4
\]
has rank at most \(2\) exactly when all its \(3\times3\) minors vanish.

* On the chart \(e=1\), lexicographic elimination gives a polynomial of degree \(10\) in \(c\). Its Sturm sequences at \(-\infty\) and \(+\infty\) have signs
  \[
  (+,-,-,+,-,-,-,+,+,-,-),
  \]
  \[
  (+,+,-,-,-,+,-,-,+,+,-).
  \]
  Both have five variations. Hence the polynomial has no real roots.
* On each remaining projective chart
  \[
  (a,b,c,e)=(a,b,1,0),\quad(a,1,0,0),\quad(1,0,0,0),
  \]
  the minors generate the unit ideal.

These statements use exact integer and rational computations.

Now take a basis \(A_0,\ldots,A_5\) of \(K^\perp\), with respect to
\[
\langle A,C\rangle=\operatorname{tr}(AC),
\]
choosing \(A_0=I\). This is possible because \(\dim K=4\) and every matrix in \(K\) has trace zero. Set
\[
B(u,v)=(u^{T}A_0v,\ldots,u^{T}A_5v).
\]

If \(B(u,v)=0\), then
\[
M=uv^T+vu^T\in K.
\]
Also \(u\cdot v=0\), from the \(A_0=I\) coordinate. If both vectors were nonzero, \(M\) would have rank exactly \(2\), contradicting (1). Thus \(B\) is nonsingular, and its first coordinate is positive definite.

This proves the base case.

### 2.2. Doubling

Suppose a positive nonsingular map exists in dimension \(n\ge3\). Write \(m=2n-2\).

First make an arbitrarily small real perturbation of its symmetric forms so that the complexification
\[
B_{\mathbb C}:\mathbb C^n\times\mathbb C^n\longrightarrow\mathbb C^m
\]
has these two properties:

1. the projective set
   \[
   Z=\{([z],[w]):B_{\mathbb C}(z,w)=0\}
   \subset\mathbb {CP}^{n-1}\times\mathbb {CP}^{n-1}
   \]
   is finite;
2. \(Z\) does not meet the diagonal.

Here are details justifying the generic perturbation. The map
\[
([z],[w])\longmapsto[zw^T+wz^T]
\]
has finite fibers: the associated quadratic polynomial is a product of two linear forms, which determine their unordered pair of projective factors. Its image therefore has dimension \(2n-2=m\), while the diagonal image has dimension \(n-1<m\). Generic \(m\) hyperplanes cut the first image in a finite set and miss the second. The corresponding good choices form a nonempty Zariski-open set, hence are dense among real choices. Nonsingularity is open by compactness of \(S^{n-1}\times S^{n-1}\), and positive definiteness is open as well. Thus the perturbation preserves both required real properties.

Choose a positive-definite Hermitian matrix \(H_1\) such that
\[
z^*H_1w\ne0\qquad (([z],[w])\in Z).
\]
There are only finitely many conditions, each excluding a proper real-linear subspace of the space of Hermitian matrices.

Next choose a Hermitian matrix \(H_2\) such that
\[
\frac{z^*H_2w}{z^*H_1w}\notin\mathbb R
\qquad (([z],[w])\in Z). \tag{2}
\]
This is possible because \([z]\ne[w]\): for two linearly independent complex vectors, the real-linear map
\[
H\longmapsto z^*Hw
\]
from Hermitian matrices onto \(\mathbb C\) is surjective. To see this, use unitary coordinates with \(z=e_1\) and \(w=ae_1+be_2\), \(b\ne0\), and vary the complex entry \(H_{12}\). Each forbidden condition in (2) is therefore a proper real hyperplane.

Identify \(\mathbb C^n\) with \(\mathbb R^{2n}\), and define
\[
\widetilde B(z,w)=
\bigl(
\operatorname{Re}B_{\mathbb C}(z,w),
\operatorname{Im}B_{\mathbb C}(z,w),
\operatorname{Re}(z^*H_1w),
\operatorname{Re}(z^*H_2w)
\bigr).
\]
This is a real symmetric bilinear map with
\[
2m+2=4n-2=2(2n)-2
\]
coordinates. Its \(H_1\) coordinate is positive definite.

If its first \(2m\) coordinates vanish for nonzero \(z,w\), their projective pair belongs to \(Z\). But (2) says that \(z^*H_1w\) and \(z^*H_2w\) are real-linearly independent complex numbers. Their real parts cannot both vanish. Thus \(\widetilde B\) is nonsingular.

Starting with \(n=4\) and doubling proves the algebraic lemma for all powers of two \(n\ge4\).

## 3. Turning the algebra into counterexamples

Fix \(n=2^{s-1}\) and a positive nonsingular system
\[
B(u,v)=(u^TA_0v,\ldots,u^TA_{2n-3}v),
\qquad A_0>0.
\]
Replacing
\[
A_i\longmapsto A_i+t_iA_0
\]
for sufficiently large \(t_i\), \(i>0\), makes every matrix positive definite. This invertible triangular change of output coordinates preserves nonsingularity. Denote the resulting positive-definite matrices by \(P_i\).

In
\[
\mathbb R^{3n-3}=L\oplus E,
\qquad \dim L=2n-3,\quad \dim E=n,
\]
choose \(2n-2\) affinely independent points \(c_i\in L\). Let \(\mu_i\) be the Gaussian probability measure with mean \(c_i\) and covariance
\[
I_L\oplus P_i.
\]
These are absolutely continuous.

Suppose two affine hyperplanes equipartitioned all the measures.

Each hyperplane would individually bisect every Gaussian. A hyperplane bisects a nondegenerate Gaussian exactly when it contains its mean. Hence both hyperplanes would contain all the \(c_i\), and therefore all of \(L\). Their nonzero normal vectors \(u,v\) would lie in \(E\).

For the \(i\)-th Gaussian, the two signed distances from these hyperplanes are centered jointly normal variables, with covariance
\[
u^TP_iv.
\]
Two nondegenerate centered jointly normal variables have all four sign probabilities equal to \(1/4\) exactly when their covariance is zero. For instance,
\[
\Pr(X>0,Y>0)=\frac14+\frac{\arcsin\rho}{2\pi}.
\]
We would therefore have
\[
u^TP_iv=0\qquad\text{for every }i,
\]
contradicting nonsingularity.

Thus the required property fails in dimension \(3n-3\). The property is monotone in dimension: project any collection of measures to a lower-dimensional coordinate space and lift a partition back. Consequently,
\[
D_s\ge3n-2.
\]

Together with the upper bound, this proves the claimed formula.

## 4. Executable exact verification

The following complete script verifies the computational base case, constructs its six positive-definite forms, and checks the upper-bound arithmetic. I ran it successfully.

```python
import itertools
import sympy as S

K = [S.Matrix(a) for a in [
    [[12, 6, -15, 4],
     [6, -15, -6, -11],
     [-15, -6, 3, 3],
     [4, -11, 3, 0]],

    [[-3, 5, 7, 5],
     [5, -13, 5, 3],
     [7, 5, 7, 3],
     [5, 3, 3, 9]],

    [[-15, 10, 3, -4],
     [10, 14, -8, 2],
     [3, -8, 1, -3],
     [-4, 2, -3, 0]],

    [[6, -2, -5, 7],
     [-2, -4, 0, -9],
     [-5, 0, 9, -5],
     [7, -9, -5, -11]]
]]

# Symmetry, zero traces, and independence.
assert all(A == A.T and S.trace(A) == 0 for A in K)
assert S.Matrix.hstack(
    *(A.reshape(16, 1) for A in K)
).rank() == 4

x, y, z = S.symbols("x y z")
triples = list(itertools.combinations(range(4), 3))

def rank_two_equations(coefficients):
    M = sum(
        (c*A for c, A in zip(coefficients, K)),
        S.zeros(4)
    )
    return [
        M.extract(I, J).det()
        for I in triples for J in triples
    ]

# Projective chart with fourth coefficient nonzero.
G = S.groebner(
    rank_two_equations([x, y, z, 1]), x, y, z
)
p_expr = G.polys[-1].as_expr()
assert p_expr.free_symbols <= {z}
p = S.Poly(p_expr, z)
assert p.degree() == 10

# Exact Sturm calculation.
sturm = [
    S.Poly(f, z)
    for f in S.sturm(p.as_expr(), z)
]

def infinity_signs(negative):
    return [
        int(S.sign(q.LC())) *
        (-1 if negative and q.degree() % 2 else 1)
        for q in sturm
    ]

def variations(signs):
    return sum(a != b for a, b in zip(signs, signs[1:]))

minus = infinity_signs(True)
plus = infinity_signs(False)

assert minus == [1, -1, -1, 1, -1, -1, -1, 1, 1, -1, -1]
assert plus == [1, 1, -1, -1, -1, 1, -1, -1, 1, 1, -1]
assert variations(minus) == variations(plus) == 5
assert p.count_roots(-S.oo, S.oo) == 0

print("Sturm signs at -infinity:", minus)
print("Sturm signs at +infinity:", plus)

# The three remaining projective charts.
for coefficients, variables in [
    ([x, y, 1, 0], (x, y)),
    ([x, 1, 0, 0], (x,)),
    ([1, 0, 0, 0], (x,))
]:
    H = S.groebner(
        rank_two_equations(coefficients), *variables
    )
    assert list(H) == [1]

print("All three patches at infinity have ideal (1).")

# Compute K-perp in the ten-dimensional symmetric matrix space.
E = []
for i in range(4):
    for j in range(i, 4):
        A = S.zeros(4)
        A[i, j] = A[j, i] = 1
        E.append(A)

C = S.Matrix([
    [S.trace(A*B) for B in E]
    for A in K
])
assert C.rank() == 4

forms = [S.eye(4)]
for v in C.nullspace():
    A = sum((v[i]*E[i] for i in range(10)), S.zeros(4))
    rank = S.Matrix.hstack(
        *(B.reshape(16, 1) for B in forms + [A])
    ).rank()
    if rank > len(forms):
        forms.append(A)

assert len(forms) == 6

# Add multiples of I to obtain strict diagonal dominance,
# hence positive definiteness, while preserving their span.
positive_forms = [forms[0]]
for A in forms[1:]:
    shift = 1 + max(
        [S.Integer(0)] + [
            sum(abs(A[i, j]) for j in range(4) if j != i)
            - A[i, i]
            for i in range(4)
        ]
    )
    positive_forms.append(A + shift*S.eye(4))

assert all(
    A[i, i] >
    sum(abs(A[i, j]) for j in range(4) if j != i)
    for A in positive_forms for i in range(4)
)
assert all(
    S.trace(A*B) == 0
    for A in positive_forms for B in K
)
assert S.Matrix.hstack(
    *(A.reshape(16, 1) for A in positive_forms)
).rank() == 6

print("Six independent positive definite forms verified.")

def upper_certificate(s):
    assert s >= 3
    n = 1 << (s - 1)
    j, d, k = 2*n - 2, 3*n - 2, n - 2

    # Lucas's criterion for an odd binomial coefficient.
    assert (k & ~j) == 0
    assert (j+k, 2*j-k) == (d-2, d)
    return d

for s in range(3, 11):
    print("s =", s, "D_s =", upper_certificate(s))

# Independent direct binomial checks.
for s in range(3, 10):
    n = 1 << (s - 1)
    assert S.binomial(2*n - 2, n - 2) % 2 == 1
```

Its final values are
```text
s = 3 D_s = 10
s = 4 D_s = 22
s = 5 D_s = 46
s = 6 D_s = 94
s = 7 D_s = 190
s = 8 D_s = 382
s = 9 D_s = 766
s = 10 D_s = 1534
```

**Proved:** both the universal upper bound and matching Gaussian counterexamples one dimension below it, for every \(s\ge3\). **Nothing remains open in the stated question.**