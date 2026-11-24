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
