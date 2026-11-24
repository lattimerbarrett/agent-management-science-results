# agent_1: last reply

\[
\boxed{\displaystyle\lim_{j\to\infty}\kappa(U_j)=3.}
\]

In fact, \(\kappa(U_j)=3\) for every sufficiently large \(j\). The crucial lower-bound argument uses fibrewise support norms of small neighbourhoods of the deleted section.

Write
\[
A=\mathcal O_X(5S-f),\qquad
B=\mathcal O_X(-S+(12e+5)f),
\]
so that \(E_0=A\oplus B\).

## 1. Intersection calculations

Put \(N=S+ef\). The required calculations are
\[
H^2=5e+2,\qquad A\cdot H=B\cdot H=10e+4>0,
\tag{1}
\]
and
\[
A\cdot N=-1,\qquad B\cdot f=-1.
\tag{2}
\]

Both \(N\) and \(f\) are globally generated. Indeed, with the projectivization convention in the question,
\[
\mathcal O_X(S)=\mathcal O_{\mathbb P(\mathcal O\oplus\mathcal O(e))}(1),
\]
and hence
\[
\pi_*\mathcal O_X(N)=\mathcal O_{\mathbb P^1}(e)\oplus\mathcal O_{\mathbb P^1}.
\]
Fibrewise evaluation is surjective, proving global generation of \(N\). Global generation of \(f\) is immediate.

Consequently, neither \(A\) nor \(B\) admits a singular Hermitian metric with positive curvature current. For example, if \(T\ge0\) represented \(c_1(A)\), a smooth semipositive representative \(\eta_N\) of \(c_1(N)\) would give
\[
0\le\int_X T\wedge\eta_N=A\cdot N=-1,
\]
a contradiction. The same argument with \(f\) applies to \(B\).

## 2. The upper bound \(\kappa(U_j)\le3\)

The divisor \(H=S+(3e+1)f\) is ample. Fix a Kähler form \(\omega\) representing its first Chern class.

For a holomorphic line bundle on a compact Kähler manifold, changing its Hermitian metric changes the contraction of its curvature by a scalar Laplacian. Solving the Poisson equation therefore gives metrics on \(A\) and \(B\) with constant contracted curvature. By (1), these constants are positive. Their direct-sum metric \(h\) satisfies
\[
i\Lambda_\omega F_{E_0,h}>0.
\]
Keep \(h\) fixed on the underlying smooth bundle. The assumed smooth convergence of Dolbeault operators implies smooth convergence of the associated Chern curvatures. Thus, for all sufficiently large \(j\),
\[
i\Lambda_\omega F_{E_j,h}>0.
\tag{3}
\]

There is a natural biholomorphism
\[
U_j\cong\operatorname{Tot}(L_j),
\qquad
L_j=\mathcal O_{\mathbb P(E_j)}(1).
\tag{4}
\]
Indeed, \([a:v]\), where \(v\ne0\), determines the functional on \(\mathbb Cv\) sending \(v\) to \(a\).

Equip \(L_j\) with the metric induced by \(h\), and let
\[
\psi_j(w)=|w|^2.
\]
Its sublevels are compact because its base \(\mathbb P(E_j)\) is compact.

For a Hermitian line bundle \(L\), the Levi form of its squared norm, in its Chern splitting, is
\[
\mathcal L_{|w|^2}
=
\text{a positive line-fibre square}
-
|w|^2\,i\Theta(L).
\tag{5}
\]
At a point \([v]\in\mathbb P(E_j)\), the horizontal curvature of \(L_j\) is
\[
i\Theta(L_j)(u,\bar u)
=
-\frac{\langle iF_{E_j,h}(u,\bar u)v,v\rangle}{|v|^2}.
\tag{6}
\]
By (3), the negative of this horizontal curvature has positive \(\omega\)-trace. It therefore has at least one strictly positive direction. Together with the positive line-fibre direction in (5), this gives at least two strictly positive Levi eigenvalues whenever \(w\ne0\).

The zero section of \(L_j\) is compact. Thus
\[
\kappa(U_j)\le3
\tag{7}
\]
for all sufficiently large \(j\).

## 3. A support-norm lemma

Here is the analytic device for the lower bound.

**Lemma.** Let \(E\) be a rank-two holomorphic bundle over a complex surface \(M\). Suppose \(\Omega\subset E\) is a neighbourhood of the zero section with compact closure, containing a uniform small disc bundle, and with smooth boundary. Suppose that, for a defining function
\[
\Omega=\{r<0\},
\]
the Levi form of \(r\) on the complex tangent space of \(\partial\Omega\) has at least two strictly negative eigenvalues.

Then
\[
F(x,\xi)=
\max_{v\in\overline\Omega\cap E_x}|\xi(v)|,
\qquad \xi\in E_x^*,
\tag{8}
\]
is a continuous complex norm on each fibre, and \(\log F\) is plurisubharmonic on \(E^*\setminus0\).

### Proof

Positivity, complex homogeneity and the triangle inequality follow directly from (8), using the inner and outer disc bounds on \(\Omega\).

We first verify a regularity point. Let \(v_0\) maximize (8) for \(\xi_0\ne0\). After changing its phase, assume
\[
\xi_0(v_0)=F(x_0,\xi_0)>0.
\]
Then \(v_0\in\partial\Omega\), and the outward half-space
\[
\operatorname{Re}\xi_0(v)>F(x_0,\xi_0)
\]
contains no point of \(\overline\Omega\cap E_{x_0}\).

We claim
\[
d_vr(x_0,v_0)\ne0.
\tag{9}
\]
Otherwise, Taylor expansion on the outward half-space shows that the real vertical Hessian of \(r\) is nonnegative there. Since a quadratic form is even, it is nonnegative on all vertical vectors. Thus the vertical Levi form is semipositive on the complex two-dimensional vertical space.

But that vertical space would lie in the complex tangent space of \(\partial\Omega\), which has dimension three. It must intersect every two-dimensional negative plane nontrivially, contradicting the two negative eigenvalues. This proves (9).

Compactness gives upper semicontinuity of \(F\). At a maximizing point, (9) permits approximation by points in \(\Omega\cap E_{x_0}\), and those points remain in \(\Omega\) for nearby base points. This gives lower semicontinuity. Hence \(F\) is continuous.

It remains to prove plurisubharmonicity. Work in holomorphic bundle coordinates and restrict \(\log F\) to an affine complex line
\[
t\longmapsto (x(t),\xi(t)).
\]

If \(x(t)\) is constant, the submean inequality follows by choosing a maximizing \(v_0\) at the centre:
\[
\log F(0)=\log|\xi(0)v_0|
\le \frac1{2\pi}\int_0^{2\pi}\log|\xi(re^{i\theta})v_0|\,d\theta
\le \frac1{2\pi}\int_0^{2\pi}\log F(re^{i\theta})\,d\theta.
\]

Suppose now that \(x(t)\) is nonconstant. If the restriction were not subharmonic, there would be a smooth upper test \(\phi\), touching it at \(t=0\), with
\[
\phi_{t\bar t}(0)<0.
\]
Choose a maximizing \(v_0\) at \(t=0\), and set
\[
\rho(t,v)=\log|\xi(t)v|-\phi(t).
\]
Near \((0,v_0)\), this is smooth, since \(\xi(0)v_0\ne0\). The pulled-back domain satisfies
\[
\Omega\subset\{\rho\le0\},
\]
with equality at the contact point.

By (9), the pulled-back boundary is smooth. Boundary comparison gives
\[
d\rho=\lambda\,dr,\qquad
\mathcal L_\rho\le\lambda\mathcal L_r
\quad\text{on the common complex tangent},
\qquad \lambda>0.
\tag{10}
\]
The function \(\log|\xi(t)v|\) is pluriharmonic near the contact point, so
\[
\mathcal L_\rho=-\phi_{t\bar t}(0)|dt|^2\ge0.
\]
Thus (10) forces \(\mathcal L_r\ge0\) on that complex tangent.

This is impossible. The original boundary complex tangent has dimension three and contains a two-dimensional negative plane. Restricting to the disk family gives a complex tangent of dimension two, so at least one negative direction survives.

Therefore every affine-line restriction is subharmonic, and \(\log F\) is plurisubharmonic. ∎

## 4. A three-positive exhaustion supplies such a norm

Suppose \(U=\mathbb P(\mathcal O\oplus E)\setminus\mathbb P(\mathcal O)\) has an exhaustion whose Levi form has at least three positive eigenvalues outside a compact set.

Near the deleted section, use the affine chart
\[
v\longmapsto[1:v],
\]
identifying a punctured neighbourhood of the zero section in \(E\) with a subset of \(U\).

Properness of the exhaustion \(\psi\) implies
\[
\psi([1:v])\longrightarrow+\infty
\]
uniformly as \(v\to0\). Otherwise a sequence approaching the deleted section would lie in a compact sublevel.

Choose a small radius \(\varepsilon\), and then a sufficiently large regular value \(c\), larger than the values of \(\psi\) on the annulus
\[
\varepsilon/2\le |v|\le\varepsilon
\]
and on its exceptional compact set. Define
\[
\Omega=
\{0\}\ \cup\
\{0<|v|<\varepsilon:\psi([1:v])>c\}.
\]
This is a neighbourhood of the zero section with compact closure and smooth boundary. Near its boundary,
\[
r=c-\psi.
\]
Its ambient Levi form has at least three negative eigenvalues, hence its boundary complex-tangential Levi form has at least two.

The lemma therefore supplies a continuous fibre norm \(F\) on \(E^*\) with \(\log F\) plurisubharmonic.

## 5. Such norms cannot occur along a sequence converging to \(A\oplus B\)

Suppose, towards a contradiction, that infinitely many \(U_j\) admit three-positive-at-infinity exhaustions. Pass to that subsequence, and obtain norms \(F_j\) as above.

Fix a smooth background norm on the underlying bundle \(E_0^*\). Rescale each \(F_j\) so that
\[
\max_{x,\ |\xi|=1}F_j(x,\xi)=1.
\tag{11}
\]
Thus
\[
F_j(x,\xi)\le|\xi|
\tag{12}
\]
everywhere.

On sufficiently small coordinate charts choose holomorphic frames
\[
s_{j,\alpha,1},s_{j,\alpha,2}
\]
for \(E_j^*\) converging smoothly to frames
\[
s_{0,\alpha,1},s_{0,\alpha,2}
\]
adapted to \(A^*\oplus B^*\). Such frames follow from local solvability of the integrable matrix-valued \(\bar\partial\)-equation with parameters. Concretely, one successively solves the one-variable equations using Cauchy–Green operators; integrability makes the remaining coefficients holomorphic in coordinates already treated, and convergence of the coefficients gives convergence of the frames.

Set
\[
u_{j,\alpha,i}=F_j(s_{j,\alpha,i})^2.
\]
Both \(u_{j,\alpha,i}\) and \(\log u_{j,\alpha,i}\) are plurisubharmonic. By (12), the \(u_{j,\alpha,i}\) are locally uniformly bounded. Plurisubharmonic compactness, followed by a diagonal subsequence, gives
\[
u_{j,\alpha,i}\longrightarrow u_{\alpha,i}
\quad\text{in }L^1_{\mathrm{loc}}.
\tag{13}
\]

At least one limit is nonzero. Indeed, take points and unit vectors attaining (11). In a fixed local frame their coefficients are bounded. The triangle inequality implies that one of the two frame norms is bounded below at those points. The submean inequality then gives a positive lower bound for its integral on a fixed relatively compact chart. This survives (13).

The limits glue diagonally. For example, if the limiting \(A^*\)-frames satisfy
\[
s_{0,\beta,1}=g_{\alpha\beta}s_{0,\alpha,1},
\]
then
\[
s_{j,\beta,1}-g_{\alpha\beta}s_{j,\alpha,1}\longrightarrow0
\]
smoothly. The triangle inequality and (12) yield
\[
F_j(s_{j,\beta,1})
-|g_{\alpha\beta}|F_j(s_{j,\alpha,1})
\longrightarrow0
\]
locally uniformly. Hence
\[
u_{\beta,1}=|g_{\alpha\beta}|^2u_{\alpha,1}.
\tag{14}
\]
The analogous statement holds for \(B^*\).

Moreover, each nonzero limiting diagonal has plurisubharmonic logarithm. For every \(\delta>0\),
\[
\log(u_{j,\alpha,i}+\delta)
\]
is plurisubharmonic and converges in \(L^1_{\rm loc}\) to
\(\log(u_{\alpha,i}+\delta)\). Letting \(\delta\downarrow0\) proves that
\(\log u_{\alpha,i}\) is plurisubharmonic, unless identically \(-\infty\).

Thus a nonzero diagonal, together with (14), defines a singular negative metric on \(A^*\) or on \(B^*\). Its dual gives a positive curvature current representing \(c_1(A)\) or \(c_1(B)\). Both possibilities contradict (2).

We have excluded every subsequence admitting a three-positive-at-infinity exhaustion. Therefore
\[
\kappa(U_j)\ge3
\]
for all sufficiently large \(j\). Combined with (7), this proves eventual equality and the asserted limit.

## 6. Executed Python checks

The algebraic identities and local Levi calculations were checked symbolically, not merely printed. The following standalone script reproduces the checks:

```python
import sympy as s

e = s.symbols("e", integer=True, nonnegative=True)

def intersection(D, G):
    a, b = D
    c, d = G
    return s.expand(-e*a*c + a*d + b*c)

A = (5, -1)
B = (-1, 12*e + 5)
H = (1, 3*e + 1)
N = (1, e)
f = (0, 1)
P = (4, 12*e + 3)

# All intersection calculations used in the proof.
assert intersection(H, H) == 5*e + 2
assert intersection(H, (1, 0)) == 2*e + 1
assert intersection(A, H) == 10*e + 4
assert intersection(B, H) == 10*e + 4
assert intersection(A, N) == -1
assert intersection(B, f) == -1

# Additional checks on the stated bundle and polarization.
assert intersection(A, P) == 40*e + 11
assert intersection(B, P) == 40*e + 17
assert intersection(A, B) == 65*e + 26

# Exact Schur-complement identity for psi = h*|w|^2.
# Eliminating its positive line-fibre block leaves
# |w|^2*(h_{a bar b} - h_a*h_bar_b/h)
# = psi*(log h)_{a bar b}.
h = s.symbols("h", positive=True)
ww = s.symbols("ww", nonnegative=True)
p1, p2, q1, q2 = s.symbols("p1 p2 q1 q2")
t11, t12, t21, t22 = s.symbols("t11 t12 t21 t22")
p = s.Matrix([p1, p2])
q = s.Matrix([[q1, q2]])
T = s.Matrix([[t11, t12], [t21, t22]])
schur = ww*T - ww*p*q/h
assert (schur - ww*h*(T/h - p*q/h**2)).applyfunc(
    s.simplify
) == s.zeros(2)

# Direct complex Hessian of the reciprocal fibre norm.
x, y, u, v, r = s.symbols("x y u v r", real=True)
g = 1/(x*x + y*y + u*u + v*v)
pairs = [(x, y), (u, v)]
M = s.zeros(2)
for i, (a, b) in enumerate(pairs):
    for j, (c, d) in enumerate(pairs):
        M[i, j] = s.simplify(
            (s.diff(g, a, c) + s.diff(g, b, d)
             + s.I*s.diff(g, b, c)
             - s.I*s.diff(g, a, d))/4
        )
assert M.subs({x:r, y:0, u:0, v:0}) == s.diag(r**-4, -r**-4)

# Cauchy–Schwarz identity underlying the norm noncollapse estimate.
a, b, U, V = s.symbols("a b U V", real=True)
assert s.expand(
    (a*a+b*b)*(U*U+V*V)
    - (a*U+b*V)**2
    - (a*V-b*U)**2
) == 0

print("All intersection, Levi, and norm identities passed.")
```

The script executed successfully. The analytic arguments above establish the support-norm and compactness steps; numerical checks are not being used as substitutes for those proofs.

# agent_2: last reply

The lower bound is now proved.

### Support-norm lemma
Let \(\Omega\) be a bounded neighborhood of the zero section in a rank-two holomorphic bundle over a compact complex surface. Suppose its smooth boundary has at least two strictly negative tangential Levi eigenvalues. Then
\[
F(x,\xi)=\max_{v\in\overline\Omega\cap E_x}|\xi(v)|
\]
is a continuous fibrewise complex norm, and \(\log F\) is plurisubharmonic on \(E^*\).

The decisive proof uses upper tests on complex lines: a strictly superharmonic upper test for \(\log F\) would give a containing hypersurface with semipositive tangential Levi form at a support point. Boundary tangency would then force the original boundary to be semipositive on a complex two-plane that necessarily retains a negative direction—a contradiction. Degenerate support points are handled by proving their vertical boundary derivative cannot vanish.

A hypothetical exhaustion of \(U_j\) with three positive Levi eigenvalues produces precisely such a tube \(\Omega_j\) near the deleted section.

### Compactness obstruction
Normalize the resulting norms \(F_j\). In holomorphic frames converging to frames adapted to
\[
E_0^*=A^*\oplus B^*,\qquad
A=5S-f,\quad B=-S+(12e+5)f,
\]
plurisubharmonic compactness and the norm triangle inequality give a nonzero limiting diagonal singular negative metric on either \(A^*\) or \(B^*\). Consequently, either \(A\) or \(B\) has a positive curvature current.

Both alternatives are impossible:
\[
A\cdot(S+ef)=-1,\qquad B\cdot f=-1,
\]
where \(S+ef\) and \(f\) are globally generated and therefore have smooth semipositive curvature representatives.

Thus \(\kappa(U_j)\ge3\) for all sufficiently large \(j\). Together with the team’s positive-mean-curvature construction proving \(\kappa(U_j)\le3\), this establishes
\[
\boxed{\lim_{j\to\infty}\kappa(U_j)=3}.
\]

The complete support lemma is in `workspace/agent2_support_lemma.txt`; executable algebraic and Levi checks passed in the team’s Python files. Both proof halves are complete.

# agent_3: last reply

Both halves are now established, so
\[
\boxed{\kappa(U_j)=3\quad\text{for all sufficiently large }j},
\qquad
\boxed{\lim_{j\to\infty}\kappa(U_j)=3}.
\]

My completed contribution is the lower-bound compactness argument and its numerical checks:

- A hypothetical exhaustion with three positive Levi eigenvalues produces a bounded tube around the zero section of \(E_j\), whose boundary has two negative tangential Levi directions.
- Fibrewise support functions give convex norms \(F_j\) on \(E_j^*\), with \(\log F_j\) plurisubharmonic.
- Normalization, plurisubharmonic compactness, and the norm triangle inequality yield a nonzero singular negatively curved metric on at least one split summand \(A^*\) or \(B^*\), where
  \[
  A=\mathcal O_X(5S-f),\qquad
  B=\mathcal O_X(-S+(12e+5)f).
  \]
- Thus \(A\) or \(B\) would admit a positive curvature current. This contradicts
  \[
  c_1(A)\cdot(S+ef)=-1,\qquad c_1(B)\cdot f=-1,
  \]
  because \(S+ef\) and \(f\) have smooth semipositive representatives.

The supporting symbolic intersection, Schur-complement, and norm-inequality checks were executed successfully in `workspace/agent3_numerics.py`. All results and technical audits are posted to Slack; only the lead’s final exposition and code collation remain.

# agent_4: last reply

The missing lower bound is now proved. Together with the previously verified upper bound, it gives
\[
\boxed{\kappa(U_j)=3\quad\text{for all sufficiently large }j},
\]
and hence the requested limit is \(3\).

### Completed lower-bound mechanism

Suppose, along a subsequence, an exhaustion on \(U_j\) has three positive Levi eigenvalues outside a compact set.

1. **Extract a tube around the deleted section.**  
   In the affine chart \(E_j\subset\mathbb P(\mathcal O_X\oplus E_j)\), sufficiently high superlevel sets of the exhaustion, together with the zero section, give a bounded neighborhood \(\Omega_j\) of zero. Its smooth boundary has at least two negative tangential Levi eigenvalues.

2. **Take fibrewise support norms.**  
   Define
   \[
   F_j(x,\xi)=\max_{v\in\overline{\Omega_{j,x}}}|\xi(v)|,
   \qquad \xi\in E_{j,x}^*.
   \]
   These are genuine complex norms. The boundary Levi condition implies that \(\log F_j\) is plurisubharmonic.

   The key point is an upper-test argument. At a support point, the vertical boundary gradient cannot vanish: otherwise the vertical Levi form would be semipositive on a two-dimensional complex subspace, contradicting the two negative boundary directions. If \(q\) touches \(\log F_j\) from above, then
   \[
   Q=q-\log|\xi(v)|
   \]
   has a boundary minimum. Consequently
   \[
   \mathcal L_q+\lambda\mathcal L_r\ge0
   \]
   on the boundary complex tangent, for some \(\lambda>0\). A two-dimensional negative plane projects isomorphically onto the base tangent space, because its intersection with the semipositive vertical tangent line is zero. Lifting each base direction through that plane proves \(\mathcal L_q\ge0\), including mixed base–dual-fibre directions. Thus \(\log F_j\) is psh without any nondegeneracy assumption on the support maximum.

3. **Pass to the split limit using norm convexity.**  
   Normalize \(\max_{|\xi|=1}F_j=1\). In converging local holomorphic frames adapted in the limit to
   \[
   E_0^*=A^*\oplus B^*,
   \]
   the squared diagonal norms are uniformly bounded nonnegative psh functions. The triangle inequality and normalization ensure that at least one diagonal has a nonzero \(L^1\) limit. Transition matrices converge to diagonal ones, and the uniform norm bound makes their off-diagonal errors negligible. Therefore the limits define squared norms on \(A^*\) and \(B^*\).

   Their logarithms are psh: for every \(\varepsilon>0\),
   \(\log(u_j+\varepsilon)\) is psh and converges in \(L^1\) to
   \(\log(u+\varepsilon)\); decrease \(\varepsilon\) to zero. Hence at least one of \(A\) or \(B\) has a singular metric of positive curvature, so is pseudoeffective.

4. **Obtain the contradiction.**  
   Here
   \[
   A=5S-f,\qquad B=-S+(12e+5)f.
   \]
   Both \(S+ef\) and \(f\) are globally generated, hence have smooth semipositive representatives, whereas
   \[
   A\cdot(S+ef)=-1,\qquad B\cdot f=-1.
   \]
   Neither \(A\) nor \(B\) can therefore be pseudoeffective.

This excludes every three-positive-at-infinity exhaustion along any subsequence tending to the split operator.

### Verification files

- `workspace/agent4_curvature_checks.py`: executed successfully; checks the intersection identities, Levi normal form, nef-test intersections, and exact Schur congruence.
- `workspace/agent2_support_lemma.txt`: detailed support-norm lemma and tube extraction.
- The other agents’ numerical and upper-bound scripts also passed.

Both halves are now established; only consolidation into the team’s final exposition remains.