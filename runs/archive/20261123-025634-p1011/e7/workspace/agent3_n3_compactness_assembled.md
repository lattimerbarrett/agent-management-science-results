# Dimension-three positive Green mass and integrated compactness argument

## External classical theorems used

The analytic arguments in this proof use local Harnack and Schauder theory, Sobolev/trace theory and Lax-Milgram, positive Green kernels for coercive Robin forms, the Caffarelli-Gidas-Spruck classification of smooth positive entire critical solutions on R^3, and the dimension-three positive mass theorem including its minimal-boundary/halfspace version. The noncompact-boundary PMT used here is the theorem of Almaraz-Barbosa-de Lima. No recent compactness theorem is being assumed as a black box. The halfspace critical classification follows by even reflection from the whole-space theorem.

## Positive boundary Green mass

Let p belong to the boundary of a fixed smooth positive-Yamabe LCF 3-manifold. Conformally choose a metric flat near p with H(p)=0. This is possible because the first jet of a flat Mobius conformal factor is arbitrary; choose its normal component to cancel the initial mean curvature. Near p write the domain t>f_2(z)+O(|z|^3), tr D^2f_2=0. The explicit parametrix and coercive Robin correction constructed in agent3_green_expansion.md give

    G_p=r^-1+q+A_p+O(r^alpha),
    q=f_2(z)/(2(r+t)^2), 0<alpha<1,

with derivative remainder O(r^(alpha-1)). The positive Green function is normalized by the coefficient 1 of r^-1. Positivity follows from the coercive form and the negative-part test.

The metric ghat=G_p^4 g is complete off p and has scalar curvature zero and boundary mean curvature zero. Under inversion X=x/r^2, R=|X|, its end has

    ghat_ij=[1+4(A_p+q(X))/R+O(R^(-1-alpha))]delta_ij.

The inverted boundary is a graph of bounded leading height

    T=f_2(Z)/|Z|^2+O(R^-1).

Its derivatives are O(R^-1), so flattening produces an asymptotically flat halfspace chart of decay tau=1>1/2. Scalar and mean curvature are identically zero, hence the PMT's integrability conditions hold.

Here the anisotropic q term does not change the mass. Before flattening, the bulk ADM integral with halfspace normalization 1/(16pi) is

    (1/(16pi)) int_{S_R^+}(-2 partial_R[4(A_p+q)/R])dS
       =(1/(2pi)) int_{S_+^2}(A_p+q)domega=A_p,

since q has zero hemisphere average. The leading flattening gauge has displacement F(Z)=f_2(Z)/|Z|^2, homogeneous degree zero and angular mean zero. Its boundary mass term is proportional to the integral of partial_R F=0, and its bulk term is proportional to the angular average of Delta_Z F, also zero. All remaining gauge terms decay one power faster and have zero limiting ADM contribution. These angular cancellations are checked explicitly in agent3_checked_identities.py.

Thus the halfspace ADM mass is A_p. The boundary positive mass theorem gives A_p>=0. Its rigidity says mass zero forces ghat to be Euclidean halfspace. Compactifying its unique end recovers a conformal round hemisphere. The compactification is smooth: near the end the isometry, in flat conformal coordinates, is a Euclidean conformal map and hence Mobius, so inversion extends it across p. Therefore the hypotheses excluding the hemisphere give

    A_p>0.

The same conclusion is available on a nonorientable manifold by passing to its orientable double cover. A zero-mass lifted end would force a single-ended Euclidean halfspace, incompatible with the second lifted end. Extra compact minimal boundary components do not weaken the conclusion and are excluded by zero-mass rigidity.

## Positive interior Green mass

At an interior point p, choose the metric flat near p. Its Green expansion is G_p=r^-1+A_p+O(r). The conformal metric G_p^4g is complete scalar-flat asymptotically flat with a full-space end and nonempty compact minimal boundary. The usual three-dimensional PMT with minimal boundary gives nonnegative mass (equivalently double across the minimal boundary and use the PMT for the resulting scalar-nonnegative corner metric). Zero mass would force Euclidean space and in particular no compact minimal boundary. Thus A_p>0. The full-space ADM normalization gives mass 2A_p, so the sign is the same.

## Integrated dimension-three compactness conclusion

Suppose a sequence of positive solutions had unbounded maximum. Normalize H=0 once by the positive principal eigenfunction; solution correspondence preserves unboundedness and local conformal flatness.

Use the reflection-invariant fixed-threshold selection of agent3_compactness_bridge.md. Its local simple-decay proof is in agent3_n3_local_lemmas.md; its local sign SP is proved in agent3_n3_pohozaev_proof.md. More precisely, the local sign computation gives the stronger assertion B=0 for the regular constant of every normalized isolated-simple Green profile, with its explicit tracefree angular q term included. It is uniform under local rescalings, so it applies to the second-critical-radius and cluster limits.

The bridge then proves, in order:

1. An isolated selected point cannot be nonsimple: the second critical radius gives a harmonic profile with positive constant B=A, contradicting SP.
2. Selected actual/mirror centers cannot collapse. In the bounded-rescaled-height case, entire classification contradicts two strict maxima. In the unbounded-height case, simple decay and Harnack force all local selected heights to diverge; positive core Green lower bounds then prove neighboring-height comparability and a harmonic limit with at least two positive poles. Its regular constant is positive, again contradicting SP.
3. The selected set has bounded cardinality and uniformly separated points. Normalize by one unbounded selected height M_i. Strong decay on its fixed annulus and Harnack chains bound M_i u_i away from the finite pole set. At a fixed exterior point, positivity of the global Robin Green kernel also bounds the total source mass int M_i u_i^5. Its weak limit is a nonnegative finite sum of point masses, with a strictly positive coefficient at the chosen point. The normalized limit is consequently a nonnegative sum of positive Green functions; coercivity excludes an additional homogeneous term.
4. Its regular constant at the chosen point is strictly positive: its own pole contributes its positive coefficient times A_p>0, and all other Green poles contribute nonnegative values. This contradicts SP's B=0.

Thus no unbounded sequence of positive solutions exists. In particular max_{boundary M}u has a finite bound on each fixed manifold satisfying the problem's hypotheses in dimension 3.

## Audit status

The proof is assembled from explicit local constructions and a general selection bridge, not a quoted compactness theorem. It still requires independent audit of the fixed-threshold selection and mixed Green estimates; those are the standard-analytic steps where a hidden gap would matter. It proves no assertion in dimensions 4,5,6, and does not address the requested existence dimensions 7 through 18.
