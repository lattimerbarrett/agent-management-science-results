# Diagnostic audit: weighted analytic estimates in dimension7

This is an audit of a possible compactness argument, NOT a claimed disproof of the user's stated answer and NOT a noncompactness construction. The main task's n7..18 existence remains unproved.

Set n7,p9/5,U=(1+r²)^(-5/2). Suppose an isolated-simple solution has local bubble convergence and strong decay v<=C U in the physical graph domain. Its boundary graph after scaling is epsilon f2+epsilon²f3+..., with f2 tracefree and b=|f2| bounded. The physical Jacobi corrections satisfy |D^l Phi2|<=Cb(1+r)^(-4-l), |D^lPhi3|<=CA3(1+r)^(-3-l), l<=7, after fixing center value and tangential gradients by kernel additions.

## Subquadratic nonlinearity

There is no automatic Taylor failure atp<2 for these models. For |eta|<=U/2,
|(U+eta)^p-U^p-pU^(p-1)eta|<=C U^(p-2)eta²,
by the integral second-derivative formula, because U+teta>=U/2. On r<=delta0/epsilon,
epsilon|Phi2|/U<=Cb delta0,
epsilon²|Phi3|/U<=CA3 delta0².
Choosing one fixed small delta0 makes both models uniformly positive/comparable toU. For the actual difference against a positive modelW, its exact divided-difference coefficient satisfies 0<=A<=C U^(p-1)<=C(1+r)^(-4), using onlyv<=CU andW<=CU. This needs no lower boundv>=cU. Gradient estimates need only a bounded coefficient, via localW2q estimates, not a uniform derivative of the subquadratic divided difference.

## First approximation

The geometry and nonlinear Taylor source after U+epsilonPhi2 is bounded by epsilon²(1+r)^(-5) in the bulk and epsilon²(1+r)^(-4) on the boundary. The model remains positive as above. The usual weighted exterior supersolution gives v-U-epsilonPhi2=O(epsilon²(1+r)^(-3)) with gradient O(epsilon²(1+r)^(-4)). Its contradiction proof has a Jacobi limitdecayr^-3; dividing byU gives sphericalgrowthrho^-2, subfundamentalrho^-5, so removability and the centerconstraints kill the kernel.

## Coarse quadratic-jet rate

The proposed exact stress expansion before extractingPhi3 gives a positivequadraticterm c b²/epsilon³ and absolute-errorbounds Cb/epsilon²+C/epsilon+C_delta. Purequadraticcubics b³/epsilon² are absorbed since their ratio to thepositivequadraticterm isepsilon b->0. The linearquartic/sexticcounterterms must first be removed exactly. The resultingquadraticinequality implies b=O(epsilon). This stage depends on the stresscalculation; it is not obtained fromweightedestimatesalone.

## Second model source bounds

Let W=U+epsilonPhi2+epsilon²Phi3 and assume the coarse rateb=Oepsilon. On the positivehalfspace its nonlinear quadratic remainder is bounded by sums
epsilon²b²r^-7, epsilon³b A3 r^-6, epsilon4 A3²r^-5,
all dominated by Cepsilon³r^-4. Subquadratic Taylor is valid by the relative modelbound above.

Belowtheflatplane use a finiteC7 matching extension. ForPhi2 its Neumann data have size b r^-5 and its tangentialLaplacian b r^-7. Multiplying by the extensionstripheight O(epsilon b r²+epsilon²A3r³+epsilon³A4r4) and the outsideepsilon produces terms
epsilon²b²r^-5, epsilon³b A3r^-4, epsilon4 b A4r^-3,
all bounded by Cepsilon³r^-4, usingb=Oepsilon andepsilon r<=delta0. ForPhi3 the analogousterms areepsilon³b A3r^-4 andepsilon4A3²r^-3, again bounded by the same target. Higherjets gainfactors epsilon r.

On the graph, the uncancelledlinearquartic source isepsilon³r^-3. Quadratic-squared sources epsilon²b²r^-4 are smaller. Quadratic/cubic interactions epsilon³b r^-3, cubic-squaredepsilon4r^-2, and allnormalization/curvatureterms have the same targetbound usingepsilon r<=delta0. Hence
|DeltaW+35 W^p|<=Cepsilon³(1+r)^(-4),
|B_scaled W|<=Cepsilon³(1+r)^(-3).

## Exterior inverse

For the second error, the supersolutionXi=C r^-2-Dt r^-3 ispositivewhenC is sufficiently larger thanD. In7D,
-Delta r^-2=6r^-4,
Delta(t r^-3)=-12t r^-5,
partial_out(-t r^-3)=r^-3 on t0.
Thus -DeltaXi>=c r^-4 and partial_outXi>=c r^-3 forC large. On a small-slopegraph the perturbations are relativelyOdelta0. The potentialAXi=O(r^-6) is absorbed forr>=R0large. Robinmean-curvatureperturbations are relativelyOdelta0². A positive supersolution gives the exterior mixed maximum principle after the ground-state transform, even though the original potential has the unfavorable sign.

The outerboundaryerror hasweightednormO(epsilon³): its three contributions divided byepsilon³R^-2 areR^-3/epsilon³=delta0^-3, b/(epsilon²R²)=b/delta0², and A3/(epsilonR)=A3/delta0. These are uniformlybounded for one fixeddelta0.

If the weighted norm ofv-W divided byepsilon³ were unbounded, normalize by that norm. Any local limit solves the homogeneousJacobiNeumannproblem and decaysr^-2. Its stereographicquotientgrowsrho^-3=o(rho^-5), so the punctureisremovable; the centerconstraints killtheJacobi kernel. The exteriorpositivebarrier thenrulesoutescapingmaxima. Consequently the proposedestimate is
|v-W|<=C_delta0 epsilon³(1+r)^(-2),
|D(v-W)|<=C_delta0 epsilon³(1+r)^(-3).

No displayed analyticpowercount orkernelclassification fails specifically atn7. This audit doesnot replace a fully integrated proof of the claimed n7compactness extension, and it doesnot supplythe n7..18 noncompactness construction requested bytheuser. A trustworthyrecentreference or a concrete defectinthis diagnostic remainsnecessary before making anysharpclaim.
