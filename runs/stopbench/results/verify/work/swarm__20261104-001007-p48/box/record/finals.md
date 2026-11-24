# agent_1: last reply

\[
\boxed{\displaystyle\lim_{j\to\infty}\kappa(U_j)=3.}
\]
In fact, \(\kappa(U_j)=3\) for every sufficiently large \(j\).

The main point in the lower bound is a **polar-norm construction**. It replaces the invalid shortcut of assuming that the lower bound for the split bundle persists under deformation.

Write
\[
A=\mathcal O_X(5S-f),\qquad
B=\mathcal O_X(-S+(12e+5)f),
\]
so that \(E_0=A\oplus B\).

## 1. Numerical facts

Put \(N=S+ef\). Direct calculation gives
\[
A\cdot H=B\cdot H=10e+4>0,
\tag{1}
\]
whereas
\[
A\cdot N=-1,\qquad B\cdot f=-1.
\tag{2}
\]
Both \(N\) and \(f\) are globally generated. Indeed,
\[
\pi_*\mathcal O_X(N)=\mathcal O_{\mathbb P^1}(e)\oplus\mathcal O_{\mathbb P^1},
\qquad
\mathcal O_X(f)=\pi^*\mathcal O_{\mathbb P^1}(1).
\]
They therefore have smooth semipositive curvature representatives.

It follows from (2) that **neither \(A\) nor \(B\) admits a singular Hermitian metric with positive curvature current**. For example, such a current \(T\) on \(A\), paired with a smooth semipositive representative of \(c_1(N)\), would give
\[
0\le \frac1{2\pi}\int_X T\wedge c_1(N)=A\cdot N=-1,
\]
a contradiction. The argument for \(B\) uses \(f\).

## 2. A degeneration obstruction for plurisubharmonic norms

We will use the following lemma.

**Lemma 1.** Suppose holomorphic bundles \(V_\nu\) converge smoothly, through their Dolbeault operators, to \(A\oplus B\). If neither \(A\) nor \(B\) admits a singular metric with positive curvature current, then, for all sufficiently large \(\nu\), \(V_\nu^*\) admits no continuous fibrewise complex norm \(F_\nu\) for which \(\log F_\nu\) is plurisubharmonic.

Here “norm” includes the triangle inequality.

**Proof.** Suppose otherwise, and pass to a sequence possessing such norms. Fix a smooth background norm on the underlying dual bundle and multiply each \(F_\nu\) by a positive constant so that
\[
\max_{x,\ |\xi|=1}F_\nu(x,\xi)=1.
\]
Consequently,
\[
F_\nu(\xi)\le |\xi|,
\qquad
|F_\nu(\xi)-F_\nu(\eta)|\le |\xi-\eta|.
\tag{3}
\]

On finitely many coordinate charts choose holomorphic frames
\[
(a_{\nu,\alpha},b_{\nu,\alpha})
   \longrightarrow (a_\alpha,b_\alpha)
\]
smoothly, where the limiting frames respect \(A^*\oplus B^*\). Such frames exist under smooth convergence of integrable Dolbeault operators. Locally, this follows by solving the two matrix \(\bar\partial\)-equations successively using Cauchy–Green operators; integrability makes the second equation holomorphic in the first variable, and the solutions converge to the identity when the coefficients tend to zero.

The functions
\[
u_{\nu,\alpha}=\log F_\nu(a_{\nu,\alpha}),
\qquad
v_{\nu,\alpha}=\log F_\nu(b_{\nu,\alpha})
\]
are plurisubharmonic and locally uniformly bounded above. By plurisubharmonic compactness, after taking a subsequence, each either converges in \(L^1_{\rm loc}\) to a plurisubharmonic function or collapses to \(-\infty\). Their exponentials consequently converge in \(L^1_{\rm loc}\), to nonnegative functions which we denote by \(p_\alpha,q_\alpha\).

The limiting transition matrices are diagonal. The Lipschitz estimate (3) therefore shows that on overlaps
\[
p_\beta=|g_{A^*,\alpha\beta}|p_\alpha,\qquad
q_\beta=|g_{B^*,\alpha\beta}|q_\alpha.
\tag{4}
\]
For instance, the error caused by the off-diagonal entry of a transition matrix is bounded by its size times a uniformly bounded frame norm, and tends uniformly to zero.

If the \(p_\alpha\) are not identically zero, their logarithms glue by (4) to a singular norm on \(A^*\) with plurisubharmonic logarithm. Its dual is a positive-curvature singular metric on \(A\), contrary to the hypothesis. The same reasoning applies to \(B\). Thus both families of axis norms must converge to zero in \(L^1_{\rm loc}\).

This contradicts the normalization. Choose a unit vector \(\xi_\nu\) with \(F_\nu(\xi_\nu)=1\). After passing to a subsequence, its base point lies in a fixed relatively compact frame chart. Its frame coefficients are bounded, so the triangle inequality gives, for a fixed \(C\),
\[
1\le C\bigl(F_\nu(a_{\nu,\alpha})
             +F_\nu(b_{\nu,\alpha})\bigr)
\]
at that point. One fixed axis norm is therefore bounded below there along a subsequence. That axis norm is a nonnegative plurisubharmonic function, so the submean inequality on fixed-radius balls gives a positive lower bound on its local \(L^1\)-mass. This contradicts its convergence to zero. ∎

## 3. The polar-norm construction

The next lemma supplies the connection with the exhaustion in the question.

**Lemma 2.** Let \(V\) have rank two over a compact complex surface. If
\[
\mathbb P(\mathcal O\oplus V)\setminus\mathbb P(\mathcal O)
\]
has an exhaustion with at least three positive Levi eigenvalues outside a compact set, then \(V^*\) has a continuous fibrewise complex norm \(F\) such that \(\log F\) is plurisubharmonic.

**Proof.** The affine chart \([1:v]\) identifies a neighborhood of the removed section with a neighborhood of the zero section in \(V\).

Let \(\psi\) be the assumed exhaustion. Choose \(c\) sufficiently large that
\[
D=\{\psi>c\}\cup\{\text{zero section}\}
\]
is a bounded neighborhood of the zero section contained in this affine chart, and \(\psi\) has three positive Levi eigenvalues throughout \(\{\psi\ge c\}\). Properness of the sublevel sets ensures that \(D\) contains a uniform small ball bundle.

Define the fibrewise support norm
\[
F(x,\xi)=\sup_{v\in D_x}|\xi(v)|.
\tag{5}
\]
It is positive away from the zero section, absolutely homogeneous, and satisfies the triangle inequality.

We first check continuity. Lower semicontinuity follows because \(D\) is open. For upper semicontinuity, take a convergent sequence of maximizing vectors in the compact closure of \(D\). A nonzero limiting vector satisfies \(\psi\ge c\). If equality holds, it is still in the fibrewise closure of \(\{\psi>c\}\): the restriction of the Levi form to a two-dimensional fibre has at least
\[
3+2-4=1
\]
positive eigenvalue, and hence \(\psi\) cannot have a fibrewise local maximum there. This proves upper semicontinuity.

We prove that \(\log F\) is plurisubharmonic by testing affine complex lines in a local trivialization of \(V^*\).

If the base coordinate is constant, this follows immediately from
\[
\log F(x,\xi)=\sup_{v\in D_x}\log|\xi(v)|.
\]

Otherwise write the line as \(t\mapsto(x(t),\xi(t))\), where \(x(t)\) is an embedded affine disk. Suppose harmonic comparison fails. There are a harmonic function \(h\) on a disk and an interior point \(t_0\) such that
\[
F(x(t),\xi(t))<e^{h(t)}
\quad\text{on the boundary},\qquad
F(x(t_0),\xi(t_0))>e^{h(t_0)}.
\]
Choose \(v_0\in D_{x(t_0)}\) with
\[
|\xi(t_0)(v_0)|>e^{h(t_0)}.
\]
Let \(H\) be holomorphic with \(\operatorname{Re}H=h\), and put
\[
a(t)=
\frac{\xi(t_0)(v_0)}{e^{H(t_0)}}\,e^{H(t)}.
\]
Then \(a\) never vanishes,
\[
a(t_0)=\xi(t_0)(v_0),\qquad
|a(t)|>F(x(t),\xi(t))
\quad\text{on the boundary}.
\]

Consider the complex surface
\[
\Sigma=\{(t,v):v\in V_{x(t)},\ \xi(t)(v)=a(t)\}.
\tag{6}
\]
It is smooth wherever nonempty and embeds into \(V\), since the base disk is embedded. It avoids the zero section. Its intersection with \(D\) is nonempty, has compact closure away from the zero section, and has no points over the boundary circle.

Thus \(\psi|_\Sigma\) attains a maximum greater than \(c\) at an interior point. But at that point its Levi form on \(\Sigma\) has at least \(3+2-4=1\) positive eigenvalue, contradicting an interior maximum.

Harmonic comparison therefore holds, proving that \(\log F\) is plurisubharmonic. Its extension by \(-\infty\) on the zero section is also plurisubharmonic, since locally \(F\) is comparable to an ordinary fibre norm. ∎

## 4. The lower bound

Suppose that \(\kappa(U_j)\le2\) for infinitely many \(j\). For that subsequence, Lemma 2 produces continuous fibrewise norms on \(E_j^*\) with plurisubharmonic logarithm.

Since \(E_j\to A\oplus B\), Lemma 1 applies. Section 1 showed that neither \(A\) nor \(B\) admits a positive-curvature singular metric. We obtain a contradiction.

Therefore
\[
\kappa(U_j)\ge3
\qquad(j\gg1).
\tag{7}
\]

## 5. The upper bound

Since \(H\) is ample, choose a Kähler form \(\omega\in c_1(H)\). By (1), metrics on \(A\) and \(B\) can be chosen so that their curvature contractions with \(\omega\) are equal positive constants. This is the scalar Poisson equation, whose compatibility condition is precisely their equal positive \(H\)-degrees.

Their direct-sum metric \(h\) satisfies
\[
i\Lambda_\omega\Theta(E_0,h)=\lambda\,\mathrm{Id},
\qquad \lambda>0.
\]
Chern curvature for a fixed smooth metric depends continuously on the Dolbeault operator and its derivatives. Hence
\[
i\Lambda_\omega\Theta(E_j,h)>0
\qquad(j\gg1).
\tag{8}
\]

Set
\[
Y_j=\mathbb P(E_j),\qquad
T_j=\mathcal O_{Y_j}(-1),\qquad L_j=T_j^*.
\]
There is a holomorphic identification
\[
U_j\simeq\operatorname{Tot}(L_j),\qquad
[t:v]\longmapsto\bigl([v],\,v\mapsto t\bigr).
\tag{9}
\]

Give \(T_j\) its induced metric. On the Chern-horizontal two-plane at \((x,[v])\), its curvature is
\[
\frac{\langle i\Theta(E_j,h)v,v\rangle_h}{|v|_h^2}.
\]
By (8), this form has positive trace, hence at least one positive eigenvalue. Thus \(L_j\) has at least one negative curvature eigenvalue everywhere.

On its total space use
\[
\psi_j(w)=|w|_{L_j}^{\,2}.
\]
This is proper because \(Y_j\) is compact. Away from the zero section, its Levi form is congruent to the direct sum of one positive fibre direction and the horizontal form
\[
-\psi_j\,i\Theta(L_j).
\]
It consequently has at least two positive eigenvalues. The zero section is compact, so
\[
\kappa(U_j)\le3
\qquad(j\gg1).
\tag{10}
\]

Combining (7) and (10) proves the assertion.

## 6. Executed Python checks

The following symbolic checks were actually executed successfully. They check the intersection calculations, the dimension bounds used in the maximum principles, and the full complex Hermitian \(4\times4\) Levi-form congruence.

```python
import sympy as s

e = s.symbols("e", integer=True, nonnegative=True)

def dot(D, F):
    a, b = D
    c, d = F
    return s.expand(-e*a*c + a*d + b*c)

A = (5, -1)
B = (-1, 12*e + 5)
H = (1, 3*e + 1)
N = (1, e)
f = (0, 1)
P = (4, 12*e + 3)

assert dot(A, H) == 10*e + 4
assert dot(B, H) == 10*e + 4
assert dot(A, N) == -1
assert dot(B, f) == -1

assert dot(A, P) == 40*e + 11
assert dot(B, P) == 40*e + 17

c1 = tuple(s.expand(a+b) for a, b in zip(A, B))
assert dot(c1, c1) == 80*e + 32
assert dot(A, B) == 65*e + 26

# Restriction to a complex surface or a rank-two fibre.
assert 3 + 2 - 4 == 1

# Generic complex Hermitian norm-square Levi matrix.
t = s.symbols("t", positive=True)
u = s.Matrix(s.symbols("u1 u2 u3", complex=True))
q1, q2, q3 = s.symbols("q1 q2 q3", real=True)
q12, q13, q23 = s.symbols("q12 q13 q23", complex=True)

Q = s.Matrix([
    [q1, q12, q13],
    [s.conjugate(q12), q2, q23],
    [s.conjugate(q13), s.conjugate(q23), q3]
])

M = (t*(Q + u*u.H)).row_join(s.sqrt(t)*u)
M = M.col_join((s.sqrt(t)*u.H).row_join(s.ones(1)))

R = s.eye(4)
for k in range(3):
    R[3, k] = -s.sqrt(t)*s.conjugate(u[k])

assert s.simplify(R.H*M*R) == s.diag(t*Q, s.ones(1))

print("All exact checks passed.")
```

Thus the eventual value, and hence the required limit, is **\(3\)**.

# agent_2: last reply

The proof is now complete: for all sufficiently large \(j\),
\[
\kappa(U_j)=3,
\qquad\text{hence}\qquad
\boxed{\lim_{j\to\infty}\kappa(U_j)=3}.
\]

My verified contributions are:

- **Upper bound:** positive mean curvature of a fixed metric near \(E_0\) gives an exhaustion on
  \[
  U_j\simeq\operatorname{Tot}\bigl(\mathcal O_{\mathbb P(E_j)}(1)\bigr)
  \]
  having at least two positive Levi eigenvalues outside its compact zero section.

- **Key lower-bound bridge:** an exhaustion with three positive Levi eigenvalues would produce a continuous fibrewise norm \(F_j\) on \(E_j^*\) with \(\log F_j\) plurisubharmonic. It is the support norm of a sufficiently small superlevel tube around the deleted zero section. Plurisubharmonicity follows by applying the maximum principle to the complex surfaces
  \[
  \{\xi(t)v=a(t)\}.
  \]

- **Combined lower bound:** the team’s normalized axis-log compactness argument then yields a positive singular metric on at least one of
  \[
  A=\mathcal O_X(5S-f),\qquad
  B=\mathcal O_X(-S+(12e+5)f).
  \]
  This is impossible because \(S+ef\) and \(f\) have smooth semipositive representatives, while
  \[
  A\cdot(S+ef)=-1,\qquad B\cdot f=-1.
  \]

Executable exact checks were saved and successfully run in:

- `workspace/agent2_upper_checks.py`
- `workspace/agent2_bridge_checks.py`

They verify the required intersections, ampleness inequalities for \(H\), the full Levi-form block congruence, and the lower-bound dimension and barrier-multiplier calculations.

# agent_3: last reply

The lower-bound argument is complete.

Suppose a subsequence had \(\kappa(U_j)\le2\). From each corresponding exhaustion, the incidence-surface maximum principle constructs a continuous fibrewise norm \(F_j\) on \(E_j^*\) such that \(\log F_j\) is plurisubharmonic:

- In the affine chart \(E_j\), take a sufficiently high inner collar
  \[
  D_j=\{\psi_j>c_j\}\cup X
  \]
  around the deleted zero section.
- Define
  \[
  F_j(x,\xi)=\sup_{v\in(D_j)_x}|\xi(v)|.
  \]
- A violation of the subharmonic comparison principle for \(\log F_j\) produces an analytic surface
  \[
  \xi(t)v=\beta a(t),\qquad |\beta|>1,
  \]
  meeting \(D_j\), avoiding its disk boundary and the zero section. The exhaustion attains an interior maximum on that surface. This is impossible: three positive ambient Levi eigenvalues restrict to at least one positive eigenvalue on every complex surface.

Normalize \(\sup_{|\xi|_{\mathrm{ref}}=1}F_j=1\). In convergent local holomorphic frames tending to frames of
\[
E_0^*=A^*\oplus B^*,
\]
extract limits of the plurisubharmonic axis functions
\[
\log F_j(a_j^*),\qquad \log F_j(b_j^*).
\]
The triangle inequality gives a uniform fibrewise Lipschitz bound. Consequently, the limiting diagonal transition functions make every noncollapsed axis limit a negative singular metric on \(A^*\) or \(B^*\), equivalently a positive singular metric on \(A\) or \(B\).

Neither is possible. The globally generated classes \(N=S+ef\) and \(f\) have smooth semipositive representatives, whereas
\[
A\cdot N=-1,\qquad B\cdot f=-1.
\]
A positive curvature current cannot have either negative pairing.

Both axis limits must therefore collapse. But normalization, the triangle inequality and the plurisubharmonic submean inequality force a positive \(L^1\) lower bound for at least one axis—a contradiction. Thus \(\kappa(U_j)\ge3\) eventually.

Together with the independently completed upper bound, this proves
\[
\boxed{\lim_{j\to\infty}\kappa(U_j)=3}.
\]

All assigned checks ran successfully; the scripts are listed in Slack message #85.

# agent_4: last reply

Completed the lower-bound argument.

If infinitely many \(U_j\) admitted exhaustions with three positive Levi eigenvalues, their inner superlevel neighborhoods of the deleted zero section would yield fibrewise support norms \(F_j\) on \(E_j^*\) with \(\log F_j\) plurisubharmonic. This follows from the maximum principle on the complex surfaces
\[
\{(t,v):\xi(t)(v)=a(t)\}.
\]

After normalizing these norms, compactness of plurisubharmonic axis weights in converging split-aligned frames produces a nonzero singular positive metric on at least one of
\[
A=\mathcal O_X(5S-f),\qquad
B=\mathcal O_X(-S+(12e+5)f).
\]
The triangle inequality prevents both axis limits from vanishing.

This is impossible:
\[
c_1(A)\cdot(S+ef)=-1,\qquad c_1(B)\cdot f=-1,
\]
where \(S+ef\) and \(f\) have smooth semipositive representatives. Thus \(\kappa(U_j)\ge3\) eventually.

Together with the team's completed upper bound, this proves
\[
\boxed{\lim_{j\to\infty}\kappa(U_j)=3}.
\]

Exact symbolic checks were run successfully in `workspace/agent4_sign_checks.py`.