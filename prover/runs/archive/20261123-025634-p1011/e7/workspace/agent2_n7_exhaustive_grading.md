# Exhaustive n7 stress grading: diagnostic audit addendum

This supplements agent2_n7_diagnostic.md. It proves the COMBINATORIAL/homogeneity assertion that all model terms of mass order or lower fall into the displayed finite list, provided the already stated weighted bounds for the graph and Jacobi corrections hold. It does not independently reprove those analytic bounds or certify a final compactness theorem contrary to the problem's asserted answer.

## General grading lemma

Work at r>=1, epsilon r<=delta0, in ambient dimension7. Assign graph jet f_k and its associated physical/material correction the weight w=k-1. A graph jet has size epsilon^w r^(w+1), so its displacement divided by r, slope, and r times its Hessian each have size O((epsilon r)^w). A Jacobi correction of weight w has size epsilon^w r^(w+2-n), whose ratio to U~r^(2-n), and whose gradient's ratio to DU, each are O((epsilon r)^w). For the included model we need only w1(Phi2) and w2(Phi3), whose derivative bounds are already established.

The baseline quadratic-gradient stress has radial primitive scaling r^(2-n)=r^-5. Every extra shape or relative correction factor of weight w multiplies it by epsilon^w r^w. Therefore a model monomial of total weight d has bound
C epsilon^d integral_1^R r^(d-6)dr.
For d<5 this is O(epsilon^d) (finite core coefficient), d5 gives O(epsilon^5 logR), and d>5 gives O(epsilon^5 delta^(d-5)). The critical nonlinear term U^q decays TWO EXTRA POWERS of r compared with the gradient stress, so it cannot invalidate this upper-bound grading.

This covers every geometric coefficient:
* Normal and area factors are analytic functions of Dh near zero. Taylor terms are products of weighted slopes.
* H is a sum of Hessian terms multiplied by analytic slope factors. Its stress occurrence includes the compensating length factor; xT.DH has the same weight.
* Evaluating a field at t=h adds normal derivatives. Each derivative costs r^-1, canceled by a factor h of size epsilon^w r^(w+1), leaving exactly weight w.
* The physical spherical cap is expressed by solving r_z^2+h^2=R^2. The implicit solution is analytic in h/R near zero and produces the same products of graph weights; it has no independent coefficient or exceptional weight.
* Boundary-edge factors follow the same differentiation rule and have the same primitive scaling without radial integration.

A C7 Taylor expansion of the actual graph through f6 has remainder O(epsilon^6r7), with its derivatives through the stress order. This is simply a remainder of weight6 and hence O(delta) after mass normalization. No analyticity of the actual smooth graph is assumed.

The included positive model U+epsilonPhi2+epsilon^2Phi3 stays between U/2 and2U. Thus even though p9/5 and q14/5 are nonintegers, their MODEL Taylor series are analytic in the relative perturbation on this interval. Convergent tails of total weight>=6 sum to O(delta) for small delta0. Near r<=1 their remainders are O(epsilon^6), hence o(epsilon^5).

## Unknown remainder

The proved proposed second estimate is |E|<=Cepsilon^3r^-2, |DE|<=Cepsilon^3r^-3. Relative to U and DU these are both O((epsilon r)^3), so E acts as weight3. It need not be analytic or small relative to U at the outermost radius: the first/second Taylor bounds for s^q on 0<=s<=CU suffice, since q>2. An E-linear flux term also contains at least one graph factor, because the flat-plane Robin stress has x.nu=H=0. The E-linear terms of weight at most5 are exactly4(f2E),5(f3E), and5(E times two weight1 factors, such as f2^2 or f2Phi2). The first two are the dangerous terms handled by Young. The third has coefficient b^2logR=O(epsilon^2logR), hence tends to zero. This extra harmless class must be included for literal exhaustiveness. Any E-square term has total weight>=7, hence O(delta^2). E times higher model/graph factors has no smaller weight and is included by the same rule.

## Complete finite partition list

The entries below are graph DEGREES k; their weights are k-1. Every partition of weight1,...,5 appears exactly once. The checker generates all integer partitions and verifies this exhaustive list.

weight1: (2) -- tracefree linear term zero.
weight2: (3) odd; (2,2) positive quadratic Jacobi norm.
weight3: (4) known divergent linear counterterm; (2,3) odd; (2,2,2) coefficient b^3/epsilon^2=O(epsilon).
weight4: (5) odd; (2,4) bounded cross b A4/epsilon, Young against b^2/epsilon^3 leaves O(epsilon); (3,3) positive cubic Jacobi norm; (2,2,3) odd; (2,2,2,2) coefficient b^4/epsilon=O(epsilon^3).
weight5: (6) known finite ADM counterterm; (2,5),(3,4) odd; (2,2,4) coefficient b^2A4 logR=o(1); (2,3,3) coefficient b A3^2logR=o(1); (2,2,2,3) odd; (2,2,2,2,2) coefficient b^5logR=o(1).

Here b=O(epsilon) is the already derived coarse II rate, and all higher jets are bounded. Tangential parity is intrinsic to these polynomials: each factor of odd graph degree reverses parity, including its physical/material Jacobi correction; differentiation and tensor contraction preserve the total scalar parity. The whole stress is invariant under tangential reflection, so odd monomials integrate to zero on its symmetric reference cap; asymmetric-cap corrections are already additional weighted graph factors and hence appear elsewhere in the exhaustive list.

## What this does and does not resolve

This removes a purely combinatorial 'there might be another low-order analytic monomial' loophole. If the previously claimed weighted inverse estimates, exact bilinear coefficients, ADM matching and compactness bridge are correct and uniformly applicable, the n7 route remains a real conflict with the supplied answer. The honest next audit must target one of those substantive analytic claims or the problem's intended theorem/hypotheses; one must not silently invent a negative monomial absent from this exhaustive partition list. No final disproof or alternate classification is claimed here.


## Finite smooth normal extension, not field analyticity

Normal shifts of Phi2/Phi3 do not require an analytic extension. Use the finite Seeley reflection
Phi_ext(z,t)=sum_(k=1)^8 A_k Phi(z,-kt), t<0,
A_k=(-1)^(k+1) k binom(9,k+1),
so (A1,...,A8)=(36,-168,378,-504,420,-216,63,-8).
For every m=0,...,7, sum A_k(-k)^m=1. Thus derivatives through order7 match at the plane. Uniform weighted derivative estimates persist because k ranges over a fixed finite set and 1+|(z,-kt)| is uniformly comparable to1+|(z,t)|. Taylor's theorem with these C7 bounds gives the required finite weighted remainder O((epsilon r)^6) for the total grading; no analyticity of Phi or of the actual graph is needed. The Jacobi equation still matches at the plane through its second derivatives, so its extension residual is O(|t|) times the weighted third-derivative bound, exactly as used in the earlier source estimates.
