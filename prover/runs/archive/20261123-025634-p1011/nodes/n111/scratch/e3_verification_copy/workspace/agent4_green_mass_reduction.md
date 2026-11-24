# Conditional Green-metric positive-mass and rigidity reduction

This establishes a conditional geometric reduction, NOT the missing blow-up or
Pohozaev estimates. Standard spin positive mass with noncompact boundary and
Malcev residual finiteness are invoked as external established theorems.

## 1. Every compact locally conformally flat manifold is virtually spin

Pass first to the orientation double cover if necessary. The orientation-
preserving conformal holonomy is rho:pi_1(M)->SO^+(n+1,1) (equivalently the
corresponding effective quotient). Its image Gamma is finitely generated.
The inverse image Gammatilde in Spin^+(n+1,1) is a finitely generated linear
group: it is a finite central extension of Gamma, and Spin is linear through
its faithful Clifford-algebra representation. By Malcev's theorem it is
residually finite. Thus it has a finite-index normal subgroup H not containing
central -1. The projection H->Gamma is injective; its image Gamma0 has finite
index and admits a homomorphic spin lift. The finite cover of M corresponding
to rho^{-1}(Gamma0) is spin: pull back the sphere's conformal spin-frame bundle
by the developing map and quotient by the lifted holonomy. This construction
also works for manifolds with boundary, since their conformal charts extend
smoothly to the boundary. No assumption on their second fundamental form is
needed.

## 2. Sufficient jets imply AF Green ends

Assume that near a boundary pole p, a flat conformal chart has boundary
x_n=f(x'), f=O(|x'|^d), with differentiated estimates and d>n/2. Normalize the
positive Robin Green function to G=|x|^{2-n}(1+o(1)). Under inversion y=x/|x|^2,
the boundary becomes y_n=F(y'), with F=O(r^{2-d}) and derivatives, and its
Euclidean mean curvature is O(r^{-d}). The Kelvin factor
w(y)=|y|^{2-n}G(y/|y|^2) tends to 1 and satisfies the flat harmonic equation
and the conformally invariant Robin condition. Exterior barriers
r^{-q}(C-y_n/r), for 0<q<min(d-1,n-2), give w-1=O(r^{-q}); differentiated
bounds follow from scaled boundary elliptic estimates. Such barriers have
negative Laplacian for C sufficiently large, since
Delta r^{-q}=-q(n-2-q)r^{-q-2}, and positive outward normal derivative of order
r^{-q-1}, dominating the inhomogeneous Robin source O(r^{-d}). Exterior
comparison may be justified by the small trace-form norm of H on far tails.
Since d>n/2, choose q>(n-2)/2. Flattening the end changes the Euclidean metric
by O(r^{1-d}), so G^{4/(n-2)}g is AF of order q. This argument deliberately
does not assume a constant-term Green expansion, which generally requires
additional work when lower-order geometric singular terms are present.

## 3. Spin boundary PMT and rigidity

Invoke the spin positive mass theorem for AF manifolds with noncompact boundary:
a complete spin manifold, with smooth boundary, AF halfspace ends of rate
q>(n-2)/2 (usual first/second derivative bounds), and integrable nonnegative
scalar and outward mean curvatures, has nonnegative mass at each end. Zero
mass at one end implies that the manifold is Euclidean halfspace. The
multiend statement follows from the same Witten proof by prescribing a
constant asymptotic spinor on the selected end and zero at other ends.

The finite spin cover from (1), equipped with the lifted Green metric, is
complete and has finitely many AF halfspace ends, one per lift of p. Scalar
and mean curvatures are identically zero. The PMT thus applies in every
dimension. Mass at corresponding ends is unchanged under the local covering.
If one mass is zero, rigidity gives a single Euclidean halfspace end, so the
cover has degree one. The isometry of the punctured original manifold with
halfspace gives a conformal equivalence with punctured hemisphere. Locally
at p the map is a Euclidean conformal map in flat conformal charts; Liouville's
theorem for n>=3 makes it a Möbius map, which extends conformally across p.
Hence the original manifold is conformally a hemisphere.

## 4. STILL MISSING

This file does NOT prove that actual blow-ups force the jet condition in (2),
or that their local Pohozaev flux equals minus a positive multiple of the AF
mass. For a full sphere and harmonic G, direct calculation gives

  int Ric_{G^{4/(n-2)}delta}(x,nu_hat) dS_hat
     =4(n-1)/(n-2) * P_full(r,G),

where P=int[(n-2)G G_r/2-r|gradG|^2/2+r G_r^2]. On curved halfsphere patches,
spherical integration by parts gives an edge term. Its cancellation with the
noncompact-boundary mass correction, or vanishing under sufficient jets,
still needs to be established. Therefore this reduction is not a complete
low-dimensional compactness proof.


## 5. Direct compensated mass formula (completion of the conditional flux calculation)

Assume the AF estimates from (2), with q>(n-2)/2. In Kelvin coordinates the
metric is w^{4/(n-2)}delta on y_n>=F(y'), where
F=O(R^{1-q}), DF=O(R^{-q}), w-1=O(R^{-q}), with two derivatives.
Let T(z)=(z',z_n+F(z')); v=w composed with T. The pulled-back metric is

 g_ij=delta_ij + 4/(n-2)(v-1)delta_ij
       +F_i delta_jn+F_j delta_in+O(R^{-2q}),

and the derivative of the error is O(R^{-2q-1}). In the standard upper-
halfspace convention, the unnormalized boundary ADM flux is

 int_{S_R^+}(g_ij,j-g_jj,i) mu_i + int_{edge_R} g_an eta_a.

The error is O(R^{n-2-2q})=o(1). The conformal linear term contributes
-C int partial_R v, C=4(n-1)/(n-2). The graph linear term contributes
int_{S_R^+} Delta'F mu_n=int_{edge_R} partial_R F, by the divergence theorem
on the Euclidean half-ball. The explicit boundary ADM term gives the same
edge contribution. Replacing the flattened halfsphere by the physical curved
halfsphere, and v by w, changes this by O(R^{n-2-2q}). Consequently

 massflux=lim[-C int_{physical S_R} partial_R w
                 +2 int_{edge_R} partial_R F].

Under inversion write G=r^{2-n}+W, with W=O(r^{2-n+q}). The radial Pohozaev
functional is quadratic. Its fundamental term is identically zero, and its
cross term with W is, pointwise in the angular variable,

 P_cross=-a[(n-2)W+r W_r],  a=(n-2)/2,

where integration over the unit angular surface is understood. This equals
a times the Kelvin flux int partial_R w. Its quadratic W term is
O(r^{2-n+2q})=o(1). These identities hold on the physical curved halfsphere,
without angular integration by parts. We obtain

 massflux=-(C/a) lim_{r->0} P_aug(r,G),

 P_aug(r,G)=P_phys(r,G)-a*b int_{edge_{1/r}} partial_R F,
 b=(n-2)/(2(n-1)), a*b=(n-2)^2/[4(n-1)].

The usual normalization factor in the boundary ADM mass is positive and
irrelevant to signs. This proves the needed CONDITIONAL mass identification.
What is still missing is the analytic assertion that actual blow-up sequences
force nonnegative limiting P_aug. The finite shape-matrix positivity alone
does not establish that assertion.


## 6. Mixed full/half ends and compact boundary components

The normalized Green limit can have interior poles as well as boundary poles.
An interior pole gives a full AF end; a boundary pole gives a half-AF end.
Take the finite spin cover and then double across all minimal boundary
components using geodesic/Fermi collar coordinates (not the vertical graph
flattening, whose mixed metric entries need not vanish at the boundary).
The doubled metric is continuous and locally Lipschitz. Its distributional
scalar curvature is the ordinary scalar curvature on each side plus the
corner term proportional to the mean-curvature jump. Both sides are scalar
flat and both outward mean curvatures vanish, so the distributional scalar
curvature is nonnegative (indeed zero). The spin structures double.

The established spin positive mass theorem for continuous W^{1,n}_loc AF
metrics with nonnegative distributional scalar curvature applies in all
dimensions. At a doubled half-end its mass is a positive fixed multiple of
the boundary mass; interior full ends occur twice. Compact boundary components
cause no difficulty because they become compact seams in the double.

If a chosen boundary-end mass vanishes, rigidity makes the complete double
Euclidean space, which has exactly one end. Consequently there were no
interior poles, precisely one boundary pole upstairs, and the covering degree
is one. The doubling involution becomes a nontrivial Euclidean isometric
reflection with a codimension-one fixed set, hence reflection across a
hyperplane. One original side is Euclidean halfspace. This also excludes any
extra compact boundary components. The conformal compactification argument
in (3) then identifies the original metric conformally with a hemisphere.

As throughout, this is conditional on the jet and compensated-flux conclusions
for actual blow-ups. Those conclusions belong to the separate local analytic
lemma, not to the mass theorem itself.
