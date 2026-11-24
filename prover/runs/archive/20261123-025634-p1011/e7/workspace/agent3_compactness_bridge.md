# Compactness bridge from local simple-blow-up signs (all dimensions)

This document separates the selection/isolation/clustering argument from the sharp local Pohozaev calculation. It does NOT assert the required local sign in dimensions 4,5,6. The classical analytic tools used below are local elliptic Harnack/Schauder estimates, positive Green kernels for coercive Robin operators, and the classification of positive entire critical solutions on Euclidean space (equivalently also on a flat Neumann halfspace by even reflection).

Let a=(n-2)/2, p=(n+2)/(n-2), K=n(n-2). Normalize a fixed positive-Yamabe metric conformally so H=0. Even reflection through its boundary gives a compact doubled space with uniformly elliptic Lipschitz metric and bounded scalar potential. The reflected quadratic form is coercive: each half contributes the coercive original form. No positive-mass theorem is applied to this nonsmooth double; it is used only for selection, elliptic estimates, and its positive Green kernel. Positive mass is applied on the original smooth manifold in GM. The reflected positive solutions solve the weak critical equation. The local principal coefficients are I+O(r), with bounded first derivatives. Original-side boundary Schauder estimates supply the derivative estimates used below. At blow-up scales the coefficients converge to Euclidean ones, including at the reflected interface.

## A. Precise local input needed

(SP) Suppose local positive solutions have an isolated simple blow-up at points p_i, heights M_i -> infinity, scales epsilon_i=M_i^(-1/a), and a normalized local Green limit G=lim M_i u_i away from the point. If the limiting geometry is Euclidean (space or halfspace), write G=A|x|^(2-n)+B+O(|x|), A>0. Then B<=0. For a fixed nonflat LCF geometry the corresponding statement is the local ADAPTED Pohozaev nonnegativity needed to force its renormalized Green mass nonpositive, after whatever jet-vanishing conditions the local argument proves. This need not be the raw constant term: in n=5 it includes the quartic-jet correction in agent3_mass_renormalization.md. The statement must be uniform under bounded smooth families and coordinate rescaling.

(GM) At the final fixed-manifold candidate point, the jet-vanishing conditions supplied by (SP) make the normalized positive Green function's adapted mass defined and strictly positive unless the original manifold is conformally a round hemisphere. At an interior pole, the same holds with nonempty compact minimal boundary ruling out the Euclidean zero-mass case.

Everything after A is a bridge conditional on these two local/global inputs. In dimension 3, the explicit q-parametrix and sharp closeness argument are intended to supply SP; boundary PMT supplies GM. They are not proved merely by this bridge.

## B. Isolated-simple decay, proved by the averaged ODE

Assume u_i<=C r^-a near an isolated selected peak, and assume its microscopic bubble convergence. Annular Harnack and derivative estimates give

    |D^k u_i|<=C r^-k A_i(r), k=1,2,

where A_i is the spherical average of the even reflection (or ordinary spherical average for interior points). Writing the equation in Euclidean principal part gives

    A_i''+(n-1)r^-1 A_i'=-k_i(r)A_i^p+E_i(r),
    0<c<=k_i<=C, |E_i|<=C A_i/r.

Indeed the coefficient error is O(r)D^2u_i+O(1)Du_i+O(1)u_i; averaging and Harnack give the assertion. Set t=log r and v_i=r^a A_i. Then

    v_i''=(a^2-k_i v_i^(p-1)+e_i(t))v_i, |e_i(t)|<=C exp(t).

Simplicity means v_i'<0 after its first critical point. At t0=log(R epsilon_i), bubble convergence makes v_i(t0) as small as needed by choosing fixed R large. Choose outer delta small and kappa in (0,a) so the ODE coefficient is >=kappa^2. Backward comparison gives

    v_i(s)<=2v_i(t) exp(-kappa(s-t)), t<=s<=T=log delta.

For z_i=v_i'+a v_i,

    z_i'-a z_i=-k_i v_i^p+e_i v_i.

Integrate backwards from T, where z_i(T)<=a v_i(T). Dividing by v_i(t) and applying the preliminary decay bounds gives

    z_i(t)/v_i(t) <= C exp(-(a+kappa)(T-t)) + C v_i(t)^(p-1) + b_delta(t),

where b_delta has uniformly bounded integral. Explicitly one may take

    b_delta(t)=C exp(t) int_0^(T-t) exp((1-a-kappa)s) ds.

Its integral from -infinity to T is finite and O(delta), including the logarithmic case a+kappa=1 (reverse integration, or integrate the displayed elementary exponential). The nonlinear term also has bounded integral by preliminary decay. Therefore

    v_i(t)<=C v_i(t0) exp(-a(t-t0)),
    u_i(x)<=C M_i^-1 r^(2-n).

The proof works through an endpoint with v_i'(T)=0. This endpoint fact is crucial in the next step.

## C. Every isolated selected blow-up is simple, assuming SP

If not, choose a second critical radius rho_i ->0. (If second critical radii stay bounded below, the point is simple on a smaller fixed neighborhood.) Microscopic bubble convergence gives rho_i/epsilon_i ->infinity. Before rho_i there is exactly one critical radius and the averaged quantity is decreasing after it. Step B applies through rho_i.

Rescale by rho_i and set m_i=M_i rho_i^a ->infinity. The normalized rescaled solutions m_i*rho_i^a*u_i(p_i+rho_i x) have an upper bound C|x|^(2-n) for 0<|x|<=1. Their lower bound is c|x|^(2-n), obtained from a local positive mixed Green kernel and the core bubble mass int u_i^p >=c/M_i. Subsequence convergence gives a positive Euclidean harmonic (Neumann, for boundary points) profile G with spherical average

    average G(r)=A r^(2-n)+B, A>0.

The derivative condition at the second critical radius passes to this average and gives

    0=(d/dr)[r^a average G(r)]_{r=1}=a(B-A),

so B=A>0. To pass the derivative at r=1, first propagate the O(1/m_i) bound from the annulus 1/2<r<3/4 to 1/2<r<3/2 by annular Harnack. This annulus lies inside the isolation neighborhood because rho_i tends to zero there. Its linearized potential is uniformly bounded after rescaling by the isolation estimate. Elliptic estimates now give C1 convergence of the normalized average through r=1. Equivalently, integrate the averaged equation using these annular bounds. On every smaller ball the central blow-up is simple, so SP gives B<=0, a contradiction.

The same argument applies when the original metric itself varies towards Euclidean after a cluster rescaling. If there is no uniformly small simple radius, select second critical radii tending to zero in those coordinates; otherwise retain a fixed simple radius. Both outcomes suffice for Step D.

## D. Fixed-threshold selection, including reflected peaks

Choose a fixed large R and fixed small tolerance eta. There exists C(R,eta) so any sequence with unbounded maximum admits finite sets S_i of strict local maxima such that:

1. each selected center is either on the reflection interface or has its reflected center also in S_i;
2. in microscopic coordinates at each selected center, u_i/M_i is eta-close to a normalized standard bubble on B_{4R};
3. the balls B_{R epsilon_{ij}}(p_{ij}) are pairwise disjoint;
4. u_i(x) dist(x,S_i)^a <=C(R,eta) everywhere.

Here and below harmless fixed multiples of R may be absorbed by choosing initial R larger. A detailed selection construction is as follows. If the last bound fails for the current set, take a point of large weighted height. The doubling point-picking procedure, inside a ball avoiding that set, supplies a point x of height M and a ball B_{L M^(-1/a)} where u<=2M, with L chosen in advance as large as desired. Rescaling and local elliptic compactness show that, for L sufficiently large, this bounded solution contains a strict local maximum with a profile eta-close on B_{2R} to a whole-space bubble: otherwise let L->infinity, extract a bounded entire positive critical solution, and contradict its classical bubble classification. The same holds at the reflection interface by evenness. Choose eta so small that a C2-eta perturbation of the bubble has only one critical point on B_{4R}; its Hessian is negative definite near its maximum, and its gradient is bounded away from zero on the remaining fixed annulus. Thus distinct centers are separated by at least 2R times the larger of their microscopic scales (use the uniqueness on the 4R profile balls). Consequently their R-bubble cores are disjoint. Add its reflection if different. Evenness and the same uniqueness ensure a reflected partner is either the identical interface maximum or outside its core. For each fixed i the process terminates: u_i is bounded, so all chosen epsilon are bounded below, and disjoint cores cannot be packed infinitely in a compact space. On termination the weighted bound holds with its fixed threshold C(R,eta).

All selected centers with microscopic heights relevant to a shrinking cluster have physical heights tending to infinity; low-height centers have a fixed positive exclusion radius. This selection does not assume a priori finite energy or a uniform bound on the number of peaks.

## E. No selected centers can collapse (explicit unequal-height argument)

Suppose d_i=min_{p!=q in S_i}dist(p,q)->0. This includes actual/mirror distances and therefore interior-to-boundary collisions. Rescale at a closest pair by d_i. The selected set is 1-separated; after subsequences it converges locally to a discrete set S containing at least two points at distance 1. Selected rescaled heights are

    h_ij=M_ij d_i^a >=c(R)>0,

by disjointness of the microscopic cores. The selection bound becomes

    w_i(x)<=C dist(x,S_i')^-a.

There are two exhaustive possibilities.

Case 1: every selected height stays bounded on every fixed rescaled ball. The selection estimate and the fixed eta-bubble cores then give local uniform bounds everywhere. Elliptic compactness gives an entire smooth positive critical solution on Euclidean space (the doubled limit), with at least two separated strict local maxima. Strictness survives because bubble-core closeness gives a fixed negative Hessian at each bounded-height selected center. This contradicts entire bubble classification.

Case 2: some selected height tends to infinity in a bounded rescaled ball. It is an isolated blow-up on a ball of radius <1/3, uniformly in i. Step C makes it simple on some fixed smaller ball, and B gives w_i<=C/h_ij on one fixed annulus. Hence w_i->0 there. Annular Harnack chains propagate convergence to zero throughout the connected complement of the locally finite selected set. A selected center with bounded height would then contradict its fixed bubble core and local elliptic regularity; consequently every local selected height, including both members of the closest pair, tends to infinity.

Let p_i,q_i be the closest pair, relabelled so h_ip>=h_iq. At p_i choose the fixed simple annulus provided by B,C. Its upper bound is C/h_ip. The positive global Green representation and q_i's bubble core give on the same annulus a lower bound c/h_iq: indeed the core has integral w_i^p >=c/h_iq, and the rescaled Green kernel is >=c at distance comparable to 1. Thus h_ip<=C h_iq. In particular their ratio lies in [1,C]. This proves comparability rather than assuming it.

Normalize by h_ip. Harnack chains from the p-annulus give local bounds away S; the nonlinear right side tends to zero there because w_i->0. Extract a positive harmonic limit G on R^n minus S. The positive core lower bound shows that the pole at p has coefficient >=c and the pole at q coefficient >=c*h_ip/h_iq>=c. In the halfspace formulation the limit is Neumann and is evenly reflected; in the doubled formulation both are ordinary positive poles.

The regular constant at p is strictly positive. To see this without an unjustified global subtraction, compare G with the sum of Dirichlet Green functions in a large ball for its positive poles p and q. On punctured balls the difference has nonnegative limiting boundary values, so the maximum principle applies; let the large radius tend to infinity. This gives G>=A_p|x-p|^(2-n)+A_q|x-q|^(2-n), hence the regular part at p is >=A_q|p-q|^(2-n)>0. SP at p gives the opposite inequality. Contradiction.

Thus d_i is bounded below. The number of selected centers is consequently uniformly bounded by packing.

## F. Terminal fixed-manifold contradiction, assuming GM

All unbounded selected peaks are now isolated on fixed-radius neighborhoods, hence simple by C and satisfy B. Normalize by the height M_i of any such peak p_i->p. Harnack chains off the finite peak set and the chosen peak's fixed-annulus estimate give local bounds for M_i u_i. Extract its positive Green limit. The nonlinear source measures are nonnegative; the core at p has a strictly positive coefficient. Coercivity eliminates any homogeneous solution, so the limit is a nonnegative linear combination of global positive Green functions. After dividing by its positive leading pole coefficient, the ADAPTED mass functional at p is its own strictly positive normalized Green mass from GM plus nonnegative contributions from the smooth positive Green values of every other pole. The local geometric counterterm scales with the leading coefficient squared in Pohozaev, or is unchanged after normalizing that coefficient to 1; it must not be counted anew for each smooth pole. SP contradicts this positivity. In dimension 3 no counterterm is present, and this is simply positivity of the ordinary regular constant.

Therefore a sequence satisfying SP and GM has uniformly bounded maximum. In particular this proves boundary bounds as well. The bridge includes interior peaks and virtual image poles; it is not a boundary-maxima-only selection argument.
