# Dimension-three local isolated-simple Pohozaev sign

This file proves the local input SP in agent3_compactness_bridge.md in dimension 3, using the bounded Jacobi correction constructed in agent3_n3_local_lemmas.md. Standard tools used explicitly are mixed Green kernel estimates, boundary elliptic estimates, and the Euclidean bounded Jacobi kernel classification (proved below).

## 1. Normalizations and assumptions

Work in a conformally flat neighborhood of a selected point p_i. A flat conformal representative, followed by a local Mobius factor with prescribed first jet, can arrange simultaneously:

* p_i=0, tangent plane t=0, u_i(0)=M_i;
* the tangential derivatives of u_i at 0 vanish;
* H_i(0)=0.

The first jet of a Mobius conformal factor is arbitrary, so its tangential components cancel the flattening factor's tangential derivatives and its normal component makes H(0)=0. The value is normalized to 1. All transformations and their inverses have uniformly bounded smooth norms. At a blow-up core strict maximality is preserved, since its negative Hessian has order M_i^5, whereas the conformal-factor Hessian error has order M_i. Equivalently, recenter at the unique nearby core maximum.

Set epsilon_i=M_i^-2 and

    w_i(y)=M_i^-1 u_i(epsilon_i y).

The domain is t>F_i(z), where

    F_i(z)=epsilon_i f_i(z)+O(epsilon_i^2 |z|^3),
    |D^k(F_i-epsilon_i f_i)|<=C epsilon_i^2 |z|^(3-k), k<=2,

and f_i is a uniformly bounded tracefree quadratic polynomial. This follows from H_i(0)=0. Fix ONE sufficiently small physical outer radius delta_0. In Sections 1--4 the notation delta means this fixed delta_0, and R_i=delta_0/epsilon_i. In Section 5 the Pohozaev sphere radius r varies below delta_0/2; the correction and gradient constants remain those obtained at delta_0, independent of r. We work for |y|<R_i. Suppose the point is isolated simple, so the already proved decay lemma gives

    w_i(y)<=C/(1+|y|),
    w_i -> U=(1+|y|^2)^(-1/2) locally in C^2.

The equation and boundary condition are

    Delta w_i+3w_i^5=0,
    partial_nu w_i+(H_i^scaled/4)w_i=0,
    |H_i^scaled(y)|<=C epsilon_i^2 |y|.

The last bound uses H_i(0)=0 and smoothness.

## 2. Uniform mixed Green estimate

The domains D_i={t>F_i(z)} intersected with B_{R_i} have uniformly small graph slopes when delta is small. Let G_i be the Green kernel of -Delta with Neumann data on the graph and Dirichlet data on the outer sphere. Then

    0<=G_i(x,y)<=C/|x-y|,

and the boundary-source kernel obeys the same estimate. Constants are independent of R_i and i. One justification is to flatten the graph by a uniformly bilipschitz map, extend across its Neumann part, and extend by zero across the Dirichlet outer part. This gives a uniform critical Sobolev inequality. Testing the Green equation against truncations gives a uniform weak-L^3 bound; interior and reflected-boundary Moser estimates upgrade this to the displayed pointwise bound. This argument is invariant under dilation, so no constant grows with R_i. Mixed outer-edge corners can be rounded or exhausted from within; estimates persist by weak convergence. The associated harmonic extension from the outer boundary has sup norm no larger than its boundary sup, by the maximum principle.

## 3. A uniformly O(epsilon_i) lift of the geometric boundary error

Write B_i=partial_nu+H_i^scaled/4. Directly from the graph formula,

    -B_i U = epsilon_i f_i(z)/(1+|z|^2)^(3/2)+O(epsilon_i^2)

uniformly on the graph for |z|<R_i. Indeed

    partial_nu U=-(z.DF_i-F_i)/[(1+|z|^2+F_i^2)^(3/2) sqrt(1+|DF_i|^2)],

and all deviations from its tracefree-quadratic term are O(epsilon_i^2) on this range. The H term is also O(epsilon_i^2).

Let Phi_i be the bounded correction from agent3_n3_local_lemmas.md. Extend it below t=0 by

    Phi_i(z,t)=Phi_i(z,-t)+2t b_i(z), t<0,
    b_i(z)=-f_i(z)/(1+|z|^2)^(3/2).

This is C^2 across t=0. On the thin region needed here, |t|<=C epsilon_i |z|^2<=C delta |z|, it obeys |Phi_i|<=C and |D^k Phi_i|<=C(1+r)^(-k), k=1,2. In that strip,

    (Delta+15U^4)Phi_i=2t(Delta_z b_i+15U^4 b_i),

so its additional Laplacian error is O((1+r)^-2). On t>=0 the Laplacian is O((1+r)^-4). On the actual graph, Taylor's formula gives

    partial_nu(epsilon_i Phi_i)=-B_i U+O(epsilon_i^2).

Let V_i solve Delta V_i=0 in D_i, partial_nu V_i=-B_iU on the graph, and V_i=0 on the outer sphere. Comparing with epsilon_i Phi_i and using the mixed Green estimate shows

    ||V_i||_infinity<=C_delta epsilon_i.

Here are the potentially nonintegrable terms, explicitly controlled. The boundary remainder O(epsilon_i^2) has potential at most C epsilon_i^2 R_i=C delta epsilon_i. The positive-halfspace volume source epsilon_i(1+r)^-4 has potential O(epsilon_i). In a dyadic strip annulus r~s, the negative-t strip has thickness C epsilon_i s^2 and tangential diameter Cs. Its Newton-kernel integral is at most C epsilon_i s^3. Multiplying by the extra source bound epsilon_i s^-2 gives C epsilon_i^2 s; summing dyadically to R_i gives C epsilon_i^2 R_i=C delta epsilon_i. The outer comparison data have size O(epsilon_i). This proves the asserted bound without taking an absolute-value potential of the uncancelled, borderline m=2 boundary source.

## 4. Sharp closeness and the escaping-maximum argument

Put e_i=w_i-U. Then

    Delta e_i+c_i(y)e_i=0,
    0<=c_i<=C(1+r)^-4,
    partial_nu e_i=-B_iU-(H_i^scaled/4)e_i.

Mixed Green representation and the preceding lift imply, with E_i=||e_i||_infinity,

    E_i<=C_delta epsilon_i+C(R0) sup_{r<R0}|e_i|
                   +(C/R0^2+C delta^2) E_i.                 (1)

For clarity, the exterior potential norm is

    sup_x int_{r>R0} |x-y|^-1 (1+|y|)^-4 dy <=C/R0^2.

The Robin boundary perturbation has norm at most

    C epsilon_i^2 sup_x int_{graph, r<R_i}|x-y|^-1 r dS_y
        <=C epsilon_i^2 R_i^2=C delta^2.

The outer boundary values are O(1/R_i)=O_delta(epsilon_i) by the isolated-simple bound. These account for every term in (1).

Suppose E_i/epsilon_i ->infinity. The normalized functions e_i/E_i are bounded by 1 and converge locally, after subsequences, to a bounded solution psi of

    (Delta+15U^4)psi=0, partial_t psi=0.

The center conditions give psi(0)=0 and partial_{z_j}psi(0)=0.

The bounded kernel is precisely the scale and two tangential translation modes. To verify that the usual finite-energy kernel classification applies, write a bounded solution as the Neumann Newton potential of 15U^4 psi plus a bounded Neumann harmonic function. Even reflection and Liouville give

    psi=C+O(r^-1), Dpsi=O(r^-2).

Green's identity with the scale Jacobi field Z0=(1-r^2)/(2(1+r^2)^(3/2)) on a large hemisphere shows C=0: its limiting Wronskian is a nonzero constant times C, while the interior identity is zero. Hence psi has finite Dirichlet energy. Stereographic transfer to the round hemisphere identifies it with a first spherical harmonic satisfying Neumann boundary data, so psi lies in the stated three-dimensional kernel. Its value and tangential derivatives at 0 kill all three coefficients. Thus psi=0.

Divide (1) by E_i, first fix R0 large and delta small so its last coefficient is <1/2, then let i->infinity. The inner term tends to zero, and epsilon_i/E_i->0, giving a contradiction. Therefore

    ||w_i-U||_infinity<=C_delta epsilon_i.

Boundary and interior annular gradient estimates yield, for r<=R_i/2,

    |D(w_i-U)|<=C_delta epsilon_i/(1+r).

Indeed its amplitude is O(epsilon_i), its interior coefficient is O((1+r)^-4), and the graph boundary forcing and its scaled Holder norms are O(epsilon_i/(1+r))+O(epsilon_i^2). This gives the asserted estimate after dilation of each annulus.

## 5. The local Pohozaev limit is zero

For Delta u+3u^5=0 the critical stress flux through a smooth surface with outward normal n is

    (x.Du) partial_n u -(x.n)|Du|^2/2 +u partial_n u/2 +(x.n)u^6/2.

Its divergence is zero. On the graph, substitute partial_n u=-Hu/4 and integrate its tangential derivative term. The graph flux equals

    int_graph [ (xT.DH+H)u^2/8 -3H^2(x.n)u^2/32
                       -(x.n)|D_Tu|^2/2 +(x.n)u^6/2 ]
       -int_edge H u^2(xT.eta)/8.                           (2)

No mean-curvature convention is suppressed here: H is the trace, exactly as in the problem.

Let v_i=M_i u_i and suppose it converges locally away from 0 to a positive Green profile G. On a fixed physical sphere of radius r, its nonlinear stress coefficient is M_i^-4=epsilon_i^2 and tends to zero. Under y=x/epsilon_i the normalized stress is epsilon_i^-1 times the stress of w_i.

Use (2), F_i=epsilon_i f_i+O(epsilon_i^2 |z|^3), and the sharp estimates. The only potentially order-one geometric term is

    int f_i(z) [ -|D_z U(z,0)|^2+U(z,0)^6 ]/2 dz,

whose angular integral is exactly zero because f_i is tracefree and the bracket is radial. All remaining terms are bounded by C_delta0(r+r^2)+o_i(1), where C_delta0 is fixed before r tends to zero. No C_r constant is allowed to grow as r tends to zero. Explicitly, with R=r/epsilon_i:

* the gradient difference contributes at most C(epsilon_i R+epsilon_i^2 R^2)=C(r+r^2);
* the nonlinear difference contributes O(epsilon_i);
* graph cubic and normalization remainders contribute O(epsilon_i R)+O(epsilon_i^2 R^2);
* the H and edge terms contribute O(epsilon_i R)=O(r);
* the H^2 term contributes O(r^4).

The graph's intersection with the sphere differs from a flat disk only by a relative O(r^2) radial displacement; this is included in the normalization remainder. The exact radial-bubble spherical stress vanishes pointwise, so no artificial cap term occurs.

Consequently

    |P(G,r)|<=C(r+r^2),
    lim_{r->0}P(G,r)=0.                                    (3)

At an interior simple blow-up point, the same conclusion follows more easily from the exact Euclidean Pohozaev identity on balls, without any graph correction.

In dimension 3 the boundary Green parametrix is

    G=A/r+A q+B+O(r^alpha),

with q the mean-zero degree-zero angular correction. Its limiting Pohozaev value is

    -(AB/2)|S^2_+|.

Thus (3) implies B=0, in particular the required B<=0. If the metric itself is rescaled towards flat, all estimates above remain uniform, so this sign applies to the second-critical-radius and clustering limits in the general bridge.

This completes the dimension-three SP lemma, conditional only on isolated-simple decay and local microscopic convergence; both are supplied for selected points by the bridge's earlier steps. The circularity is avoided by applying the lemma on smaller balls before a second critical radius when proving simplicity.
