# agent_1: last reply

\[
\boxed{d=5.}
\]

The lower bound uses the low-dimensional classification of uniform bundles, including the recent rank-seven theorem on \(\mathbb P^4\). The upper bound has a relatively short, explicit construction. I give the construction and prove both its uniformity and its non-homogeneity.

## 1. The classification input and the lower bound

We use the following established classification results, in precisely these forms:

> **Low-dimensional classification of uniform bundles.**
> Every uniform bundle of rank \(3\) on \(\mathbb P^2_{\mathbb C}\), of rank \(5\) on \(\mathbb P^3_{\mathbb C}\), or of rank \(7\) on \(\mathbb P^4_{\mathbb C}\) is homogeneous.

The last assertion is the recent rank-seven classification. It is essential here: the older classification in rank at most the dimension would not suffice.

These statements also give the assertions in every smaller rank. Indeed, suppose \(E\) is uniform of rank \(r<R\), where \(R\) is respectively \(3,5,7\). Then
\[
E\oplus\mathcal O^{R-r}
\]
is uniform, hence homogeneous. For every projective automorphism \(g\), therefore,
\[
g^*E\oplus\mathcal O^{R-r}
 \cong E\oplus\mathcal O^{R-r}.
\]
Krull–Schmidt cancellation for vector bundles on a proper variety gives \(g^*E\cong E\). Here Krull–Schmidt applies because the Hom spaces are finite-dimensional and idempotents split.

Consequently, there is no example in the question for \(n=2,3,4\). Thus
\[
d\geq5.
\]

The classification theorem above is the deep input to the proof; the computations below do not purport to replace it.

## 2. An explicit rank-nine bundle on \(\mathbb P^5\)

Let \(V=\mathbb C^6\), with basis \(e_0,\ldots,e_5\), and regard \(\mathbb P(V)\) as parametrizing one-dimensional subspaces. Write
\[
0\longrightarrow\mathcal O(-1)
 \longrightarrow V\otimes\mathcal O
 \longrightarrow Q\longrightarrow0
\]
for the tautological sequence. Set
\[
F=\bigwedge\nolimits^2Q.
\]
It has rank \(10\).

Choose the nondegenerate bivector
\[
w=e_0\wedge e_1+e_2\wedge e_3+e_4\wedge e_5.
\]
It induces a section \(s_w\) of \(F\).

At \(x=[\ell]\), its value is the image of \(w\) in \(\bigwedge^2(V/\ell)\). This image cannot vanish: otherwise \(w\in\ell\wedge V\), which would force \(w\) to have rank at most \(2\), whereas its rank is \(6\).

Thus \(s_w\) is nowhere zero, and
\[
0\longrightarrow\mathcal O
 \xrightarrow{s_w}F
 \xrightarrow{q_w}E_w
 \longrightarrow0                                      \tag{1}
\]
defines an algebraic vector bundle of rank \(9<2\cdot5\).

## 3. Uniformity

A projective line \(L\subset\mathbb P(V)\) is \(\mathbb P(U)\) for a two-dimensional subspace \(U\subset V\). On it,
\[
Q|_L\cong\mathcal O_L(1)\oplus\mathcal O_L^4,
\]
so
\[
F|_L\cong\mathcal O_L(1)^4\oplus\mathcal O_L^6.            \tag{2}
\]

The component of \(s_w|_L\) in the trivial summand is precisely
\[
\bar w\in\bigwedge\nolimits^2(V/U).
\]
This component is nonzero. Indeed, if it vanished, then
\[
w\in U\wedge V.
\]
Writing \(U=\langle u,v\rangle\), every element of \(U\wedge V\) has the form
\[
u\wedge a+v\wedge b,
\]
and hence has rank at most \(4\). Again this contradicts \(\operatorname{rank}(w)=6\).

A section of the bundle in (2) whose trivial component is a nonzero constant can be transformed by a bundle automorphism into one of the standard sections of \(\mathcal O_L^6\): first change basis in the trivial summand, then subtract its positive-degree component. Taking the quotient gives
\[
E_w|_L\cong\mathcal O_L(1)^4\oplus\mathcal O_L^5
\]
for **every** line \(L\). Thus \(E_w\) is uniform.

## 4. Recovering the bivector from the bundle

We next prove
\[
E_w\cong E_{w'}\quad\Longrightarrow\quad
\mathbb Cw=\mathbb Cw'                                  \tag{3}
\]
for nondegenerate bivectors \(w,w'\).

### 4.1. Two vanishings

We have
\[
F^*=\Omega_{\mathbb P^5}^2(2),
\]
and
\[
H^0(F^*)=H^1(F^*)=0.                                   \tag{4}
\]

For completeness, these particular vanishings follow directly from the exterior Euler complex
\[
0\longrightarrow\Omega^2(2)
 \longrightarrow\bigwedge\nolimits^2V^*\otimes\mathcal O
 \longrightarrow V^*\otimes\mathcal O(1)
 \longrightarrow\mathcal O(2)\longrightarrow0.
\]
Its complex of global sections is
\[
0\longrightarrow\bigwedge\nolimits^2V^*
 \longrightarrow V^*\otimes V^*
 \longrightarrow\operatorname{Sym}^2V^*
 \longrightarrow0,
\]
which is exact. The other terms have no positive-degree cohomology.

### 4.2. Simplicity of \(F\)

We also need
\[
\operatorname{End}(F)=\mathbb C.                         \tag{5}
\]

The exterior tautological resolution gives
\[
H^0(F)=\bigwedge\nolimits^2V.
\]
An endomorphism of \(F\) consequently induces a linear map \(A\) on \(\bigwedge^2V\) preserving, for every nonzero \(x\in V\), the evaluation kernel
\[
x\wedge V.
\]
For independent \(x,y\),
\[
(x\wedge V)\cap(y\wedge V)=\mathbb C(x\wedge y).
\]
Therefore every decomposable bivector is an eigenvector of \(A\).

In particular, write
\[
A(e_i\wedge e_j)=\lambda_{ij}e_i\wedge e_j.
\]
Applying the same observation to \((e_i+e_k)\wedge e_j\) shows
\(\lambda_{ij}=\lambda_{kj}\) whenever \(i,j,k\) are distinct. All the eigenvalues are equal, so \(A\) is scalar. Since \(F\) is globally generated, its original endomorphism is scalar as well. This proves (5).

### 4.3. Uniqueness of the quotient map

Apply \(\operatorname{Hom}(F,-)\) to (1). Equations (4) and (5) imply
\[
\operatorname{Hom}(F,E_w)\cong\mathbb C,
\]
generated by \(q_w\).

If \(\phi:E_w\overset{\sim}{\longrightarrow}E_{w'}\), then
\[
\phi q_w=cq_{w'}
\]
for some nonzero scalar \(c\). Their kernels in \(F\) coincide. Hence the two nowhere-zero sections defining these kernels differ by a nonzero constant, proving (3).

## 5. Non-homogeneity

The natural projective-linear action on \(F\) carries the construction for \(w\) to that for the corresponding transformed bivector.

Take the projective automorphism induced by
\[
g=\operatorname{diag}(2,1,1,1,1,1).
\]
Its action sends \(w\) to
\[
2e_0\wedge e_1+e_2\wedge e_3+e_4\wedge e_5,
\]
which is not proportional to \(w\). The inverse action likewise gives a nonproportional bivector, so the choice of pullback convention is immaterial.

By (3), the corresponding pullback of \(E_w\) is not isomorphic to \(E_w\). Thus \(E_w\) is **not homogeneous**.

This proves \(d\leq5\), completing the mathematical argument.

## 6. Executable symbolic checks

Here is Python using only SymPy. It checks the linear algebra underlying the construction, the global-section exactness used in (4), the eigenvalue constraints used in (5), and the explicit transformation used to disprove homogeneity.

It also independently computes the Chern character from the resolution
\[
0\longrightarrow\mathcal O(-2)
 \longrightarrow V\otimes\mathcal O(-1)
 \longrightarrow
 \bigl(\bigwedge\nolimits^2V/\mathbb Cw\bigr)\otimes\mathcal O
 \longrightarrow E_w\longrightarrow0.
\]

```python
import sympy as s
from itertools import combinations, permutations

N = 6
pairs = list(combinations(range(N), 2))

# The chosen nondegenerate bivector.
W = s.zeros(N)
for i in range(0, N, 2):
    W[i, i + 1] = 1
    W[i + 1, i] = -1
assert W.rank() == 6

# Representatives of the two symplectic types of two-plane:
# non-isotropic and isotropic. Their projected bivectors are nonzero.
for U, expected_rank in [([0, 1], 4), ([0, 2], 2)]:
    rest = [i for i in range(N) if i not in U]
    assert W.extract(rest, rest).rank() == expected_rank

# Universal factorization:
# u wedge a + v wedge b = M J M^t, with M having only four columns.
# Therefore every bivector in <u,v> wedge V has rank at most four.
u, v, a, b = [
    s.Matrix(s.symbols(f"{name}0:6"))
    for name in ["u", "v", "a", "b"]
]
M = s.Matrix.hstack(u, v, a, b)
J = s.zeros(4)
J[0, 2] = J[1, 3] = 1
J[2, 0] = J[3, 1] = -1
assert M * J * M.T == (
    u*a.T - a*u.T + v*b.T - b*v.T
)

# Simplicity: all 15 eigenvalues lambda_ij must coincide.
# Check that the displayed equality constraints have rank 14.
rows = []
for i, j, k in permutations(range(N), 3):
    row = [0] * len(pairs)
    row[pairs.index(tuple(sorted((i, j))))] = 1
    row[pairs.index(tuple(sorted((k, j))))] -= 1
    rows.append(row)
assert s.Matrix(rows).rank() == 14

# Degree-two Koszul exactness:
# wedge^2 V* -> V* tensor V* -> Sym^2 V*.
monomials = sorted(pairs + [(i, i) for i in range(N)])
mult = s.zeros(len(monomials), N*N)
alt = s.zeros(N*N, len(pairs))

for i in range(N):
    for j in range(N):
        mult[monomials.index(tuple(sorted((i, j)))), N*i+j] = 1

for col, (i, j) in enumerate(pairs):
    alt[N*i+j, col] = 1
    alt[N*j+i, col] = -1

assert mult.rank() == 21
assert alt.rank() == 15
assert mult * alt == s.zeros(21, 15)
assert 36 - mult.rank() == alt.rank()

# The explicit automorphism changes the projective bivector.
g = s.diag(2, 1, 1, 1, 1, 1)
Wp = g * W * g.T
assert s.Matrix.hstack(
    W.reshape(36, 1), Wp.reshape(36, 1)
).rank() == 2

# Independent Chern-character and Chern-class checks.
h = s.symbols("h")
ch = s.series(
    14 - 6*s.exp(-h) + s.exp(-2*h), h, 0, 6
).removeO()

log_c = sum(
    (-1)**(k-1) * s.factorial(k-1) * ch.coeff(h, k) * h**k
    for k in range(1, 6)
)
c = s.series(s.exp(log_c), h, 0, 6).removeO().expand()

assert ch.coeff(h, 0) == 9
assert c == 1 + 4*h + 9*h**2 + 14*h**3 + 14*h**4

print("All assertions passed.")
print("ch(E) =", ch)
print("c(E)  =", c)
```

I ran this code; all assertions passed.

Combining the low-dimensional classification with the explicit uniform, non-homogeneous rank-nine bundle on \(\mathbb P^5\) proves
\[
\boxed{d=5}.
\]
No dimension or rank case in the question remains unresolved.