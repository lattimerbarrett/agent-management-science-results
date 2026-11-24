# Sharp boundary Yamabe threshold

The result is D={19,20,21,...}.

The proof below is organized as independently checked components. Standard inputs
are the classification of positive critical bubbles in full/halfspace, elliptic
regularity and Harnack inequalities, Bôcher's theorem, Sobolev/trace Hardy
inequalities, Malcev residual finiteness for finitely generated linear groups,
and the spin positive-mass theorem with noncompact minimal boundary. The new
local estimates, exact boundary normalizations, shape algebra, fixed-domain
construction and global reduction are all given below.

Computer certificates are in the accompanying zip. Run `python run_checks.py`
from its extracted root (requires sympy, numpy, scipy and mpmath). They use
assertions, exact rational interval bounds, and certified infinite-tail bounds,
not guessed numerical signs. The dimension-exclusion and finite-minimum checks
also have entirely exact rational-moment versions.



---

# Geometric side conditions and conformal invariance
Let n>=3 and c=(n-2)/(4(n-1)). The quadratic form of the boundary spectral problem is
Q_g(v)=int_M (|dv|_g^2+c R_g v^2) dv_g+2c int_boundary H_g v^2 ds_g.
This follows from integration by parts with outward normal and B_g v=0.

If (Omega,delta) is a smooth bounded connected Euclidean domain with H>=0 everywhere
and H>0 on a nonempty open subset of its boundary, Q(v)>0 for every v!=0,
and the first eigenvalue is strictly positive. To prove the uniform spectral gap,
suppose int v_j^2=1 and Q(v_j)->0. Poincare's inequality gives v_j-a_j->0 in H1,
and a subsequence a_j converges to a nonzero constant a. The trace theorem gives
boundary L2 convergence, forcing int H v_j^2->a^2 int H>0, contradiction.
The first eigenvalue depends continuously on the metric/domain in C2, by pulling
back to a fixed domain and comparing the quadratic forms and L2 norms. Therefore
positive Yamabe type persists under sufficiently small C2 graph perturbations.

A smooth convex bounded Euclidean domain with an open planar boundary patch and
with H>0 elsewhere can be made by smoothing a convex body having one flat face;
Q positivity follows as above. Such a fixed domain is a convenient unperturbed
background for all local graph constructions.

Under ghat=exp(2f)g, nuhat=exp(-f)nu, and the conformal connection formula yields
IIhat=exp(f)(II+nu(f)g_T),
Hhat=exp(-f)(H+(n-1)nu(f)),
IIhat^0=exp(f)II^0.
In particular a single nonumbilic point rules out conformal equivalence with the
hemisphere. Every Euclidean domain, with its Euclidean metric, is locally
conformally flat up to the boundary by definition.

Conformal covariance, with ghat=w^(4/(n-2))g, is
L_ghat(v)=w^(-(n+2)/(n-2)) L_g(wv),
B_ghat(v)=w^(-n/(n-2)) B_g(wv).
Thus u solves the required nonlinear equation for g iff u/w solves it for ghat.
Since w is fixed smooth positive on a compact manifold, boundary blowup is
preserved by this correspondence. The quadratic forms satisfy Q_ghat(v)=Q_g(wv),
so positivity of the first eigenvalue is conformally invariant as well.


# Virtually spin reduction for conformally flat manifolds
Pass first to the orientable finite cover. A conformally flat structure has a
developing map dev:Mtilde->S^n and holonomy rho:pi1(M)->SO^+(n+1,1).
The holonomy image Gamma is finitely generated because M is compact. Its inverse
image Gamma_tilde in Spin(n+1,1) is a finite extension of Gamma, hence finitely
generated, and is a linear group over characteristic zero. Malcev residual
finiteness supplies a finite-index normal subgroup K not containing the central
nontrivial element -1. The projection K->Gamma is therefore injective, and its
image Gamma' has finite index. The finite cover associated to rho^{-1}(Gamma')
has holonomy lifted to Spin(n+1,1). Pulling the standard conformal spin structure
of S^n through dev and this lifted action gives a spin structure on that cover.
This argument does not require dev to be injective.

Consequently a Green-function blowup of a compact conformally flat manifold can
be lifted to a finite spin cover. If the Green metric is scalar-flat, minimal on
the boundary, complete asymptotically flat with the usual rate and integrability,
apply the spin version of the asymptotically-flat boundary positive mass theorem
to each lifted end. A boundary pole lifts to finitely many boundary ends, with
unchanged individual masses. Zero mass rigidity forces the covering Green
manifold to be a Euclidean halfspace, hence to have exactly one end. Thus if the
cover has degree greater than one all individual masses are strictly positive.
If its degree is one, zero mass implies that the original compactification is
conformally a hemisphere (extension across the missing pole follows from the
smooth conformally flat compactification). This is the strict-mass conclusion
needed in the compactness argument.

The positive-mass input here is the spin case of Almaraz--Barbosa--de Lima,
'A positive mass theorem for asymptotically flat manifolds with a non-compact
boundary', Communications in Analysis and Geometry 24 (2016), 673--715.
One must FIRST establish the Green metric AF regularity and mass identity from
the blowup/jet analysis; the spin-cover argument alone does not establish them.


---

# Uniform bounded-form estimates for localized shape Taylor expansion

Write s=(1+|y|^2+t^2)^(1/2), choose chi(t/(1+|y|)) supported where
t<=2(1+|y|), and Phi_F(y,t)=(y,t+chi F(y)). Work with additive MATERIAL
H1 correction z and comparison bubble U o Phi_F, rather than composing z.
Define
 delta(F)=sup[|DF|+|F|/(1+|y|)+(1+|y|)|D2F|+(1+|y|)^2|D3F|]
and
 N(F)^2=int_{halfspace} U^2[|D2F|^2+|DF|^2/s^2+|F|^2/s^4] on the extension strip.
For the dilation direction DFgen=y.gradF-F include its analogous seminorms;
for finite jets of bounded degree these are bounded by fixed multiples.
For a scaled smooth tangent graph on radius R=r/eps, delta<=C r.

The following direct coefficient estimates justify functional Taylor uniformly
in R. The cutoff deformation is assumed to vanish before the outer cap.

* D Phi-I=O(delta), and s D2Phi=O(delta).
* The pulled-back Dirichlet matrix and volume density are analytic functions
  of D Phi when delta<1/2. Their first variations in the graph/dilation
  directions are O(delta); subsequent directional variations gain another
  graph factor. They multiply grad z.grad z or |U+z|^q, controlled by D-energy
  and Sobolev, uniformly in R.
* H_F dS_F=(delta_ab-F_a F_b/(1+|DF|^2)) F_ab dy. Its difference from Delta F
  is bounded by C|DF|^2|D2F|. Boundary coefficients are bounded by
  C delta/(1+|y|). The trace Hardy inequality controls the quadratic z term.
* On the extension strip |D^j U|<=C_j U s^(-j). Consequently
  ||(Phi_F-Id).gradU||_D<=C N(F), and each extra graph derivative contributes
  delta. This also controls all material terms from U o Phi_F.
* Direct fixed-ambient-U energy is odd under F->-F, so its second graph
  derivative at0 vanishes EXACTLY. The remaining cubic graph derivative is
  bounded by C delta N(F)^2. For example the boundary cubic coefficient is
  |DF|^2|D2F|U^2; after one graph factor is bounded by delta, its remaining
  weighted quadratic integral is bounded by N(F)^2 by tangential integration
  by parts and Cauchy-Schwarz. Bulk terms are treated by the previous U bounds.
* The mixed graph-u derivative at0 is the boundary source S_F, by the exact
  integration-by-parts identity in Slack193. Its variation away from0 is bounded
  by C delta N(F)||z||_D; the second-z shape derivative is bounded by
  C delta||z||_D^2. The energy nonlinearity has C^(2,alpha) modulus,
  alpha=min(1,4/(n-2)), giving O(||z||_D^(2+alpha)); for low n use cubic.

Thus after the EXACT full first-shape rim subtraction the localized Ward
expansion has leading mixed term <S_DFgen,z>, with error bounded by
 C delta [N(F)^2+N(F)||z||_D+||z||_D^2]
 +o(N(F)^2+||z||_D^2).
No derivative/composition of a general H1 correction is taken.

For F=sum eps^(k-1)F_k plus physical Taylor remainder of degree d+1,
radial integration gives
 N(F)<=C[eta+eps^((n-2)/2)r^(d+1-n/2)].
Indeed the degree-k squared radial integrand is r^(2k-n-1), yielding finite
energy for2k<n and logR for2k=n. The remainder has degree d+1 and yields exactly
the stated positive power of physical r. These are the same majorants as the
boundary-source estimates, so the Ward estimate is compatible with the
projected-inverse/cross estimates already established.

Outer matching h must NOT be treated only through its full D norm at the fine
stage. First use the coarse C_r eps^(n-2) bound to force vanishing jets. Then
pass to the normalized Green limit and use F=O(r^(d+1)), G-pole=O(r^(d+2-n))
to bound cap/high-graph quadratic terms by O(r^(2d+2-n)), cubic by
O(r^(3d+2-n)); both tend to0. Full linear terms are retained in the exact rim.


---

# Local sign and jet-vanishing lemma (under isolated-simple decay)

## Statement
Let 3<=n<=18. In uniformly smooth flat conformal charts the lower boundary is
x_n=F_i(x'), with F_i(0)=dF_i(0)=0. Normalize the radial quadratic graph jet to0
by a bounded local Mobius change. Suppose positive solutions have a boundary
bubble at0, epsilon_i=M_i^(-2/(n-2))->0, and on a fixed chart satisfy the
isolated-simple estimates

 u_i(x)<=C M_i^(-1)|x|^(2-n),
 |grad u_i(x)|<=C M_i^(-1)|x|^(1-n),   C epsilon_i<|x|<r0,

and the usual rescaled C^2_loc limit U=(1+|y|^2)^(-(n-2)/2).
After modulation by o(epsilon_i) and scale 1+o(1), the following hold.
(1) All physical boundary Taylor jets of degrees2 through d=floor(n/2) vanish
at the limiting point (apart from the removed conformal gauge).
(2) For every local normalized limit G=lim M_i u_i away from0, its invariant
ADM-corrected Pohozaev flux has limit >=0 at0.

All constants and errors are uniform for graph families bounded in C^(d+5),
uniform simple-decay constants, and bounded conformal-chart equivalence.
In particular the statement is stable under shrinking/rescaling a chart.
Selection, isolation and simplicity themselves are NOT assumptions to hide:
they must be proved separately before using this lemma.

## Proof: notation
Put a=(n-2)/2, b_i=epsilon_i^a, R=r/epsilon_i and v_i(y)=M_i^(-1)u_i(epsilon_i y).
Write f_i(y)=epsilon_i^(-1)F_i(epsilon_i y) and its homogeneous jets
sum_{k=2}^d A_{i,k}(y), where A_{i,k}=epsilon_i^(k-1)F_{i,k}.
Set eta_i^2=sum_{k<n/2}|A_{i,k}|^2 plus |A_{i,d}|^2 logR if n is even.
The omitted graph gauges are constant, linear, and radial quadratic.
All polynomial coefficient norms are equivalent in this finite-dimensional space.

## A. Exact identities, including ALL linear graph terms
Let beta=(n-2)/(2(n-1)), C=(n-2)^2/(4(n-1)), and
Z=a U(s^2-1)/(1+s^2). The Eulerian Robin source is
S_f=(n-2)U[(f-y.grad f)/(1+s^2)+Delta f/(2(n-1))].
Twice integrating by parts gives the EXACT full-graph identity

 <S_f,Z>_(B_R')=C(1+R^2)^(-(n-1))int_rim[(R^2-1)f_r-2Rf].                 (A1)

Indeed use B=C(s^2-1)(1+s^2)^(-(n-1)), A=2(n-1)B/(1+s^2):
A+div(Ay)+Delta B=0 and -B'-sA=-2Cs(1+s^2)^(-(n-1)).
Thus A1 includes high graph jets, including radial degree n-1 mass order.

The critical stress tensor/vector has zero divergence, and integration by parts
with the Robin condition gives its bottom-graph shape term. Equivalently, for
Y=x.grad u+a u, critical scaling u_lambda=lambda^(-a)u(x/lambda) gives

 d/dloglambda J_Omega(u_lambda)=-int_cap partial_nu u Y,
 J_Omega(u_lambda)=J_(lambda^(-1)Omega)(u).

The cap-domain derivative is -int_cap e(x.nu), where
 e=|grad u|^2/2-n(n-2)u^(2n/(n-2))/(2n/(n-2)).
The graph derivative is in direction Df=y.grad f-f. Consequently

 P_outer=-J_shape[Df],                                                     (A2)

with the exact bottom/cap edge term. Its complete linear part at U is A1,
with the same orientation; define P_corrected=P_outer+the A1 rim functional.
One may localize graph deformation to0 nearcap; all errors then live in an annulus.
The full linear annular/edge term is still A1 and is removed BEFORE truncating f.

## B. Uniform correction and profile estimates
Each degree-k source has |S_k|<=C(1+s)^(k-n). For k<n/2 it has bounded trace-dual
L^(2(n-1)/n) norm. At k=n/2 its squared H^(-1/2) norm on B_R is O(logR):
the Newton boundary kernel |y-z|^(2-n) gives constant dyadic self interaction
and shell-separation decay 2^(-h(n-2)/2). Hence ||S_jets||_*<=C eta_i.
Taylor remainder degree d+1 gives

 ||S_rem||_*<=C epsilon_i^d R^(d+1-n/2)=C b_i r^theta,
 theta=d+1-n/2 in {1/2,1}.                                                (B1)

The material displacement T_f=U composed Phi_f-U, with smooth vertical graph
extension Phi_f, satisfies the same bound. Its degree-k radial Dirichlet majorant
is |A_k|^2 int_1^R s^(2k-n-1)ds. Thus ||T_f||_D<=C(eta_i+b_i r^theta),
up to outer cutoff terms O_r(b_i).

The flat Jacobi operator is invertible on the complement of its n-dimensional
bubble kernel. This follows by transferring to the compact hemisphere, whose
Neumann eigenvalue n eigenspace is exactly the tangential coordinate functions.
The graph form is an O(r) bounded operator perturbation, using |Df_i|<=Cepsilon_i(1+s),
trace Hardy for its Robin term, and small fixed r. Thus the projected inverse
is uniformly bounded. Modulation gives exact orthogonality to the kernel.
Simple decay and local convergence imply global critical-Lq convergence after
cutoff; hence the semilinear error is o_i(||w||_D). Outer cutoff error is O_r(b_i).
Absorption yields ||w||_D<=C(eta_i+C_r b_i).

The projected source profiles psi_k have |D^j psi_k|<=C(1+s)^(k+1-n-j), j<=2.
Proof: Kelvin preserves the Jacobi smooth potential. The transformed Neumann source
is O(rho^(-k)); on a small halfball its mixed Green kernel is <=C|z-zeta|^(2-n).
Its boundary layer is <=C rho^(1-k), since 2<=k<n-1. Boundary elliptic estimates
give derivatives. For k<n/2 the D solution extends weakly through0; critical k=n/2
is constructed first as this Green layer, then its compact forcing is corrected by
the projected inverse. Orthogonality follows A1 and its translation counterparts
at infinity. Critical energy is O(logR), with cutoff discrepancy O(|A_d|)=o(eta_i).

Subtract the profiles and extend the outer mismatch regularly by a mixed harmonic
h_i. On the outer sphere every profile, U, and v_i is O_r(b_i^2); therefore
|h_i|<=C_r b_i^2 nearcore, and ||h_i||_D<=C_r b_i. Its potential residual is o_i(b_i).
The remaining correction first obeys the COARSE bound

 ||q_i||_D<=o_i(eta_i)+C_r b_i.                                           (B2c)

Only AFTER C3 has forced physical jetvanishing do cutoff-profile tail terms become
o_i(b_i) for fixed r, improving this to the REFINED bound

 ||q_i||_D<=o_i(eta_i)+C b_i r^theta+o_i(b_i).                              (B2r)

Graph-operator perturbation of profiles is o_i(eta_i): its weighted square is
bounded by epsilon_i^2 int_1^R s^(2k-n+1)ds; at the critical degree divide by logR.
All cutoff-profile tail discrepancies are coarse O_r(b_i); after physical jets
vanish they are o_i(b_i) for fixed r.

## C. The second-order calculation is a bounded-form Taylor calculation
Use the fixed material variable z, not composition of an arbitrary H^1 correction:

 Etilde(f,z)=J_(Phi_f^*delta)(U composed Phi_f+z).

It is twice differentiable in z, analytic in the graph, and its graph-dilation
derivatives have uniform bounds below. Direct ambient-bubble graph energy is odd
under f->-f; its first variation vanishes for compact deformation. Therefore
Etilde_ff(0,0)=0. Its mixed derivative is exactly <S_f,z>: starting from
- int f[|grad u|^2/2-Nu^q/q]+c_n int Delta f u^2, differentiate at U and use
Delta' U=-N U^p-U_tt, obtaining grad f.grad'U-f U_tt+beta Delta f U=S_f.
Its zz Hessian is the Jacobi form A0. Consequently elimination z=-A0^(-1)S_f gives
quadratic energy -1/2<S_f,A0^(-1)S_f>.
By A2, corrected Pohozaev is the NEGATIVE graph-dilation derivative, hence

 Q_i=1/2 sum_{k,h}(k+h-2) C_kh A_{i,k} A_{i,h},                            (C1)

not its negative. These are precisely the harmonic dilation matrices certified
positive definite in dimensions<=18. For critical degrees the highest diagonal
is positive times logR; the lower block is one of the convergent positive blocks,
so Schur complement gives Q_i>=c eta_i^2 for large R.

Here are sufficient explicit bounds for the Taylor remainder. For the vertical
extension let delta_f bound |f|/(1+s), |Df|, (1+s)|D^2f|, (1+s)^2|D^3f|,
and one more derivative in the dilation direction. Smooth physical graphs give
delta_f<=Cr. Bulk coefficient derivatives are bounded by DV; Robin curvature
is linear in D^2V with analytic DV coefficients. Trace Hardy bounds its quadratic
z term. Thus the quadratic-in-z graph remainder is <=Cr||z||_D^2. Define the explicit graph majorant N_f^2=int_strip U^2[|D^2f|^2+|Df|^2/s^2+f^2/s^4],
so N_f^2<=C(eta_i^2+b_i^2 r^(2theta)) by polar integration. Pure graph cubic
terms are <=Cr N_f^2: for example D^2f|Df|^2U^2<=Cr |Df|^2U^2/(1+s), and
D^2f f^2 U U_tt<=Cr f^2U^2/(1+s)^3, precisely the height-integrated bulk majorants.
Mixed remainders use Cauchy-Schwarz, and the semilinear Taylor remainder is
O(||z||_D^sigma), sigma=min(3,2n/(n-2))>2. The same estimates hold for Df, which
preserves each homogeneous degree. General mixed semilinear remainders may be written
o_i(N_f^2+||z||_D^2), which is sufficient; no reverse bound from ||T_f|| to N_f is used.

The source/h cross is sharper than a bare D-norm bound:

 |<A_k S_k,h_i>|<=C_r|A_k|b_i^2 R^(k-1)
 =C_r|A_k|b_i epsilon_i^(n/2-k)=o_i(eta_i b_i).                            (C2)

At critical k use the extra sqrt(logR) in eta. Bulk potential cross is smaller
(int_1^R s^(k-4)ds). Thus it is o_i(eta_i^2+b_i^2). Pairing q with the source
uses B2c and Young at the coarse stage, costing a small multiple of eta_i^2 plus
C_r b_i^2. Only after C3/jetvanishing does B2r improve this cost to
a small multiple of eta_i^2 plus C b_i^2r^(2theta)+o_i(b_i^2).

For cap localization, after exact A1 subtraction every term is at least quadratic
in graph/correction. Simple decay gives coarse O_r(b_i^2). This includes all h_i^2
terms; they must NOT be asserted uniformly small as r->0 at this stage.
Combining A2,C1,C2 and the bounded-form Taylor estimates, choosing r small to
absorb Cr eta_i^2, gives

 P_corrected(v_i,R)>=c eta_i^2-C_r b_i^2.                                  (C3)

Its left side is O_r(b_i^2) by simple decay and A1. Hence eta_i^2<=C_r b_i^2,
which forces every physical graph jet through degree d to vanish at the limit:
|F_{i,k}|^2<=C_r epsilon_i^(n-2k) for k<n/2 and |F_{i,d}|^2<=C_r/logR at critical k.
This proves (1).

## D. Refined limit and invariant mass sign
Now fix r and pass i->infinity. The normalized limit G has pole coefficient1
(from the bubble flux integral) and F=O(r^(d+1)). Boundary Green-potential estimates,
iterating the small graph perturbation, give

 G=r^(2-n)+H,  H=O(r^(d+2-n)(1+|logr|))+O(1).

No unjustified constant-only Green expansion is used. The possible log is harmless
for every power below. Now use the REFINED correction bound B2r; it has not been used to establish C3.
The core low-jet nonlinear error remains absorbed in Q_i;
the semilinear error is o_i(b_i^2) for fixed r by the coarse bound and sigma>2.
The high-graph/cap quadratic error has order r^(2d+2-n) times logarithms;
F H^2 and pure cubic graph error have order r^(3d+2-n) times logarithms.
Both exponents are positive. Taylor-tail cost is r^(2theta)=r^(2d+2-n).
Therefore, dropping the nonnegative Q_i term,

 liminf_i b_i^(-2)P_corrected(v_i,R)
 >=-C r^(2d+2-n)(1+|logr|)^C,

and r->0 gives (2).

Indeed Kelvin gives metric w^(4/(n-2))delta on z_n>=b(z'), with
b=O(R^(1-d)), w-1=O(R^(-d)logR). Flattening and taking the standard +rim ADM flux yields

 ADMnum=lim[-4(n-1)/(n-2)int_{S_R+}partial_R w+2int_rim partial_R b].

Quadratic errors are O(R^(n-2-2d)log^2R)->0. Direct Kelvin transformation gives
P_raw=(n-2)/2 int partial_R w+o(1), while A1 supplies -C int_rim partial_R b.
Thus lim P_corrected=-(n-2)^2/[8(n-1)] ADMnum, with no missing boundary mass term.

## Scope and verification
This is a proof of the LOCAL conditional sign/jet lemma, not the full theorem:
its hypotheses include isolated-simple decay and normalized bubble convergence.
The exact identities and spectral coefficients have independent SymPy/interval/rational
certificates in the shared scripts. Analytic inequalities above use only Sobolev,
trace Hardy, local mixed Green kernel bounds, elliptic estimates, and bounded-form
Taylor formulas whose majorants are explicitly displayed. Global selection, simplicity,
clustering, and strict positive mass are separately required.


---

# Global reduction from the local sign lemma

The local Pohozaev sign/jet lemma invoked below is proved separately in
agent2_local_sign_lemma.md, with the uniformity stated here. This note supplies
the remaining global selection and mass argument.

## Required local input
On a uniformly smooth conformally flat chart, suppose a positive critical
Robin solution sequence has one isolated bubble at epsilon_i, is simple out to
radius r_i, and satisfies the sharp estimate
u_i(x)<=C M_i^{-1}|x-q_i|^{2-n}, M_i=epsilon_i^{-(n-2)/2}.
Let the homogeneous graph-jet dilation forms of all degrees k<=floor(n/2)
be positive, with logarithmic top degree in even dimension. Required conclusions:
(1) whenever r_i is bounded below, the limiting boundary graph jets through
floor(n/2) vanish; (2) for any harmonic limit obtained by rescaling a first
nonsimple radius or a closest-point distance, its corrected local Pohozaev flux
at the singularity is nonnegative; (3) for a fixed-scale limiting Green function,
the corrected flux at the pole has liminf >=0. Uniformity is needed when the
chart itself is rescaled. The correction is the FULL first-shape rim functional,
not only its low-degree Taylor part (agent1_linear_stress_rim.py).

## Selection and sharp decay
Use the usual point-picking construction based on d(x,Q)^{(n-2)/2}u_i(x).
The classification of positive entire critical solutions (whole space and
Neumann halfspace) gives selected bubbles; merge centers at comparable bubble
scales, choosing point-picking radii tending slowly to infinity, so every pair
satisfies dist(q_j,q_k)/max(eps_j,eps_k)->infinity. Otherwise classification
gives a single bubble with one maximum instead of two centers. It also gives
the isolated bound u<=C d^{-a},
a=(n-2)/2. Maximal selection gives that bound everywhere relative to the selected
set. For a fixed i this construction is finite by smoothness and disjointness
of fixed multiples of bubble-scale balls; the cardinality is not yet uniform.

For a bubble simple up to rho_i, radial-profile monotonicity first gives weak
decay v(s)<=C(1+s)^{2-n+eta}, eta>0 as small as desired. A proof without an unjustified outer Dirichlet comparison uses t=log(s) and
y(t)=s^a vbar(s). Annular Harnack and simplicity give y<=delta outside a large
fixed ball and yprime<=0 up to the first later critical time T. The radial
equation gives ydoubleprime>=(a^2-C delta^(p-1))y=kappa^2 y. With yprime(T)<=0,
ODE comparison gives y(t)<=2y(t0)exp(-kappa(t-t0)). Thus v<=C s^(2-n+eta),
with eta=a-kappa as small as desired. Graph/Robin terms are a uniformly O(r)
perturbation of this inequality; conjugating by an exponential absorbs the
first-derivative term and changes kappa by O(r). With eta chosen p eta<2,
the source integral int v^p is uniformly bounded. The radial mean
identity and profile monotonicity then give sharp decay: in the flat case put
A(s)=-s^{n-1} vbar'(s); A is bounded by the source integral, while simplicity
implies vbar(s)<=A(s)s^{2-n}/a. For the graph/Robin perturbation use an integral flux inequality. Define the
mean over the actual cap and A0=-s^(n-1)vbar-prime. Moving-cap differentiation
gives A0=-int_cap partial_r v+O(eps s^(n-1)vbar). Harnack and simplicity give
vbar<=A0 s^(2-n)/a, so the error is <=C eps s A0. Divergence theorem gives
-int_cap partial_r v=N int_domain v^p-beta int_graph Hscaled v. The source
integral is uniformly bounded by weak decay; |Hscaled|<=C eps and the same
profile bound give boundary error<=C eps int_0^s A0(t)dt. Absorb C eps s A0
for eps s<=r small; Gronwall yields A0(s)<=C exp(C eps s)<=C exp(Cr).
Annular Harnack transfers this to pointwise bounds,
and interior/boundary gradient estimates give the differentiated bound.
The same argument works up to a first later critical radius, including its
outer endpoint. All constants are uniform under chart rescaling with bounded
smooth norms.

## No nonsimple bubbles
Suppose the radial profile has a first later critical radius rho_i with
rho_i/epsilon_i->infinity. Before rho_i it is decreasing. Its value there tends
to zero: compare with L epsilon_i, let i->infinity, then L->infinity.
Rescale by rho_i and divide by an annular value. The equation becomes harmonic;
Harnack and the sharp estimate give a positive harmonic Neumann limit with one
pole. Even reflection and Bocher's theorem give h=A|x|^{2-n}+H(x) locally,
where H is regular harmonic. Its spherical/hemisphere mean is H(0)=B.
The critical-profile condition at radius1 gives B=A>0 (normalization fixes A>0).
Its Pohozaev flux is -(n-2)^2 |S^{n-1}| A B/4 in the halfspace, hence negative.
The rescaled local sign lemma contradicts this. Thus each selected bubble is
simple throughout its isolated region.

## No clustering
Let d_i->0 be the least distance of two selected points. Their isolation regions
have radius comparable to d_i. Sharp decay at the midpoint and the positive
Green lower bound give M_j/M_k bounded above and below for a closest pair
(apply the two estimates with the points exchanged). Rescale by d_i. Minimal
separation gives bounded numbers of poles in compact sets. Divide by a value
away from poles. The rescaled nonlinear term tends to zero by sharp decay;
Harnack gives a positive harmonic multipole limit with at least two nonzero
positive poles. In a halfspace reflect evenly. At either pole the regular part
is strictly positive: compare with Dirichlet Green functions on expanding balls;
the other pole gives a positive contribution and the positive boundary data give
no negative contribution. Its local Pohozaev is negative, contradicting the
rescaled local sign lemma. Thus all selected points are uniformly separated,
and packing gives a uniform finite number.

## Interior poles and approach to boundary
For the requested boundary compactness, isolated interior bubbles a positive
distance from boundary need not be ruled out separately: they become additional
full asymptotically flat ends of the Green metric. We apply positive mass at a
BOUNDARY end, guaranteed by the assumed boundary blowup. Interior clustering is
excluded by the ordinary flat local Pohozaev identity, with no mass theorem.
For an interior center drifting to boundary use the MINIMUM of its nearest-
neighbor distance and its boundary distance as the intermediate scale. If the
neighbor distance is smaller/comparable the multipole argument applies first;
otherwise the boundary-distance rescaling is isolated. In the latter case,
if d_i->0 and d_i/epsilon_i->infinity, rescale by d_i.
The harmonic Neumann limit has an interior pole and its positive reflected pole;
the latter gives a strictly positive regular part at the former. The ordinary
interior flat Pohozaev is zero, contradicting the negative harmonic flux.
If d_i/epsilon_i stays bounded, halfspace bubble classification recenters the
bubble on the boundary. Thus genuinely boundary-centered bubbles are the only
boundary candidates.

## Global Green convergence and mass
Away from the separated poles, local sharp estimates on annuli and connected-
set Harnack force u_i->0. They also compare heights of different bubbles: all
M_i^j are comparable. After choosing one height M_i, elliptic compactness gives
M_i u_i->G, a positive solution of -L_g G=0, B_g G=0 off the poles. Positivity of
-L_g with Robin boundary excludes a homogeneous kernel; distributionally G is
a positive sum of Green functions at the poles.

The local jet conclusion gives graph F=O(r^{d+1}), d=floor(n/2). A local harmonic
parametrix gives G=r^{2-n}+O(r^{d+2-n}) plus regular/mass terms (logs, if present,
can be allowed with a small loss). Kelvin inversion has boundary height
O(R^{1-d}), slope O(R^{-d}), and conformal factor 1+O(R^{-d}); hence AF rate can
be chosen strictly greater than (n-2)/2. Scalar curvature and mean curvature of
the Green metric vanish exactly. The virtually-spin finite-cover argument in
agent1_geometric_lemmas.md permits the spin boundary positive mass theorem.
At every end mass is strictly positive unless the original manifold is
conformally a hemisphere (multiple lifted poles also force strictness).

The ADM numerator equals
-4(n-1)/(n-2) int_{S_R+} partial_R v +2 int_{rim} partial_R b+o(1).
The full linear first-shape subtraction matches the second term exactly;
therefore the corrected Pohozaev limit is a strictly negative multiple of mass.
This contradicts conclusion(3) of the local sign lemma. Compactness follows.

## Closing the argument
The local sign lemma and its two-stage nonlinear remainder estimate are proved
in agent2_local_sign_lemma.md; the bounded-form estimates used there are expanded
in agent1_shape_taylor_bounds.md. The annular Harnack and elliptic estimates above
apply to uniformly elliptic smooth conformal graph charts and Robin operators
with uniformly bounded rescaled coefficients. Thus their hypotheses hold here.


---

# Fixed smooth-domain construction from a stable polynomial shape minimum

This note proves the construction implication; its only finite-dimensional input
is the stable shape minimum certified in the agent3 scripts. It does not invoke
the compactness/Pohozaev criterion needed for the opposite implication.

## 1. Statement, conventions, and Hilbert space

Fix n>=19, a=(n-2)/2, q=2n/(n-2), beta=(n-2)/(2(n-1)). Write
U_{t,xi}(y,s)=[t/(t^2+|y-xi|^2+s^2)]^a on the upper half-space.
Let F be a polynomial on R^{n-1}, of degree at most 8, vanishing to order 2
at zero. Suppose its shape functional Psi_F, defined below, has a strict
nondegenerate local minimum at (t_*,xi_*), with t_*>0. We will construct one
smooth compact connected bounded Euclidean domain Omega, of positive Yamabe
type and not conformal to a hemisphere, with smooth positive critical Robin
solutions whose boundary maxima diverge.

The energy on a smooth bounded Euclidean domain is

 E_Omega(v)=1/2 Q_Omega(v,v) -(n-2)^2/2 integral_Omega (v_+)^q,
 Q_Omega(v,w)=integral_Omega grad v.grad w + beta integral_boundary H v w.

For positive-type Omega, Q is an equivalent Hilbert norm on H^1(Omega).
The trace, critical Sobolev, and dual trace estimates used below are

 ||v||_{L^q(Omega)}+||v||_{L^{2(n-1)/(n-2)}(boundary)} <= C ||v||_Q,
 |integral_boundary f v| <= C ||f||_{L^{2(n-1)/n}} ||v||_Q.

These are valid, with uniform constants, for the bounded C^2-small domain
perturbations used here. Coercivity follows from the positive first Robin
eigenvalue. Conversely, for the explicit base below it follows directly from
Poincare with a nonzero nonnegative boundary term, and persists by pullback
under a sufficiently small C^2 perturbation.

## 2. Half-space source and shape functional

The Jacobi bilinear form is

 A_{t,xi}(v,w)=integral_half grad v.grad w
             -n(n+2) integral_half U_{t,xi}^{4/(n-2)} v w.

Its kernel in D^{1,2}(R^n_+) has dimension n and is spanned by the scale and
n-1 tangential-translation derivatives of U. This follows, for example, by
conjugating by U to the round hemisphere: the equation becomes
(-Delta_{S^n}-n)f=0 with Neumann boundary data; its kernel is exactly the
restrictions of the n coordinate functions tangent to the equator. This
conjugation is an isomorphism of the energy spaces. Since its potential is a
compact multiplication perturbation of the Dirichlet inner product, A has a
bounded inverse on the Dirichlet-orthogonal complement of this kernel.

For Omega_epsilon={s>epsilon F(y)}, evaluate the outward critical Robin
operator on the AMBIENT bubble U_{t,xi}, restricted to Omega_epsilon. Its
first-order boundary defect is epsilon S_{F,t,xi}, where

 S_{F,t,xi}=(n-2)U_{t,xi} [F-(y-xi).grad F]/[t^2+|y-xi|^2]
                        + beta (Delta F) U_{t,xi}             (s=0).

For t,xi in a fixed compact parameter set with t bounded away from zero,
S and its parameter derivatives are bounded by C(1+|y|)^{8-n}. Thus they
belong to L^{2(n-1)/n}(R^{n-1}) for n>16. In particular they define bounded
energy-space functionals ell_{F,t,xi}(v)=integral_boundary S v.

For every compactly supported graph, the first shape variation of E at every
ambient bubble is zero. Explicitly its coefficient after tangential
integration by parts is

 -1/2 |grad_y U|^2 +(n-2)^2/2 U^q + (beta/2) Delta_y(U^2)=0.

The identity is pointwise, with the bubble scale included. Differentiating it
with respect to each bubble parameter gives ell(Z_alpha)=0 for every kernel
function Z_alpha. Approximation by cutoffs proves the same assertion for our
polynomial F, because all the resulting pairings converge for n>16.

Let w_{F,t,xi} solve A(w,v)=-ell(v), orthogonally to the kernel. Define

 Psi_F(t,xi)= -1/2 A(w,w)
            =-1/2 ell(A^{-1}ell).

(The inverse here acts on the kernel complement.) This is precisely the
finite-dimensional function used in the spectral certificates. Multiplying
all coefficients by the same positive constant does not change its minima.

## 3. One fixed smooth positive-type domain

Use any smooth bounded convex domain Omega_0 with an open flat bottom disk
containing {|y|<1/2,s=0}; let H>=0 and H not identically zero. One fully
explicit choice is

 h(v)=0 (v<=1), h(v)=(v-1)^2 exp[-1/(v-1)] (v>1),
 Omega_0={h(|y|^2)+(s-1)^2<1}.

Its boundary is smooth, its defining function is convex, and its bottom
contains {|y|<1,s=0}. The positive Robin form is coercive: if coercivity
failed, normalized functions with energy tending to zero would converge to
a constant, and the nonzero H term would force that constant to vanish.

For i>=2 take p_i=2^{-i}e_1, rho_i=2^{-i-5}, lambda_i=2^{-(i+I)^2}, with I fixed
sufficiently large. A harmless increase of I ensures lambda_i<<rho_i.
Choose a smooth radial chi equal to 1 on B_{3/4} and 0 outside B_1, and set

 f_i(y)=lambda_i^9 F((y-p_i)/lambda_i) chi((y-p_i)/rho_i).

For F=H_2 P_3 this is the same as
lambda_i^7 H_2(y-p_i)P_3(|y-p_i|^2/lambda_i^2) chi.
The disks B_{rho_i}(p_i) are pairwise disjoint and lie in the flat disk.
For every k,

 sup |D^k f_i| <= C_k lambda_i rho_i^{8-k}.

For polynomial terms of degree below 8 the bound is smaller by a power of
lambda_i/rho_i. Therefore the sum f=sum_i f_i, extended by zero at the
accumulation point 0 and outside the disks, is C^infinity, with every jet
zero at 0. Replacing only the bottom flat patch by s=f(y) gives one fixed
smooth bounded connected domain Omega. It is obtained from Omega_0 by a
C^2-small diffeomorphism, and Q_Omega remains coercive. It is Euclidean,
hence locally conformally flat including at the boundary.

If F has a nonzero tracefree quadratic term (as all our certified profiles
do), the boundary is nonumbilic at p_i: its tracefree second fundamental form
there is a nonzero multiple of lambda_i^7 (D^2 F(0))^0. The tracefree second
fundamental form transforms under a conformal change ghat=e^{2h}g by
IIhat^0=e^h II^0. The round hemisphere is totally geodesic, so Omega cannot
be conformally equivalent to it.

## 4. The scale comparisons and elementary weighted estimates

Set epsilon_i=lambda_i^8, R_i=rho_i/lambda_i. Under x=p_i+lambda_i z the
chosen patch is exactly z_n=epsilon_i F(z') for |z'|<3R_i/4. The remaining
patches lie outside the selected chart. On this chart

 epsilon_i(1+R_i)^7 = O(lambda_i rho_i^7)=:delta_i ->0.

The polynomial and graph-cutoff derivatives obey
|D^k F_R(z')|<=C(1+|z'|)^{8-k}, k<=3. In the region in which an ambient
bubble or its cutoff is evaluated, both the graph slope and the relative
height displacement |epsilon F|/(1+|z'|) are bounded by C delta_i.
All radial quantities evaluated at height epsilon F are consequently
comparable to their values at height zero. To identify the energy spaces, use
the vertical map Phi(y,s)=(y,s+epsilon F_R(y) zeta(s/(1+|y|))), with a fixed
smooth zeta equal to 1 near zero and compactly supported. Its derivative
differs from the identity by O(delta_i). The pulled-back Dirichlet form differs
by O(delta_i) in operator norm. The Robin term has the same bound, since
|H|<=C delta_i/(1+|y|), and the trace Hardy inequality bounds
integral_boundary (1+|y|)^(-1) v^2 by C integral_half |grad v|^2.
The physical comparison bubble pulls back as U composed with Phi, not U;
we retain that distinction throughout.

Here are the estimates needed for Taylor expansion (also for first parameter
derivatives on compact sets):

 (i) integral_{|z|>R} [(1+|z|)^14 |grad U|^2
                       +(1+|z|)^16 |D^2 U|^2]
       <= C R^{16-n};

 (ii) ||(1+|y|)^{8-n}||_{L^{2(n-1)/n}(|y|>R)}
       <= C R^{(16-n)/2}.

Both follow by polar integration. All Taylor remainders of the graph normal,
its area element, and its mean curvature have the extra factor delta_i
relative to their quadratic energy, or to their linear Robin-source,
majorants. For clarity, the normal is (epsilon grad F,-1)/sqrt(1+epsilon^2
|grad F|^2), H=div(epsilon grad F/sqrt(1+epsilon^2|grad F|^2)), and its
nonlinear error is bounded by C delta_i^2 epsilon |D^2F|. Evaluating U at
height epsilon F uses the ordinary Taylor formula, with
|epsilon F|/(1+|y|)<=C delta_i. The same estimates bound all mixed terms.
Estimates (i),(ii), the trace inequality, and Holder therefore give:

 * Robin residual = epsilon_i ell_{F,t,xi}+o(epsilon_i) in dual energy norm;
 * its first parameter derivatives have the same expansion;
 * fixed-bubble energy = E_half(U)+o(epsilon_i^2), in C^1(parameters),

once the chart cutoff errors below are included. One can check the last
assertion directly without retaining spurious quadratic terms: with an
ambient bubble even in z_n, both the domain-volume difference and the
integrated H term are odd functions of epsilon. Their linear term vanishes
by the stress cancellation in section 2. Their cubic remainder is bounded
by C delta_i epsilon_i^2 times the finite integral in (i).

Choose the physical bubble cutoff eta_i equal to 1 on B_{rho_i/4}(p_i),
zero outside B_{rho_i/2}(p_i), radially symmetric about p_i. Its energy-norm
error is O(R_i^{-a}), its fixed-bubble energy error is O(R_i^{2-n}),
uniformly with one parameter derivative. The possible linear graph term
in this cutoff annulus is at most C delta_i R_i^{2-n}, hence is covered by
the same energy error. Crucially,

 R_i^{-a}/epsilon_i
 =lambda_i^{(n-18)/2} rho_i^{-(n-2)/2} ->0       (n>=19).

Thus all cutoff errors are little-o of the relevant residual/energy scales.
The explicit superexponential lambda_i makes these comparisons valid even
with any fixed power of rho_i^{-1} coming from cutoff derivatives.

## 5. Uniform projected inverse

Let W_i(t,xi)(x)=eta_i(x)lambda_i^{-a}
U_{t,xi}((x-p_i)/lambda_i), restricted to the fixed domain Omega.
Let K_i be the span of its n parameter derivatives, and Pi_i the
Q-orthogonal projection onto K_i. Their Gram matrices converge uniformly to
the nonsingular half-space Gram matrix.

Let T be the Q-Riesz inverse for interior data:
Q(Tf,v)=integral_Omega f v. The linearized projected map on K_i^perp is

 L_i phi=(1-Pi_i)[phi-T(n(n+2)W_i^{4/(n-2)}phi)].

There are constants c>0 and i_0 independent of the compact parameter set
such that ||L_i phi||_Q>=c||phi||_Q for i>=i_0. Here is the full usual
contradiction argument. If not, choose normalized phi_i with projected image
tending to zero. Test the unprojected equation against each cutoff kernel
function; its Jacobi defect tends to zero by the residual estimates, so all
kernel coefficients tend to zero. Thus the unprojected image tends to zero.
The weak limit away from the single accumulation point solves the homogeneous
coercive Robin problem, and hence is zero; test functions avoiding that point
are dense in H^1 because n>=3. Rescaling at p_i gives a bounded D^{1,2}
sequence. Its weak limit solves the half-space Jacobi equation and is
orthogonal to all n kernel functions, so is zero. Rellich compactness makes
the weighted potential integral vanish on each fixed rescaled ball. Outside
that ball use Holder and
||U^{4/(n-2)}||_{L^{n/2}(|z|>R)} ->0.
Consequently integral W_i^{4/(n-2)}phi_i^2 ->0. Pairing the unprojected
equation with phi_i now gives 1=o(1), the contradiction. Since L_i is
self-adjoint Fredholm of index zero on the complement, this lower bound
proves surjectivity and the asserted uniformly bounded inverse.

## 6. Solving the infinite-dimensional equation

The gradient of E is G(v)=v-T(n(n-2)(v_+)^{q-1}). Its residual at W_i is
O(epsilon_i), uniformly C^1 in the parameters. For n>=19, 2<q<3, and

 ||G(W+phi)-G(W)-DG(W)phi -
   [G(W+psi)-G(W)-DG(W)psi]||_Q
 <= C(||phi||_Q+||psi||_Q)^{q-2} ||phi-psi||_Q.

This is the pointwise Holder estimate for derivative of x_+^{q-1}, followed
by Sobolev and Holder. The contraction mapping theorem on a ball of radius
C epsilon_i, using the uniform inverse of section 5, gives a unique
phi_i(t,xi) in K_i^perp with

 (1-Pi_i)G(W_i+phi_i)=0,   ||phi_i||_Q<=C epsilon_i.

The contraction depends C^1 on parameters (x_+^{q-1} is C^1), hence phi_i
is C^1 and ||partial_parameter phi_i||_Q<=C epsilon_i. Here is the derivative estimate needed because p=q-1 lies in (1,2), so
a bare Holder operator bound is insufficient. Each parameter derivative obeys
|partial W|<=C W. For f(v)=v_+^p, pointwise splitting into |z|<=W/2 and its
complement gives

 |fprime(W+z)-fprime(W)| W <= C(W^(p-1)|z|+|z|^p),
 |fprime(W+z)-fprime(W)-fsecond(W)z| |partial W| <= C|z|^p.

The first inequality bounds the differentiated linear term by O(epsilon_i),
and the second bounds the parameter derivative of the nonlinear remainder by
O(epsilon_i^p), in the dual Sobolev norm. The term multiplying partial phi is
O(epsilon_i^(p-1)) in operator norm and is absorbed using the uniform inverse.
The differentiated source is O(epsilon_i), and the kernel projections have
uniformly bounded derivatives; these facts give the asserted O(epsilon_i)
bound. Values where W=0 cause no difficulty since partial W=0 there.
One may identify the varying complements with a fixed complement using
their smooth Gram projections.

## 7. Reduced energy, including its C^1 remainder

Define J_i(t,xi)=E(W_i+phi_i). In rescaled variables, on every fixed ball,
phi_i/epsilon_i converges strongly to w_{F,t,xi}. To see this without
any possible loss of energy at infinity, approximate w_F in D^{1,2} by a
fixed compactly supported smooth function, scale and transport it into the
selected patch by Phi, and project it onto K_i^perp. First let i tend to
infinity, then exhaust the half-space by these approximations. The source
converges strongly in the dual energy norm by section 4, the form perturbation
is O(delta_i), all kernel Gram matrices converge, and the uniform inverse
from section 5 bounds the difference from the actual correction. This proves
strong energy convergence globally, rather than merely local convergence. The potential tail
estimate used there gives global energy convergence, not just local weak
convergence. These statements are uniform on the compact parameter set;
otherwise a countersequence of parameters has a convergent subsequence.
Differentiating the equations proves the same conclusion for first parameter
derivatives: the coefficients and source converge with one parameter
derivative, the differentiated projected inverse is uniformly bounded, and
the refined weighted pointwise inequalities of section 6 make the
differentiated nonlinear remainder O(epsilon_i^{q-1})=o(epsilon_i). Thus no differentiation of an uncontrolled little-o is involved.

Taylor expansion of E, with the q-power remainder, gives

 J_i=E(W_i)+E'(W_i)[phi_i]+1/2 E''(W_i)[phi_i,phi_i]
                  +O(||phi_i||_Q^q).

Testing the projected equation against phi_i combines the middle two terms
as -1/2 E''(W_i)[phi_i,phi_i]+O(epsilon_i^q). The strong convergences and
section 4 consequently give the precise reduced expansion

 J_i(t,xi)=E_half(U)+epsilon_i^2 Psi_F(t,xi)
                          +o_{C^1}(epsilon_i^2).

All constants are uniform on the selected compact parameter neighborhood.
Since q>2, epsilon_i^q=o(epsilon_i^2). This derivation is made in ambient
coordinates. If the domain is flattened first, the transported bubble
U(y,z_n+epsilon F(y)) must also be differentiated; its F U_n term cancels
the apparent extra direct F^2 term.

## 8. From the minimum to positive smooth blowup solutions

Take a small closed parameter ball around the strict local minimum of Psi,
with strictly larger Psi on its boundary. Uniform C^0 convergence in
section 7 suffices to give an interior minimum of J_i for all large i.
At that point partial J_i=0. The full gradient G(W_i+phi_i) already lies in
K_i; the matrix pairing its kernel components with the parameter derivatives
of W_i+phi_i is the kernel Gram matrix plus O(epsilon_i), hence invertible.
It follows that G(W_i+phi_i)=0 in the full Hilbert space.

The resulting weak solution u_i solves the truncated critical equation.
Testing with its negative part gives Q(u_i^-,u_i^-)=0, so u_i>=0. It is
not zero because its rescaled bubble has nonzero trace norm. Brezis--Kato
iteration (split the L^{n/2} potential into bounded and small-norm parts),
followed by the interior and Robin boundary elliptic estimates, gives
smoothness; the strong maximum principle and boundary Hopf lemma give
u_i>0 on the closed domain. It then solves the untruncated equation.

Finally, on any fixed rescaled boundary disk the trace of the rescaled
correction tends to zero, whereas U_{t,xi} has a positive fixed trace norm.
Thus max_boundary u_i >= c lambda_i^{-a}->infinity. This trace argument
does not assume an a priori pointwise error bound.

This proves the construction implication from the certified strict minimum.
For n=19,...,32 that input is certified by agent3_transcert.py (with exact
moment arithmetic and outward interval tail bounds). For n>=33 it follows
from agent3_all_n33.py and the exact translation-Hessian identities in
agent3_transall.py. Thus the construction side holds for every n>=19.


---

# Algebraic certificates

`agent1_all_exact_spd.py` certifies every one of the 78 convergent harmonic
blocks in dimensions 5 through 18. Dimensions 3/4 and critical logarithmic
blocks are covered analytically by the positive angular energy described in
the local lemma. `agent1_exact_finite_minima.py` certifies full nondegenerate
shape minima for dimensions 19 through 32 using exact rational arithmetic and
a Machin-certified enclosure of pi. `agent3_all_n33.py` and `agent3_transall.py`
prove the corresponding assertions for every integer n>=33 by symbolic
polynomial inequalities. Independent outward-interval certificates are also
included and have been run.

The symbolic bubble, source, stress, full first-shape rim, Kelvin/ADM matching,
and explicit flat-patch background identities are included in the checker.
