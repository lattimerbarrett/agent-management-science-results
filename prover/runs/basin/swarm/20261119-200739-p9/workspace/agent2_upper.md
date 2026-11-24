# Upper-bound proof for beta(p)

Let A=[W]_{A_p}, U=W^{1/p}, and q=p/(p-1). Constants below depend only on p and dimension 2. Write <h>_I=|I|^{-1}int_I h.

## Standard auxiliary results required

(S1) Scalar reverse Holder: if w is scalar A_s, then for 1<r<=1+c_s/[w]_{A_s}, (<w^r>_I)^{1/r}<=2<w>_I, uniformly in I.

(S2) Convex-body sparse domination for the componentwise Hilbert transform: for integrable C^2-valued h,k supported in a bounded interval (and by truncation more generally), its bilinear form is bounded by a fixed finite sum of forms
C sum_{I in S}|I| sup{|<u,v>|: u in K_I(h),v in K_I(k)},
where K_I(h)={ <phi h>_I: phi scalar measurable, |phi|<=1 }, and S is eta-sparse with universal eta>0. The complex version follows by viewing C^2 as R^4 and applying to real and imaginary parts. This statement is linear-invariant, which is essential: replacing convex bodies by Euclidean average norms at the outset loses the needed estimate.

(S3) Hardy--Littlewood maximal norm: ||M_a f||_s <= C_s ((s/a)')^{1/a} ||f||_s for 1<=a<s, where M_a f=(M(|f|^a))^{1/a}.

Complete proofs of S1, S2 and S3 are supplied below, including an elementary maximal-determinant substitute for the ellipsoid theorem.

## Reducing matrices and their exact relation to the given characteristic

For each interval I choose positive definite reducing matrices V_I and V'_I such that
|V_I e| <= (<|Ue|^p>_I)^{1/p} <= C|V_I e|,
|V'_I e| <= (<|U^{-1}e|^q>_I)^{1/q} <= C|V'_I e|.
Existence follows from John's ellipsoid theorem on the real dimension-four unit balls, chosen invariant under multiplication by i so its defining quadratic form is Hermitian. The constants only depend on dimension. Finiteness follows by the original characteristic (choose one good x to see U^{-1} in L^q locally).

For any matrix B and t>0, ||B||^t is comparable to sum_{j=1}^2 |Be_j|^t. Thus
(<_x (<_y ||U(x)U(y)^{-1}||^q)^{p/q}>)^{1/p}
~ (<_x ||V'_I U(x)||^p>)^{1/p}
= (<_x ||U(x)V'_I||^p>)^{1/p}
~ ||V_I V'_I||.
All averages are over I. Consequently
sup_I ||V_I V'_I|| <= C A^{1/p}.
Moreover, for dual weight Sigma=W^{-q/p}, whose q-root is U^{-1}, the same calculation and ||V'_I V_I||=||V_I V'_I|| show
[Sigma]_{A_q} <= C A^{q/p}=C A^{1/(p-1)}.
This proves the required duality for this precise (mixed operator norm) definition, not an unjustified equality of the two characteristics.

## Directional reverse Holder and normalized moments

For fixed e!=0 the scalar weight w_e(x)=|U(x)e|^p satisfies [w_e]_{A_p}<=A: apply
|U(x)e|/|U(y)e| <= ||U(x)U(y)^{-1}||
and then take the exact two mixed averages. Likewise z_e=|U^{-1}e|^q has scalar A_q characteristic at most C A^{1/(p-1)}.

Choose r=1+c_p/A and t=1+c_p/A^{1/(p-1)}, with c_p small enough. S1 and the reducing properties, applied to e=V_I^{-1}e_j and e=(V'_I)^{-1}e_j, give
(< ||U V_I^{-1}||^{pr}>_I)^{1/(pr)} <= C_p,
(< ||U^{-1}(V'_I)^{-1}||^{qt}>_I)^{1/(qt)} <= C_p.
By adjoints the same estimates hold with the factor orders reversed.

## Sparse estimate

Put h=U^{-1}f and k=Ug, where f in L^p(C^2), g in L^q(C^2). For u in K_I(h),v in K_I(k), insert the reducing matrices into the pairing to obtain
|<u,v>| <= ||V_I V'_I|| <|(V'_I)^{-1}U^{-1} f|>_I <|V_I^{-1}Ug|>_I.
Let a=(qt)'<p and b=(pr)'<q. Holder with qt and pr and the normalized moment estimates shows this is at most
C A^{1/p} (<|f|^a>_I)^{1/a} (<|g|^b>_I)^{1/b}.
For a sparse collection choose disjoint sets E_I subset I, |E_I|>=eta|I|. Its sum is therefore bounded by
C A^{1/p} int M_a f M_b g
<= C A^{1/p} ||M_a f||_p ||M_b g||_q.
By S3,
||M_a||_{L^p} <= C_p (t-1)^{-1/p} <= C_p A^{1/[p(p-1)]},
||M_b||_{L^q} <= C_p (r-1)^{-1/q} <= C_p A^{1/q}.
To check the exponents rigorously, S3 initially yields (t-1)^{-1/a}, but 1/a-1/p=(t-1)/(qt); hence (t-1)^{-(1/a-1/p)} is uniformly bounded for t in the fixed interval used. The same argument applies to b.
Thus
|| U H U^{-1} ||_{L^p -> L^p} <= C_p A^{1/p+1/[p(p-1)]+1/q}
= C_p A^{1+1/[p(p-1)]}.
Truncation and density give the claim for smooth compactly supported original test functions, whenever [W]_{A_p}<infinity.


## Self-contained proof of S1 (agent_1's stopping-time argument)

Let B=[w]_{A_s}, with s>1. Scalar Holder and the A_s inequality give, for every measurable E subset J,
w(E)/w(J) >= B^{-1}(|E|/|J|)^s.
In the dyadic descendants of a given interval J, take the maximal subintervals K with <w>_K>2<w>_J. Their union has Lebesgue measure at most |J|/2, and each satisfies <w>_K<=4<w>_J by maximality and the dyadic parent bound. The weight of the retained portion is therefore at least 2^{-s}B^{-1}w(J). Set d=2^{-s}/B and rho=1-d. Iterating this stopping rule, and writing F_k for the union of generation-k stopping intervals, gives w(F_k)<=rho^k w(I), while dyadic differentiation gives
w(x)<=2*4^k<w>_I a.e. on F_k minus F_{k+1}.
The exceptional intersection of all F_k has w-measure zero. Hence for epsilon>0 with 4^epsilon rho<1,
int_I w^{1+epsilon}
<=2^epsilon <w>_I^epsilon sum_{k>=0}4^{k epsilon}(w(F_k)-w(F_{k+1}))
<=2^epsilon <w>_I^epsilon w(I) (1-rho)/(1-4^epsilon rho).
The last inequality is summation by parts followed by w(F_k)<=rho^k w(I); it is NOT obtained by bounding each exit mass by (1-rho)rho^k.
Choose epsilon=log(1+d/4)/log(4). Then 4^epsilon=1+d/4, so
1-4^epsilon rho=d(3+d)/4>=3d/4.
Also d<=1/2 and 2^epsilon=sqrt(1+d/4)<=sqrt(9/8). Thus the prefactor is at most (4/3)sqrt(9/8)=sqrt(2)<2. Dividing by |I| proves
(<w^{1+epsilon}>_I)^{1/(1+epsilon)}<=2<w>_I.
Since log(1+d/4)>=d/8 for 0<d<=1/2, epsilon>=2^{-s}/(8 log(4) B), proving S1 with an explicit constant. This uses only Holder, dyadic differentiation, and geometric summation.


## Proof of convex-body sparse domination S2

Work over R^d, d<=4, using real and imaginary parts. For an interval J define
K_J(h)={|J|^{-1}int_J phi h : phi real measurable, |phi|<=1}.
Realification suffices for real bilinear pairings, and the complex norm estimate follows from their duality. If K has deficient dimension, all calculations below take place in its real span. John's symmetric ellipsoid theorem supplies an invertible real map B_J on that span such that
B(0,1) subset B_J K_J(h) subset B(0,sqrt(d)).
In particular avg_J |B_J h|<=d sqrt(d): apply the supporting-functional identity sup_{u in K_J(h)}|u_j|=avg_J |h_j| and sum coordinates.

We use the following scalar facts, with their proofs recalled below:
(i) ||Hh||_{L^{1,infinity}}<=C||h||_1;
(ii) ||H_*h||_{L^{1,infinity}}<=C||h||_1;
(iii) ||Mh||_{L^{1,infinity}}<=C||h||_1.
Here H_* is the supremum of absolute symmetric truncations. Define, with h extended by zero outside 3Q0,
G_Q0 h(x)=sup_{P dyadic subset Q0, x in P} esssup_{z in P}|H(h 1_{3Q0 minus 3P})(z)|.
Kernel subtraction shows G_Q0 h(x)<=H_*h(x)+C Mh(x). Indeed, for z,x in P, compare its tail at z with a truncation at x of radius 2|P|: their kernel difference off 3P is bounded by C|P|/|y-x|^2, summable over doubling annuli; the intervening annulus is bounded by C Mh(x). Consequently G_Q0 is also weak (1,1).

Fix Q0 and let B=B_{3Q0}. Put g=B h 1_{3Q0}. Coordinatewise weak (1,1) shows that the exceptional subset E of Q0 where either |Hg| or G_Q0 g exceeds a dimensional constant L has measure at most C_d ||g||_1/L<=C'_d |Q0|/L. Choose L so that |E|<=|Q0|/16. Select the maximal dyadic subintervals P of Q0 on which avg_P 1_E>1/4. They cover E a.e. and have total length at most |Q0|/4. Since their dyadic parents have average at most 1/4, each P has |P intersect E|<=|P|/2 and hence contains a good point. At such a point the definition of G_Q0 shows
esssup_{z in P}|H(g 1_{3Q0 minus 3P})(z)|<=L.
Outside their union |Hg|<=L. Therefore
1_Q0 H(h1_{3Q0})=r_Q0+sum_P 1_P H(h1_{3P}),
where r_Q0(x) belongs to L K_{3Q0}(h) a.e.; this follows from |B r_Q0|<=L and B^{-1}B(0,1) subset K_{3Q0}(h).

Iterate the construction. The resulting dyadic collection S is 3/4-sparse. Its generation-n union has measure at most 4^{-n}|Q0|, so for almost every x the recursion terminates after finitely many generations. Thus
H(h1_{3Q0})(x)=sum_{Q in S}r_Q(x)1_Q(x),
with r_Q(x) in L K_{3Q}(h). No limit of singular integrals along shrinking intervals is required for this conclusion.

To integrate against k, let E be the John ellipsoid of K_{3Q}(h), with semiaxes a_j e_j. Since E subset K subset sqrt(d)E,
int_Q |r_Q(x) dot k(x)| dx
<=C_d sum_{j=1}^d int_Q |a_j e_j dot k(x)| dx
<=C_d |Q| sup_{u in K_{3Q}(h),v in K_Q(k)} |u dot v|.
Here avg_Q |u dot k|=sup_{v in K_Q(k)}|u dot v|, by choosing phi as the sign of u dot k, and each a_j e_j lies in K. Since K_Q(k) subset 3K_{3Q}(k), the last display is at most
C_d |3Q| sup_{u in K_{3Q}(h),v in K_{3Q}(k)} |u dot v|.
The collection {3Q:Q in S} is still sparse: its witnesses E_Q subset Q are disjoint and have measure >=(3/4)|Q|=(1/4)|3Q|. For compactly supported h,k choose Q0 containing supp(k) with 3Q0 containing supp(h). This proves precisely S2 with one non-dyadic 1/4-sparse collection. Approximation extends the pairing statement whenever both sides are defined.

### Elementary scalar facts used in this proof

The Hardy--Littlewood weak-(1,1) bound (iii) follows from the usual interval covering argument: extract disjoint selected intervals whose triples cover the level set, and sum lambda|I|<int_I|h|. The same proof gives M:L^{r,infinity}->L^{r,infinity} for every r>1, or this follows directly by splitting h at half the target level and integrating its weak distribution tail.

For (i), the Fourier multiplier of H is -i sign(xi), obtained by regularizing the odd kernel, so Plancherel gives ||H||_{2->2}=1. Perform the dyadic Calderon--Zygmund decomposition of h at height lambda: h=g+sum_J b_J, with disjoint J, int_J b_J=0, sum|J|<=||h||_1/lambda, ||g||_2^2<=2lambda||h||_1, and sum||b_J||_1<=2||h||_1. The good part is controlled by L2 Chebyshev. Outside the union of 3J, cancellation gives
|Hb_J(x)|<=C |J| dist(x,J)^{-2} ||b_J||_1.
Its integral over (3J)^c is at most C||b_J||_1. Summing and using L1 Chebyshev controls the bad part, proving (i). These arguments first apply to bounded compactly supported h, the only case needed for the original smooth input, and extend by approximation.

For (ii), fix 0<delta<1. Kolmogorov's elementary estimate, obtained by integrating distribution functions, states
(|J|^{-1}int_J |F|^delta)^{1/delta}<=C_delta ||F||_{L^{1,infinity}}/|J|.
For a truncation radius epsilon and x fixed, average over y in J=(x-epsilon/2,x+epsilon/2). Kernel subtraction bounds the difference between H_epsilon h(x) and H(h1_{R minus (x-epsilon,x+epsilon)})(y) by C Mh(x). Thus
H_*h(x)<=C_delta[(M(|Hh|^delta)(x))^{1/delta}+Mh(x)].
Indeed, subtract H(h1_{(x-epsilon,x+epsilon)})(y) from Hh(y), take the local L^delta quasiaverage, and apply (i) and Kolmogorov to the local piece. Finally (i), M bounded on weak L^{1/delta}, and (iii) give weak (1,1) of H_*. This completes all singular-integral auxiliary estimates in S2.


### Eliminating John's theorem, if complete elementary self-containment is desired

For any symmetric compact convex body K with interior in R^m, choose v_1,...,v_m in K maximizing the absolute determinant, and let T have these columns. The determinant is positive for some choice, so T is invertible. Replacing the j-th column by u in K shows |(T^{-1}u)_j|<=1. Thus K subset T[-1,1]^m subset sqrt(m) T B_2. Conversely, convexity and symmetry give T{a:sum|a_j|<=1} subset K, hence (1/sqrt(m))T B_2 subset K. Set E=(1/sqrt(m))T B_2. Then E subset K subset m E. This elementary ellipsoid substitutes for John's ellipsoid everywhere above, merely changing dimensional constants from sqrt(m) to m. For complex norm unit balls one may instead use agent_4's determinant-maximizing complex basis to obtain positive Hermitian reducing matrices directly. The sparse proof uses real bodies, so the elementary real argument just given is sufficient.


## Elementary quantitative proof of S3 (sharper form)

The weak-(1,1) covering estimate applied after splitting at lambda/2 gives
|{Mh>lambda}|<=C/lambda int_{|h|>lambda/2}|h|.
Integrate distribution functions and switch integrals:
||Mh||_r^r<=C r int |h(x)| int_0^{2|h(x)|} lambda^{r-2} d lambda dx
=C 2^{r-1} r/(r-1) ||h||_r^r.
Thus ||M||_{r->r}<=2 C^{1/r}(r')^{1/r}. For a<s and r=s/a, raising to power 1/a gives directly
||M_a||_{s->s}<=C_s ((s/a)')^{1/s}.
In the application a=(qt)',
(p/a)'=p/(p-a)=(qt-1)/(t-1),
which is at most C_p/(t-1) on the fixed bounded range for t. Therefore
||M_a||_{p->p}<=C_p(t-1)^{-1/p}
without even needing the earlier harmless endpoint-correction argument. Similarly ||M_b||_{q->q}<=C_p(r-1)^{-1/q}. This completes S3 from the interval-covering lemma and distribution-function integration.
