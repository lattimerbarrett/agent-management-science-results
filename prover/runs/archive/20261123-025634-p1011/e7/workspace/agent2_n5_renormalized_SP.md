# Dimension-five renormalized isolated-simple Pohozaev calculation

## Scope and conventions

This calculation uses the weighted approximation proved in agent2_n5_n6_weighted_first_approximation.md and is conditional on local bubble convergence and isolated-simple strong decay. The selection/compactness bridge is separate. It also requires the Green-mass matching recorded by agent3; raw spherical Pohozaev alone is not the mass invariant at a nonumbilic boundary germ.

Let n=5, beta=3/8,c=3/16,a=3/2,k=15,q=10/3. In a locally flat chart at a boundary maximum choose H(0)=0 and write
h(z)=f2(z)+f3(z)+f4(z)+O(|z|^5),
with f_j homogeneous of degree j, tr D^2 f2=0. After scaling x=epsilon y, the graph is epsilon f2+epsilon^2 f3+epsilon^3 f4+O(epsilon^4 r^5). Write U=(1+r^2)^(-3/2), v=M^(-1)u(epsilon y), epsilon=M^(-2/3). Fix an outer delta0 once and for all. The proved estimate is
v=U+epsilon Phi2+e,
|e|<=C_delta0 epsilon^2(1+r)^(-1), |De|<=C_delta0 epsilon^2(1+r)^(-2),
for r<delta0/epsilon. Phi2 is linear in f2 and |D^j Phi2|<=C|f2|(1+r)^(-2-j).

Let P_r(w)=integral_(partial B_r intersect M)[a w partial_r w-r|Dw|^2/2+r(partial_r w)^2] be the LINEAR spherical Pohozaev flux. For the original solution u the exact critical flux adds k r u^q/q. For w=M u its exact normalized counterpart adds k epsilon^2 r w^q/q; this term is o_i(1) at every fixed r by strong decay. Thus multiplication by epsilon^(-3) of the rescaled exact flux agrees with P_r(Mu) up to o_i(1). Define
sigma5(f4)=(9/8) integral_[S3]f4,
Ptilde_r(w)=P_r(w)+sigma5(f4).
Then, for each sufficiently small fixed delta<delta0/2,
Ptilde_delta(Mu)>=c0 |II(0)|^2/epsilon-o_i(1)-C_delta0 delta,
where c0>0 is dimensional and the o_i is taken with delta fixed. The quartic counterterm is essential.

## Exact stress identity

For any smooth solution, the critical stress is
J=(x.Du+a u)Du-x|Du|^2/2+(k/q)x u^q,
and div J=0. On the graph use partial_nu u=-beta H u. Tangential integration gives
P_sphere(u)= -beta/2 integral_graph (xT.DH+H)u^2
 -beta(beta-1)/2 integral_graph H^2(x.nu)u^2
 +1/2 integral_graph (x.nu)|D_T u|^2
 -(k/q) integral_graph (x.nu)u^q
 +beta/2 integral_edge H u^2(xT.eta).
This is an exact identity, not an ansatz statement.

## Linear graph terms and the counterterm

Inserting U into the Robin-substituted graph flux and retaining terms linear in a homogeneous f_j leaves only an edge expression after integration by parts, since
c Delta_z(U^2)=|D_z U|^2/2-(k/q)U^q.
The f2 term has zero angular average by tracefreeness, and f3 is odd. For f4, only its spherical mean matters. Per unit mean and unit sphere area the GRAPH flux is
9 R^6(R^2-2)/[8(1+R^2)^4],
which tends9/8; hence the spherical flux has the negative of this coefficient. The checker derives this expression exactly from the edge formula
c[-3R^7(U^2)'-12R^6U^2].
At R=delta/epsilon this contributes -epsilon^3 sigma5(f4)+o(epsilon^3). Higher linear jets have size O(epsilon^3 delta): a degree j>=5 edge contribution scales as epsilon^(j-1)R^(j-4)=epsilon^3 delta^(j-4). Smooth Taylor remainders satisfy the same bound using uniformly bounded fifth derivatives.

## Positive quadratic contribution

The terms bilinear in epsilon f2 and epsilon Phi2 have coefficient
K2=integral_[R4] f2(DU.DPhi2-kU^p Phi2).
Tangential integration by parts and Delta_z U+kU^p=(n-2)(1+r^2)^(-n/2), together with z.Df2=2f2, give
K2=(n-2) integral f2(1+r^2)^(-n/2)Phi2
=integral_[R5_+] (|DPhi2|^2-35(1+r^2)^(-2)Phi2^2).
Thus K2=(2/pi+9pi/32)||f2||_[S3]^2>0, exactly as computed in agent2_n5_n6_local_coefficients.md. Truncating at R changes K2 by O(|f2|^2/R); its normalized contribution is O(|f2|^2/delta), absorbed into half the leading |f2|^2/epsilon for fixed delta and sufficiently small epsilon.

## Error table

All constants below depend only on the fixed outer delta0 and uniform graph bounds, not on the evaluation radius delta. Put b=|D^2h(0)|. Expand the exact graph coefficients through the displayed jets; use epsilon r<=delta0 and the derivative estimates. The only critical or supercritical radial groups are listed here; all omitted terms have an extra epsilon r or extra decaying U factor and are bounded by the same groups.

1. Quadratic graph paired with gradient error: epsilon b*r^2*r^(-4)*epsilon^2*r^(-2)*r^3 dr =epsilon^3 b r^(-1)dr. Bound Cepsilon^3 b log(2+R).
2. Cubic or higher graph paired with error: the cubic term is epsilon^2*r^3*r^(-4)*epsilon^2*r^(-2)*r^3dr=epsilon^4dr, giving Cepsilon^3 delta. Higher jets have additional epsilon r factors.
3. Linear cubic H paired with Ue: epsilon^2*r* r^(-3)*epsilon^2*r^(-1)*r^3dr=epsilon^4dr, also Cepsilon^3delta. Its edge term has the same bound.
4. Quadratic graph paired with the square of its first correction, and cubic-in-II curvature terms: Cepsilon^3 b^3 integral_1^R r^(-1)dr. All higher pure-quadratic geometric terms are smaller by O(epsilon b r), hence bounded by Cdelta0 times the positive quadratic contribution, plus the same logarithmic group.
5. Terms involving two cubic-or-higher jets have total homogeneous degree at least6; their worst integral gives epsilon^4R=epsilon^3delta. A quadratic/cubic pairing of formal order epsilon^3 is odd and integrates to zero on the symmetric tangent disc; curved-measure errors move it into the previous groups.
6. H^2(x.nu) terms, gradient-error squares, and nonlinear-power remainders have the bounds Cepsilon^3delta (or Cdelta0 epsilon^2b^2). For the nonlinear term use v,w0<=CU and the mean value theorem; no smallness of e/U is needed.

These estimates can also be organized by homogeneous degree: graph/correction pairs of degrees j,l have radial integrand r^(j+l-6); the convergent pair2+2 is the positive model, pair2+3 is odd, and every pairj+l>=6 yields an epsilon^3delta^(j+l-5) bound. Nonlinear pure-quadratic cubic terms are the sole extra critical log group above.

Consequently, taking delta0 small enough to absorb its relative quadratic error,
P_delta(Mu)+sigma5(f4)
>= c1 b^2/epsilon-C b log(2+delta/epsilon)-C b^3 log(2+delta/epsilon)-Cdelta-o_i(1).
Because b is uniformly bounded, the cubic-log group is absorbed directly into b^2/epsilon using epsilon b log(2+delta/epsilon)->0. Young's inequality bounds the remaining b log term by (c1/2)b^2/epsilon+C epsilon log^2(2+delta/epsilon), whose last term tends0. This proves the stated renormalized lower bound.

## Mass matching and what remains

At a limiting umbilic point, write the Green expansion with cubic odd and quartic mean-zero angular corrections and finite coefficient B. The boundary ADM mass is m=B-(3/8)avg_[S3]f4. Since |S3|/|S4|=3/4,
P(G)+sigma5(f4)=-(9/4)|S4|m.
Thus positive mass produces the needed negative terminal invariant. This algebra and the mass gauge sign were independently checked by agent3. One must use this modified invariant, not identify raw P with m. The bridge must invoke its rescaling version; the correction is order d^3 under clustering scales and disappears in the flat multipole limit.

This document supplies the detailed local calculation for audit. It does not by itself prove the separate Green parametrix/ADM theorem or the global selection bridge.
