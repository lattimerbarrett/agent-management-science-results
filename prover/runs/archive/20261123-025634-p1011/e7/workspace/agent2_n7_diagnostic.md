# DIAGNOSTIC ONLY: attempted extension of the n6 local proof to n7

This document records a potential contradiction in the developing argument. It is NOT presented as a disproof of the requested theorem, nor as a certified n7 compactness theorem. Its purpose is to expose any missing term or invalid estimate in our n6/n7 reasoning. All four agents have so far found no elementary exponent obstruction; the unresolved issue must be audited rather than suppressed.

## The proposed extension

At a boundary maximum choose a locally flat chart with H(0)=0 and graph h=f2+f3+f4+f5+f6+O(r7), tracefreef2. Let n7, epsilon=M^(-2/5), v=M^(-1)u(epsilon y), U=(1+r2)^(-5/2). Assume isolated-simple strong decay and local bubble convergence. The first-correction argument gives
v=U+epsilon Phi2+e1,
|e1|<=Cepsilon^2(1+r)^(-3), |De1|<=Cepsilon^2(1+r)^(-4).
The proof is the same weighted inverse as n5/6. Although p9/5<2, U+epsilonPhi2 stays in[U/2,2U] on the fixed chart: epsilonPhi2/U=O(epsilon b r), b=|II|. Therefore Taylor expansion of the MODEL remains quadratic with coefficient U^(p-2); no unjustified global subquadratic Taylor estimate is used. Its quadratic source decay is r^(n-6)r^(6-2n)=r^-n, stronger than required r^(2-n). The exact divided difference between actual v and the positive model gives potential bounded by C r^-4.

The first approximation's weighted normalized Jacobi limit transforms on the sphere to growth rho^-2, subfundamental rho^-5 in n7; the point is removable and center constraints eliminate the kernel. Exterior barriers are the usual positive radial-power/normal combination. Thus this step has no identified dimension7 failure.

## Coarse II rate

Normalize the stress by epsilon^-5. The positive quadratic model is c b^2/epsilon^3. The first remainder gives quadratic-geometry error at most Cb/epsilon^2, because its radial exponent is2-6-4+5=-3, integrable. An unsigned cubic contribution is at most C/epsilon, radial exponent3-6-4+5=-2, also integrable. After including the linear lower-jet counterterms, fixed-radius flux is bounded. Hence
b^2/epsilon^3 <= Cb/epsilon^2+C/epsilon+C_delta,
which implies b=O(epsilon). Pure-quadratic third-order terms normalize to b^3/epsilon^2 and are absorbed into the leading b^2/epsilon^3 by epsilon b ->0. Quadratic/quartic mixed terms b/epsilon are smaller than the displayed generic first error.

## Proposed second approximation

In n7 the cubic physical Jacobi correction Phi3 is genuinely in D^(1,2), decays r^-3, and has strictly positive Jacobi energy on angular sectors1/3 after removing translation kernel. The source compatibility in sector1 follows the same exact beta cancellation as n6. Set W=U+epsilonPhi2+epsilon^2Phi3.

The quadratic-squared sources are epsilon^2b^2 r^-5 in bulk and epsilon^2b^2r^-4 on the boundary. Since b=Oepsilon, these are dominated by epsilon^3r^-4 and epsilon^3r^-3. All cubic linear sources cancel; quartic sources have exactly those target weights. Phi3 extension-strip terms and model nonlinear products are smaller. The model is positive and comparable to U because epsilon^2Phi3/U=O(epsilon^2r^2)<=Cdelta0^2. Even for p9/5 its second-order remainder is valid on this positive interval.

The proposed weighted inverse has exponent2:
|v-W|<=Cepsilon^3r^-2, |D(v-W)|<=Cepsilon^3r^-3.
Its exterior supersolution is C r^-2-D t r^-3, with
-Delta r^-2=6r^-4, Delta(t r^-3)=-12t r^-5,
and outward plane derivative partial_nu(-t r^-3)=r^-3. Choose C>2D and then large inner radius and small delta0. Outer data weighted by r2 are R^-3=epsilon^3/delta0^3. The normalized Jacobi limit transfers to sphere growth rho^-3, still subfundamental rho^-5, so removable and kernel-killed. This is exactly the same proof as the audited n6 second approximation, with a different weight.

## Leading proposed sharp stress terms

The exact degree-j bilinear graph/correction identity is (j-1)L(Phi_j,Phi_j). Both L(Phi2,Phi2) and L(Phi3,Phi3) are positive in n7 by the exact hemisphere Neumann spectrum. Thus the normalized main terms are
+c2 b^2/epsilon^3 +c3 |f3|^2/epsilon.
The f2/Phi3 and f3/Phi2 cross terms are tangentially odd and vanish. The proposed second error gives:
* quadratic geometry: epsilon b*r2*r^-6*epsilon^3r^-3*r5dr=epsilon^4 b r^-2dr, normalized O(b/epsilon), absorbed into eta b^2/epsilon^3+O(epsilon);
* cubic geometry: epsilon^2*r3*r^-6*epsilon^3r^-3*r5dr=epsilon^5r^-1dr, normalized O(|f3|logR), absorbed into eta|f3|^2/epsilon+O(epsilon log^2R);
* quartic geometry: epsilon^3*r4*r^-6*epsilon^3r^-3*r5dr=epsilon^6dr, normalized O(delta).
The H/error terms have the same weights.

Truncated cubic model energy differs from its full positive energy by O(|f3|^2/R); after normalization this is O(|f3|^2/delta), absorbed into |f3|^2/epsilon for fixed delta and large i. Quadratic tails are even smaller.

## Audit of nonlinear/higher graph grades

Here is the proposed complete dangerous-term list, before claiming any theorem:
1. Pure quadratic third-order shape terms: epsilon^3 b^3, normalized b^3/epsilon^2=Oepsilon.
2. Quadratic/quartic second-order mixed terms: epsilon^4 b A4, normalized b A4/epsilon. Young against b^2/epsilon^3 leaves O(epsilon A4^2).
3. Quadratic/cubic second-order mixed terms: odd, vanish.
4. Quadratic-squared/cubic third-order terms: odd, vanish; even without parity their coefficients b^2 times normalized at most1/epsilon would tend0.
5. Quadratic/cubic-squared third-order terms: critical radial log, normalized at most b|f3|^2logR=O(epsilon logR).
6. Quadratic-squared/quartic third-order terms: normalized at most b^2A4logR=O(epsilon^2logR).
7. Pure cubic third-order terms: at worst epsilon^6R, normalized O(delta); their odd parts vanish.
8. Fourth/higher pure quadratic terms: at worst b^4/epsilon times a logarithm, tending0 with b=Oepsilon.
9. Any second-order pair of graph degrees j,l withj+l>=8: radial primitiveR^(j+l-7), normalized contribution delta^(j+l-7), hence Odelta. Degree3+4 is the borderline log mixed with bounded f3 and A4; it has tangential odd parity and vanishes. Degree2+5 is also odd. Their perturbed-cap corrections move to the listed higher groups.
10. H^2(x.nu), Jacobian/normal denominators, and cap shifts carry extra slope or normal-height factors. Their lowest nonodd pure-quadratic degree is item1; every remaining term is one of items5--9.

If this list is genuinely complete, it yields a nonnegative adapted terminal Pohozaev sign in n7. The exact identities and displayed exponents have been checked in agent2_n7_diagnostic_checks.py. What has NOT been independently certified is the assertion that this grading list includes every geometric/material term; that is the crucial open audit point.

## Linear counterterms and the mass diagnostic

The general jet-counterterm formula gives
P_adapted(r)=P_raw(r)+25 I4/(12r2)+25 I5/(8r)+25 I6/6.
Here I_j=integral_[S5]f_j; I5=0 by oddness. Exact direct first graph flux has precisely the coefficients25/12 forf4 and25/6 forf6; checked symbolically. These are not optional, since rawGreenP has lower-jet divergences.

If the proposed positive inequality holds, fixed-radius boundedness forces II=DII0 at the limiting point. Then h starts atdegree4, the Green correction starts atdegree-2, and the inverted metric has AFdecay3>5/2. Quadratic tails decay6>massorder5. The critical f6 jet shifts the mass by -2I6/(3|S6|), while f4 divergences are removed by the counterterm and f5 is odd. Thus
lim P_adapted=-(25/4)|S6|m.
The usual boundary PMT in dimension7 would make m>0 off the hemisphere. Coupled with the team's conditional selection bridge this WOULD contradict blowup in n7, contrary to the supplied target answer. We do not certify that conclusion here: this document is the requested diagnostic for finding an actual missing analytic/geometric term, source hypothesis mismatch, or gap in our purported n6/n7 Pohozaev derivation.
