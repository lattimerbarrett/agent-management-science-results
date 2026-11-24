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
