# agent_1: last reply

\[
\boxed{\displaystyle\lim_{j\to\infty}\kappa(U_j)=3.}
\]

In fact, \(\kappa(U_j)=3\) for all sufficiently large \(j\). My earlier answers missed the lower-bound argument using the parameter space of compact projective lines.

The proof has two halves: stability gives \(\kappa(U_j)\leq3\), while the specified degeneration rules out \(\kappa(U_j)\leq2\).

## 1. The upper bound: \(\kappa(U_j)\leq3\)

Put
\[
A=\mathcal O_X(5S-f),\qquad
B=\mathcal O_X(-S+(12e+5)f).
\]
The underlying smooth bundle is fixed, so
\[
c_1(E_j)=c_1(A)+c_1(B)=4S+(12e+4)f.
\]
Moreover,
\[
P=4S+(12e+3)f.
\]
The usual ampleness criterion on a Hirzebruch surface shows that \(P\) is ample, and
\[
c_1(E_j)\cdot P=80e+28>0.
\]

Choose a Kähler form representing \(P\). By the Hermitian–Einstein theorem, the assumed slope-stability gives a smooth Hermitian metric \(h_j\) whose contracted curvature is a positive scalar multiple of the identity.

The chart in \(\mathbb P(\mathcal O_X\oplus E_j)\) where the \(\mathcal O_X\)-coordinate is nonzero identifies a neighbourhood of the removed section with a neighbourhood of the zero section of \(E_j\). Write
\[
r(x,w)=|w|_{h_j}^{2}.
\]
On its punctured part consider
\[
\psi=r^{-1}.
\]

At a point, use a holomorphic frame normal for \(h_j\). The mixed horizontal–vertical Levi block vanishes. The horizontal block is
\[
r^{-2}\big\langle R_{h_j}(\,\cdot\,,\overline{\cdot})w,w\big\rangle.
\]
Its Kähler trace is positive, so it has at least one positive eigenvalue.

The vertical block is the Levi form of \(1/|w|^2\) on \(\mathbb C^2\setminus\{0\}\). Its eigenvalues are
\[
|w|^{-4},\qquad -|w|^{-4}.
\]
Thus \(\psi\) has at least two positive eigenvalues near the removed section.

Extend \(\psi\) smoothly over the remainder of \(U_j\), modifying it only away from a smaller punctured neighbourhood. Since \(\psi\to+\infty\) at the removed section, the extension is an exhaustion. Consequently,
\[
\boxed{\kappa(U_j)\leq3.} \tag{1}
\]

## 2. What a \(2\)-convex end would imply

Call a function \(N:V\to[0,\infty)\) a **plurisubharmonic fibrewise seminorm** if it is finite and plurisubharmonic on the total space of \(V\), and its restriction to every fibre is a complex seminorm. It is a fibrewise norm if it vanishes only on the zero section.

We need the following implication.

### Lemma 1
Let \(E\) be a rank-two holomorphic bundle over a compact complex surface, and put
\[
U=\mathbb P(\mathcal O\oplus E)\setminus\mathbb P(\mathcal O).
\]
If \(U\) has an exhaustion with at least three positive Levi eigenvalues outside a compact set, then \(E^*\) admits a plurisubharmonic fibrewise norm.

### Proof

#### (a) The compact graph lines

For \(\lambda\in E_x^*\), define the compact projective line
\[
C_\lambda
 =\{[\lambda(v):v]:[v]\in\mathbb P(E_x)\}\subset U.
\]
For the asserted exhaustion \(\psi\), set
\[
F(\lambda)=\max_{p\in C_\lambda}\psi(p).
\]
This is continuous. It is also an exhaustion of \(E^*\): as \(|\lambda|\to\infty\), one can choose unit vectors \(v\) with \(|\lambda(v)|\to\infty\), and the points
\[
[\lambda(v):v]
\]
approach the removed section.

We claim that \(F\) is plurisubharmonic wherever
\[
F>\max_K\psi, \tag{2}
\]
where \(K\) is the compact exceptional set for the Levi condition.

Here is the local argument, including the relevant linear algebra. Let \(\phi\) be a smooth upper test function for \(F\) at \(\lambda_0\), and choose a maximizing point \(p_0\in C_{\lambda_0}\). On the universal family of graph lines, let
\[
p:\mathcal C\longrightarrow E^*,\qquad
\mathrm{ev}:\mathcal C\longrightarrow U
\]
be the parameter projection and evaluation. The function
\[
\psi\circ\mathrm{ev}-\phi\circ p
\]
has a local maximum at \((\lambda_0,p_0)\). Therefore
\[
\mathrm{ev}^*\mathcal L_\psi\leq p^*\mathcal L_\phi. \tag{3}
\]

Suppose \(\mathcal L_\phi\) were negative on a parameter direction \(\eta\). Let \(t\ne0\) be tangent to the projective-line fibre of \(p\), and choose \(w\) with \(dp(w)=\eta\). On the complex two-plane
\[
W=\operatorname{span}_{\mathbb C}\{t,w\},
\]
the right side of (3) is nonpositive.

Evaluation is injective on \(W\). Indeed, if \(at+bw\ne0\) belonged to its kernel, then \(b\ne0\), since evaluation embeds each graph line. But (3) would give
\[
0\leq |b|^2\mathcal L_\phi(\eta,\eta)<0,
\]
a contradiction.

Thus evaluation maps \(W\) to a complex two-plane on which \(\mathcal L_\psi\) is nonpositive. This is impossible for a Hermitian form with at least three positive eigenvalues in complex dimension four: every complex two-plane intersects its positive subspace nontrivially.

Hence every upper test function for \(F\) has nonnegative Levi form. The upper-test characterization of plurisubharmonicity proves the claim.

#### (b) Balanced convex sublevel sets

Define
\[
G(\lambda)=\max_{|a|\leq1}F(a\lambda).
\]
It is continuous, proper, and invariant under multiplication of \(\lambda\) by complex numbers of modulus one. By (2), it is plurisubharmonic wherever its value is sufficiently large: locally there, only branches \(F(a\lambda)\) lying in the plurisubharmonic region can attain the maximum.

Choose \(c\) larger than this threshold and larger than all values on the zero section. Set
\[
D=\{G<c\}\subset E^*.
\]
Then \(D\) contains the zero section, is relatively compact, and has a plurisubharmonic defining function near its boundary.

Its fibres are balanced and convex. Indeed, \(\lambda\in D_x\) means
\[
\psi([a\lambda(v):v])<c
\quad\text{for every }[v]\in\mathbb P(E_x),\ |a|\leq1. \tag{4}
\]
If \(\lambda,\mu\in D_x\) and \(0\leq s\leq1\), then
\[
|s\lambda(v)+(1-s)\mu(v)|
 \leq\max\{|\lambda(v)|,|\mu(v)|\}.
\]
For each fixed \(v\), condition (4) includes the whole disc of possible first coordinates. It therefore holds for \(s\lambda+(1-s)\mu\). Balancedness is immediate.

Let \(N\) be the fibrewise Minkowski functional of \(D\). The fibres being bounded, balanced, convex neighbourhoods of zero, \(N\) is a fibrewise norm.

For clarity, the standard Minkowski-functional argument gives
\[
\log N\quad\text{plurisubharmonic off the zero section}. \tag{5}
\]
One can see this directly by the analytic-disc comparison principle. If \(\log N\) failed harmonic comparison on a disc, multiply the fibre coordinate by the exponential of a holomorphic function to arrange that the disc boundary lies strictly in \(D\), while an interior point lies outside \(D\). Starting with a sufficiently small scalar multiple of this disc, increase the scalar to the first contact with \(\partial D\). At that contact, \(G\) is subharmonic along the disc, is at most \(c\), and attains \(c\) at an interior point. Its contact set is therefore open as well as closed, contradicting the strict boundary inclusion.

This proves (5). Hence \(N\) is plurisubharmonic off zero. Locally \(N\leq C|\lambda|\), so it extends plurisubharmonically by zero across the zero section. ∎

## 3. Compactness of these norms under convergence of Dolbeault operators

### Lemma 2
Suppose holomorphic structures \(V_j\) on a fixed smooth bundle over a compact complex manifold converge smoothly to \(V_0\). If every \(V_j\) has a plurisubharmonic fibrewise norm, then \(V_0\) has a **nonzero** plurisubharmonic fibrewise seminorm.

### Proof
Fix a background norm and multiply each norm \(N_j\) by a positive constant so that
\[
\max_{\substack{x\in X\\|\xi|=1}}N_j(x,\xi)=1. \tag{6}
\]

Smooth convergence of the Dolbeault operators gives, on sufficiently small fixed coordinate polydiscs, holomorphic frames for \(V_j\) converging smoothly to frames for \(V_0\). This is the local parametric form of holomorphic triviality; it also follows by successively solving the small matrix-valued \(\bar\partial\)-equations in each coordinate.

In these frames,
\[
0\leq N_j(z,\xi)\leq C|\xi|.
\]
The compactness theorem for locally bounded plurisubharmonic functions gives a subsequence converging in \(L^1_{\mathrm{loc}}\). A diagonal extraction over finitely many bundle charts gives local limits.

The fibrewise norm laws pass to the limit. More explicitly, the triangle inequality gives the uniform estimate
\[
|N_j(z,\xi)-N_j(z,\eta)|\leq C|\xi-\eta|.
\]
Consequently, after extraction, convergence is uniform on compact fibre sets for almost every base point. The limits are seminorms there. Averaging in the base, passing to the limit, and then decreasing the averaging radius to zero extends the seminorm inequalities to every base point. The converging transition matrices ensure that these local limits glue to a plurisubharmonic fibrewise seminorm \(N_0\).

Finally, the limit is not zero. Choose unit vectors \((x_j,\xi_j)\) attaining (6), and pass to a convergent subsequence. In one of the converging local trivializations, the plurisubharmonic functions \(N_j\) have value \(1\) at points converging to an interior point. Their submean inequalities give a uniform positive lower bound for their integrals on a fixed small ball. Their \(L^1\)-limit is therefore nonzero. ∎

## 4. The split dual admits no such nonzero seminorm

We now show
\[
E_0^*=A^*\oplus B^*
\quad\text{has no nonzero plurisubharmonic fibrewise seminorm}. \tag{7}
\]

We use an elementary observation. If a positive-degree line bundle
\(\mathcal O_{\mathbb P^1}(d)\), \(d>0\), carries a finite plurisubharmonic fibrewise seminorm, that seminorm is zero. Indeed, for any global holomorphic section \(s\), the function \(N\circ s\) is plurisubharmonic on the compact curve \(\mathbb P^1\), hence constant. The section has a zero, so this constant is zero. Global sections generate the line bundle, proving the observation.

First,
\[
B^*|_f\simeq\mathcal O_{\mathbb P^1}(1).
\]
Thus any seminorm as in (7) vanishes on the \(B^*\)-summand over every fibre, hence everywhere on \(B^*\).

For the other summand, consider sections of \(X\to\mathbb P^1\) obtained as graphs
\[
\mathcal O\longrightarrow\mathcal O\oplus\mathcal O(e),
\qquad 1\longmapsto(1,p),
\]
where \(p\in H^0(\mathbb P^1,\mathcal O(e))\). Their images \(C_p\) have class
\[
C=S+ef.
\]
They cover \(X\setminus S\), since \(\mathcal O(e)\) is globally generated. Now
\[
A\cdot C
 =(5S-f)\cdot(S+ef)=-1.
\]
Therefore
\[
A^*|_{C_p}\simeq\mathcal O_{\mathbb P^1}(1),
\]
and the seminorm vanishes on \(A^*\) over \(X\setminus S\).

The triangle inequality makes it zero on all of \(E_0^*\) above \(X\setminus S\). A finite plurisubharmonic function which is zero off an analytic subset is zero everywhere. This proves (7).

## 5. The lower bound and the limit

Suppose infinitely many \(U_j\) had \(\kappa(U_j)\leq2\). Their defining exhaustions would have at least three positive Levi eigenvalues outside compact sets.

Lemma 1 would give plurisubharmonic fibrewise norms on those \(E_j^*\). The dual Dolbeault operators converge smoothly to that of \(E_0^*\), so Lemma 2 would give a nonzero plurisubharmonic fibrewise seminorm on \(E_0^*\). This contradicts (7).

Hence
\[
\kappa(U_j)\geq3
\quad\text{for all sufficiently large }j.
\]
Together with (1), this gives
\[
\boxed{\kappa(U_j)=3\ \text{eventually},\qquad
       \lim_{j\to\infty}\kappa(U_j)=3.}
\]

Notice that no implication from ampleness to Griffiths-positive curvature was used. Stability supplies the upper bound; the specified degeneration supplies the lower bound.

## 6. Executed Python checks

The analytic lemmas above are proved analytically, not inferred from computation. The following script checks the divisor identities, the universal evaluation map, and the local Levi calculations exactly. I executed it; all assertions passed.

```python
import sympy as s

e = s.symbols('e', integer=True, nonnegative=True)

def dot(D, F):
    a, b = D
    c, d = F
    return s.expand(-e*a*c + a*d + b*c)

H = (1, 3*e + 1)
P = (4, 12*e + 3)
A = (5, -1)
B = (-1, 12*e + 5)
C = (1, e)
c1 = tuple(s.expand(x+y) for x, y in zip(A, B))

checks = [
    (dot(P, (1, 0)), 8*e + 3),
    (dot(P, (0, 1)), 4),
    (dot(P, P), 80*e + 24),
    (dot(c1, P), 80*e + 28),
    (dot(C, (1, 0)), 0),
    (dot(C, (0, 1)), 1),
    (dot(A, C), -1),
    (dot(B, (0, 1)), -1),
    (dot(A, B), 65*e + 26),
]
assert c1 == (4, 12*e + 4)
for lhs, rhs in checks:
    assert s.expand(lhs-rhs) == 0
assert (8*e+3).is_positive
assert (80*e+24).is_positive
assert (dot(c1, P)/2).is_positive

# Universal graph-line evaluation, in the chart v=(1,z).
x, y, l1, l2, z = s.symbols('x y l1 l2 z')
ev = s.Matrix([x, y, l1+l2*z, z])
J = ev.jacobian([x, y, l1, l2, z])

assert J.rank() == 4
assert J*s.Matrix([0, 0, 0, 0, 1]) == s.Matrix([0, 0, l2, 1])
assert J*s.Matrix([0, 0, -z, 1, 0]) == s.zeros(4, 1)
assert 3+2-4 == 1

# Exact Wirtinger differentiation of the vertical Levi block.
w1, w2, bw1, bw2 = s.symbols('w1 w2 bw1 bw2')
a = s.symbols('a', positive=True)
r = w1*bw1+w2*bw2

Lv = s.Matrix([
    [s.diff(1/r, u, v) for v in (bw1, bw2)]
    for u in (w1, w2)
])
at_w = {w1:a, bw1:a, w2:0, bw2:0}
assert Lv.subs(at_w) == s.diag(a**-4, -a**-4)

# General horizontal curvature contracted with w=(a,0).
z1, z2, bz1, bz2 = s.symbols('z1 z2 bz1 bz2')
k11, k12, k21, k22 = s.symbols('k11 k12 k21 k22')
K = s.Matrix([[k11, k12], [k21, k22]])

quad = (k11*z1*bz1 + k12*z1*bz2
        + k21*z2*bz1 + k22*z2*bz2)
r_model = (1-quad)*w1*bw1+w2*bw2
zero_base = {z1:0, z2:0, bz1:0, bz2:0}

Lh = s.Matrix([
    [s.diff(1/r_model, u, v) for v in (bz1, bz2)]
    for u in (z1, z2)
])
assert Lh.subs(zero_base).subs(at_w) == K/a**2

mixed = s.Matrix([
    [s.diff(1/r_model, u, v) for v in (bw1, bw2)]
    for u in (z1, z2)
])
assert mixed.subs(zero_base) == s.zeros(2)

print("All exact checks passed.")
```

**Proved:** both bounds needed for eventual equality, and therefore the requested limit \(3\). **What remains:** nothing for the stated problem.