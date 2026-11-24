# DIAGNOSTIC: seven-dimensional Green mass after degree-two/three boundary jets vanish

This is a Green/ADM bookkeeping lemma, NOT a claim of compactness or a refutation of the problem. It isolates the GM side of the n7 diagnostic. If a nonlinear blow-up argument really forces the flat boundary's quadratic and cubic jets to vanish, no obstruction to applying the standard n7 boundary PMT is apparent here.

## Local Green expansion

Assume a positive-Yamabe LCF 7-manifold, a boundary point p, a representative flat near p, and graph

    t=f4(z)+f5(z)+f6(z)+O(|z|^7), z in R6.

The Robin coefficient is beta=5/12; the leading Green pole is r^-5. For homogeneous f_k the degree-(k-7) leading Robin defect is

    -5(k-1)f_k+(5/12)Delta_z f_k.

Construct the following exact homogeneous harmonic corrections in the flat halfspace:

    q4=r^-2Y4, (Delta_S6-6)Y4=0,
    partial_nu Y4=(5/3)f4-(5/12)Delta_S5 f4;

    q5=r^-1Y5, (Delta_S6-4)Y5=0,
    partial_nu Y5=(5/4)f5-(5/12)Delta_S5 f5;

    q6=Y6, Delta_S6 Y6=0,
    partial_nu Y6=-(5/12)Delta_S5 f6, int_{S6_+}Y6=0.

The radial identity used is Delta_z f_k|S5=Delta_S5 f_k+k(k+4)f_k. The first two angular operators with their Neumann condition are coercive. The last problem is compatible because its source has zero integral. Y5 is odd. Integrating the first equation gives

    int_{S6_+}Y4=(5/18)I4, I4=int_{S5}f4.

All data/operators are analytic, so analytic boundary regularity and Cauchy continuation extend the corrections harmonically through a fixed equatorial collar. The actual graph belongs to this collar as |t|/r=O(r^3).

The residual B(r^-5+q4+q5+q6) on the actual graph is bounded. The worst interaction is f4 D^2q4=O(r^4)O(r^-4)=O(1), with Df4 Dq4 and Hf4 q4 also O(1). The seventh-order graph remainder contributes O(1). Thus cutoff plus the coercive global Robin solve gives

    G=r^-5+q4+q5+q6+B+O(r^alpha), 0<alpha<1,

with the usual derivative bound O(r^(alpha-1)). Positivity follows from the principal-eigenvalue maximum principle.

## AF mass

The conformal metric G^(4/5)g is complete, scalar-flat and minimal-boundary off p. Under inversion, its slowest relative metric/flattening terms have decay R^-3, so tau=3>(7-2)/2=5/2. Quadratic products decay R^-6, faster than the mass order R^-5, and their ADM contributions vanish. Thus linear bookkeeping suffices.

The q4 conformal bulk mass term is canceled exactly by the quartic boundary-flattening flux. The q5/quintic terms are odd. The q6 conformal correction has zero hemisphere mean. The sixth-order boundary-flattening term has homogeneous degree -4 and contributes

    -2 I6/(3|S6|), I6=int_{S5}f6.

Therefore the normalized halfspace ADM mass is

    m=B-2 I6/(3|S6|).

This is the general formula m=B+(3-n)I_{n-1}/[(n-1)|S^{n-1}|] at n=7. It is not valid to replace m by B without the sixth-jet correction.

Assuming the standard boundary positive mass theorem in its usual dimension range 3<=n<=7, m>=0 and zero mass implies Euclidean halfspace. The same smooth conformal compactification argument as in the lower dimensions then gives the round hemisphere. Hence nonhemisphere would give m>0.

## Adapted Pohozaev

The linear fundamental/q4 Pohozaev cross term is

    -(15/2)r^-2 intY4=-(25/(12r^2))I4.

The q5 term has zero integral by oddness (its formal counterterm is 25I5/(8r)). The q6 mean is zero. The constant B term is -25|S6|B/4. Consequently

    P_adapted(r)=P_raw(r)+25I4/(12r^2)+25I5/(8r)+25I6/6

has limit

    lim P_adapted=-(25/4)|S6|m.

No quadratic Green-correction term survives this limit because its slowest possible order is r^1.

## Diagnostic status

All displayed local parametrix, AF, and linear mass identities follow by the same arguments as the audited n5/n6 GM lemmas. This file establishes no nonlinear seven-dimensional Pohozaev sign. Combining it with an incorrectly justified SP7 would produce an incorrect compactness claim; the weighted nonlinear approximation and complete stress grading must therefore be audited independently. No precise recent construction theorem or source has yet been identified by this team.
