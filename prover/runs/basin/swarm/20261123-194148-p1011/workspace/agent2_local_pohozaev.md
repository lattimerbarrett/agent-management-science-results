# Conditional boundary local-sign lemma: organized proof and exact remaining issue

This file distinguishes proved estimates/identities from the final coefficient-level
Ward remainder assertion. It is not, by itself, a complete compactness theorem.

## Setup and hypotheses

Work in a flat conformal chart. The domain is x_n >= F_i(x'), with uniformly smooth
F_i, F_i(0)=dF_i(0)=0. A bounded local Mobius change removes the radial quadratic
mean-curvature jet, not any higher radial jets. Let epsilon_i -> 0, a=(n-2)/2,
R_i=r/epsilon_i, and rescaled positive solutions v_i have the isolated-simple estimates

  v_i(y) <= C(1+|y|)^(2-n),
  |grad v_i(y)| <= C(1+|y|)^(1-n),
  v_i -> U=(1+|y|^2)^(-a) in C^2_loc.

These are assumptions here; selection and simple-blowup arguments are separate.
Modulate the n tangential/scale bubble parameters so the correction is orthogonal
to the halfspace Jacobi kernel. The scalar bubble/Robin equations use the constants
of the problem, with the outward normal on the lower graph.

Put d=floor(n/2), b_i=epsilon_i^a, and expand the scaled graph

 f_i(y)=epsilon_i^(-1)F_i(epsilon_i y)
       =sum_{k=2}^d epsilon_i^(k-1) F_{i,k}(y)+f_rem.

The coefficients of F_{i,k} are physical homogeneous Taylor jets. Write A_{i,k}
for epsilon_i^(k-1) times their coefficient vector, and

 eta_i^2=sum_{k<n/2}|A_{i,k}|^2
          +1_{n even}|A_{i,d}|^2 log R_i.

All graph conformal gauges are omitted (constant, linear, radial quadratic).

## 1. Exact linear source and exact full-graph rim

For any smooth graph displacement f, the Eulerian Robin source at U is

 S_f=(n-2)U[(f-y.grad f)/(1+|y|^2)+Delta f/(2(n-1))].

For the scale Jacobi field Z=a U(|y|^2-1)/(1+|y|^2), the exact identity is

 int_{B_R'} S_f Z
 = C(1+R^2)^(-(n-1)) int_{partial B_R'}[(R^2-1)f_r-2Rf],
 C=(n-2)^2/[4(n-1)].

Proof: set B=C(s^2-1)(1+s^2)^(-(n-1)), A=2(n-1)B/(1+s^2).
Twice integrating by parts gives zero bulk since
A+div(Ay)+Delta B=0; the rim uses -B'-sA=-2Cs(1+s^2)^(-(n-1)).
This is verified symbolically in agent2_dilation_rim.py.

For f_i=epsilon_i^(-1)F_i(epsilon_i y), divide this identity by b_i^2 and let
R_i=r/epsilon_i. The limit is

 C int_{S^{n-2}}[r^(2-n)F_r(r theta)-2r^(1-n)F(r theta)],

which is -C times the Kelvin boundary rim integral int partial_R b, where
b(R theta)=R^2 F(theta/R). This uses the FULL F, not a Taylor truncation.
In particular the degree n-1 radial graph term is retained at constant mass order.

## 2. Norm estimates for graph sources and material bubble displacement

Degree-k source S_{F_k}=O((1+s)^(k-n)). For k<n/2, its dual trace Lq norm is
bounded, q=2(n-1)/n. For k=n/2 its H^(-1/2) norm squared is O(log R): the
boundary Newton kernel is |x-z|^(2-n); equal dyadic shells have bounded interaction,
and shells separated by h have O(2^(-h(n-2)/2)) interaction. Thus

 ||S_jets||_{(D^1,2)*} <= C eta_i.

The Taylor remainder source is bounded by epsilon_i^d(1+s)^(d+1-n), so

 ||S_rem||_* <= C epsilon_i^d R_i^(d+1-n/2)
             = C b_i r^theta, theta=d+1-n/2 in {1/2,1}.

For an interior graph extension V_f with vertical component
f(y) chi(t/(1+|y|)), the material bubble displacement is V_f.grad U.
The same weighted integral proves

 ||V_jets.grad U||_D <= C eta_i,
 ||V_rem.grad U||_D <= C b_i r^theta.

Indeed its degree-k radial energy is bounded by
|A_{i,k}|^2 int_1^R s^(2k-n-1) ds. This is finite for k<n/2 and logarithmic
at k=n/2. The remainder is exactly b_i^2 r^(2theta).

## 3. Uniform projected inverse and conditional correction bound

On K-perp the halfspace Jacobi operator
A0=Id-i*(n(n+2)U^(4/(n-2))) is invertible: conformal hemisphere transfer identifies
its kernel with the n tangential spherical coordinates and no other modes.
The flattened graph form is an O(r) operator perturbation. Bulk terms use
|Df_i|<=C epsilon_i(1+s)<=Cr; the Robin curvature term uses trace Hardy.
Thus for small fixed r the projected inverse remains bounded uniformly in i.

The assumed simple decay gives critical-Lq convergence of the cutoff v_i to U,
by dominated convergence and integrable radial tail s^(-n-1). The nonlinear
remainder is consequently o_i(||w_i||_D). The cutoff-annulus dual residual is
O(R_i^(-a)), by the pointwise gradient estimate. Absorbing yields

 ||w_i||_D <= C[eta_i+C_r b_i].

The comparison bubble MUST be U composed with the graph map. If one instead
centers on U in material coordinates, subtract V_f.grad U before identifying
the Eulerian corrector -A0^(-1)S_f; otherwise false direct quadratic terms appear.

To upgrade to a separated approximation, one needs standard weighted Jacobi
profile estimates psi_k=O((1+s)^(k+1-n)), with matching gradient estimates.
For k<n/2 these can be obtained by the Kelvin regular-singular halfball problem;
for k=n/2 construct its homogeneous tail and cut it off, with bounded-energy
remainder. Their graph-operator perturbation is o_i(eta_i): the weighted square
is controlled by epsilon_i^2 int_1^R s^(2k-n+1)ds; at the critical degree divide
by log R. This tends to zero for every allowed degree.

The outer mismatch after subtracting U and these profiles is O_r(epsilon_i^(n-2))
on the scaled outer cap. Its regular mixed harmonic extension h_i obeys
|h_i|<=C_r epsilon_i^(n-2) near the core. This requires only fixed-r simple decay,
not a global Green expansion with a constant regular part. Its bulk potential
residual is o_i(b_i). Projected inversion then gives a remainder

 ||q_i||_D <= o_i(eta_i)+C b_i r^theta+o_i(b_i).

## 4. Outer cross, with no unjustified Green expansion

The boundary source cross is directly bounded by

 |<A_{i,k} S_k,h_i>|
 <= C_r |A_{i,k}|epsilon_i^(n-2)R_i^(k-1)
 = C_r |A_{i,k}| b_i epsilon_i^(n/2-k).

This is o_i(eta_i b_i): for k<n/2 there is a positive epsilon exponent, and for
k=n/2 there is the extra 1/sqrt(log R_i). Hence the total is
 o_i(eta_i^2+b_i^2). Bulk-potential cross is smaller since V=O(s^-4) and its
radial integral is int_1^R s^(k-4)ds. Gradient crosses follow by integration by parts.

## 5. Exact quadratic coefficient and nonlinear bounded-form control

The critical Robin energy is
J=1/2 int |grad u|^2+c_n int H u^2-[n(n-2)/(p+1)]int u^(p+1).
At the ambient even bubble U its direct graph dependence is odd in f. Its first
shape variation vanishes for compactly supported f; thus no direct f^2 term occurs.
The mixed shape/u derivative is <S_f,z>. Solving A0 z=-S_f gives reduced
quadratic energy -1/2<S_f,A0^(-1)S_f>. Dilation acts on homogeneous F_k by k-1.
Its symmetric quadratic coefficient is therefore proportional, with positive
convention factor, to ((k+h-2)/2) C_{kh}. These are precisely the certified matrices.

For nonlinear remainder bounds, use the interior extension V_f and pulled-back
functional, not unbounded traces of |grad_boundary w|^2. Its coefficient derivatives
are bounded by ||DV_f||_infty+||(1+s)D^2V_f||_infty<=Cr; trace Hardy controls
boundary curvature terms. Thus the quadratic-in-w remainder in the shape derivative
is at most Cr||w||_D^2. Pure graph cubic terms are bounded by Cr times the weighted
material bubble displacement squared, which is controlled by eta_i^2+b_i^2 r^(2theta).
The semilinear Taylor remainder has order sigma=min(3,2n/(n-2))>2.

IMPORTANT: applying Cr||w||_D^2 to h_i gives C_r b_i^2, not a small-r error.
One must use the following two-stage limit, not suppress this term.

## 6. Two-stage sign/mass argument, conditional on the Ward remainder identity

First the coarse expansion and outer decay give

 P_corrected(v_i,R_i) >= c eta_i^2-C_r b_i^2,
 |P_corrected(v_i,R_i)|<=C_r b_i^2.

Hence eta_i^2<=C_r b_i^2. Thus every physical F_k(q_i)->0 through degree d:
strict degrees gain epsilon_i^(n-2k), critical degree gains 1/log R_i.
The limiting graph has F=O(r^(d+1)). A local normalized Green limit then has
G=r^(2-n)+O(r^(d+2-n))+mass mode (allow angular geometric corrections).
The exponent d is sufficient for AF decay after Kelvin inversion.

Second pass i->infty for fixed r. The low-jet nonlinear errors are absorbed by
positive quadratic form; the q/source-tail error costs C r^(2theta). The remaining
physical high-graph stress terms have vanishing powers:
F-H cross: r^(2d+2-n), F-H^2 and cubic-F: r^(3d+2-n), where
H=G-r^(2-n)=O(r^(d+2-n))+mass. Both exponents are positive.
This would give liminf_{r->0} P_corrected(G,r)>=0.

After inversion and flattening the ADM numerator equals
 -4(n-1)/(n-2) int_{S_R+} partial_R w +2 int_rim partial_R b+o(1).
The exact full-graph rim identity in section 1 and Kelvin Pohozaev identity then give
 limit P_corrected=-(n-2)^2/[8(n-1)] times ADM numerator.
The nonlinear metric flux errors vanish because 2d>n-2.

## Exact remaining analytic issue

Sections 1,2,4 and the displayed exponent bounds are direct calculations/estimates.
The projected inverse bound is conditional on the explicitly stated simple decay.
The profile-tail construction in section 3 is described but not fully written out.
Most importantly, a complete proof still must write and bound the SECOND-ORDER
LOCAL WARD EXPANSION with arbitrary outer data, explicitly tracking material versus
Eulerian correctors and every outer-cap term, to justify the coarse and refined
inequalities in section 6 from section 5. The bounded-form reasoning gives the
right majorants and no apparent obstruction, but the complete coefficient/outer-term
calculation has not been independently supplied here. It must not be passed off
as an already proved general compactness theorem. Cluster/simple selection is separate.


## Addendum: profile-tail construction supplied

Let L=-Delta-n(n+2)/(1+|x|^2)^2. Kelvin preserves this operator's form.
For source g=S_{F_k}=O(|x|^(k-n)), the transformed Neumann source is
bar g(z)=|z|^(-n)g(z/|z|^2)=O(|z|^(-k)). Choose a small halfball about0;
its mixed (outer Dirichlet, flat Neumann) Green kernel for L is bounded by
C|z-zeta|^(2-n), since the bounded potential is dominated by the first mixed
Laplacian eigenvalue on a small ball. Its boundary layer has bound

 int_{|zeta|<rho, zeta_n=0}|z-zeta|^(2-n)|zeta|^(-k)d zeta
 <= C|z|^(1-k),  2<=k<n-1.

This follows by splitting |zeta|<|z|/2, |zeta-z|<|z|/2, and their complement;
the far radial integrand is s^(-k), integrable at infinity after scaling for k>1.
For k<n/2 the Kelvin transform of the global D-solution is weakly a solution
through0 (the Neumann source lies in H^(-1/2), and an extra pointmass would have
infinite D energy). Green representation gives this bound, and scaled boundary
elliptic estimates give |grad bar psi|<=C|z|^(-k). Thus
psi=O(|x|^(k+1-n)), grad psi=O(|x|^(k-n)).

At k=n/2, construct the singular Green layer on the small halfball first.
Undo Kelvin and cut off its tail to obtain an approximate profile. Its remaining
forcing is compactly supported and belongs to D*. It is orthogonal to K:
the full source pairs zero with K by first-shape Ward identities, while the
Wronskian at infinity is O(R^(k+1-n))=O(R^(1-k))->0. The projected global
Jacobi inverse corrects this compact forcing. The D-correction has faster
O(|x|^(2-n)) tail by the same Kelvin removable-singularity argument.
The resulting critical profile has truncated D-energy O(log R), since its
radial energy is int_1^R s^(2k-n-1)ds. This supplies the profile-tail
construction previously listed as missing; only standard local Green-kernel
and boundary elliptic estimates are used.

The remaining unverified step in this file is the complete second-order local
Ward expansion and all outer-cap/material-coordinate bookkeeping, not this
profile-tail estimate.


## Addendum: localized Banach-Taylor route to the Ward/cap calculation

The following provides a precise way to finish, and identifies the operator bounds
that should be checked in a final manuscript rather than treating the Ward identity
as a black-box compactness theorem.

Localize the physical graph deformation by a smooth cutoff equal to1 on B_(r/2)
and0 near the outer cap. Work on a fixed halfspace with a smooth vertical extension
Phi_f(y,t)=(y,t+chi(t/(1+|y|))f(y)). Use the additive MATERIAL H^1 variable z and set

 Etilde(f,z)=J_{Phi_f^*delta}(U composed Phi_f + z).

This is essential: do not differentiate composition of a general H^1 z. The reference
U composed Phi_f is smooth in f as a weighted-D function, whereas z is simply added
in the fixed material chart. At (0,0), Etilde_ff=0 by the direct ambient-bubble oddness,
Etilde_fz[f,z]=<S_f,z>, and Etilde_zz=A0. Thus the quadratic energy is
<S_f,z>+1/2 A0(z,z), and elimination z=-A0^(-1)S_f gives -1/2<S,A0^(-1)S>.
No unaccounted material-coordinate quadratic term remains.

For coefficient bounds define
 delta_f=sup[|f|/(1+s)+|Df|+(1+s)|D^2f|+(1+s)^2|D^3f|],
and include one more derivative when differentiating the graph dilation direction.
For a smooth physical graph tangent to the plane, delta_f<=Cr. Let Lambda_f be the
weighted-D size of the reference displacement U composed Phi_f-U. Its square is
bounded by the explicit integrals

 int [|Df|^2|grad U|^2+|f|^2|D^2U|^2+|f|^2(1+s)^(-2)|grad U|^2],

with the corresponding boundary traces. The coefficient Taylor formula gives

 |R(f,z)|+|dilation R(f,z)|
 <= C delta_f (Lambda_f^2+||z||_D^2)+C||z||_D^sigma,
 sigma=min(3,2n/(n-2))>2,

when z is the projected solution, whose parameter derivative has the same norm bound.
Justification term by term: bulk inverse metric/Jacobian derivatives are bounded by
DV; boundary curvature is linear in D^2V with analytic DV coefficients and is controlled
by trace Hardy. Cubic pure-graph terms contain at most delta_f times the squared
reference-displacement majorant: e.g. D^2f|Df|^2 U^2 is bounded by delta_f times
|Df|^2 U^2/(1+s), and D^2f f^2 U U_tt by delta_f f^2 U^2/(1+s)^3.
Those are exactly the height-integrated bulk majorants above. Mixed terms follow by
Cauchy-Schwarz. The semilinear term uses Sobolev and its C^(2,sigma-2) Taylor bound.
The same estimates apply to Df=y.grad f-f, since it preserves each jet degree.
Sections2/3 show Lambda_f<=C(eta+b r^theta), apart from outer-cutoff terms.

All outer-cap/localization terms that are linear in f are retained EXACTLY in the
full-F rim of section1 before any Taylor truncation. Consequently every remaining
cap term is at least quadratic in (graph, correction). Simple decay bounds it by
C_r b^2 at the coarse stage. After jets vanish, the limiting physical graph has
F=O(r^(d+1)) and G-pole=O(r^(d+2-n))+mass; cap quadratic/cubic terms are respectively
O(r^(2d+2-n)) and O(r^(3d+2-n)). Thus they vanish as r->0, exactly as required in the
two-stage argument. There is no surviving pure h^2 term at f=0: the exact flat-boundary
stress identity has zero geometry RHS.

Finally, dilation of the reduced quadratic form gives the certified D matrices,
with sign P_corrected=-d/dlog(lambda) E_reduced, hence positive D. The exact stress
identity, rather than the derivative of an arbitrary outer-data energy alone,
identifies this with P_outer plus the full-F rim. This last equality is an elementary
Noether/integration-by-parts identity, using the critical exponents; it must be
written explicitly when converting this organized proof into the final argument.

Peer-check status: the scheme removes the earlier conceptual cap/material-variable
gap and gives concrete uniform coefficient majorants. It is not a substitute for
writing the final Noether equality and checking each outer orientation/sign.
