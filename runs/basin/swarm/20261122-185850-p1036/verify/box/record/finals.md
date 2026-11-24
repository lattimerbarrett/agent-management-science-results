# agent_1: last reply

The answer is
\[
\boxed{\mathscr P_n=[5/2,\infty)\qquad(n\ge2).}
\]

The exponent \(5/2\), rather than \(2\), comes from rapidly oscillating convex perturbations of a ball. Their asymmetry is of order \(k^{-2}\), whereas their PPW deficit is of order \(k^{-5}\).

Here is a proof. Constants denoted by \(C,c>0\) may change from line to line and depend only on the dimension.

We use the classical PPW theorem, including its equality statement, and the classical Ashbaugh–Benguria trial-function lemma. We state the precise trial-function fact where it is used. No quantitative PPW theorem is assumed.

## 1. Normalizations and notation

Put
\[
\alpha^2=\lambda _1(B_1),\qquad \beta^2=\lambda _2(B_1),\qquad
\sigma=|\mathbb S^{n-1}|.
\]
Let \(z\) be the positive, \(L^2\)-normalized first eigenfunction of \(B_1\), extended by zero outside \(B_1\).

Both quantities in the question are invariant under translations and dilations. We consequently normalize domains by
\[
\lambda _1(\Omega)=\alpha^2.
\]
Write \(u\) for their positive, \(L^2\)-normalized first eigenfunction, extended by zero.

We first prove two local estimates:
\[
\delta(\Omega)\ge c\inf_x\|u-z(\cdot-x)\|_2^2,                     \tag{1}
\]
and
\[
\inf_x\|u-z(\cdot-x)\|_2^2\ge c\mathcal A(\Omega)^{5/2}.           \tag{2}
\]
Here “local” means that, after translation, the convex domain is sufficiently close to \(B_1\) in Hausdorff distance. We then remove this restriction.

---

## 2. A compactness observation

We will need the following fact:
\[
\delta(\Omega_j)\longrightarrow0
\quad\Longrightarrow\quad
\Omega_j\longrightarrow B_1
\quad\text{in Hausdorff distance, after normalization and translation.} \tag{3}
\]

Here are details, including the possible issue of unbounded diameters.

Normalize \(\lambda _1(\Omega_j)=\alpha^2\), and translate so that
\[
\int x u_j^2(x)\,dx=0.
\]
For sufficiently large \(j\), the spectral gap is bounded below by a positive dimensional constant. The trial functions \(x_i u_j\) give
\[
(\lambda _2-\lambda _1)\int x_i^2u_j^2\le1.
\]
Thus
\[
\int |x|^2u_j^2\le C.                                           \tag{4}
\]

If \(\ell(x)>0\) is the distance from a supporting hyperplane of \(\Omega_j\), the one-dimensional Hardy inequality gives
\[
\int \frac{u_j^2}{\ell^2}\le4\alpha^2.
\]
Jensen's inequality, and our choice of barycenter, imply
\[
\ell(0)\ge\frac1{2\alpha}.
\]
Consequently,
\[
B(0,1/(2\alpha))\subset\Omega_j.                                 \tag{5}
\]

Take a locally Hausdorff-convergent subsequence of these convex sets. By (4), local Rellich compactness upgrades to global strong \(L^2\) convergence of \(u_j\). The limit is a nonzero \(L^2\) ground state, with eigenvalue \(\alpha^2\), of the limiting convex open set.

An unbounded convex open set has no \(L^2\) ground state. Indeed, it has a recession direction \(e\), so that
\[
D+te\subset D\qquad(t>0).
\]
If \(v\) were a normalized ground state, its zero extension translated by \(te\) would be another Rayleigh minimizer on \(D\). Simplicity and positivity would make it equal to \(v\). A nonzero \(L^2\) function cannot be invariant under a nonzero translation.

The limiting domain is therefore bounded. Convexity and (5) then also bound the diameters of the sequence: otherwise segments joining the fixed inner ball to points tending to infinity would give an unbounded local limit. Standard convergence of Dirichlet eigenvalues on bounded convex domains now applies. The limiting domain has eigenvalues \(\alpha^2,\beta^2\), so the equality statement in PPW makes it \(B_1\). This proves (3).

In particular, it suffices to establish the desired inequality near the ball. Away from that neighborhood, \(\delta\) has a positive lower bound, while \(\mathcal A\le2\).

---

## 3. What the classical PPW proof controls quantitatively

Let \(v=u^*\) be the symmetric decreasing rearrangement of \(u\), and let \(R\) be its support radius. Set
\[
M(r)=\int_0^r v(s)s^{n-1}\,ds,\qquad
e(r)=\alpha^2M(r)+r^{n-1}v'(r).
\]
Coarea, Cauchy–Schwarz on level surfaces, and the isoperimetric inequality give
\[
e(r)\ge0,\qquad
0\le-v'(r)\le \frac{\alpha^2M(r)}{r^{n-1}}\le Cr.                 \tag{6}
\]
These assertions hold almost everywhere; all subsequent identities can equivalently be obtained by approximation.

### The classical trial-function input

Let \(q\) be the positive radial factor of a second eigenfunction of the ball, so that its second eigenfunctions are \(q(r)\theta_i\). On \([0,1]\), put
\[
g=q/z,
\]
and extend \(g\) constantly for \(r\ge1\). The Ashbaugh–Benguria trial-function lemma says that
\[
g\ \text{is increasing},\qquad
N(r)=g'(r)^2+\frac{n-1}{r^2}g(r)^2\ \text{is decreasing}.         \tag{7}
\]
The decreases needed below are strict on \((0,1)\).

Centering the vector-valued trial function \(g(r)\theta u\), and then rearranging, gives
\[
\lambda _2-\alpha^2
 \le \frac{\int N u^2}{\int g^2u^2}
 \le \frac{\int N v^2}{\int g^2v^2}.                            \tag{8}
\]
Define
\[
K=N-(\beta^2-\alpha^2)g^2,\qquad
J=-\int_{\mathbb R^n}K v^2.
\]
It follows from (8), and boundedness of \(g\), that
\[
\delta(\Omega)\ge cJ.                                          \tag{9}
\]

The ball identity gives \(\int Kz^2=0\). Moreover, \(K\) is strictly decreasing,
\[
K(0)>0,\qquad K(1)<0.
\]
For the last inequality, observe that
\[
\beta^2-\alpha^2>n-1:
\]
the radial Rayleigh quotient for angular degree \(1\) contains the additional potential \((n-1)/r^2>n-1\).

Put
\[
H(r)=\int_0^r K(s)z(s)^2s^{n-1}\,ds.
\]
Then
\[
H(r)>0\quad(0<r<1),\qquad
H(r)\asymp r^n(1-r)^3.                                         \tag{10}
\]

### A rearrangement-defect estimate

For domains close to the ball, we claim
\[
\begin{split}
&\|v-z\|_2^2+\|v^2-z^2\|_{H^1(\mathbb R^n)}^2\\
&\quad+
\left(\int|\nabla u^2|^2-\int|\nabla v^2|^2\right)
\le CJ.                                                        \tag{11}
\end{split}
\]

We supply the argument, since this is an important quantitative step.

On \(0<r<1\), let \(y=v/z\). The Wronskian identity is
\[
r^{n-1}z^2y'
   =ze-\int_0^r z'(s)e(s)\,ds\ge0.                              \tag{12}
\]
In particular \(y\) is increasing. Integration by parts gives
\[
\frac J\sigma
 =\int_0^1H(r)(y^2)'(r)\,dr
  +\int_1^R(-K(r))v(r)^2r^{n-1}\,dr.                           \tag{13}
\]

Let \(Q(r)=\int_0^r z^2s^{n-1}ds\). By (10), \(H\) is comparable to
\[
\min\{Q(r),Q(1)-Q(r)\}.
\]
For an increasing function \(a\), the elementary weighted covariance identity gives
\[
\int_0^1|a-\bar a|\,dQ
 \le C\int_0^1\min\{Q,Q(1)-Q\}\,da .
\]
Apply this with \(a=y^2\). Normalization, together with the outside term in (13), yields
\[
\int|v^2-z^2|\le CJ,\qquad \|v-z\|_2^2\le CJ.                  \tag{14}
\]

Write \(b=v(1)\). By (6),
\[
\int_{r>1}v^2\ge cb^3,
\]
and hence \(J\ge cb^3\). On \(r\le1-Lb\), where \(L\) is a sufficiently large fixed constant, (6) gives \(v\le C(1-r)\). Equations (10), (12), and (13), after dropping the nonnegative integral term in (12), imply
\[
J\ge c\int_0^{1-Lb}r v^2e\,dr.
\]
The omitted inner strip has length \(Lb\) and \(v\le Cb\). Thus
\[
\int_0^1r v^2e\,dr\le CJ.                                      \tag{15}
\]

Testing the eigenfunction equation with \(u^3\) gives the exact identity
\[
\int|\nabla u^2|^2-\int|\nabla v^2|^2
 =4\sigma\int_0^R v^2(-v')e\,dr.                               \tag{16}
\]
On \((0,1)\), use (6) and (15); on \((1,R)\), use
\(|v'|\le C\) and the outside term of (13). This bounds (16) by \(CJ\).

Finally, on \((0,1)\),
\[
(v^2-z^2)'=
2v\left[-\alpha^2\frac{M-M_z}{r^{n-1}}
                  +\frac e{r^{n-1}}\right]+2(v-z)z'.
\]
The averaging operator
\[
w\longmapsto r^{1-n}\int_0^r w(s)s^{n-1}\,ds
\]
is bounded on radial \(L^2\). Also \(e\le Cr^n\), so
\[
\int_0^1\frac{v^2e^2}{r^{n-1}}\,dr
 \le C\int_0^1r v^2e\,dr.
\]
These facts, (14), (15), and the outside estimate prove the remaining \(H^1\) bound in (11).

---

## 4. From rearrangement stability to eigenfunction stability

We now prove (1). This step also explains why squaring the eigenfunction is useful.

Let
\[
F_0=z^2.
\]
Define a function \(W\), with \(W(0)=0\), by
\[
W'(z(r)^2)=\Delta(z^2)(r)
          =-2\alpha^2z(r)^2+2z'(r)^2.                           \tag{17}
\]
It is smooth away from zero, extends smoothly beyond the maximum of \(z^2\), and satisfies
\[
W'(0)=2z'(1)^2>0,\qquad
W''(s)\ge-C,\qquad |W''(s)|\le C(1+s^{-1/2}).                   \tag{18}
\]
In particular,
\[
W''(z^2)=-4\alpha^2-2(n-1)\frac{z'}{rz}.                        \tag{19}
\]

Consider
\[
\mathcal E(F)=\frac12\int|\nabla F|^2+\int W(F),\qquad F\ge0.
\]
Since \(u^2\) and \(v^2\) are equimeasurable,
\[
\mathcal E(u^2)-\mathcal E(v^2)
 =\frac12\left(\int|\nabla u^2|^2-\int|\nabla v^2|^2\right).
                                                                    \tag{20}
\]
Equations (18) and (11) also imply
\[
|\mathcal E(v^2)-\mathcal E(F_0)|\le CJ.                         \tag{21}
\]
For example, the potential remainder is bounded by
\(C(v-z)^2\); outside \(B_1\), \(W(v^2)\le Cv^2\).
There is no boundary term in the energy expansion because
\(F_0=\partial_\nu F_0=0\) on \(\partial B_1\).

### The relevant quadratic form

Set
\[
\mathcal Q(h)=\int_{B_1}\bigl(|\nabla h|^2+W''(F_0)h^2\bigr).
\]
On functions whose spherical mean vanishes at almost every radius,
\[
\mathcal Q(h)\ge0,
\]
and its kernel consists exactly of
\[
\partial_1F_0,\ldots,\partial_nF_0.                              \tag{22}
\]
Furthermore,
\[
\mathcal Q(h)\ge c\|h\|_{H^1(B_1)}^2                            \tag{23}
\]
when \(h\) is orthogonal to those translations.

To verify these statements, decompose in spherical harmonics. Differentiating
\(-\Delta F_0+W'(F_0)=0\) shows that
\(-F_0'(r)>0\) is the zero ground state of the angular-degree-\(1\) radial operator. Higher angular degrees add the strictly positive potential
\[
\frac{\ell(\ell+n-2)-(n-1)}{r^2}.
\]
The degree-\(1\) operator has a positive gap off its ground state. Compactness of its form domain, and the lower bound in (18), then give (23).

### Coercivity by contradiction

Translate \(u^2\) so that its \(L^2\) distance to \(F_0\) is minimized, and put
\[
\eta^2=\|u^2-F_0\|_{H^1(\mathbb R^n)}^2+\int_{\mathbb R^n\setminus B_1}u^2.
\]
We claim that, sufficiently near the ball,
\[
\eta^2\le C\delta(\Omega).                                      \tag{24}
\]

Otherwise take a sequence with \(\delta_j=o(\eta_j^2)\).
By (9)–(11), both the rearrangement deficit and
\[
\|v_j-z\|_2^2+\|v_j^2-F_0\|_{H^1}^2
\]
are \(o(\eta_j^2)\). Equations (20)–(21) give
\[
\mathcal E(u_j^2)-\mathcal E(F_0)=o(\eta_j^2).                   \tag{25}
\]

Let \(h_j=(u_j^2-F_0)/\eta_j\). After a subsequence, \(h_j\) converges weakly in \(H^1\) and strongly in \(L^2\) to \(h\in H_0^1(B_1)\).
Equimeasurability gives, for every smooth \(\Phi\) with \(\Phi(0)=0\),
\[
\int\Phi(u_j^2)=\int\Phi(v_j^2).
\]
Its first-order expansion, divided by \(\eta_j\), shows
\[
\int_{B_1}\Phi'(F_0)h=0.
\]
Since \(F_0\) is strictly decreasing in radius, this says precisely that \(h\) has zero spherical mean. The minimizing translation gives the orthogonality in (22).

Expand the left side of (25). On \(B_1\), use Fatou's lemma for the potential remainder, whose negative part is uniformly bounded by \(Ch_j^2\). Outside \(B_1\), (18) gives \(W(u_j^2)\ge c u_j^2\). If
\[
a=\lim\|\nabla h_j\|_2^2,\qquad
b=\lim\frac{\int_{B_1^c}u_j^2}{\eta_j^2},
\]
we obtain
\[
0\ge
\frac12\mathcal Q(h)
+\frac12\bigl(a-\|\nabla h\|_2^2\bigr)+cb.                       \tag{26}
\]
All three terms are nonnegative. By (23) they vanish only if
\(h=0,a=0,b=0\). But the definition of \(\eta_j\), and strong \(L^2\) convergence, give
\[
a+b+\|h\|_2^2=1.
\]
This contradiction proves (24).

### Taking square roots

The eigenfunctions on convex domains close to the ball have a uniform Lipschitz bound. For completeness, a supporting-plane quadratic barrier gives
\[
u(x)\le C\,\operatorname{dist}(x,\partial\Omega);
\]
the constant is uniform because the diameter, eigenvalue, and \(L^\infty\) norm are bounded. Interior gradient estimates then give the global Lipschitz bound for the zero extension.

For nonnegative uniformly Lipschitz \(u\), one has
\[
\|u-z\|_2^2
 \le C\left(\|u^2-z^2\|_{H^1}^2+\int_{B_1^c}u^2\right).         \tag{27}
\]
Here is a direct verification of the only boundary issue in this inequality. On a radial line put \(a=u(\theta)\). In the inner strip of thickness \(Ca\), the contribution of \((u-z)^2\) is \(O(a^3)\). Beyond that strip use
\[
(u-z)^2\le \frac{(u^2-z^2)^2}{c(1-r)^2}
\]
and the one-dimensional Hardy inequality, after subtracting a cutoff extension of the boundary value \(a^2\). Its derivative costs \(O(a^3)\). The Lipschitz bound gives
\[
\int_1^\infty u(r\theta)^2\,dr\ge ca^3.
\]
Integrating in \(\theta\), and treating \(r\le1/2\) directly, proves (27).

Combining (24) and (27) proves (1).

---

## 5. A geometric trace estimate with exponent \(5/2\)

We prove (2). Write the nearly spherical convex domain as
\[
\Omega=\{r\theta:0\le r<1+f(\theta)\},\qquad
a=\int_{\mathbb S^{n-1}}|f|.
\]
Convexity and Hausdorff closeness imply
\[
\|f\|_\infty+\|\nabla f\|_\infty=o(1),\qquad
D_{\mathbb S}^{\,2}f\le C I                                    \tag{28}
\]
in the distributional sense. Thus
\[
\|\Delta_{\mathbb S}f\|_{\rm TV}\le C.                           \tag{29}
\]
Also
\[
\mathcal A(\Omega)\le Ca.                                      \tag{30}
\]

Let \(\bar z\) be the smooth radial continuation of \(z\) through \(r=1\), without cutting it off there, and put \(w=u-\bar z\) in \(\Omega\). Then
\[
(-\Delta-\alpha^2)w=0.
\]

### A boundary-layer comparison

We need
\[
\|w\|_{L^2(\Omega)}^2\le C\|u-z\|_{L^2(\mathbb R^n)}^2.          \tag{31}
\]
It suffices to show
\[
\int_{\mathbb S^{n-1}}f_+^3\le C\|u-z\|_2^2.                   \tag{32}
\]

For a point with \(f(\theta)=s>0\), the small Lipschitz norm in (28) provides balls of radius \(cs\), centered near
\((1-s)\theta\) and \((1+s/2)\theta\), joined by a uniformly bounded Harnack chain in \(\Omega\). On the inner ball \(z\ge cs\); on the outer ball the zero-extended \(z\) vanishes. Harnack's inequality and the triangle inequality therefore imply that the sum of the two contributions to \(\|u-z\|_2^2\) is at least \(cs^{n+2}\).

Choose disjoint angular caps of radii \(cf(\theta)\), whose fixed enlargements cover \(\{f>0\}\). The Lipschitz bound makes \(f\) comparable to its central value on each cap, and the associated inner and outer balls can be chosen disjoint. Summing gives (32), because an angular cap has measure comparable to \(s^{n-1}\). Since
\[
\int_{\Omega\setminus B_1}\bar z^2\le C\int f_+^3,
\]
(31) follows.

### Smooth inner approximation

Let \(p\) be the gauge of \(\Omega\), restricted to the sphere:
\[
p(\theta)=\frac1{1+f(\theta)}.
\]
Its homogeneous extension is convex, so
\[
D_{\mathbb S}^{\,2}p+pI\ge0.
\]
Let \(P_t\) be the spherical heat semigroup. It is an average of rotations, and hence preserves convexity of homogeneous gauge functions. For \(0<h<1\), put
\[
p_h=P_{h^2}p+Ch^2,
\]
where the dimensional constant is large enough that \(p_h\ge p\). Let \(K_h\subset\Omega\) be the convex body with gauge \(p_h\), and write its radial function as \(1+f_h\). Then
\[
f_h\le f,\qquad
\int(f-f_h)\le Ch^2,                                           \tag{33}
\]
and the principal curvatures of \(\partial K_h\) are bounded above by \(C/h\).
These follow respectively from \(\Delta_{\mathbb S}p\ge-C\), preservation of the spherical mean by \(P_t\), and the heat-semigroup derivative bound
\(\|D^2P_{h^2}p\|_\infty\le C/h\).

Set
\[
\psi=P_{h^2}(\operatorname{sgn}f).
\]
Then \(|\psi|\le1\), \(\|D^j\psi\|_\infty\le C_jh^{-j}\), and, by (29),
\[
\int f\psi
 =\int(P_{h^2}f)\operatorname{sgn}f
 \ge a-\|P_{h^2}f-f\|_1
 \ge a-Ch^2.                                                   \tag{34}
\]

On \(\partial K_h\), the Lipschitz bound for \(u\), (33), and the Taylor expansion of \(\bar z\) at \(r=1\) give
\[
\left|\int_{\partial K_h}w\,\psi\,dS\right|
 \ge ca-Ch^2.                                                  \tag{35}
\]
Indeed, \(\int_{\partial K_h}u\le Ch^2\), while
\(\bar z((1+f_h)\theta)=z'(1)f_h+O(f_h^2)\). The surface Jacobian is \(1+o(1)\), and (33)–(34) apply.

The curvature bound gives an inner tubular collar of width \(ch\).
Using distance to \(\partial K_h\), construct \(V\in H^2(K_h)\cap H_0^1(K_h)\), supported in that collar, such that
\[
\partial_\nu V=\psi,\qquad
\|(\Delta+\alpha^2)V\|_2\le Ch^{-1/2}.                          \tag{36}
\]
Explicitly, in the collar use
\[
V=-d(x)\psi(x/|x|)\chi(d(x)/(ch)).
\]
Its second derivatives are \(O(h^{-1})\), and the collar has volume \(O(h)\), proving (36).

Green's identity, (31), (35), and (36) now yield
\[
ca-Ch^2
 \le C h^{-1/2}\|u-z\|_2.
\]
Choose \(h=\varepsilon\sqrt a\), with a sufficiently small fixed \(\varepsilon>0\). We obtain
\[
\|u-z\|_2^2\ge ca^2h=ca^{5/2}.
\]
Together with (30), this proves (2).

Combining Sections 2–5 proves the uniform estimate
\[
\boxed{\delta(\Omega)\ge c_n\mathcal A(\Omega)^{5/2}}.           \tag{37}
\]

---

## 6. Sharpness in every dimension

We construct smooth strictly convex domains satisfying
\[
\mathcal A(\Omega_k)\ge ck^{-2},\qquad
\delta(\Omega_k)\le Ck^{-5}.                                    \tag{38}
\]

Some care is needed to keep the entire second-eigenvalue cluster together.

### Symmetric oscillations

Let \(H\) be the group of signed permutation matrices, and
\(G=\{T\in H:\det T=1\}\). Choose a small spherical patch \(U\) whose \(H\)-translates are disjoint, a nonzero smooth cutoff \(\chi\) supported in \(U\), and a smooth phase \(\phi\) with \(|\nabla\phi|>0\) there. Define
\[
f_k(\theta)=\sum_{T\in H}\det(T)\,
 \chi(T^{-1}\theta)\cos(k\phi(T^{-1}\theta)).
\]
Then
\[
f_k(T\theta)=\det(T)f_k(\theta),
\]
and nonstationary phase and integration by parts give
\[
\|f_k\|_\infty\le C,\quad
\|f_k\|_{C^j}\le C_jk^j,\quad
\|f_k\|_2\ge c,\quad
\|f_k\|_{H^{-1/2}}^2\le C/k.                                   \tag{39}
\]
For the last bound, integration by parts first gives
\(\|f_k\|_{H^{-1}}\le C/k\), and interpolation with \(L^2\) gives the assertion.

The degree-\(0,1,2\) spherical-harmonic components vanish. Indeed, the mean changes sign under a reflection, there is no \(G\)-fixed vector, and every \(G\)-invariant symmetric matrix is scalar.

Consider
\[
\Omega_{k,t}=\{r\theta:0\le r<1+t f_k(\theta)\}.
\]
These domains are \(G\)-invariant, and a reflection takes
\(\Omega_{k,t}\) to \(\Omega_{k,-t}\). The standard representation of \(G\) is irreducible; its self-adjoint commutant is scalar, also when \(n=2\). Thus the second-eigenvalue cluster stays a single eigenvalue of multiplicity \(n\). Its eigenvalue, and the first eigenvalue, are even analytic functions of \(t\).

### The quadratic term

Write \(\nu=n/2-1\), and define the ball Dirichlet-to-Neumann eigenvalue
\[
d_\ell(x)=\ell-x\frac{J_{\ell+\nu+1}(x)}{J_{\ell+\nu}(x)}.
\]
Hadamard's second-variation formula gives, for a displacement \(f\) with vanishing degrees \(0,1,2\),
\[
\delta(\Omega_t)
 =\frac{2\beta^2}{\sigma\alpha^2}t^2
   \sum_{\ell\ge3}c_\ell\|f_\ell\|_2^2+O(t^3),                 \tag{40}
\]
where
\[
c_\ell=d_\ell(\alpha)
 -\frac{\ell}{2\ell+n-2}d_{\ell-1}(\beta)
 -\frac{\ell+n-2}{2\ell+n-2}d_{\ell+1}(\beta).                   \tag{41}
\]

For clarity, the two weights in (41) are the squared-norm proportions of the degree-\(\ell-1\) and degree-\(\ell+1\) pieces of the functions \(\theta_i f_\ell\), summed over \(i\). The curvature terms in the two eigenvalue variations cancel. Pohozaev's identity gives the factor in (40).

The elementary fixed-argument, large-order Bessel expansion gives
\[
d_\ell(x)=\ell-\frac{x^2}{2\ell+n}+O(\ell^{-3}),
\]
so
\[
c_\ell=
 \frac{\beta^2-\alpha^2-(n-2)}{2\ell}+O(\ell^{-2}).
\]
In particular,
\[
|c_\ell|\le C/(1+\ell).
\]
By (39), the quadratic coefficient in (40), with \(f=f_k\), is \(O(k^{-1})\).

### Uniform remainder

We need a uniform estimate, not just a fixed-\(k\) Taylor expansion:
\[
\delta(\Omega_{k,t})\le C\left(t^2/k+t^4k^3\right),
 \qquad |t|\le c/k.                                            \tag{42}
\]

Here are the perturbation details. Extend the boundary displacement to
\[
X_k(r\theta)=\rho(k(r-1))f_k(\theta)\theta,
\]
with a fixed cutoff \(\rho\). It is supported in a layer of width \(O(k^{-1})\), and
\[
\|DX_k\|_\infty\le Ck,\qquad
\|X_k\|_{H^1}^2\le Ck.
\]
Pull the Dirichlet forms back by \(I+tX_k\). They are holomorphic for
\(|t|\le c/k\). On the fixed ball eigenspaces their first-order source terms have \(H^{-1}\) norm \(O(|t|\sqrt k)\); their diagonal second-order remainders are \(O(t^2k)\). The reduced resolvent is uniformly bounded, because the ball eigenvalue clusters are separated. The Schur-complement formula therefore gives
\[
|\lambda_j(t)-\lambda_j(0)-t\lambda'_j(0)|\le C|t|^2k
\]
on that complex disk, for the first eigenvalue and for the second cluster.

The first derivatives vanish. The ratio deficit is even. Cauchy's estimate on a disk of radius \(c/k\) consequently bounds its remainder after the quadratic term by \(Ct^4k^3\). Together with (40), this proves (42).

Take
\[
t_k=\varepsilon k^{-2}
\]
with a small fixed \(\varepsilon>0\). The radial second-fundamental-form formula
\[
r^2I+2\,dr\otimes dr-rD^2r
\]
and (39) show that \(\Omega_k=\Omega_{k,t_k}\) is strictly convex. Equation (42) gives
\[
\delta(\Omega_k)\le Ck^{-5}.                                    \tag{43}
\]

Finally,
\[
\mathcal A(\Omega_{k,t})\ge c|t|                                \tag{44}
\]
uniformly in large \(k\). To see this, the equal-volume radius is
\(1+O(t^2)\). Any potentially minimizing center is \(O(t)\), and radial integration gives
\[
|\Omega_{k,t}\Delta B(x,r_{\Omega_{k,t}})|
 =\int_{\mathbb S^{n-1}}|t f_k-x\cdot\theta|\,d\theta+O(t^2).
\]
Orthogonality to degree \(1\), the lower \(L^2\) bound, and the upper \(L^\infty\) bound in (39) imply
\[
\int|f_k-b\cdot\theta|
 \ge \frac{\int f_k(f_k-b\cdot\theta)}{\|f_k\|_\infty}
 =\frac{\|f_k\|_2^2}{\|f_k\|_\infty}\ge c.
\]
This proves (44), and hence (38).

For every \(p<5/2\),
\[
\frac{\delta(\Omega_k)}{\mathcal A(\Omega_k)^p}
 \le Ck^{2p-5}\longrightarrow0.
\]
No such \(p\) is admissible.

For \(p\ge5/2\), (37) and \(\mathcal A\le2\) give
\[
\delta(\Omega)
 \ge c_n\,2^{\,5/2-p}\mathcal A(\Omega)^p.
\]
This proves the claimed set of exponents.

---

## 7. Python checks

The proof above is analytic. The code below checks its algebraic identities symbolically, checks the Bessel Hessian formula and its asymptotic numerically, and independently computes actual planar spectral deficits by Fourier–Bessel boundary collocation. The collocation calculations are diagnostics, not substitutes for the proof.

I ran this code successfully. In particular, the symbolic checks are exact assertions, not printed conjectures.

```python
import sympy as S
import numpy as np
from scipy.special import jv, hyp0f1
from scipy.optimize import brentq

# ----- Exact symbolic checks -----

r = S.symbols("r", positive=True)
n, lam = S.symbols("n lam", positive=True)
z = S.Function("z")(r)
Z = z*z
ode = -(n-1)*S.diff(z, r)/r - lam*z

# W'(z^2) = Delta(z^2)
Wp = (S.diff(Z, r, 2) + (n-1)*S.diff(Z, r)/r)
Wp = Wp.subs(S.diff(z, r, 2), ode).simplify()
assert S.simplify(
    Wp - (-2*lam*z*z + 2*S.diff(z, r)**2)
) == 0

# Formula (19)
Wpp = (S.diff(Wp, r)/(2*z*S.diff(z, r)))
Wpp = Wpp.subs(S.diff(z, r, 2), ode).simplify()
assert S.simplify(
    Wpp + 4*lam + 2*(n-1)*S.diff(z, r)/(r*z)
) == 0

# Translation kernel of the angular-degree-1 operator
p = S.diff(Z, r)
Lp = (-S.diff(p, r, 2) - (n-1)*S.diff(p, r)/r
      + (n-1)*p/r**2 + Wpp*p)
Lp = Lp.subs(S.diff(z, r, 3), S.diff(ode, r))
Lp = Lp.subs(S.diff(z, r, 2), ode).simplify()
assert Lp == 0

# Wronskian identity behind (12)
v, M = S.Function("v")(r), S.Function("M")(r)
err = lam*M + r**(n-1)*S.diff(v, r)
wr = r**(n-1)*(S.diff(v, r)*z - v*S.diff(z, r))
check = S.diff(wr, r) - z*S.diff(err, r)
check = check.subs(S.diff(M, r), r**(n-1)*v)
check = check.subs(S.diff(z, r, 2), ode)
assert S.simplify(check) == 0

# Hessian's large-degree coefficient
h, A, B = S.symbols("h A B", positive=True)
k = 1/h
wm = k/(2*k+n-2)
wp = (k+n-2)/(2*k+n-2)
d = lambda j, X: j-X/(2*j)
c = d(k, A)-wm*d(k-1, B)-wp*d(k+1, B)
assert S.simplify(
    S.limit(c/h, h, 0) - (B-A-(n-2))/2
) == 0

# Scaling of the uniform remainder
e, kk = S.symbols("e k", positive=True)
t = e/kk**2
assert S.simplify(
    t*t/kk + t**4*kk**3 - (e**2+e**4)/kk**5
) == 0
print("Exact symbolic identities: passed")


# ----- Bessel coefficients -----

def first_zero(nu):
    lo = .05
    for hi in np.arange(.1, 100, .05):
        if jv(nu, lo)*jv(nu, hi) < 0:
            return brentq(lambda x: jv(nu, x),
                          lo, hi, xtol=1e-14)
        lo = hi
    raise RuntimeError("Root not bracketed")


def D(n, k, x):
    # Continued fraction avoids large-order Bessel underflow.
    f = 0.
    for ell in range(k+150, k-1, -1):
        f = x*x/(2*ell+n-f)
    return k-f


def coeff(n, k, a, b):
    return (D(n, k, a)
            - k/(2*k+n-2)*D(n, k-1, b)
            - (k+n-2)/(2*k+n-2)*D(n, k+1, b))


for n in range(2, 9):
    a, b = first_zero(n/2-1), first_zero(n/2)
    assert b*b-a*a > n-1
    for k in range(3, 61):
        nu = n/2-1
        direct = k-a*jv(k+nu+1, a)/jv(k+nu, a)
        assert abs(D(n, k, a)-direct) < 1e-10
        assert coeff(n, k, a, b) > 0
    limit = (b*b-a*a-(n-2))/2
    observed = 2000*coeff(n, 2000, a, b)
    assert abs(observed/limit-1) < .01
    print(n, observed, limit)


# ----- Independent planar spectral calculations -----
# Boundary: r(theta) = 1 + e*cos(k*theta).
# This collocation is numerical, not part of the analytic proof.

def matrix(q, k, e, l, J=4, N=128):
    js = np.arange(-J, J+1)
    theta = 2*np.pi*np.arange(N)/(N*k)
    r = 1+e*np.cos(k*theta)
    modes = l+js*k
    M = np.empty((N, len(js)), complex)
    for a, m in enumerate(modes):
        h = abs(int(m))
        M[:, a] = (np.exp(1j*m*theta)*r**h
                   * hyp0f1(h+1, -q*q*r*r/4))
    return np.exp(-1j*np.outer(modes, theta)) @ M/N


def shape_root(k, e, l, J):
    def residual(q):
        M = matrix(q, k, e, l, J=J)
        ix = [j for j in range(2*J+1) if j != J]
        val = (M[J, J] - M[J, ix] @ np.linalg.solve(
            M[np.ix_(ix, ix)], M[ix, J]))
        return float(np.real(val))
    q0 = first_zero(l)
    return brentq(residual, .99*q0, 1.01*q0, xtol=1e-14)


a, b = first_zero(0), first_zero(1)
for k in [4, 6, 8, 12, 16, 24]:
    e = .1/k**2
    th = np.linspace(0, 2*np.pi, 20001)
    r = 1+e*np.cos(k*th)
    rp = -e*k*np.sin(k*th)
    rpp = -e*k*k*np.cos(k*th)

    # Exact polar convexity criterion, evaluated on the grid.
    assert np.min(r*r+2*rp*rp-r*rpp) > 0

    roots = [
        [shape_root(k, e, l, J) for l in [0, 1]]
        for J in [3, 4]
    ]
    assert np.max(np.abs(
        np.array(roots[0])-roots[1]
    )) < 1e-10

    q0, q1 = roots[1]
    deficit = (b/a)**2-(q1/q0)**2
    area = np.pi*(1+e*e/2)
    centered_difference = (
        np.trapezoid(abs(r*r-area/np.pi), th)/(2*area)
    )
    assert deficit > 0
    print(k, deficit, centered_difference,
          deficit/centered_difference**2.5)

print("All executable checks passed.")
```

For example, the last quotient in the planar calculation is approximately
\[
21.6123,\ 19.3655,\ 18.8917,\ 18.7532,\ 18.8065,\ 18.9467,
\]
for the displayed values of \(k\), consistent with the rigorously proved \(k^{-5}\) versus \(k^{-2}\) scaling.

**Conclusion.** The inequality holds for every \(p\ge5/2\), and the smooth strictly convex sequence constructed above rules out every \(p<5/2\), in every dimension \(n\ge2\). Thus \(\mathscr P_n=[5/2,\infty)\). Nothing remains to determine in the stated problem.