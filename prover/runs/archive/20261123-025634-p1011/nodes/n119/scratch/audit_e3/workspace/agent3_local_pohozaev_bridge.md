# Local compensated-Pohozaev lemma: detailed analytic assembly

STATUS: independently audited end-to-end by agents 2 and 4 after the
corrections recorded below. The conditional local lemma is established using
standard Sobolev/trace, elliptic, spectral Green-kernel and implicit-function
theorems together with the explicitly proved identities and estimates.
This file is the analytic bridge, not merely a finite-matrix calculation.

## Statement

Fix 3<=n<=18. In a flat conformal boundary chart write the domain as
x_n>h_i(x'), h_i(0)=Dh_i(0)=0, with uniformly bounded smooth derivatives.
By a uniformly controlled Mobius change arrange Delta h_i(0)=0. During
finite-dimensional modulation use center-dependent osculating-sphere Mobius
charts, so this trace condition is imposed at the final modulated center,
not merely at an initial approximate center. The adapted bubble center differs
from the ordinary one by O(epsilon_i^2 H); its parameter kernels differ by
O(epsilon_i), so the modulation implicit-function argument is unchanged. Let positive
solutions have an isolated boundary blowup at 0, height M_i, epsilon_i=
M_i^(-2/(n-2)), and suppose the sharp simple-profile bound holds up to a
fixed outer radius rho_0 (or a radius made fixed by rescaling):
 u_i(x)<=C M_i^(-1)|x|^(2-n) for C epsilon_i<=|x|<=rho_0.
Assume bubble convergence on every fixed epsilon_i-rescaled halfball.
Then every normalized harmonic Green limit G=lim M_i u_i satisfies:

1. The boundary graph at the limiting pole vanishes through every degree
   d<=n/2, except the degree-0,1,2 pure conformal gauge modes already removed.
2. With a=(n-2)/2, b=(n-2)/(2(n-1)), and
   H(r)=integral_{S^(n-2)} h(r theta) dtheta,
   L_h(r)=ab r^(-(n-2)) [2H(r)/r-H'(r)],
   lim_{r->0} [P(r,G)-L_h(r)] >= 0.
Here the sphere is intersected with the actual domain, and
 P(r,G)=integral [(n-2)G G_r/2-r|grad G|^2/2+rG_r^2].
The difference between the physical and tangent sphere conventions is included
in the shape expansion below; it is quadratic after the linear compensation.

## Step 1: exact graph functional and cutoff forcing

Flatten by T(y)=(y',y_n+h(y')). Its Jacobian is 1 and
 |grad_g v|^2=|grad v|^2-2h_a v_a v_n+|Dh|^2 v_n^2.
The Robin action is
 I_h(v)=1/2 integral |grad_g v|^2 + c integral_boundary b_h v^2
        - n(n-2)/q integral (v_+)^q,
 q=2n/(n-2), c=(n-2)/(4(n-1)),
 b_h=Delta h-h_a h_b h_ab/(1+|Dh|^2).
Thus I_h-I_0 is EXACTLY a quadratic form in v, denoted E_h(v,v)/2.
The graph expansion is linear+quadratic in Dh in the bulk, linear+cubic
in the boundary curvature density.

Scale epsilon_i, cut off the solution at R=rho/epsilon_i, and extend by zero.
Choose this cutoff in PHYSICAL Euclidean radius first, then pull back by graph
flattening. Thus its level cap is exactly the physical Pohozaev cap. Its pulled-
back expression is chi(|T(y)|/rho), not chi(|y|/R); the annular estimates below
are unchanged. Include its graph/parameter derivative in the forcing.
The cutoff solution v_i has uniformly bounded H1 norm and tends strongly to U
in H1: Caccioppoli on dyadic annuli and the sharp profile bound give
 integral_{|y|>A} |grad v_i|^2 <= C A^(2-n).
It solves I_h'(v_i)=F_i with F_i supported in R<|y|<2R. Write
 F_i(phi)=integral(f_i phi+B_i.grad phi)+integral_boundary g_i phi,
where |f_i|<=C R^(-n), |B_i|+|g_i|<=C R^(1-n), with corresponding scaled
first derivatives. Hence ||F_i||_{H*}+||d_p(F_i o T_p)||_{H*}<=C R^(-a).
Here T_p denotes the parameter identification described next, including the
ambient conformal gauge, not just graph flattening.

## Step 2: exact forced Schur complement, including parameter derivatives

For EACH parameter p (tangential center and width), first compose its ambient
Mobius osculating-sphere normalization, then translate/scale, and then flatten
its graph to the FIXED reference halfspace. The resulting functional is
 J_p(eta)=I_0(U+eta)+E_p(U+eta,U+eta)/2-F_p(U+eta).
The unperturbed I_0 is exactly p-independent by critical conformal covariance;
one need not assume these identifications are all self-maps of the initial
halfspace. Choose eta perpendicular to the fixed n-dimensional kernel K.
A concrete smooth gauge family uses the full-space bubble centered at
p-t nu(p), t=k epsilon^2/(1+sqrt(1-k^2 epsilon^2)), k=H(p)/(n-1);
it is exactly Robin on the osculating sphere and smooth at k=0. Its parameter
kernels differ from the standard ones by O(epsilon), so the modulation Gram
matrix remains invertible. Width variation fixes its center, hence its H-gauge.
Let A=I_0''(U)|Kperp, e_p=P E_p U, f_p=P F_p.
A has a bounded inverse by the hemisphere spectrum. The projected operator is
A+P E_p|Kperp, invertible if ||Dh||infinity+||b_h||L^(n-1) is small.
The reduced functional is
 j(p)=I_0(U)+E_p(U,U)/2-F_p(U)
      -1/2 <e_p-f_p,(A+E_p)^(-1)(e_p-f_p)> + Rem(p),
 |Rem|+|d_p Rem| <= C zeta^gamma,
 zeta=X_i+C(rho)epsilon_i^a, gamma=min(3,q)>2.
Here X_i is the jet norm defined in Step 3; the same zeta bounds e_p,f_p and
their parameter derivatives, uniformly on a compact parameter neighborhood.
Thus no unproved equivalence between a residual norm and its derivative is
being used.

Reason for the differentiated estimate: after trivialization only E_p and F_p
vary; their parameter derivatives have the same bounds as themselves. The
implicit derivative eta_p is O(zeta). Apply the scalar Taylor estimates for
(t_+)^q and its first derivative; for q>=3 use a cubic plus q-power remainder,
and for 2<q<3 use the q-power remainder. No unbounded differentiation generator
is applied to the nonlinear unperturbed action.

Expanding the inverse to first order gives
 (A+E)^(-1)=A^(-1)-A^(-1)EA^(-1)+O(||E||^2),
with the same parameter derivative bounds. In particular all linear-in-graph
terms must be retained: these include <e,A^(-1)f>, not merely the E f^2 term.

For comparison with the physical bubble use JOINT forced Schur invariance.
Under a first-order base change U->U+W, W=hU_n, set R=e-f and
B=E(U,U)/2-F(U). Direct expansion gives
 B -> B+R(W)+A(W,W)/2, R -> R+AW,
and B-<R,A^(-1)R>/2 is unchanged on Kperp. In particular -F(W) is INCLUDED
in R(W), so no forcing/pullback cross term is omitted. For arbitrary W the
exact defect is R_K.W_K. Either absorb W_K into the bubble parameters or use
 e(K)=O(X_i^2+epsilon_i^(n-2)), f(K)=O(R^(2-n)),
 W_K=O(X_i+R^(-a)).
The e(K) estimate follows by differentiating the vanishing direct FIRST graph
variation for every bubble parameter; the remaining graph terms are quadratic.
The f(K) estimate is the kernel tail estimate. Thus the defect and its parameter
derivative are o(X_i^2+epsilon_i^(n-2)) for each fixed rho. After this explicit
kernel adjustment, forced joint-Schur invariance is exact to the required
quadratic order. It includes the physical pullback and cutoff chain terms.

## Step 3: polynomial graph terms and uniform norms

Let D=floor(n/2), expand h_i=sum_{d=2}^D h_{i,d}+h_{i,>D}, and put
 t_{i,d}=epsilon_i^(d-1) h_{i,d}. Define
 X_i^2=sum_{d<n/2} epsilon_i^(2d-2)|h_{i,d}|^2
       +1_even epsilon_i^(n-2)log(rho/epsilon_i)|h_{i,n/2}|^2.
All coefficients are measured in a fixed orthonormal harmonic polynomial basis.

The linear graph residual has norm bounded by
 C[X_i+epsilon_i^a rho^((2D+2-n)/2)].
This follows from the explicit degree-d weights
 grad h_d grad U = O(r^(d-n)),
 (Delta h_d)U = O(r^(d-n)),
whose squared bulk radial integral is integral r^(2d-n-1)dr.
For d<n/2 it converges, for d=n/2 it is log R, and for d=D+1 it gives
 epsilon_i^(n-2)rho^(2D+2-n). The boundary dual estimate has the same threshold. At the borderline one
must NOT use the crude trace-Holder estimate (it loses a logarithmic power).
Instead use the explicit homogeneous angular corrector V=r^(1-d)phi and the
flattening shift h_d U_n; both have energy O(log R). The residual is A applied
to these fields plus cutoff terms of bounded norm, proving the sharp
H* norm O(sqrt(log R)).
Parameter derivatives multiply each homogeneous coefficient by d-1 or take a
translation derivative; they obey the same uniform estimates on compact
parameter sets. Cutoff derivative contributions satisfy the same radial bounds.

For finite degrees the NEGATIVE graph-only reduced scale derivative is a
positive constant times the certified matrices
 M_ell,jk=(ell-1+j+k)Q_ell,jk.
All finite-integral blocks n=5,...,18 are positive definite (142 exact minors).
For even n=2d the top-degree correction has leading homogeneous form
 V=r^(1-d)phi on the hemisphere, with
 (Delta_S-(d-1)^2)phi=0 and boundary source proportional to
 [1-d+j(4d-2j-3)/(2d-1)]P_ell.
This coefficient is nonzero for every nongauge sector. Its energy is
 log R integral[(d-1)^2 phi^2+|grad_S phi|^2]>0.
Top/lower cross terms are finite and absorb against the positive log diagonal.
The only d=2 zero source is the radial quadratic Mobius gauge.

## Step 4: first stage -- jet bounds at one fixed radius

At any one sufficiently small fixed rho, ||E_h||=O(rho). In the Schur formula
all terms involving f are bounded by eta X_i^2+C_eta(rho)epsilon_i^(n-2).
The graph-only errors are O(rho)X_i^2, the Taylor remainder is bounded by
eta X_i^2+C_eta epsilon_i^(n-2)rho^(2D+2-n), and the nonlinear C1 remainder
is o(X_i^2+epsilon_i^(n-2)) as i->infinity. The scale equation therefore gives
 c X_i^2 <= C(rho) epsilon_i^(n-2).
The outer cutoff/kernel pairing is bounded by the sharp annular profile estimate.
Fix rho=rho_0 once; this proves uniform coefficient bounds
 |h_{i,d}|^2 <= C epsilon_i^(n-2d), d<n/2,
 |h_{i,n/2}|^2 <= C/log(1/epsilon_i), even n.
Consequently the limiting graph starts in degree d_0>n/2.

## Step 5: localization, forcing mass, and the exact linear compensation

The Euclidean inverse kernel of A off K is obtained by conformally conjugating
the hemisphere resolvent of -Delta-n off its kernel. For x in a fixed inner
ball, and y in the annulus |y|~R,
 |partial_x^alpha K(x,y)|<=C_alpha R^(2-n).
Therefore A^(-1)F_i=O(R^(2-n)) in inner balls, not merely O(R^(-a)).

For the forcing-only Schur term, the Laplacian-inverse part is conformally
invariant and has zero scale derivative. Its difference from the A-inverse
part contains the bubble potential V=O((1+r)^(-4)); its derivative is
 O(R^(4-2n)) for n=3, O(R^(-4)log R) for n=4, O(R^(-n)) for n>=5.
All these are o(R^(2-n)). The comparison between the projected bubble inverse
and the Laplacian inverse also includes finite-rank kernel terms; their
pairings and differentiated pairings are O(R^(4-2n)), since f(K)=O(R^(2-n)),
and are likewise o(R^(2-n)). The leading forcing derivative is thus -F_i(Z_0).
The identification of the forcing pairing is an EXACT cutoff commutator
calculation, not merely comparison with a radial test profile. In physical
coordinates let w=chi v on an annulus where Delta v=0 and Bv=0 to leading
normalized order. Then
 F_out,bulk=-2 grad chi.grad v-v Delta chi,
 F_out,boundary=(partial_nu chi)v.
For the exact nonlinear equation add A(chi-chi^p)v^p to the bulk force.
Moreover div(v grad z-z grad v)=A z v^p, not zero. Both corrections pair
with z or Z_0 at O(R^(-n)) under the sharp profile bound, hence are
explicit o(R^(2-n)) errors. The formulas displayed next are the harmonic
leading part with precisely these errors understood.
For harmonic z=r^(2-n), integration by parts cancels the explicit boundary
cutoff term and gives
 F_out(z)=integral_annulus grad chi.(v grad z-z grad v).
A second integration by parts, using
 (v grad z-z grad v).nu=v Bz on the physical boundary, gives
 F_out(z)=integral_{S_rho}(z v_r-v z_r)
          +integral_{Sigma outside rho} chi v Bz.
The corrections from the normalized nonlinear equation vanish for fixed rho.
The width kernel satisfies Z_0=a z+O(R^(-n)), with the corresponding gradient
bound on the forcing annulus; hence
 F_out(Z_0)-a F_out(z)=O(R^(-n))=o(R^(2-n)).
At zero geometry the boundary term vanishes. The Wronskian is exactly minus
the linear Pohozaev cross term divided by a. Its nonlinear remainder is the
quadratic Pohozaev flux of v-z; by the AF bound below it tends to zero.
Consequently F_i(Z_0)=-P+lower-order terms in the flat case. In particular,
for z+B this reads F_i(Z_0)=2a^2 B |S_half|, P=-2a^2 B |S_half|.

Retained-jet mixed terms vanish after normalization: for degree d<n/2,
 epsilon_i^(-(n-2)) |<e_{i,d},A^(-1)F_i>|
 <= C(rho)epsilon_i^((n-2d)/2)->0.
The borderline case is O(1/sqrt(log(1/epsilon_i)))->0.
This uses the annular Green gain above, not the coarse H1 estimate.

ALL first-order terms of the limiting graph, including the graph/forcing cross
and first-order inverse correction, are canceled by the following exact
linearized identity. For U=r^(2-n) and physical correction V,
 Delta V=0,
 partial_nu V=-(n-2)r^(-n)[h-rh_r+r^2 Delta h/(2(n-1))].
If H(r)=integral h(r theta), harmonic angular averaging gives
 d_r P_linear(U,V)
 =-ab r^(-n)[r^2H''-nrH'+2(n-1)H]
 =d_r{ab r^(-(n-2))[2H/r-H']}.
Thus subtracting L_h removes every radius-dependent singular linear
geometric term, leaving a radius-independent regular/mass coefficient.
For the cutoff commutator above the linearized boundary integral satisfies
 a integral_rho^outer chi z Bz = L_h(rho)+integral_rho^outer chi' L_h.
TWO constants must be distinguished:
 C_chi=integral_rho^outer chi' L_h  (artificial, cutoff-dependent),
 C_mass=P_linear-L_h             (physical, radius-independent).
The commutator calculation reads
 F_out(Z_0)=-P_aug+C_chi+o(R^(2-n)).
C_chi MUST CANCEL; it is not the mass. Specifically the remaining first-order
physical graph/Schur/coordinate terms in the SCALE derivative equal +C_chi.
Here is the localization computation fixing this coefficient, rather than
merely determining its radial derivative. The differentiated exact physical
Noether conservation identity is (P_linear-L_h)'=0. Multiply by the physical
cutoff chi and integrate the annulus, using chi(inner)=1, chi(outer)=0:
 C_mass=-integral chi'(P_linear-L_h)
       =-integral chi' P_linear + integral chi' L_h.
The first summand is the annular forcing/physical-cap term -F_out(Z_0)
(as also verified by the exact commutator above). The second summand is the
remaining lateral-boundary/graph Noether contribution, exactly
 N_chi=integral chi' L_h=C_chi.
This equality follows from local conservation itself, including both cap
orientations, and leaves no undetermined radius-independent cutoff artifact.

The harmonic identity is used only after the normalized outer limit, not
claimed for the global bubble Jacobi corrector at finite scale. Indeed the
Jacobi potential-tail term for degree d has radial integrand
 U^(p-1) z V_d dvol = O(r^(d-n-2))dr.
Its annular integral is O(R^(d-n-1)); multiplying epsilon^(d-1) and dividing
by epsilon^(n-2) gives O(epsilon^2 rho^(d-n-1))->0 for each fixed rho.
Thus passage from exact Jacobi Noether conservation to the stated harmonic
outer conservation has a verified vanishing error. No global Jacobi field is
silently assumed harmonic, and no calibration constant is presumed zero.

To identify this Noether contribution with the sum of Schur terms, vary the
physical graph by t h while holding the physical outer forcing fixed.
Differentiate the EXACT forced equation/Robin data at t=0. Away from the bubble
its normalized derivative is the unique harmonic linear correction V with the
Neumann datum displayed above. On Kperp its uniqueness is precisely uniqueness
of the projected inverse in the Schur calculation. Joint forced-Schur base
invariance accounts for the flattening/pullback terms, including -F(W).
Thus the differentiated Schur functional and the differentiated physical
Noether identity describe the SAME derivative, not two functions merely having
the same radial scaling. Their remaining contribution is the explicit N_chi.
Consequently the scale equation has linear part
 -F_out(Z_0)+N_chi=P_aug-C_chi+C_chi=P_aug.
C_mass remains in P_aug. The artificial C_chi cancels exactly. This distinction
also shows that changing the cutoff cannot change the limiting mass sign. This includes the physical cap shift,
since the background fundamental solution has pointwise zero Pohozaev current.
The connection to the forced reduced gradient is obtained by the exact Noether
identity: with Z=a u+x.grad u and L=|grad u|^2/2-A u^q/q,
 grad u.grad Z-Au^(q-1)Z=div(xL).
Integrate on the physical domain cut by a sphere, include the boundary action
variation, use Robin, and integrate the tangential term. This gives exactly the
Robin Pohozaev identity checked in agent3_pohozaev_identity.py. With cutoff
forcing the right side is its pairing with Z; no cutoff edge is omitted.
After flattening the physical generator is
 a v+y.grad v+[h-y'.grad h]v_n.
The difference from the flat generator is the coordinate/base shift in the
Schur complement. At a projected solution, the residual annihilates Kperp,
so changing generator changes the reduced gradient by its finite K-projection
matrix, which tends to the identity and is invertible. At an actual solution
all reduced components vanish, and this gives the stated Noether projection.
Differentiating this EXACT identity at h=0 produces the linear formula above,
including all direct, mixed, inverse, cutoff, and cap-displacement terms.

To justify using the fundamental linear identity when G differs from U,
first use the AF barrier after jet vanishing: for some tau>(n-2)/2,
 G-U=O(r^(2-n+tau)) with derivative bounds. Every linear graph cross term
with G-U is then O(rho^(d_0+tau+1-n))=o(1), since d_0>n/2 and tau>(n-2)/2. Thus only U
is needed to identify the singular linear counterterm; its radius-independent
constant is retained as the mass, NOT discarded.

After this cancellation the remaining outer terms are at least quadratic in
the graph. Since h=O(r^d_0), d_0>n/2, their normalized bounds are
 O(rho^(2d_0-n)), O(rho^(d_0-n/2)), and O(rho^(d_0-1)), all tending to zero.
Equivalently these follow from inverse remainder E^2 f^2, E e f, E e^2,
using the fixed-radius jet bound from Step 4. Taylor remainder gives an
additional O(rho^(2D+2-n)). The nonlinear remainder vanishes for each fixed rho
as i->infinity, since epsilon_i^(a(gamma-2))->0.

The scale equation, with width-dilation orientation, consequently yields
 liminf_i P_aug(rho,M_i u_i)
 >= c liminf_i epsilon_i^(-(n-2))X_i^2 - o_rho(1).
Letting rho->0 proves the asserted compensated nonnegative-flux sign.

## Scope and audit status

This proof uses no energy bound or already-established global simplicity; it
uses precisely the sharp pre-second-radius bound. Its scale uniformity follows
from uniform chart derivative bounds, the annular Green estimates, and choosing
the physical cutoff before pulling back. Exact Noether, cutoff-commutator,
forced joint-Schur invariance, and uniqueness of the projected linearization
identify every first-order graph/forcing term; their radius-independent
constant is retained, not set to zero. Independent end-to-end re-audits by agents 2 and 4 found no remaining
unproved dimension-specific analytic step. The unified theorem still needs
to present the connected selection/cluster and global mass/rigidity modules,
not merely cite this local lemma without its stated proof.
