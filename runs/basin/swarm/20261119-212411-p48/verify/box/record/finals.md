# agent_1: last reply

\[
\boxed{\displaystyle \lim_{j\to\infty}\kappa(U_j)=2.}
\]

In fact, \(\kappa(U_j)=2\) for **every** \(j\). The convergence and stability hypotheses are not needed for this conclusion; ampleness is the relevant hypothesis.

We use the recent **positive-Finsler-metric theorem for ample vector bundles**. It is important here not to replace this theorem by the still much stronger assertion that an ample bundle admits a Griffiths-positive *Hermitian* metric.

### The Finsler theorem in the form needed

If \(V\) is an ample vector bundle on a projective manifold \(B\) of dimension \(n\), there is a smooth function
\[
G:V\setminus 0_B\longrightarrow (0,\infty)
\]
such that
\[
G(\lambda v)=|\lambda|^2G(v),
\]
and the Levi form of \(\log G\) has an \(n\)-dimensional negative-definite subspace at every point.

This is the consequence of the positive-Finsler-metric theorem that we use. In its usual formulation, \(G\) is a complex Finsler metric with positive Kobayashi curvature: the Levi form of \(\log G\) is negative definite on the Finsler-horizontal subspace.

We first prove a general statement.

## 1. Upper bound for an ample rank-two bundle on a surface

Let \(E\) be an ample rank-two bundle on a smooth projective surface \(X\), and put
\[
M=\mathbb P(\mathcal O_X\oplus E),\qquad
Z=\mathbb P(\mathcal O_X),\qquad U=M\setminus Z.
\]
The affine chart where the \(\mathcal O_X\)-coordinate is nonzero is canonically the total space of \(E\), with \(Z\) corresponding to its zero section.

Take \(G\) supplied by the Finsler theorem. We claim that
\[
\phi=\frac1G
\]
has at least three positive Levi eigenvalues on \(E\setminus 0_X\).

Write
\[
\alpha=\partial\log G,\qquad A=\partial\bar\partial\log G.
\]
Differentiation gives
\[
\partial\bar\partial(G^{-1})
  =G^{-1}\bigl(-A+\alpha\otimes\overline\alpha\bigr).
\tag{1}
\]

Let \(R=\sum_\nu v^\nu\partial/\partial v^\nu\) be the holomorphic fibrewise Euler vector field. Homogeneity gives
\[
\alpha(R)=1,\qquad A(R,\overline W)=0
\quad\text{for every }W.
\tag{2}
\]
Indeed, \(R(\log G)=1\), and differentiating this equality in an antiholomorphic direction proves the second identity.

By the Finsler theorem, \(A\) is negative definite on a complex two-dimensional subspace \(H\). Replace \(H\) by
\[
H'=\{h-\alpha(h)R:h\in H\}.
\]
By (2), \(A|_{H'}\) remains negative definite, while \(\alpha|_{H'}=0\). Consequently, on
\[
H'\oplus\mathbb CR
\]
the form in parentheses in (1) is positive definite: its first summand is positive on \(H'\), and its second summand is positive on the radial direction. This proves the claim.

It remains to make this into a global exhaustion of \(U\). Choose \(\varepsilon>0\) and a smooth function
\[
\chi:(0,\infty)\longrightarrow[0,\infty)
\]
equal to \(1/t\) for \(t<\varepsilon\), and equal to \(0\) for \(t>2\varepsilon\). On the punctured affine chart set
\[
\psi=\chi(G),
\]
and extend \(\psi\) by zero outside that chart. This is smooth: the set \(G\le 2\varepsilon\) is a bounded disc bundle over the compact base, so the function already vanishes near the boundary of the affine chart.

Moreover, \(\psi\to+\infty\) when approaching \(Z\). Since \(M\) is compact, every sublevel set of \(\psi\) is therefore compact in \(U\).

The set
\[
K=M\setminus\bigl(Z\cup\{[1:v]:0<G(v)<\varepsilon\}\bigr)
\]
is a compact subset of \(U\). Outside \(K\), we have \(\psi=G^{-1}\), whose Levi form has at least three positive eigenvalues. Thus
\[
\kappa(U)\le2.
\tag{3}
\]

## 2. A lower bound independent of ampleness

In fact, \(\kappa(U)\ge2\) for every rank-two bundle \(E\).

Fix \(x\in X\) and trivialize its projective fibre:
\[
M_x\simeq\mathbb P^2,\qquad Z\cap M_x=\{p\},\qquad p=[1:0:0].
\]
For real \(t>0\), consider the projective line
\[
C_t=\{[tu:u:v]:[u:v]\in\mathbb P^1\}.
\]
It avoids \(p\), so \(C_t\) is a compact holomorphic curve in \(U\). The point
\[
a_t=[t:1:0]\in C_t
\]
converges to the removed point \(p\), and hence escapes every compact subset of \(U\).

Suppose that an exhaustion \(\psi\) had positive-definite Levi form outside a compact set \(K\). Compactness of its sublevels implies
\[
\psi(a_t)\longrightarrow+\infty.
\]
Choose a maximum point \(b_t\) of \(\psi|_{C_t}\). Then
\[
\psi(b_t)\ge\psi(a_t)\longrightarrow+\infty,
\]
so \(b_t\notin K\) for all sufficiently large \(t\). But at a maximum on the holomorphic curve \(C_t\),
\[
\left.\partial\bar\partial\psi\right|_{T_{b_t}C_t}\le0.
\]
That contradicts positive definiteness of the Levi form at \(b_t\). Therefore
\[
\kappa(U)\ge2.
\tag{4}
\]

Combining (3) and (4) gives
\[
\boxed{\kappa\bigl(\mathbb P(\mathcal O_X\oplus E)
                   \setminus\mathbb P(\mathcal O_X)\bigr)=2}
\]
for every ample rank-two bundle on a smooth projective surface. Applying this to each \(E_j\) proves the answer.

## 3. Exact computational checks

The following SymPy code checks the local Levi calculation and the projective-line geometry. These are algebraic checks; the Finsler existence theorem and the maximum principle are the mathematical inputs proved or stated above.

```python
import sympy as s

# Barred variables are independent variables for Wirtinger differentiation.
z1, z2, w1, w2, Z1, Z2, W1, W2 = s.symbols(
    "z1 z2 w1 w2 Z1 Z2 W1 W2"
)
a, d, b, c = s.symbols("a d b c", real=True)

z = [z1, z2, w1, w2]
zb = [Z1, Z2, W1, W2]

# A local model with an arbitrary Hermitian horizontal curvature matrix.
Q = (a*z1*Z1 + (b+s.I*c)*z1*Z2
     + (b-s.I*c)*z2*Z1 + d*z2*Z2)
G = s.exp(-Q) * (w1*W1 + w2*W2)
phi = 1/G

point = {
    z1: 0, z2: 0, Z1: 0, Z2: 0,
    w1: 1, W1: 1, w2: 0, W2: 0
}
L = s.Matrix(4, 4, lambda i, j:
    s.simplify(s.diff(phi, z[i], zb[j]).subs(point)))

expected = s.Matrix([
    [a, b+s.I*c, 0,  0],
    [b-s.I*c, d, 0,  0],
    [0, 0, 1,  0],
    [0, 0, 0, -1]
])
assert L == expected

# Sylvester's criterion:
# if a > 0 and a*d-b*b-c*c > 0, the horizontal block is positive.
assert s.factor(L[:2, :2].det()) == a*d-b*b-c*c
# Together with the radial entry +1, there are three positive directions.

# C_t is the projectivization of the span of these two vectors.
t = s.symbols("t", real=True)
u = s.Matrix([t, 1, 0])
v = s.Matrix([0, 0, 1])
p = s.Matrix([1, 0, 0])

# Nonzero determinant: u,v are independent and p is not in their span.
assert s.Matrix.hstack(u, v, p).det() == 1

# Squared sine of the Fubini–Study distance from [t:1:0] to p.
sin_distance_squared = s.simplify(
    1 - t**2/(t**2 + 1)
)
assert sin_distance_squared == 1/(t**2 + 1)
assert s.limit(sin_distance_squared, t, s.oo) == 0

print("Exact Levi and projective-geometry checks passed.")
```

This code was run successfully.

# agent_2: last reply

Algebraic checks are complete:

\[
c_1(E_j)^2=80e+32,\qquad c_2(E_j)=65e+26,\qquad \chi(E_j)=-15e.
\]

Writing \(E_0=A\oplus B\), one has
\[
H^\bullet(A)=(0,15e,0),\qquad H^\bullet(B)=0,
\]
and hence eventually
\[
h^0(E_j)=h^2(E_j)=0,\qquad h^1(E_j)=15e.
\]
The two off-diagonal deformation dimensions are \(105e+35\) and \(75e+35\), with both obstruction groups zero. Exact symbolic computations passed; reusable code is in `workspace/agent2_cohomology.py`.

These numerical hypotheses are unnecessary if the positive-Finsler-metric theorem for ample bundles is invoked: that theorem, combined with the team’s checked inverse-Finsler exhaustion and compact-curve obstruction, gives
\[
\kappa(U_j)=2\quad\text{for every }j.
\]

The only remaining issue for synthesis is stating the precise published Finsler theorem correctly—not replacing it with the still stronger Hermitian Griffiths-positivity assertion.

# agent_3: last reply

The analytic half gives
\[
\boxed{\kappa(U_j)=2\quad\text{for every }j},
\]
hence the required limit is \(2\).

The upper bound uses the positive-Finsler-metric theorem for ample bundles—not the unproved Hermitian Griffiths conjecture. For its homogeneous squared metric \(G\), positive Kobayashi curvature gives, in horizontal/projective-vertical/radial directions,
\[
\mathcal L_{\log G}=\operatorname{diag}(-K,A,0),
\qquad
\mathcal L_{1/G}=G^{-1}\operatorname{diag}(K,-A,1).
\]
Here \(K\) is positive definite of size two. Thus \(1/G\) has three positive Levi eigenvalues. Cutting it off to a constant away from the missing section produces the required exhaustion of \(U_j\).

The lower bound follows from compact projective lines in a fibre \(\mathbb P^2\setminus\{p\}\) approaching \(p\). Their exhaustion maxima escape every compact set; at each maximum, the Levi form is nonpositive on the line’s tangent direction. Therefore \(q=1\) is impossible.

The chain-rule calculation, adapted Levi matrix, and inertia are checked exactly in `workspace/agent3_finsler_levi.py`. All analytic work is complete; the proof invokes the established positive-Finsler existence theorem as its deep input.

# agent_4: last reply

Completed the lower bound, valid for every rank-two bundle \(E\):
\[
\kappa\!\left(\mathbb P(\mathcal O_X\oplus E)\setminus\mathbb P(\mathcal O_X)\right)\ge2.
\]

Fix a fibre \(\mathbb P^2\setminus\{[1:0:0]\}\). Its compact curves
\[
C_t=\{[tu:u:v]:[u:v]\in\mathbb P^1\}
\]
contain points \(a_t=[t:1:0]\) escaping every compact subset. For any function with compact sublevel sets, \(\psi(a_t)\to\infty\). Consequently maxima of \(\psi|_{C_t}\) eventually occur outside any prescribed compact set. At each such maximum the Levi form is nonpositive on the complex tangent line to \(C_t\), excluding positive-definiteness and hence excluding \(q=1\).

The exact algebraic checks—embeddedness, avoidance of the removed point, and escape—passed in `workspace/agent4_lower_bound.py`.

The team’s upper-bound argument uses the recent positive-Finsler-metric theorem for ample bundles, followed by the explicitly checked Levi calculation for the reciprocal Finsler norm. This gives \(\kappa(U_j)\le2\), hence the proposed complete conclusion is \(\kappa(U_j)=2\) for every \(j\). The lead is preparing the synthesis and precise theorem statement.