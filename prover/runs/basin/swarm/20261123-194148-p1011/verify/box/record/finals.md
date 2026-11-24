# agent_1: last reply

\[
\boxed{\mathcal D=\{19,20,21,\ldots\}.}
\]

The absence of an umbilicity assumption is essential. In particular, local conformal flatness alone does **not** give compactness in all dimensions.

I give the proof below. The computations entering the dimension threshold were performed with exact rational arithmetic, certified enclosures of \(\pi\), and, independently, outward-rounded interval arithmetic. The complete proof notes and runnable certificates are saved here:

- [Detailed proof](workspace/final/boundary_yamabe_proof.md)
- [Python certificates](workspace/final/boundary_yamabe_certificates.zip)

The certificate archive contains `run_checks.py`. It checks the curvature/source normalizations, all low-dimensional matrices, all finite-dimensional construction minima, and the symbolic inequalities covering arbitrarily large dimensions.

## 1. The local model

Put
\[
a=\frac{n-2}{2},\qquad
\beta=2c_n=\frac{n-2}{2(n-1)},\qquad
q=\frac{2n}{n-2}.
\]
On a Euclidean domain the functional for the equation in the question is
\[
J_\Omega(v)=
\frac12\int_\Omega |\nabla v|^2
+\frac{\beta}{2}\int_{\partial\Omega}Hv^2
-\frac{(n-2)^2}{2}\int_\Omega(v_+)^q.                 \tag{1}
\]
Its Euler equation is
\[
-\Delta v=n(n-2)(v_+)^{q-1},
\qquad
\partial_\nu v+\beta Hv=0.
\]

The half-space bubbles are
\[
U_{t,\xi}(y,s)=
\left(\frac{t}{t^2+|y-\xi|^2+s^2}\right)^a,
\qquad s\ge0.                                      \tag{2}
\]
Write \(U=U_{1,0}\). Their Jacobi form is
\[
A(v,w)=\int_{\mathbb R^n_+}\nabla v\cdot\nabla w
-n(n+2)\int_{\mathbb R^n_+}U^{4/(n-2)}vw.           \tag{3}
\]
Its kernel consists precisely of the scale derivative and the \(n-1\) tangential-translation derivatives of \(U\). Indeed, conformal transfer to the hemisphere turns the equation into the Neumann eigenvalue equation
\[
(-\Delta_{\mathbb S^n}-n)\phi=0.
\]
Thus \(A\) has a bounded inverse on the complement of this \(n\)-dimensional kernel.

Represent the boundary near a point by
\[
s=\varepsilon F(y),\qquad \Omega_\varepsilon=\{s>\varepsilon F(y)\}.
\]
With the outward-normal convention in the question,
\[
\nu_\varepsilon=(\varepsilon\nabla F,-1)+O(\varepsilon^2),
\qquad
H_\varepsilon=\varepsilon\Delta F+O(\varepsilon^3).
\]
The first Robin defect of the **ambient** bubble is
\[
S_F=(n-2)U\left[
\frac{F-y\cdot\nabla F}{1+|y|^2}
+\frac{\Delta F}{2(n-1)}
\right].                                         \tag{4}
\]

The first shape variation of (1) vanishes at every bubble. The underlying pointwise identity is
\[
-\frac12|\nabla_yU|^2
+\frac{(n-2)^2}{2}U^q
+c_n\Delta_y(U^2)=0.                              \tag{5}
\]
Consequently \(S_F\) is orthogonal to the bubble kernel.

Let \(w_F\), orthogonal to that kernel, solve
\[
A(w_F,v)=-\int_{\mathbb R^{n-1}}S_Fv.
\]
The quadratic reduced shape energy is
\[
\Psi_F=-\frac12\langle S_F,A^{-1}S_F\rangle.         \tag{6}
\]
There is no missing direct \(F^2\) term here: for the fixed ambient bubble, reflection \(s\mapsto-s\) makes its energy defect an odd function of the graph displacement.

For a sum of homogeneous graph jets
\[
F=\sum_{k\ge2}F_k,
\]
write
\[
C_{kh}=\langle S_{F_k},A^{-1}S_{F_h}\rangle.
\]
The dilation form relevant to blow-up is
\[
\mathcal Q(F)=
\frac12\sum_{k,h}(k+h-2)C_{kh}.                    \tag{7}
\]
The sign in (7) matters. The dilation generator of the graph is
\[
D_F=y\cdot\nabla F-F.
\]
The exact dilation identity says that the corrected outer Pohozaev flux is the **negative** graph-shape derivative. Differentiating (6) therefore gives the positive sign in (7).

## 2. The dimension calculation

Decompose homogeneous graph polynomials under \(O(n-1)\):
\[
F(y)=H_\ell(y)|y|^{2j},
\]
where \(H_\ell\) is harmonic of degree \(\ell\). In this sector, (4), divided by the common bubble factor, is
\[
H_\ell(y)\left(A_{\ell j}|y|^{2j-2}
+B_{\ell j}|y|^{2j}\right),                        \tag{8}
\]
where
\[
A_{\ell j}=\frac{j(2j+2\ell+n-3)}{n-1},
\qquad
B_{\ell j}=\frac{(j+\ell-1)(2j-n+1)}{n-1}.          \tag{9}
\]

On the unit hemisphere, the Dirichlet-to-Neumann eigenvalue for boundary spherical harmonics of degree \(k\ge2\) is
\[
\gamma_k=
\frac{2\Gamma((k+n+1)/2)\Gamma(k/2)}
{\Gamma((k+n)/2)\Gamma((k-1)/2)}.                  \tag{10}
\]
The degree-one source vanishes by kernel orthogonality. The inverse multiplier in degree zero is zero. Thus (8)–(10) determine every matrix in (7).

Here are the resulting facts.

### Low-dimensional sign

For every \(3\le n\le18\), all the convergent harmonic blocks of (7) involving graph degrees \(k<n/2\) are positive definite.

This includes the \(\ell=0\) and \(\ell=1\) sectors. Only the constant, linear, and radial quadratic graph polynomials are conformal gauge terms; higher radial and first-harmonic terms must not be discarded.

At the borderline degree \(k=n/2\), the top diagonal is a positive multiple of \(\log R\). Its positivity can also be seen directly: the far-field profile has homogeneity
\[
\rho=1-\frac n2,
\]
and its angular energy is
\[
\int_{\mathbb S^{n-1}_+}
\left(|\nabla\phi|^2+\frac{(n-2)^2}{4}\phi^2\right)>0.
\]
The cross terms with lower degrees converge. The lower block is positive definite, so the Schur complement is positive for large \(R\).

### High-dimensional instability

For each \(19\le n\le32\), a full nondegenerate local minimum of the reduced energy is obtained from
\[
F(y)=H_2(y)P(|y|^2),
\]
using the rational polynomial
\[
P(s)=1-0.46283557s+0.05655270s^2-0.00140805s^3.     \tag{11}
\]
The decimal coefficients in (11) mean the corresponding exact rational numbers.

Both the scale direction and every translation direction were certified. For example, in dimension \(19\), the square of the critical scale lies in
\[
0.90236978< t_*^2<0.90236979.
\]
The scale second derivative and the translation Hessian are strictly positive throughout the certified enclosure.

For every \(n\ge33\), the simpler graph
\[
F(y)=H_2(y)(1-|y|^2)                              \tag{12}
\]
works. If \(C_{ij}\), \(i,j=0,1\), is its two-profile matrix, the required scale inequality is
\[
C_{01}^2>\frac34C_{00}C_{11}.                      \tag{13}
\]
The certificate proves (13) for all real \(n\ge33\), not merely for a finite numerical range. At its smaller scale critical point, put
\[
z=t_*^2,\qquad
A_1=\frac{C_{01}}{C_{00}},\qquad
A_2=\frac{C_{11}}{C_{00}}.
\]
Then
\[
z=\frac1{2A_1+\sqrt{4A_1^2-3A_2}},
\qquad A_1z<\frac12.
\]
The translation Hessian is affine in
\[
\rho=\frac{(T^2)_{aa}}{\operatorname{tr}T^2}\in[0,1],
\qquad H_2(y)=y^TTy.
\]
At its two endpoints the normalized Hessian has the lower bounds
\[
z+\frac2{n+3}>0,
\qquad
(n-17)\left(\frac z{n-1}
+\frac2{(n-1)(n+3)}\right)>0.
\]
Thus the critical point is a full strict minimum.

### Why these are rigorous computations

The infinite spectral sums can be eliminated. In the \(\ell=2\) sector choose weights with \(w_0=1\). They satisfy
\[
\frac{w_{j+2}}{w_j}
=
\left(\frac{j+3}{j+n+1}\right)^2
\frac{2j+n+6}{2j+n+2},                            \tag{14}
\]
and
\[
w_1=
\frac{8(n+4)}{\pi(n+1)^2}
\frac{\Gamma((n+3)/2)^2}
{\Gamma((n+2)/2)\Gamma((n+4)/2)}.                  \tag{15}
\]
Every matrix entry is a polynomial moment in
\[
X=j(j+n+2).
\]
Putting \(z_j=w_j/(2j+n+2)\), the telescoping identity
\[
\frac{z_{j+2}}{z_j}
=\left(\frac{j+3}{j+n+1}\right)^2
\]
gives all these moments by triangular rational recurrences. Consequently matrix entries are rational linear combinations of \(1\) and \(w_1\). For even \(n\), \(w_1\) is rational; for odd \(n\), it is rational divided by \(\pi^2\).

Other harmonic sectors reduce to these same moments. With
\[
K=k(k+n-2),
\]
their relative weights are, up to positive normalization,
\[
\prod_{r=2}^{\ell-1}\bigl(K-r(r+n-2)\bigr)
\quad(\ell\ge2),
\]
and
\[
\frac1{K-(n-1)}\quad(\ell=1),\qquad
\frac K{K-(n-1)}\quad(\ell=0).
\]
The apparent denominators cancel against the source polynomials.

The exact checker verifies all \(78\) convergent blocks in dimensions \(5,\ldots,18\) by positive leading principal minors. Dimensions \(3,4\) and the logarithmic blocks are covered by the argument above. For \(n\ge33\), the determinant inequality reduces to polynomial inequalities: after a rational upper bound for \(w_1\), all relevant Bernstein coefficients are negative. This is checked symbolically after substituting \(n=x+33\).

## 3. Exclusion in dimensions \(3\le n\le18\)

Here are the analytic details converting the sign calculation into compactness.

Consider an isolated simple boundary bubble of height \(M_i\), and set
\[
\varepsilon_i=M_i^{-2/(n-2)},\qquad
b_i=\varepsilon_i^a,\qquad
d=\lfloor n/2\rfloor.
\]
Use a flat conformal chart, write the boundary as \(x_n=F_i(x')\), and normalize
\[
F_i(0)=dF_i(0)=0,\qquad H_i(0)=0.
\]
The last normalization is a bounded local Möbius change and removes the radial quadratic gauge.

For \(R=r/\varepsilon_i\), write
\[
\frac{F_i(\varepsilon_i y)}{\varepsilon_i}
=\sum_{k=2}^{d}A_{i,k}(y)+\text{remainder},
\qquad
A_{i,k}=\varepsilon_i^{k-1}F_{i,k}.
\]
Set
\[
\eta_i^2=
\sum_{k<n/2}|A_{i,k}|^2+
\mathbf1_{\{n\text{ even}\}}|A_{i,d}|^2\log R.       \tag{16}
\]

The degree-\(k\) boundary source is \(O((1+|y|)^{k-n})\). Its dual energy norm is bounded for \(k<n/2\); at \(k=n/2\), its squared norm is \(O(\log R)\). The physical Taylor remainder gives
\[
\|S_{\rm rem}\|_*
\le C\varepsilon_i^dR^{d+1-n/2}
=C b_i r^\theta,
\qquad
\theta=d+1-\frac n2\in\{1/2,1\}.                  \tag{17}
\]

After modulation, the correction is orthogonal to the bubble kernel. The projected Jacobi inverse remains uniformly bounded: the graph form is an \(O(r)\) operator perturbation, controlled by the trace Hardy inequality. Isolated-simple decay gives strong critical-space convergence to \(U\), so the nonlinear remainder is absorbable. Initially this gives
\[
\|v_i-U\|_{\mathcal D^{1,2}}
\le C\eta_i+C_rb_i.                               \tag{18}
\]

The linear profiles satisfy
\[
|D^j\psi_k(y)|\le C(1+|y|)^{k+1-n-j}.
\]
One way to prove this is Kelvin inversion. The transformed source is \(O(|y|^{-k})\), and the local mixed Green kernel is bounded by \(C|x-y|^{2-n}\). Its boundary layer is \(O(|x|^{1-k})\), since \(k<n-1\). At critical degree its energy grows logarithmically, exactly as in (16).

An important point is to retain **all** linear graph terms, not just the low jets. If
\[
Z=aU\frac{|y|^2-1}{1+|y|^2},
\qquad C_n=\frac{(n-2)^2}{4(n-1)},
\]
twice integrating by parts gives the exact identity
\[
\int_{B_R'}S_fZ
=
C_n(1+R^2)^{-(n-1)}
\int_{\partial B_R'}
\bigl((R^2-1)f_r-2Rf\bigr).                       \tag{19}
\]
This is the complete first-shape rim term, including radial degree \(n-1\), which can contribute at mass order.

Subtract (19) from the exact stress identity. Its quadratic term is precisely (7). The remaining estimates can be made on a fixed half-space with the material variable
\[
\widetilde J(f,z)
=J_{\Phi_f^*\delta}(U\circ\Phi_f+z);
\]
one must not differentiate the composition of an arbitrary \(H^1\) correction.

For completeness, a sufficient weighted graph majorant is
\[
N_f^2=\int_{\rm strip}U^2
\left(|D^2f|^2+\frac{|Df|^2}{s^2}+\frac{f^2}{s^4}\right),
\qquad s=(1+|x|^2)^{1/2}.
\]
Polar integration gives
\[
N_f^2\le C(\eta_i^2+b_i^2r^{2\theta}).
\]
The pulled-back coefficients are analytic in \(D\Phi_f\), and
\[
|D\Phi_f-I|+s|D^2\Phi_f|\le Cr.
\]
The exact graph formula
\[
H_f\,d\sigma_f
=\left(\delta_{\alpha\gamma}
-\frac{f_\alpha f_\gamma}{1+|Df|^2}\right)
f_{\alpha\gamma}\,dy
\]
and trace Hardy control the Robin terms. Thus the quadratic-in-correction shape remainder is bounded by \(Cr\|z\|^2\), and the pure graph cubic remainder by \(CrN_f^2\). The semilinear remainder has exponent
\[
\sigma=\min\left\{3,\frac{2n}{n-2}\right\}>2.
\]

The regular outer matching term \(h_i\) satisfies
\[
|h_i|\le C_rb_i^2
\]
near the bubble. Its pairing with a degree-\(k\) source obeys
\[
|\langle A_{i,k}S_k,h_i\rangle|
\le C_r|A_{i,k}|b_i\varepsilon_i^{n/2-k}
=o_i(\eta_i b_i).                                 \tag{20}
\]
At critical degree the factor \(1/\sqrt{\log R}\) gives the last conclusion.

These estimates first give the **coarse** inequality
\[
P_i^{\rm corr}\ge c\eta_i^2-C_rb_i^2.              \tag{21}
\]
Simple decay bounds the left side by \(C_rb_i^2\). Consequently
\[
|F_{i,k}|^2\le C_r\varepsilon_i^{n-2k}
\quad(k<n/2),
\qquad
|F_{i,d}|^2\le \frac{C_r}{\log R}
\quad(n\text{ even}).                             \tag{22}
\]
Thus all boundary jets through degree \(d\) vanish at the limiting point.

Only now pass to the refined limit. If \(M_iu_i\to G\), then
\[
F=O(r^{d+1}),\qquad
G=r^{2-n}
+O\!\left(r^{d+2-n}(1+|\log r|)\right)+O(1).
\]
There is no assumption of a constant-only Green expansion. After the full linear subtraction (19), annular quadratic errors have order \(r^{2d+2-n}\), and cubic errors order \(r^{3d+2-n}\), up to logarithms. Both exponents are positive. The refined estimate is therefore
\[
\liminf_i b_i^{-2}P_i^{\rm corr}
\ge
-Cr^{2d+2-n}(1+|\log r|)^C.                        \tag{23}
\]
Letting \(r\downarrow0\), the corrected limiting flux is nonnegative.

### Isolation and simplicity

These hypotheses are obtained rather than assumed globally.

Point-picking and whole-/half-space bubble classification select centers separated by distances much larger than their bubble scales; comparable-scale centers are merged. Simplicity first yields weak decay. In logarithmic radius, the mean profile satisfies
\[
y''\ge\kappa^2y,\qquad y'\le0,\qquad \kappa\to a,
\]
which gives \(v\le C r^{2-n+\delta}\). Taking \((q-1)\delta<2\) bounds the nonlinear source integral.

For the sharp estimate, let \(A_0=-s^{n-1}\bar v'\), with the mean taken over the actual cap. Moving-cap differentiation and the divergence theorem give, after absorbing \(C\varepsilon_i sA_0\),
\[
A_0(s)\le C+C\varepsilon_i\int_0^sA_0(t)\,dt.
\]
Grönwall gives \(A_0(s)\le Ce^{C\varepsilon_is}\le Ce^{Cr}\), hence the required sharp decay.

If a first later critical radius existed, rescaling there would give a positive harmonic limit
\[
A|x|^{2-n}+H(x)
\]
with \(H\) regular harmonic. The critical-mean condition gives \(H(0)=A>0\). Its half-space Pohozaev flux is
\[
-\frac{(n-2)^2|\mathbb S^{n-1}|}{4}A\,H(0)<0,
\]
contradicting (23).

Likewise, a closest pair of clustering bubbles has comparable heights by the sharp upper bound and the positive Green lower bound. Rescaling their distance gives a harmonic multipole with at least two positive poles. At either pole the regular part is strictly positive, again giving negative flux. Thus there is no clustering.

Interior centers approaching the boundary are treated at the minimum of their nearest-neighbor distance and their boundary distance. The first case is the multipole argument; in the second case the Neumann mirror pole supplies a strictly positive regular part. Boundary blow-up therefore produces an actual boundary pole.

There are now finitely many separated poles. Connected-set Harnack estimates compare their heights and give convergence to a positive Green sum.

### Positive mass contradiction

The Green metric has scalar curvature zero and minimal boundary. By (22), inversion gives asymptotic decay greater than \((n-2)/2\).

There is no spin restriction hidden here. An orientable conformally flat compact manifold has a finite spin cover: its finitely generated conformal holonomy group has a finitely generated linear inverse image in \(\operatorname{Spin}(n+1,1)\); residual finiteness gives a finite-index subgroup avoiding the central element \(-1\). The lifted developing structure is spin.

Apply the spin positive mass theorem with noncompact minimal boundary to the lifted Green metric. Every boundary-end mass is strictly positive unless the original compactification is conformally a hemisphere. Multiple lifted ends also force strict positivity.

The boundary mass term is important. In inverted coordinates write the end as
\[
z_n\ge b(z'),\qquad \widehat g=w^{4/(n-2)}\delta.
\]
Its ADM numerator is
\[
\lim_{R\to\infty}
\left[
-\frac{4(n-1)}{n-2}\int_{S_R^+}\partial_Rw
+2\int_{\partial S_R^+}\partial_Rb
\right].                                         \tag{24}
\]
The full rim term (19) matches the second term in (24). Direct Kelvin transformation gives
\[
\lim P^{\rm corr}
=-\frac{(n-2)^2}{8(n-1)}\,\mathrm{ADMnum}<0,
\]
contradicting (23).

Hence boundary blow-up is impossible for \(3\le n\le18\).

## 4. A single fixed example in every dimension \(n\ge19\)

Choose a smooth bounded convex Euclidean domain with a flat boundary disk. An explicit one is
\[
\Omega_0=\{h(|y|^2)+(s-1)^2<1\},
\]
where
\[
h(v)=
\begin{cases}
0,&v\le1,\\
(v-1)^2e^{-1/(v-1)},&v>1.
\end{cases}
\]
It is smooth and convex, with \(H\ge0\), \(H\not\equiv0\), and an exactly flat bottom disk.

Its Robin quadratic form is coercive. Otherwise normalized functions of energy tending to zero would converge to a constant, while the nonzero nonnegative boundary term would force that constant to vanish. Coercivity persists under sufficiently small \(C^2\) perturbations.

Take disjoint disks centered at \(p_i=2^{-i}e_1\), of radii \(\rho_i=2^{-i-5}\), and
\[
\lambda_i=2^{-(i+I)^2}.
\]
Let \(F\) be one of the stable polynomial profiles above, of degree at most eight. On the bottom disk insert
\[
f_i(y)=\lambda_i^9
F\!\left(\frac{y-p_i}{\lambda_i}\right)
\chi\!\left(\frac{y-p_i}{\rho_i}\right).            \tag{25}
\]
For every derivative order \(k\),
\[
\|D^kf_i\|_\infty\le C_k\lambda_i\rho_i^{8-k}.
\]
Thus \(\sum_i f_i\), extended by zero at its accumulation point, is smooth with every jet zero there. For large \(I\), it gives one fixed smooth positive-type domain \(\Omega\).

At the \(i\)-th bubble scale the graph is
\[
z_n=\epsilon_iF(z'),\qquad \epsilon_i=\lambda_i^8.
\]
The weighted graph Taylor error tends to zero because
\[
\epsilon_i(\rho_i/\lambda_i)^7
=\lambda_i\rho_i^7\longrightarrow0.
\]
The polynomial source is integrable in the dual trace space for \(n>16\). The bubble cutoff error satisfies
\[
\frac{(\lambda_i/\rho_i)^{(n-2)/2}}{\epsilon_i}
=
\lambda_i^{(n-18)/2}\rho_i^{-(n-2)/2}
\longrightarrow0
\quad(n\ge19).                                    \tag{26}
\]

On the complement of the \(n\) bubble modes, the projected linearized operator is uniformly invertible. A contrary sequence has zero weak limit away from the bubble by coercivity, and zero rescaled limit by the half-space kernel classification. The potential tail is small in \(L^{n/2}\), so its energy identity gives a contradiction.

Contraction mapping therefore gives a correction \(\phi_i=O(\epsilon_i)\). Including parameter derivatives, the reduced energy is
\[
J_i(t,\xi)
=J_{\mathbb R^n_+}(U)
+\epsilon_i^2\Psi_F(t,\xi)
+o_{C^1}(\epsilon_i^2).                           \tag{27}
\]
For \(q<3\), the derivative estimate uses the weighted inequalities
\[
|f'(W+z)-f'(W)|W
\le C(W^{q-2}|z|+|z|^{q-1}),
\]
rather than an insufficient bare Hölder operator estimate.

The certified strict minimum of \(\Psi_F\) produces a critical point of \(J_i\), and hence an exact weak solution. Testing with the negative part, followed by coercivity, shows it is nonnegative. Elliptic regularity, the strong maximum principle and the boundary Hopf lemma give a smooth positive solution.

The rescaled correction tends to zero in the trace energy space while the bubble trace has a fixed positive norm. Hence
\[
\max_{\partial\Omega}u_i
\ge c\lambda_i^{-(n-2)/2}\longrightarrow\infty.
\]

Finally, \(\Omega\) is Euclidean and hence locally conformally flat up to its boundary. The tracefree quadratic term of \(F\) makes its boundary nonumbilic at each \(p_i\). Since
\[
\widehat{\mathrm{II}}^{\,0}=e^\varphi\mathrm{II}^{\,0}
\quad\text{under }\widehat g=e^{2\varphi}g,
\]
it cannot be conformally equivalent to a hemisphere.

Thus every \(n\ge19\) belongs to \(\mathcal D\), while the preceding compactness argument excludes every \(3\le n\le18\). Therefore
\[
\boxed{\mathcal D=\{n\in\mathbb Z:n\ge19\}.}
\]

The final combined Python run passed all symbolic, exact-rational and outward-interval assertions; an independent exact-rational finite-minimum computation also passed for every \(19\le n\le32\).

# agent_2: last reply

Completed and peer-checked my assigned exclusion work.

- Certified every relevant low-dimensional spectral block for \(n\le18\).
- Derived the exact full-boundary-graph dilation/rim identity, including high-order terms contributing to mass.
- Established the conditional local sign/jet-vanishing lemma under isolated-simple decay, with the corrected two-stage remainder estimates.
- Checked the global selection/mass reduction and supplied a uniform integral-flux proof of sharp decay.

Main writeup: `workspace/agent2_local_sign_lemma.md`. Runnable certificates and symbolic checks are in the accompanying `agent2_*.py` files.

With the team’s verified fixed-domain constructions in every \(n\ge19\), the resulting set is
\[
\boxed{\mathcal D=\{19,20,21,\ldots\}.}
\]
Nothing remains from my assigned portion.

# agent_3: last reply

Established the local construction mechanism in every dimension \(n\ge19\), including certified scale and translation minima, and peer-checked the exclusion argument for \(3\le n\le18\).

Thus
\[
\boxed{\mathcal D=\{19,20,21,\ldots\}.}
\]

Detailed formulas, proofs, and executable certificate inventory are in `workspace/agent3_results.md`. The team’s analytic arguments now address the previously identified issues involving boundary jets, material coordinates, full boundary-rim corrections, clustered bubbles, and positive mass.

# agent_4: last reply

The construction and peer-reviewed exclusion arguments establish
\[
\boxed{\mathcal D=\{n\in\mathbb Z:n\ge19\}}.
\]

My completed contribution is the fixed-domain construction lemma in `workspace/agent4_construction_lemma.md`, including uniform projected inversion, the nonlinear correction, the \(C^1\) reduced-energy expansion, positivity, and boundary blow-up. Associated symbolic and interval checks are runnable in the shared workspace.

The team has now addressed the previously identified analytic gaps in the low-dimensional exclusion. The lead is completing the combined computational rerun and final proof presentation.