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
