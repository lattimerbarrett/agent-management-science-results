# Direct local graph perturbation lemma (n=19)

This is the analytic construction whose implication conflicts with the problem's stipulated answer. It is stated here in full to permit adversarial review.

Let a=17/2, p=21/17, k=323, b=17/36. Suppose (M,g) has positive first Robin eigenvalue and admits a boundary chart in which g is Euclidean and M={x_n>0}. Put
 E_g(v,w)=int_M (grad v.grad w+c_n Rvw)+b int_boundary Hvw,
 J_g(v)=E_g(v,v)/2-k int_M(v_+)^(p+1)/(p+1).
Positive first eigenvalue and the trace interpolation inequality make E_g equivalent to the H1 norm.

Choose even polynomial F of degrees<=8. For eps>0 let rho=1/log(1/eps), mu=eps^8, R=rho/eps, and perturb boundary in this chart to
 f_eps(x')=eps^9 F(x'/eps) chi(x'/rho),
chi=1 on B1 and supported B2. The metric is unchanged ambient Euclidean metric in the chart, and unchanged elsewhere. Pulling to M by a graph diffeomorphism gives smooth metrics converging C-infinity to g, since each kth derivative of f_eps is bounded by C_k sum_{d<=8} eps^(9-d)rho^(d-k), which tends zero. The first eigenvalue stays positive. After this identification all energy forms, Riesz operators and projections below are those of the perturbed metric, denoted E_{g_eps}, A_{g_eps}; any shorter E_g notation in the reduction means this varying form, whose norms are uniformly equivalent to the fixed H1 norm.

Let sigma=(xi,lambda) range in a fixed small compact set, lambda>0. Let W_eps,sigma be the standard target-normalized bubble centered at eps xi on the old boundary plane, of scale eps lambda, with a fixed smooth cutoff supported in the flat chart and identically one throughout the graph support. In its own rescaled coordinates the graph is mu lambda^-1 F(xi+lambda y) with expanding cutoff. Every bound below is uniform in sigma. Write F_sigma=lambda^-1 F(xi+lambda y).

## Residual
On graph t=mu G(y), put Q=1+|y|^2+mu^2G^2, S=1+mu^2|grad G|^2. For U=(1+|y|^2+t^2)^(-a), direct differentiation gives
 B U=17mu(G-y.grad G)Q^(-19/2)S^(-1/2)
 +b mu[Delta G S^(-1/2)-mu^2 G_iG_jG_ij S^(-3/2)]Q^(-17/2).
For G=F_sigma with cutoff at O(R), |D^jG|<=C(1+r)^(8-j), j<=2. Thus delta=Cmu R7 ->0 and
 ||BU-mu g_G||_{L^(36/19)}<=Cdelta^2mu,
 g_G=17(G-y.grad G)(1+r2)^(-19/2)+b Delta G(1+r2)^(-17/2).
Indeed the pointwise remainder is bounded by Cdelta²mu(1+r)^(-11); this function is in L^(36/19)(R18). Also ||g_G-g_Fsigma||<=C R^(-3/2). Domain surface measure differs by1+O(delta²). The vertical graph map has derivative I+O(delta), and H has L18 norm O(delta), so trace/form constants are uniform. The fixed cutoff's interior residual has H^-1 norm O(eps^a)=O(eps^8.5)=o(mu). Consequently J'(W)/mu converges strongly, after transplantation, to the halfspace functional r_Fsigma(psi)=int g_Fsigma psi. The same estimates after one parameter derivative hold; in particular ||J'(W)||+||partial_sigma J'(W)||=O(mu).

## Projected inverse and correction
Let Z_j=partial_sigma_j W, K=span Z_j, and project using E_g onto Kperp. The operator
 T_eps=Pperp[I-pk A_g^-1(W^(p-1) .)]|Kperp
has inverse bounded independently of eps. A complete concentration proof is in agent3_formal_inverse_reduction.md / agent3_uniform_inverse.md. Its ingredients are: approximate kernel residual O(mu), positivity of A_g, removability of a boundary point for H1, halfspace bubble Jacobi kernel exactly span of parameter derivatives (unit-hemisphere first Neumann spherical harmonics), Rellich on bounded rescaled sets, and U^(p-1) in L^(19/2) with vanishing tails. Fredholm index0 gives surjectivity.

For1<p<2, pointwise |(W+phi)_+^p-W^p-pW^(p-1)phi|<=C|phi|^p, with the corresponding Lipschitz estimate on a small H1 ball. Sobolev embedding and the uniform inverse therefore give a unique projected correction phi_sigma in Kperp with ||phi||<=Cmu and Pperp J'(W+phi)=0. The map is C1 in sigma because the positive-part Nemytskii map is C1 H1->H^-1. Differentiating the fixed point gives only partial_sigma phi=o(1) (a sufficient bound is O(mu^(p-1))+O(mu)); no O(mu) derivative claim is needed. Strong residual profile convergence, transplanted finite-energy Jacobi solutions and the uniform inverse give phi/mu ->v_Fsigma, with L v_Fsigma=-r_Fsigma on the kernel complement.

## Energy
For an ambient bubble define D=|grad U|²/2-k U^(p+1)/(p+1). The domain integral is even in the normal variable, while H U² dS is odd when G is replaced by-G. First graph variation cancels exactly after integration by parts:
 D(y,0)=(b/2)Delta_y(U(y,0)^2).
The volume Taylor remainder is bounded by Cmu³ int |G|³(1+r)^(-38), since |partial_tt D|<=C(1+r)^(-38) for |t|<=delta(1+r). The boundary remainders are bounded by
 Cmu³ int [|grad G|²|D²G|(1+r)^(-34)+|Delta G|G²(1+r)^(-36)].
All three radial integrands, after r17dr, grow at worst r3. Hence the full fixed-bubble shape remainder is O(mu³(1+R4))=O(eps20 rho4)=o(mu²). The old-background/cutoff bubble energy differs from the halfspace constant by O(eps17)=o(mu²).

Taylor expansion in phi has error O(||phi||^(p+1))=o(mu²). The projected equation and phi orthogonality give
 J(W+phi)=J(W)+(1/2)J'(W)[phi]+o(mu²).
Strong profile convergence therefore identifies the leading quadratic with stationary elimination of the bubble's linear shape correction. Conformal transfer to the unit hemisphere gives
 J_red(sigma)=J_bubble-Cmu² Q(F_sigma)+o(mu²), C>0,
uniformly on compact parameter sets. The positive C only records normalization of the target bubble (radius1/2 rather than unit sphere). The exact spectral formula is
 Q(eta)=sum_{L>=2} [(L-1)(L+18)]²/mu_L * ||eta_L||²,
 mu_L=2Gamma(L/2)Gamma((L+20)/2)/[Gamma((L-1)/2)Gamma((L+19)/2)],
 eta(y)=2F_sigma(y)/(1+|y|²).
L0 contribution is zero (Neumann solution is normal coordinate, boundary trace0), L1 forcing vanishes. The source is orthogonal to the bubble kernel, since the boundary operator -(Delta+18) annihilates L1. The spectral derivation and exact maximum certificate are in agent4's notes/scripts.

## Actual solution and robustness
If Q has a strict full local maximum at sigma0, choose a small closed parameter ball with Q(sigma0)>sup_boundary Q+gamma. Uniform C0 energy expansion gives J_red(boundary)>J_red(sigma0)+Cgamma mu²/2 for small eps. A minimizer is interior and critical. The residual lies in K, and its pairing with parameter derivatives has matrix E(Z_i,Z_j)+o(1), since partial phi=o1. The bubble Gram matrix is nonsingular, so all residual coefficients vanish. Thus u=W+phi solves the full modified equation.

Test with u_-: coercivity forces u_-=0. Critical-exponent weak elliptic regularity (Brezis-Kato truncation followed by bootstrap), strong maximum principle and Robin Hopf lemma give u smooth and strictly positive on the closure. Its boundary L^(36/17) mass on an O(eps) cap is bounded below: bubble mass is uniform and phi's trace tends0. Cap area is O(eps18), so max_boundary u>=c eps^-8.5.

For each fixed sufficiently small eps the inverse, contraction, C1 natural-constraint matrix, energy boundary gap and trace lower bound persist under all sufficiently small later smooth metric/domain changes. This gives an OPEN high-peak solution packet, without requiring nondegeneracy of a chosen PDE solution.

## Certified polynomial
F(y)=(y1²-|y|²/18)[1-461|y|²/1000+7|y|4/125-693|y|6/500000].
The exact certificate agent4_exact_full_hessian.py proves Q has a strict full maximum at xi0, lambda in[.951902323,.951902324]. Translation coordinates used there differ by the positive factor lambda, which changes Hessian by positive congruence. Thus the local hypothesis is met.

Together with the robust disjoint-patch diagonal lemma, this appears to prove19 is in D, contradicting the requested conclusion. Every local estimate above has been independently audited by agents2/3/4. The team has requested a source for the alleged empty-set theorem and received none.


---

# Formal projected bubble inverse and nonlinear reduction lemma

This is a standalone analytic lemma, not an assertion about the answer to the
original compactness question. It records all function spaces and the exact
hypotheses used by the local construction. In the application n=19.

## 1. Geometric setting and notation

Fix an integer n>=7 and write
q=2n/(n-2), p=q-1=(n+2)/(n-2), k=n(n-2), a=(n-2)/2.
Thus 1<p<2. Let M be a fixed smooth compact connected n-manifold with boundary.
Let g_e be smooth metrics, identified on M by smooth diffeomorphisms, with
uniformly equivalent H^1 norms and uniform Sobolev and trace Sobolev constants.
Assume g_e converges in C^2 to g_0 and the Robin conformal quadratic form

 E_e(v,w)=int_M(<grad v,grad w>+c_n R_e v w)
             +2c_n int_boundary H_e v w

is uniformly coercive on H^1(M): E_e(v,v)>=c||v||H1^2 with c>0 independent of e.
This follows from C^2 convergence and positivity of the first Robin eigenvalue
of g_0. All norms below can be taken to be ||v||_e=E_e(v,v)^(1/2).

Assume a fixed boundary neighborhood has an ambient Euclidean coordinate
realization for each e, in which g_e=delta and the domain is
{x_n>h_e(x')} intersected with a fixed ball. Suppose the graph converges to
the plane in C^2, h_e(0)=o(e), grad h_e(0)=o(1), and the rescaled graphs
s_e(y')=h_e(e y')/e converge to zero in C^2_loc(R^(n-1)). Smooth coordinate
identifications on the complement converge to those for g_0. Equivalently,
all the following proof needs is this local Euclidean graph description,
uniform global coercivity, convergence of forms against fixed test functions,
and the usual uniform extension/Sobolev bounds. Thus a smooth background
metric outside the flat chart is allowed.

Let S be a compact subset of R^(n-1) times (0,infinity), with parameters
sigma=(xi,lambda). Let chi be a fixed smooth cutoff supported in the flat
chart, equal to one on a smaller fixed chart. Define ambient bubbles and
cut them off by

 U_(e,sigma)(x)=(e*lambda/((e*lambda)^2+|x'-e*xi|^2+x_n^2))^a,
 W_(e,sigma)=chi(x) U_(e,sigma)(x).

They are restricted to the actual graph domain and then pulled back to M.
The old-plane center is intentional; it need not lie on the perturbed boundary.
Changing to the physical boundary center is handled by the complement correction.
For S compact, W and its first two parameter derivatives are uniformly bounded
in H^1; rescaling and the integrable bubble tails prove this directly.
Let Z_j=partial_(sigma_j)W, j=1,...,n, and K_(e,sigma)=span{Z_1,...,Z_n}.
The limit Gram matrices G_jl=E_e(Z_j,Z_l) are positive definite uniformly on S.
Indeed their limits are the homogeneous H^1 Gram matrices of the n independent
halfspace Jacobi fields, related by a compact family of translations/dilations.
Write P for E_e-orthogonal projection on K-perp.

Let A_e^{-1}:H^{-1}(M)->H^1(M) denote the inverse defined by the coercive form.
Here H^{-1} means the dual of the full H^1(M), so boundary sources in H^{-1/2}
are included. For an interior f in L^(q'), q'=2n/(n+2), let i_e^* f be the
unique vector with E_e(i_e^* f,v)=int f v. Its norm is bounded uniformly by
C||f||Lq'. Define

 I_e(u)=u-k i_e^*((u_+)^p),
 J_e(u)=1/2 E_e(u,u)-k/q int (u_+)^q.

Then E_e(I_e(u),v)=J'_e(u)[v]. In particular I_e(u)=0 is the desired weak
PDE with its Robin boundary condition (using positive-part nonlinearity).
Set r_(e,sigma)=I_e(W_(e,sigma)).

## 2. Uniform inverse assertion

Define T_(e,sigma)=D I_e(W)=Id-kp i_e^*(W^(p-1) .), a self-adjoint operator
on (H^1,E_e). There are e_0>0 and C independent of e<e_0,sigma in S such that

 L_(e,sigma)=P T_(e,sigma)|_(K-perp):K-perp -> K-perp

is an isomorphism and ||L^(-1)||<=C.

### Proof, including approximate kernel control

First ||T Z_j||_e ->0 uniformly on S. On each fixed rescaled ball the graph
and metric converge to the flat halfspace, and the rescaled Z_j converges
smoothly to an exact Jacobi field z_j. For compactly supported rescaled tests,
its residual therefore tends to zero in the dual energy norm. To obtain the
full dual norm, cut off at a large rescaled radius R. Terms outside that radius
are bounded by the H^1 tail of z_j, the L^(n/2) tail of U^(p-1), and cutoff
annulus terms. All tend to zero as R->infinity, uniformly in e. Terms involving
bounded scalar/mean curvature gain respectively factors e^2 and e after
rescaling; the fixed physical cutoff contributes O(e^a). These estimates also
hold after the uniformly small graph-coordinate perturbation. This proves the
claimed strong dual residual estimate, not merely weak convergence.

Suppose the asserted lower bound fails. Pass to sequences e_i->0,sigma_i->sigma_*
and v_i in K_i-perp with ||v_i||_i=1 and ||P_i T_i v_i||_i->0. Write
T_i v_i=P_i T_i v_i+sum b_i,j Z_i,j. By self-adjointness,
E_i(T_i v_i,Z_i,l)=E_i(v_i,T_i Z_i,l)=o(1). The uniform positive Gram matrices
imply b_i,j->0, and hence T_i v_i->0 in H^1.

Take the global weak H^1 limit v. Away from the concentration point, W_i tends
to zero uniformly. For a fixed smooth test zeta the nonlinear potential term
int W_i^(p-1) v_i zeta tends to zero: split a fixed small ball about the point,
use Holder with exponents n/2,q,q and small ||zeta||Lq on the ball, and use
uniform decay of W_i outside the ball. Therefore E_0(v,zeta)=0. Density and
coercivity imply v=0. In particular v_i->0 strongly in L^2(M).

Localize to the flat chart and rescale by e_i (with the compact lambda/xi
parameters absorbed into the rescaling). Uniform graph extension operators
and the energy/Sobolev bounds give a weak limit phi in D^(1,2)(R^n_+), with
strong L^2 convergence on each finite halfball after flattening. Testing the
rescaled equation gives

 -Delta phi=n(n+2)U^(4/(n-2))phi in R^n_+,
 partial_n phi=0 on the plane,
 U=(1+|y|^2)^(-a).

Orthogonality E_i(v_i,Z_i,j)=0 passes to homogeneous-gradient orthogonality
of phi to every z_j. To justify the passage, first restrict to a fixed rescaled
ball, use weak convergence there, then make the gradient tails of z_j small.
Lower-order curvature and physical-cutoff terms vanish as above.

The finite-energy Neumann Jacobi kernel is exactly span{z_1,...,z_n}.
For completeness, even-reflect phi across the plane. The even extension belongs
to D^(1,2)(R^n) and solves the full Jacobi equation weakly. Under stereographic
projection and the conformal factor Psi=2^a U it corresponds to w in H^1(S^n)
solving (-Delta_(S^n)-n)w=0. The conformal energy identity proves H^1 membership;
a point has H^1 capacity zero when n>=3, so the equation extends over the
omitted point. The eigenspace is the (n+1)-dimensional first spherical-harmonic
space. Even reflection removes its one coordinate odd across the equator,
leaving n dimensions: tangent translations and dilation. Gradient orthogonality
to this kernel forces phi=0.

Now int W_i^(p-1)v_i^2->0. On a fixed rescaled ball this follows from strong
L^2 convergence. Outside that ball, Holder and the uniform Sobolev bound give

 int_(outside) W_i^(p-1)v_i^2
 <= (int_(outside) W_i^q)^(2/n) ||v_i||Lq^2.

The first factor is bounded by the corresponding standard fullspace bubble
tail, which tends to zero as the rescaled radius tends to infinity. But testing
T_i v_i->0 against v_i gives
1-kp int W_i^(p-1)v_i^2->0, a contradiction.

This proves the uniform lower bound. For each fixed e,sigma, multiplication by
W^(p-1) followed by i_e^* is compact on H^1: W is smooth bounded and the
H^1->L^2 embedding is compact. Thus L=Id-compact is Fredholm of index zero
on K-perp. Its lower bound implies injectivity and closed range, and index zero
implies surjectivity. This completes the inverse proof.

## 3. Contraction and the exact parameter regularity needed

Assume, in addition, sup_(sigma in S)||r_(e,sigma)||_e<=C_0 mu_e with mu_e->0.
Then there is a unique small solution phi_(e,sigma) in K_(e,sigma)-perp of

 P I_e(W+phi)=0,    ||phi||_e<=C_1 mu_e.

Uniqueness here means in a fixed ball of radius C_1 mu_e, with C_1 chosen large
enough and e small enough. To prove it, write
N_W(phi)=(W+phi)_+^p-W^p-pW^(p-1)phi. For 1<p<2,

 |N_W(phi)|<=C|phi|^p,
 |N_W(phi)-N_W(psi)|<=C(|phi|^(p-1)+|psi|^(p-1))|phi-psi|.

Since p*q'=q and H^1 embeds uniformly into L^q, these imply the corresponding
H^{-1} estimates with ||phi||H1^p and the Lipschitz factor
C(||phi||H1+||psi||H1)^(p-1). The projected equation becomes

 phi=-L^(-1)P[r-k i_e^*N_W(phi)].

The right side maps the radius C_1 mu_e ball into itself and has contraction
constant O(mu_e^(p-1)). This proves existence and uniqueness. Furthermore

 phi=-L^(-1)P r+O_H1(mu_e^p).

The map u->u_+^p is continuously Frechet differentiable L^q->L^(q'), with
Holder continuous derivative of exponent p-1. The bundle K_(e,sigma) has
C^1 orthogonal projections with uniformly bounded parameter derivatives,
because the Z_j and their derivatives are uniformly bounded and the Gram
matrices are uniformly nonsingular. Locally trivialize K-perp to a fixed
closed subspace, for example using the nearby orthogonal projections; finitely
many charts cover S. The derivative in phi of the projected equation is
L+O(mu_e^(p-1)), so it is uniformly invertible. The Banach implicit function
theorem gives C^1 dependence of phi on sigma for every fixed e.

If sup_sigma ||partial_sigma r||_e=o(1), then sup_sigma||partial_sigma phi||_e=o(1).
Indeed differentiate in the trivialized bundle. Terms from differentiating
the projection/bundle are O(mu_e); the differentiated residual is o(1); and
the nonlinear derivative difference satisfies

 ||[f'(W+phi)-f'(W)] partial_sigma W||H-1
 <=C||phi||H1^(p-1)||partial_sigma W||H1=O(mu_e^(p-1)).

Uniform inversion proves the assertion. In our setting partial_sigma r=T Z_j,
which is o(1) by Section2. Thus no stronger differentiated residual estimate is
needed. If partial_sigma r=O(mu_e), the argument gives the sufficient bound
O(mu_e^(p-1))+O(mu_e), NOT an automatically justified O(mu_e) bound.

## 4. Natural constraint, positivity and smoothness

Set j_e(sigma)=J_e(W+phi). This is C^1. The projected equation says that
I_e(W+phi)=sum b_l Z_l. At an interior critical point of j_e,

 0=partial_(sigma_j)j_e
  =sum b_l E_e(Z_l,Z_j+partial_(sigma_j)phi).

The coefficient matrix is the Gram matrix plus o(1) and hence nonsingular.
Consequently b=0 and u=W+phi is a full weak solution.

Testing the full equation with u_-=max(-u,0) gives
-E_e(u_-,u_-)=k int(u_+)^p u_-=0. Coercivity implies u_-=0. The solution is
not identically zero because ||W||_e is bounded below and ||phi||_e->0.
Standard local truncation iteration gives regularity: u^(p-1) belongs to
L^(n/2), and on sufficiently small coordinate patches its high-value part has
arbitrarily small L^(n/2) norm. Testing with truncated powers and using the
Sobolev/trace inequality absorbs that part and iteratively gives u in every
finite L^r. The linear elliptic Robin estimates then give W^(2,r), hence
C^(1,alpha). Strong maximum principle gives u>0 in the interior. A boundary
zero would, by the boundary Hopf lemma, have strictly negative outward
normal derivative, contradicting the Robin condition at u=0. Thus u>0 on
M closure. The nonlinearity is smooth on the positive range, and elliptic
bootstrapping gives u smooth up to the smooth boundary.

## 5. Matching a limiting correction and the quadratic energy

Suppose a family V_(e,sigma) in K-perp is obtained by transplanting a finite
energy limiting halfspace solution, with ||V||=O(1), and

 ||L V-P r/mu_e||_e=o(1)

uniformly on S. This matching condition follows in the application by smooth
convergence on finite rescaled balls and small H^1/source tails; no parameter
derivative convergence is required. Uniform inversion and Section3 give

 ||phi/mu_e+V||_e=o(1).

Taylor's formula in u, with 1<p<2, gives

 J_e(W+phi)=J_e(W)+E_e(r,phi)+1/2 E_e(T phi,phi)+O(||phi||_e^q).

Because phi lies in K-perp and L phi=-P r+O(mu_e^p), this becomes

 J_e(W+phi)=J_e(W)-1/2 E_e(P r,L^(-1)P r)+O(mu_e^q).

Thus the limiting correction energy is identified by the transplanted linear
solution, with error o(mu_e^2). This is the exact reduction used for the shape
quadratic. One need not posit a positive linearized quadratic form: its single
negative direction is invertible, and the relevant forcing sector has the
explicit spectral sign computed separately.

## 6. Minimal hypotheses versus verification in the degree8 patch

For h_e(x')=e^9 F(x'/e) chi(x'/rho_e), deg F<=8 and rho_e=1/log(1/e),
all fixed C^k norms tend to zero. The rescaled local graphs are mu_e F_R,
mu_e=e^8, R=rho_e/e, so they converge to zero smoothly on finite balls.
The exact graph residual calculation gives ||r||=O(mu_e), and its normalized
source converges in the dual trace space L^(36/19) when n=19. The fixed global
cutoff contributes O(e^(17/2))=o(mu_e). Transplanting the finite-energy shape
Jacobi solution verifies Section5 by finite-radius convergence plus tails.
Every hypothesis used above is therefore among the explicit independently
checked local estimates, rather than an assumed arbitrary-boundary
compactness theorem.


## 7. Additional adversarial audit: avoid differentiating T_sigma

When p<2, one must NOT assert that sigma->T_sigma is C^1 in operator norm
by differentiating W^(p-1); this could introduce W^(p-2). No such assertion
is needed anywhere above. The complete map G(sigma,phi)=P_sigma I(W_sigma+phi)
is C^1 because u->u_+^p is C^1 from H^1 to its dual, W is C^1 in H^1,
and the finite-rank projection P is C^1. Its phi derivative is uniformly
invertible on the moving complement, so the C^1 conclusion is valid directly.

There is an explicit projection-level derivative estimate. Differentiate
phi=P phi to obtain (Id-P) partial_sigma phi=(partial_sigma P)phi=O(mu).
Next differentiate P I(W+phi)=0. Since ||I(W+phi)||=O(mu),
||partial_sigma P||=O(1), and

 ||[D I(W+phi)-D I(W)] Z|| <= C mu^(p-1)||Z||,

uniform inversion of P D I(W+phi)|K-perp gives

 ||P partial_sigma phi|| <= C(||T Z||+mu+mu^(p-1))=o(1).

The component outside K-perp is already O(mu), proving the full o(1) bound.
This does not differentiate T or its inverse and uses only the demonstrated
strong approximate-kernel estimate ||T Z||=o(1).

The elementary pointwise bound behind this estimate follows from concavity:
for 0<alpha=p-1<1, |s_+^alpha-t_+^alpha|<=|s-t|^alpha. Thus
|f'(W+phi)-f'(W)|<=p|phi|^(p-1); Holder with p/q=1/q' gives exactly the
claimed critical H^1-to-dual estimate, with no hidden subcritical embedding.


---

# Spectral boundary-shape lemma and exact n=19 full-maximum certificate

This document supplies the complete analytic normalization and the finite exact
arithmetic certificate behind agent4's contribution. It does NOT by itself
assert compactness or noncompactness of the original PDE. The connection to
solutions on one fixed domain requires the separate analytic reduction and
diagonal lemmas.

## 1. Conventions and functional

Let D=S^n_+ have the UNIT round metric, Sigma=S^(n-1), R=n(n-1),
m=n-1, a=4(n-1)/(n-2), q=2n/(n-2). The normal points out of D.
Consider the unconstrained action

 J_D(w)=int_D [a|grad w|^2/2 + R w^2/2 - R(w_+)^q/q]
                  + int_Sigma H w^2.                    (1)

Its Euler equation is -a Delta w+Rw=R(w_+)^(q-1),
a partial_nu w+2Hw=0. Thus w=1 is critical on D. The interior Hessian
at1 is a(-Delta-n), and its quadratic form is

 A(v,z)=int_D (grad v.grad z-nvz).                       (2)

The Neumann kernel K is spanned by the restrictions of x_1,...,x_n,
the coordinate functions tangent to the equator in R^(n+1). Indeed the
Neumann spectrum is obtained by even reflection across the equator from the
round-sphere eigenvalues k(k+n-1). Constants have negative, but nonzero,
Hessian eigenvalue. On the L2-orthogonal complement of K, the Hessian has
a bounded inverse H1 -> (H1)*. This follows from its spectral decomposition,
or the coercivity of -Delta+1 plus a finite-rank spectral correction.

Let D_t be the normal graph t f over Sigma and pull functions back using any
smooth extension of the boundary deformation. Since1 is constant, the
first-order conformal variation is unambiguously w_t=1+t v+O(t^2).
The trace mean-curvature derivative is

 H'[f]=-(Delta_Sigma+m)f =: T f.                         (3)

For example the constant normal graph is a parallel latitude; its mean
curvature derivative is -m, verifying the sign with the stated outward normal.

## 2. Exact joint second variation

For w=1, equation(1) becomes

 J_Dt(1)=(R/n)Vol(D_t)+int_boundary(D_t) H_t.

The first variation is (R/n)int f + int Tf=0, since R/n=m.
Reflection in the equator maps D_t to the complement of D_-t. Thus both
Vol(D_t)-Vol(D) and int H_t are odd functions of t. Their second derivatives
are zero. In particular the pure-domain second variation is zero for EVERY
smooth f, not only volume-preserving f.

The first w-variation at1 on D_t is only the boundary term
2int H_t z: the interior Euler expression vanishes identically on every
round subdomain. Consequently the mixed derivative is 2int (Tf)z.
The w-w second derivative is a A(v,v). Combining the three Hessian blocks,

 d^2/dt^2 J_Dt(1+t v)|_0 = a A(v,v)+4int_Sigma (Tf)v.    (4)

This calculation does not impose a volume constraint, and therefore does
not discard or incorrectly minimize over the negative constant conformal mode.

The projected first-order correction v=v_f is characterized by

 A(v,z)=-(2/a)int_Sigma (Tf)z, z in K-perp.              (5)

The right side annihilates K because the boundary trace of K is exactly the
degree1 equatorial harmonics and T annihilates degree1. Thus(5) is also valid
for all z in H1 after fixing v perpendicular to K. Equivalently

 (Delta+n)v=0 in D, partial_nu v=-(2/a)Tf on Sigma.       (6)

Substituting(5) in(4) gives J''=-a A(v,v).

## 3. Boundary Dirichlet-to-Neumann eigenvalues

For a boundary spherical harmonic Y_L of degree L>=2, use theta in[0,pi/2]
for distance from the north pole. A regular solution of(Delta+n)v=0 with
this angular dependence is

 v(theta,omega)=(sin theta)^L
   2F1((L-1)/2,(L+n)/2;L+n/2;sin^2 theta) Y_L(omega).    (7)

Substitution in the polar-coordinate Laplacian verifies the hypergeometric
ODE. Set A=(L-1)/2, B=(L+n)/2, C=L+n/2. Then C-A-B=1/2.
Gauss's continuation formula at1 says that the scalar factor at the equator
has expansion A0+B0 cos theta+O(cos^2 theta), with

 A0=Gamma(C)Gamma(1/2)/(Gamma(C-A)Gamma(C-B)),
 B0=Gamma(C)Gamma(-1/2)/(Gamma(A)Gamma(B)).

The outward derivative is partial_theta, so the DN ratio is -B0/A0:

 mu_L=2 Gamma(L/2)Gamma((L+n+1)/2)
          /[Gamma((L-1)/2)Gamma((L+n)/2)] >0.            (8)

All gamma arguments in(8) are positive. For L=1 the Neumann solution is a
first harmonic and has zero normal derivative, as expected. For L=0 the
Dirichlet problem resonates, so one must NOT assign it a finite DN value.
Instead handle its Neumann problem directly: for f=f0 constant,
Tf=-m f0 and v=-(2m/a) f0 x_(n+1) solves(6). Its boundary value is0;
therefore A(v,v)=int_Sigma v partial_nu v=0. Degree1 f gives Tf=0.
These two modes have zero shape quadratic, without any missing radial term.

For general f, write f=sum f_L in boundary spherical harmonics and define

 Q(f)=sum_(L>=2) [(L-1)(L+n-1)]^2/mu_L * ||f_L||L2^2.    (9)

The L>=2 contribution to v's boundary value is
-(2/a)mu_L^-1 (L-1)(L+n-1) f_L. Green's identity and angular orthogonality,
including the L0 calculation, give

 A(v_f,v_f)=(4/a^2) Q(f).

Thus the projected shape action has exact Hessian and Taylor coefficient

 J''=-(4/a)Q(f),
 J_reduced(D_t)=J_D(1)-(2/a)t^2 Q(f)+o(t^2).             (10)

The principal growth mu_L~L follows from gamma-ratio asymptotics, so Q is a
continuous quadratic form on H^(3/2)(Sigma), zero exactly on degrees0,1.
This also extends(9)-(10)'s quadratic form by density to H^(3/2) shapes.
Only the quadratic form, not the nonlinear domain expansion, is asserted by
that density statement.

## 4. Stereographic shape normalization and polynomial cutoffs

On the equator under unit-sphere stereographic coordinates x in R^m,

 Omega=2/(1+r^2), z=(1-r^2)/(1+r^2),
 sin theta=2r/(1+r^2), r=sin theta/(1+z), Omega=1+z.

An OUTWARD Euclidean normal displacement t F changes spherical outward
normal height at first order by t eta, eta=Omega F. If instead the graph
is written vertically as x_n=t F with domain x_n>t F, its outward
normal height is -t eta. This harmless GLOBAL sign disappears in Q,
because Q(-eta)=Q(eta). There is NO angular-degree-dependent factor2.
For F=r^(2j)H_l(x), H_l homogeneous harmonic of degree l,

 eta=(sin theta)^l (1-z)^j(1+z)^(1-l-j)H_l(omega).       (11)

At z=0,r=1,Omega=1, both sides equal H_l(omega), a useful normalization check.
The target-normalized Euclidean bubble U=(1+r^2)^(-(n-2)/2) compactifies to a
radius1/2 hemisphere, not a unit hemisphere. Passing to the unit hemisphere
changes all actions/quadratics by an overall positive factor. There is no
l-dependent factor and none is used below.

At center xi and scale lambda, set y=(x-xi)/lambda. The unit-sphere conformal
factor becomes2/[lambda(1+|y|^2)], so the shape profile is exactly

 eta_(xi,lambda)(y)= [2/(1+|y|^2)] lambda^-1 F(xi+lambda y). (12)

For n19,m18, a degree d<=8 polynomial transforms near the omitted pole to
eta=O(s^(2-d)), with s distance from that pole. Cut it off at Euclidean
radius R. For the removed tail one has

 ||tail||H1=O(R^-2), ||tail||H2=O(R^-1)

in the worst case d8 (lower degrees decay faster). These follow by integrating
|D^k eta|^2=O(s^(4-2d-2k)) against s^17 ds, including the cutoff annulus.
Interpolation yields ||tail||H^(3/2)=O(R^-3/2). Therefore Q of cutoff profiles
converges to Q of the full polynomial, uniformly with any fixed finite number
of xi/lambda derivatives on compact parameter sets; those derivatives do not
increase the polynomial degree or its coefficient bounds.

### Exact transfer of the original Euclidean action

Here write A=4(n-1)/(n-2) to avoid confusion with the bubble exponent.
Let U=(1+|x|^2)^(-(n-2)/2), gbar=U^(4/(n-2))delta (radius1/2),
and gunit=4gbar. On ANY smooth deformed domain, integration by parts gives

 int A|grad(Uw)|^2+2int H_delta U^2w^2
 =int [A U^2|grad w|^2-A U Delta U w^2]
            +int_boundary [A U partial_nu U+2H_delta U^2]w^2
 =int_gbar [A|grad w|^2+R_gbar w^2]+2int_boundary_gbar H_gbar w^2.

Thus no additional boundary energy or flux is omitted by conformal transfer.
Also int (Uw)^q dx=int w^q dV_gbar, and A n(n-2)=4n(n-1)=R_gbar.
Consequently for the ORIGINAL target-normalized Euclidean action J_delta,

 J_delta(Uw)=J_gbar(w)/A=J_unit(w)/[A 2^(n-2)].

Here J_unit is exactly(1); scaling gunit=4gbar multiplies its action by
2^(n-2). Therefore(10) transfers with the explicit positive coefficient

 J_delta,reduced=J_delta,bubble-[2^(3-n)/A^2]t^2 Q(eta_unit)+o(t^2).

This is an identity on each deformed domain, not merely an asymptotic claim.
The outward-normal sign eta_unit=+/-2F/(1+r^2) disappears in Q.

## 5. Exact Jacobi-polynomial matrix representation

From now on n19,m18. For angular degree l, put alpha=l+8 and
P_k=P_k^(alpha,alpha), the standard Jacobi polynomial, not an orthonormal one.
The boundary harmonic with angular factor H_l(omega) is
(sin theta)^l P_k(z) H_l(omega), of total degree L=k+l. Its z-norm is

 h_k=2^(2alpha+1)/(2k+2alpha+1)
        *Gamma(k+alpha+1)^2/[Gamma(k+1)Gamma(k+2alpha+1)]. (13)

For g_j(z)=(1-z)^j(1+z)^(1-l-j), let
I_kj=int_-1^1 (1-z^2)^alpha g_j(z)P_k(z) dz.
Then, for a normalized angular factor, the raw shape Gram matrix is

 A_l,ij^raw=sum_k e_(k+l) I_ki I_kj/h_k,
 e_L=[(L-1)(L+18)]^2/mu_L for L>=2, e0=e1=0.            (14)

The physical angular norm must still multiply this raw matrix.
Formula(14) follows simply by expanding g_j in the orthogonal Jacobi basis
and then applying(9). No additional stereographic factors occur.

Useful moments, obtained from Rodrigues's formula by k integrations by parts,
are, for p positive integer,

 int (1-z^2)^alpha(1+z)^(-p)P_k(z) dz
 =(-1)^k 2^(2alpha-p+1)
 Gamma(k+alpha+1)Gamma(alpha-p+1)Gamma(k+p)
 /[Gamma(p)Gamma(k+1)Gamma(k+2alpha-p+2)].               (15)

Here alpha-p+1>0 in every moment used below. Expand(1-z)^j=[2-(1+z)]^j
and apply(15). The beta=0 term for l1 is supported at k0 only and is killed
by e1=0. Formula(15) can also be checked by the beta integral and the terminating
hypergeometric expression for P_k.

For l2, j0..3, divide these moments by the j0 moment. The resulting polynomials
are

 P0(k)=1,
 P1(k)=(k^2+21k+11)/9,
 P2(k)=(k^4+42k^3+467k^2+546k+264)/144,
 P3(k)=(k^6+63k^5+1372k^4+11319k^3+22855k^2
                             +26166k+10296)/3024.       (16)

Set C0=(9!)^2/4 and the strictly positive common weight

 w_k=(2k+21)(k+1)^2(k+20)^2
                [Gamma((k+1)/2)/Gamma((k+22)/2)]^2.     (17)

Duplication of Gamma shows A2,ij^raw=C0 sum w_k Pi(k)Pj(k).
All other radial matrices needed for translation Hessians reduce to this
same weight by shifting their index. Define

 R1(k)=(0, 2, (k^2+19k+2)/4,
             (k+1)(k+2)(k+17)(k+18)/56
                         -3(k+1)(k+18)/4+6),
 R3(k)=(1, (k+2)(k+21)/18-1,
             (k+2)(k+3)(k+20)(k+21)/432
                         -(k+2)(k+21)/9+1).

Then, with indices0..3 for A1 and0..2 for A3,

 A1,ij^raw/C0 = sum_(k>=0) w_k (k+1)(k+20)/324
                                      R1_i(k+1)R1_j(k+1),
 A2,ij^raw/C0 = sum_(k>=0) w_k Pi(k)Pj(k),
 A3,ij^raw/C0 = sum_(k>=0) w_k k(k+21)R3_i(k-1)R3_j(k-1). (18)

These identities follow directly from(13)-(15); equivalently compare equal
total degrees L for adjacent angular blocks. The k0 term of the last line
is0. The zero first row/column in A1 is the linear graph kernel.

## 6. Exact summation, with no unbounded numerical series

For every polynomial target p(k) in(18), its degree is at most12. The weight
satisfies exactly

 w_(k+2)/w_k = r(k)=(2k+25)(k+3)^2/[(2k+21)(k+20)^2],
 w0=8400*pi/(10!)^2,
 w1=23*4*441*(4^11*11!/22!)^2/pi.                       (19)

Find a polynomial B(k) such that

 (k+18)^2 B(k)-(k+3)^2 B(k+2)=(2k+21)p(k).              (20)

For every target used, B of degree at most12 exists. The exact executable
certificate constructs it by descending powers: the leading coefficient of
(20)'s left side applied to k^z is30-2z, at degree z+1. Therefore set
b_z=[current remainder]_(z+1)/(30-2z), subtract its contribution, and descend.
The final remainder is tested to be the zero polynomial, with rational
arithmetic, for every entry in all three matrices. This is a finite polynomial
identity certificate, not a numerical test.

Put q(k)=(k+18)^2 B(k)/(2k+21). Equations(19)-(20) say
q(k)-r(k)q(k+2)=p(k). Since w_k=O(k^-16) and q(k)=O(k^13), the telescoping tail
vanishes. Hence every infinite sum in(18) has the exact evaluation

 sum_(k>=0) w_k p(k)=w0 q(0)+w1 q(1).                 (21)

Thus all matrix entries belong to Q*pi+Q/pi and are computed exactly.
As an additional independent check, their numerical values agree with direct
spectral sums through100000 modes in relative error below9e-12. This numerical
agreement is not used in the certificate.

## 7. Translation algebra and angular norms

Let s=|y|^2,t=y1 and define solid spherical harmonics in R^m:
H1=t, H2=t^2-s/m, H3=t^3-3ts/(m+2).
Under normalized angular measure on S^(m-1), their squared norms are

 N1=1/m,
 N2=2(m-1)/[m^2(m+2)],
 N3=6(m-1)/[m(m+2)^2(m+4)].                            (22)

These follow from E[t^(2r)]=(2r-1)!!/[m(m+2)...(m+2r-2)].
For j>=0 write

 b_j=2(m-1)/m+4j(m-1)/[m(m+2)],
 k_j=2j b_j+6jm/(m+2)+12j(j-1)m/[(m+4)(m+2)].          (23)

Direct harmonic decomposition gives

 partial1(s^jH2)=b_j s^jH1+2j s^(j-1)H3,
 projection_l2 partial11(s^jH2)=k_j s^(j-1)H2,
 Delta(s^jH2)=2j(m+2j+2)s^(j-1)H2.                    (24)

For the sum over all coordinate first derivatives, use
partial_a(s^jH2)=(1+2j/(m+2))s^j partial_a H2
                       +2j s^(j-1)H3,a,
H3,a=y_aH2-s partial_aH2/(m+2). Orthogonality gives

 sum_a ||partial_aH2||^2=2(m+2)N2,
 sum_a ||H3,a||^2=mN2/(m+2).                           (25)

These identities can be checked from homogeneity and angular integration;
agent3_harmonic_translation_checks.py also verifies(22)-(24) symbolically.

## 8. Polynomial witness and full Hessian

Choose

 F(y)=H2(y)[1-461 s/1000+7 s^2/125-693 s^3/500000],
 c=(1,-461/1000,7/125,-693/500000).

Use center parameter zeta=xi/lambda and set
F_lambda(y)=lambda^-1 F(lambda y)=sum_(j=0)^3 v_j s^jH2,
v_j=c_j lambda^(2j+1). Define E(lambda)=Q(Omega F_lambda)/|S17|.
Let A1,A2,A3 denote the exact raw matrices(18), including C0. Then

 E=N2 v^T A2 v.

At center0, the first translation variation vanishes by evenness. Define
u1_j=b_jv_j (j0..3), u3=(2jv_j)_(j1..3),
sec=(k_jv_j)_(j1..3) followed by0,
u1sum_j=(1+2j/(m+2))v_j,
lap=(2j(m+2j+2)v_j)_(j1..3) followed by0.
The translation Hessian in the parallel direction and its trace, divided
by the same area |S17|, are

 Hparallel=2[N1 u1^T A1 u1+N3 u3^T A3 u3+N2 v^T A2 sec],
 Htrace=2N2[2(m+2)u1sum^T A1 u1sum
                    +m/(m+2)u3^T A3u3+v^T A2 lap],
 Hperp=(Htrace-Hparallel)/(m-1).                        (26)

This is the identity second_derivative Q(F)=2Q(F',F')+2Q(F,F''),
combined with(24)-(25). The scale Hessian is E''.
Since F is even in every coordinate and invariant under rotations of its
last17 coordinates, all scale-center mixed Hessian entries vanish at center0;
the center Hessian is diag(Hparallel,Hperp I17).

The exact script computes the matrices by(20)-(21), constructs(26), and then
uses rational interval arithmetic to certify

 lambda_* in[951902323/10^9,951902324/10^9],
 E'(left)>8.93061118e-11,
 E'(right)<-8.69877185e-11,
 E'' throughout interval in[-.17629396840,-.17629369241],
 Hparallel throughout interval in[-.28156987935,-.28156977858],
 Hperp throughout interval in[-.18010947169,-.18010945685]. (27)

The endpoints in(27) are outward rounded for display; the script's assertions
use exact Fractions, not these printed decimal approximations. To bound pi,
it uses Machin's identity pi=16atan(1/5)-4atan(1/239) and alternating arctangent
series with60 and20 terms. The interval evaluator treats each polynomial
coefficient as alpha*pi+beta/pi, bounds it using those rational pi bounds,
and bounds lambda powers on the positive rational interval. Each sign in(27)
is therefore a finite exact-arithmetic inequality.

By continuity and the sign change there is a root E'=0 in the displayed
interval. Strict negativity of E'' makes it unique there. Parity makes every
center derivative vanish at0, and(26)-(27) make the full Hessian negative
definite. Thus Q has a STRICT FULL LOCAL MAXIMUM at (zeta0,lambda_*).
Changing to the physical center xi=lambda zeta multiplies translation
Hessian by lambda_*^-2 and leaves strict maximality unchanged.

## 9. Reproducibility and scope

Run workspace/agent4_exact_full_hessian.py with SymPy available. It:
- constructs every required target polynomial and exact primitive;
- asserts zero remainder for every telescoping identity;
- builds exact matrices and full Hessian expressions;
- constructs rational pi bounds and asserts all signs in(27).
No floating-point operation contributes to any assertion. Decimal output is
for readability only. The associated txt file records the exact matrices
and Hessian polynomials.

The overall action coefficient from(10) is negative and nonzero. Passing
between unit and radius1/2 hemispheres changes it by a positive constant,
so it cannot change this strict maximum into a minimum or remove it.
The result here is a rigorously computer-certified analytic shape lemma.
Whether and how it implies a fixed-domain blow-up sequence is the separate
local-PDE reduction and diagonal-persistence question; no such implication
is smuggled into this algebraic lemma.


---

# Standalone robust-packet persistence and smooth diagonal lemma

This document proves the final global step conditional on a LOCAL projected
bubble construction. It assumes neither nondegeneracy nor isolation of the
resulting solutions of the full PDE. It does not by itself supply that local
construction.

## 1. Uniform projected implicit-function setup

Work on a fixed smooth compact reference manifold X with boundary, using
smooth pullbacks from variable domains. Let h range over an open subset of
C^{m,alpha}(S), m>=4, parametrizing smooth small domain graphs. Let H=H^1(X),
with any fixed equivalent Hilbert norm. For nearby h the quadratic Robin
energies E_h are uniformly coercive and equivalent to this norm. Write

 J_h(u)=1/2 E_h(u,u)-n(n-2)/q int_X (u_+)^q dV_h,
 q=2n/(n-2)>2.

Each J_h is C^2 on H, and its first two derivatives depend continuously on h.
For 2<q<3 its second derivative is Holder continuous, which is sufficient.
Here and below Riesz identifications use the fixed Hilbert structure.

Let K be a closed finite-dimensional Euclidean ball contained in an open
parameter set V. Suppose W:V->H is C^1 and there is a C^1 family of
N-dimensional subspaces Z_z with chosen C^1 frames Z_1(z),...,Z_N(z).
Let P_z be orthogonal projection to Z_z^perp. Since K has a contractible
neighborhood, the complements can be C^1-trivialized locally and patched;
equivalently formulate each equation in its moving complement bundle.

Suppose at h=h0 a C^1 family phi0(z) in Z_z^perp solves

 P_z J'_{h0}(W(z)+phi0(z))=0,

and the derivative of this projected equation with respect to phi, as an
operator Z_z^perp -> Z_z^perp, is invertible for every z near K, with uniformly
bounded inverses on K. Suppose also the natural-constraint matrix

 G_ij(z)=<Z_i(z), partial_j(W+phi0)(z)>_H

is invertible on K. These assumptions concern only the projected equation;
the full linearized PDE may have kernel.

### Uniform continuation claim

For all h in a sufficiently small C^{m,alpha} neighborhood of h0 there is a
C^1 family phi_h(z) in Z_z^perp near phi0(z), z near K, solving the projected
equation. The maps phi_h and their z derivatives converge uniformly on K
to those at h0. The matrices G_h remain invertible.

Proof. Trivialize the complement bundle in a neighborhood of each point of K.
The projected equation is a C^1 Banach-space equation whose phi derivative
is an isomorphism. The parameter implicit-function theorem gives a unique
nearby branch for z and h near that point. Cover K by finitely many such
neighborhoods and decrease the h neighborhood to their intersection.
Uniqueness in smaller overlapping tubes identifies all the local branches.
Compactness gives uniform convergence of branches and first derivatives.
Continuity and the positive lower bound of the least singular value of G
on K preserve matrix invertibility. No full-PDE nondegeneracy was used. QED.

Define U_h(z)=W(z)+phi_h(z) and e_h(z)=J_h(U_h(z)). The chain rule gives

 partial_j e_h=<J'_h(U_h),partial_j U_h>.

The projected equation says J'_h(U_h)=sum_i a_i Z_i. Thus grad e_h=0 and
invertibility of G_h imply a_i=0 for all i, hence J'_h(U_h)=0.

## 2. Robust solution packet from an energy barrier

Suppose there exist z0 in int(K) and gamma>0 such that

 min_{z in boundary K} e_{h0}(z) >= e_{h0}(z0)+gamma.

Uniform continuity from Section 1 implies that, for all sufficiently nearby
h, sup_K|e_h-e_{h0}|<gamma/4. Consequently

 min_boundaryK e_h >= e_h(z0)+gamma/2.

The continuous function e_h attains a minimum on compact K. The displayed
inequality puts every minimizer in int(K). Since e_h is C^1, a minimizer is
critical; the natural-constraint argument yields a full weak PDE solution.

In particular, if for a small fixed epsilon

 e_h0(z)=C_epsilon-A_epsilon Q(z)+o(A_epsilon), A_epsilon>0,

uniformly on K, and Q has a strict local maximum at z0 with a boundary gap,
then for sufficiently small epsilon this is a robust solution packet.
Only uniform C^0 asymptotics are needed to obtain the energy gap; C^1
asymptotics and nondegeneracy of the full PDE solution are not needed.

### Positivity and smoothness

A nonzero critical point u solves
 A_h u=n(n-2)(u_+)^{q-1}, B_h u=0, A_h=-L_h.
Test the weak equation by u_-=max(-u,0). Locality of the quadratic energy
and disjoint supports of u_+ and u_- give

 -E_h(u_-,u_-)=0.

Coercivity implies u_-=0. Thus u>=0. Standard critical elliptic regularity
applies also to this positive-part equation: split u^{q-2} in L^{n/2} into
a bounded part and a tail with arbitrarily small L^{n/2} norm, absorb the
tail in the Sobolev estimate for truncated powers, and iterate. This gives
u in L^r for every finite r. Interior and smooth Robin boundary estimates
then give W^{2,r}, boundedness, and C^{1,alpha} regularity. The strong maximum
principle gives u>0 in the interior for any nonzero solution. If u vanished
at a boundary point, Hopf's lemma would give partial_nu u<0 there, while
B_hu=0 and u=0 give partial_nu u=0, a contradiction. Therefore u>0 on the
compact closure. Its positive minimum makes the nonlinearity smooth in a
neighborhood of its range, and elliptic bootstrap gives u smooth.

Nonzeroness can be guaranteed, for example, by the trace-mass condition below.

### Boundary peak retained without pointwise correction estimates

Put s=2(n-1)/(n-2). Suppose every z in K has a boundary cap A_z with
area<=C epsilon^{n-1}, the approximate bubble obeys
||W(z)||_{L^s(A_z)}>=a>0, and sup_K||phi0(z)||_{H^1}=o(1) as epsilon->0.
The trace inequality gives ||phi0||_{L^s(boundary X)}=o(1). Thus for small
epsilon, ||U_h0(z)||_{L^s(A_z)}>=a/2, uniformly on K. This inequality
persists for all sufficiently close h by H^1 continuation and equivalence
of nearby boundary measures, say with lower bound a/4 and cap area<=2C
epsilon^{n-1}. At any critical point the positive smooth solution satisfies

 max_boundary u >= (a/4)/(2C epsilon^{n-1})^{1/s}
                =c epsilon^{-(n-2)/2}.

Hence a packet can enforce any prescribed finite boundary-height threshold.

## 3. Abstract C-infinity diagonal theorem

Let S be a compact smooth manifold, and let U_j be pairwise disjoint open
sets with compact closures, accumulating only at a point p outside every
closure U_j. Let X be an open subset of C^infinity(S) in its Frechet topology.
Let P_j be domain-properties OPEN in some finite C^{m_j,alpha} topology.
Assume the following insertion property:

For each finite sum h_j supported in U_1 union...union U_j, lying in X and
having P_1,...,P_j, one can find a perturbation f supported in U_{j+1},
arbitrarily small in every prescribed FINITE collection of C^{k,alpha}
norms, such that h_j+f remains in X and has the additional property P_{j+1}.

Then the insertions can be chosen so that a single smooth h_infty in X
has every property P_j.

Proof. At stage j choose an integer M_j>=j+4, increasing in j, large enough
that the known properties P_1,...,P_j and membership in X all persist inside
some C^{M_j,alpha} ball about h_j. (If X is Frechet-open this follows from
its finite-seminorm basic neighborhoods.) Choose r_j>0 such that this ball
of radius r_j lies inside those neighborhoods, with

 r_j<=2^{-j}, and r_j<=r_{j-1}/4 for j>1.

Use the insertion property to demand

 ||h_{j+1}-h_j||_{C^{M_j,alpha}}<r_j/2,

and, if necessary, all further finite smallness conditions needed to choose
r_{j+1} after constructing h_{j+1}. Because M_j tends to infinity and
r_j<=2^{-j}, the sequence is Cauchy in each C^{k,alpha}. The limits agree
under inclusions and define a common smooth h_infty.

For fixed j, monotonicity M_i>=M_j for i>=j and r_i<=r_j/4^{i-j} imply

 ||h_infty-h_j||_{C^{M_j,alpha}}
 <=sum_{i>=j} r_i/2 <=(2/3)r_j<r_j.

Thus h_infty is in every persistence neighborhood and has every P_j.
Also h_infty belongs to X. Each h_j is identically zero near p, so all its
jets at p vanish. Convergence in all C^k gives D^k h_infty(p)=0 for every k.
This proves smooth flatness at the accumulation point without a separate
analyticity assumption. QED.

The assumption can be initialized by h0=0 and constructing P1 in U1.
If P_j is a robust LS packet with height>j, Sections 1-2 establish exactly
the openness required here. On the limit domain choose one resulting
positive smooth solution from each packet. Their boundary maxima exceed j.

## 4. Euclidean domain geometry and all global hypotheses

Take S to be the unit sphere in R^n, and h a sufficiently small C^2 normal
graph. Its bounded domain is smooth and diffeomorphic to a ball; in
particular its closure is compact and connected with nonempty boundary.
The Euclidean metric is flat, hence LCF up to every boundary point.

Smallness in C^2 retains strictly positive trace mean curvature H>=h_*>0.
For this metric R=0, and its Robin energy is

 E(v,v)=int_Omega |dv|^2 + alpha_n int_boundaryOmega H v^2,
 alpha_n=(n-2)/(2(n-1))>0.

This has positive first L^2 eigenvalue. Indeed if normalized L^2 functions
had energy tending to zero, their gradients would tend to zero. Poincare
and compact trace imply convergence in H^1 to a nonzero constant, while
the positive boundary term tends to zero, an impossibility. Equivalently,
use the elementary boundary Poincare inequality. This verifies exactly the
positive-Yamabe-type convention in the question.

Because perturbation supports are disjoint, each unused U_j remains an
exact spherical patch after finitely many stages. A local Mobius map sends
it to a planar boundary patch. Its positive conformal factor can be extended
smoothly over the current compact domain; covariance preserves the PDE
and positive type. A local graph insertion can therefore be performed in
a flat planar conformal chart and mapped back to an actual Euclidean domain.
At each finite stage all chart constants may depend on the current domain;
the next epsilon can be chosen afterwards and arbitrarily small.

Suppose the first insertion has II^circ!=0 somewhere, and later disjoint
supports avoid that point. Then the final domain retains II^circ!=0 there.
For ghat=e^{2f}g one has IIhat^circ=e^f II^circ; diffeomorphisms also preserve
umbilicity. The round hemisphere has II^circ=0 everywhere. Thus the final
domain is not conformally equivalent to the round hemisphere.

An explicit compatible support/amplitude schedule is dist(U_j,p) comparable
to 2^{-j}, radii rho_j<=2^{-j-5}, and polynomial patch

 f_j(x)=epsilon_j^9 F((x-p_j)/epsilon_j) chi((x-p_j)/rho_j), deg F<=8.

For every fixed derivative order k,
||D^k f_j||<=C_k sum_{d<=8} epsilon_j^{9-d}rho_j^{d-k}.
At stage j choose epsilon_j sufficiently small for every persistence and
C^{M_j,alpha} budget. The local construction may require rho_j>>epsilon_j;
this is compatible with arbitrarily small epsilon_j. Alternatively choose
rho_j=1/log(1/epsilon_j) after prescribing its upper bound. Both choices
permit all finite budgets and disjoint supports.

## Scope

This proves all global/diagonal and robustness claims, including positivity
and the precise boundary maximum condition, from the single-patch projected
construction and its strict finite-dimensional energy barrier. It does not
assume full-PDE nondegeneracy and does not establish the single-patch
residual estimates or the shape-quadratic maximum; those are separate local
inputs supplied elsewhere in the team's work.


## 5. Independent adversarial recheck of domain continuity

For completeness, the asserted functional continuity has an elementary
coefficient proof. Fix a smooth reference domain and a collar pullback
Theta_h for small normal graphs h. Its metric-density matrix is
sqrt(det g_h) g_h^{-1}, depending continuously on h in C^1. For actual
Euclidean domains scalar curvature is identically zero. The pulled-back
boundary density H_h dS_h depends continuously on h in C^2. Thus, near any
fixed h0,

 |E_h(u,v)-E_h0(u,v)| <= C ||h-h0||C2 ||u||H1 ||v||H1.

The trace inequality controls the boundary contribution. The volume density
in the nonlinear integral differs by O(||h-h0||C1). Holder and Sobolev give,
on every bounded H1 ball, continuity of J_h and its first two u-derivatives,
uniformly on that ball. This is exactly the parameter continuity needed for
the projected implicit-function theorem, including for the positive-part
nonlinearity q>2. The full-PDE derivative need not be invertible.

At a fixed epsilon the packet gap, smallest projected singular value, and
trace mass are strictly positive numbers. They may be arbitrarily tiny as
epsilon tends to zero; this causes no diagonal obstruction, because the
next perturbation can be arbitrarily small in any prescribed finite norm.
The nested-budget construction never needs a uniform lower bound in j.

Finally, C-infinity convergence is not merely pointwise or finite-order:
M_j increases to infinity, so each fixed C^{k,alpha} tail is bounded by a
summable geometric series. Therefore the limit is in every persistence
Banach space and lies strictly inside every specified packet neighborhood.
The energy barrier survives on the limit domain, not merely on finite-stage
domains. Choosing initial packet heights >2j and shrinking persistence
neighborhoods retains >j and handles every stage-dependent conformal chart
factor. This exhausts the possible limit/openness loss in this global step.
