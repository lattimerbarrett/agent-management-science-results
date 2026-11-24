# Conditional compactness bridge audit in dimension seven

This audits `agent3_compactness_bridge.md` only. It is **not** a proof of the unassembled local SP7 lemma, and therefore not a claimed disproof of the question. Its conclusion is: there is no dimension-six restriction in the bridge itself. If the precise uniform SP7 and GM7 inputs in Section A of that file are established, the bridge implies compactness also for n=7.

## 1. Elliptic normalization and reflection
Positive principal Robin eigenvalue permits a smooth conformal representative with H identically zero: locally one can choose a smooth positive conformal factor with prescribed normal logarithmic derivative, keeping positivity. Conformal covariance preserves the equation and coercivity. Reflection is used only for uniformly elliptic selection and Green estimates. Its coefficients are Lipschitz, its potential bounded, and its quadratic form is the sum of the two coercive half-forms. Original-side boundary regularity suffices for all differentiated solution estimates. PMT is never applied to this double.

The subsequent local flat graph chart need not have H identically zero. This is not a simultaneous-gauge assumption: its actual Robin mean curvature is retained in SP. Conformal factors on a fixed finite atlas are bounded above/below, so blowup and boundedness are invariant.

## 2. Sharp isolated-simple decay has no n<=6 restriction
Write a=5/2 and p=9/5. After bubble convergence and annular Harnack, the averaged equation is

    v''=(a²-k(t)v^(p-1)+e(t))v, |e(t)|<=C exp(t).

On the decreasing simple annulus choose a fixed large microscopic radius and small outer radius so the bracket is at least κ², with κ=2. Since v'(s)<=0, backward comparison gives

    v(t)>=v(s) cosh(κ(s-t)), hence v(s)<=2v(t)exp(-κ(s-t)).

This remains true at a second critical endpoint v'(T)=0. With z=v'+av, integration of z'-az=-k v^p+ev gives

    z(t)/v(t)<= Cexp(-(9/2)(T-t))+Cv(t)^(4/5)+b(t),
    b(t)<=C exp(t) integral_0^(T-t) exp(-(7/2)s) ds
         <=(2C/7)exp(t).

All three right-hand terms have uniformly bounded integral in t: the last has integral <=2Cδ/7, and the nonlinear one is bounded by a constant times v(t0)^(4/5)/(κ(p-1))=(5/8)v(t0)^(4/5). Integrating (log v)'=-a+z/v yields the sharp bound u<=C M^-1 r^-5. No borderline exponent occurs at n=7.

## 3. Nonsimplicity contradiction
At a second critical radius ρ with ρ/ε→infinity, the normalized limit is positive harmonic on punctured flat space/halfspace. Its spherical average is A r^-5+B. Differentiation of r^(5/2) times this average at r=1 gives (5/2)(B-A)=0. The core lower bound gives A>0, hence B=A>0, contradicting precisely the Euclidean uniform SP input.

Passing the derivative through r=1 uses annular Harnack from [1/2,3/4] to [1/2,3/2], then elliptic estimates; it does not assume convergence only on r<1 is enough. Uniformity under rescaled geometries is a required part of SP, not obtained by just dropping geometric terms.

## 4. Fixed-threshold selection and clustering
The point-picking argument needs the entire positive critical-solution classification, valid in every n>=3, and not a uniform energy bound. Fixed C² bubble tolerance gives a uniform negative Hessian near each selected maximum and excludes other critical points on its fixed microscopic annulus. Thus the selected microscopic cores are disjoint. On a fixed individual compact manifold each u_i is bounded, so selection terminates. The number of peaks is not assumed uniformly bounded at this stage.

If d_i is the smallest selected-pair distance, put w_i=d_i^(5/2)u_i and h_ij=d_i^(5/2)M_ij. Disjointness gives h_ij>=c>0. If all local selected heights stay bounded, entire-solution compactness gives a single bubble with two strict maxima, impossible. If one height diverges, isolated simplicity and decay give w_i→0 on its fixed annulus, hence throughout the connected punctured complement by Harnack chains. All other local heights then diverge as well.

For the closest pair p,q with h_p>=h_q, take a fixed annulus inside the p-isolation ball. Its upper bound is C/h_p. The positive Green representation from q's microscopic core gives c/h_q on the same annulus, since q is at rescaled distance one. Therefore h_p<=C h_q. This proves comparability, including unequal-height configurations.

For clarity, the source scaling is exact:

    integral w_i^p dx=d_i^(ap-7) integral u_i^p dx
                       =d_i^(-a) integral u_i^p dx,

so q's core mass is at least c/h_q. The rescaled positive Green kernel is d_i^5 times the original kernel and is uniformly bounded below at rescaled distance comparable to one by its local parametrix.

After multiplying w_i by h_p, the harmonic limit has two positive fundamental poles. To justify the regular-part lower bound without an invalid direct maximum principle at zero-coefficient punctures, first compare with **(1-η)** times the two exact singular coefficients multiplied by Dirichlet Green functions in a large ball. The remaining coefficient at each puncture is positive, so the difference tends to +infinity there. The maximum principle applies. Then let η→0 and the ball radius→infinity. It follows that the regular part at p is at least A_q |p-q|^-5>0. SP contradicts this. Thus pair distances stay uniformly separated, and only now does packing give uniformly finitely many peaks.

## 5. Final fixed-manifold limit
Normalize by the height of any divergent selected peak. Its simple-annulus bound and Harnack chains bound the normalized solutions off the finite peak set and show the unnormalized solutions tend to zero there. The normalized nonlinear measures have nonnegative Dirac coefficients at the peaks and vanish off them. Coercivity eliminates a residual homogeneous solution. The limit is a nonnegative linear combination of positive global Green functions.

At the chosen pole, after dividing by its positive leading singular coefficient, its adapted mass is the strictly positive mass from GM plus nonnegative smooth Green values contributed by all other poles. Local geometric counterterms belong to the one singular coefficient, not separately to every smooth summand. The adapted Pohozaev expression is homogeneous quadratic in this normalization, so its sign is unaffected. SP and GM then contradict each other.

## 6. PMT bookkeeping
The original smooth Green-blowup manifold, not the reflected Lipschitz double, is the object for mass. For a boundary pole, the verified jet conditions f2=f3=0 yield AF decay τ=3>5/2; the scalar and mean curvatures are zero. Standard noncompact-boundary PMT includes ambient dimension seven. Boundary II=O(R^-4), and its square has integrable radial bound R^5 R^-8=R^-3. No global injectivity of a conformal developing map is needed.

For an interior pole the end is the ordinary AF end, with nonempty compact minimal boundary. Here one uses the corresponding standard low-dimensional PMT with compact minimal boundary (or its corner-doubling formulation), not a noncompact-boundary theorem with an inapplicable end type. Zero mass would force Euclidean space without such boundary, so the mass is positive. This is a standard external geometric theorem, not a Python-verified claim.

Nonorientability is handled by the orientable cover; zero-mass rigidity on the cover rules out an additional end. No spin assumption is needed in dimension seven.

## Verdict
The bridge is genuinely conditional on uniform local SP and strict GM, but those inputs, if rigorously established in n7, cannot be declared harmless diagnostics while simultaneously asserting n7 examples. No n<=6-only restriction was located in this audit. The outstanding task remains the exact full SP7 stress assembly or an actual defect/source clarifying the prescribed theorem.
