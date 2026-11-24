# Dimension18 critical-degree9 response sign

This is a local homogeneous-response lemma, NOT an endpoint construction or a
compactness theorem. It diagnoses the critical jet direction outside the
finite-energy polynomial seed class.

Let n=18, boundary dimension17, h=r^9 P_q(omega), where P_q is a degree-q
spherical harmonic on S16 and q is one of1,3,5,7,9. The leading homogeneous
part of the bubble Robin source at infinity is
 S_h = c_q r^(-9)P_q+O(r^(-11)),
 c_q=-8(q+7)(q+8)/17 !=0.
Indeed Delta_R17 h=(9-q)(q+24)r^7 P_q; insert it into the exact source formula.

The corresponding harmonic far-field response has the form z=r^(-8)Y on the
halfspace. Since sigma(sigma+n-2)=-64 at sigma=-8,
 (-Delta_S17+64)Y=0 on the hemisphere S17_+,
 partial_nu Y=c_q P_q on its equator S16.
This strictly coercive Neumann problem has a unique smooth solution; integrating
by parts gives
 int_S17+ (|grad Y|^2+64Y^2)=int_S16 Y partial_nuY>0.
The strict inequality follows since c_q P_q is nonzero.

More explicitly the regular polar solution has hypergeometric parameters
 a=b=(q+8)/2, c=q+17/2. Its Dirichlet-to-Neumann eigenvalue is
 Dcrit_q=2 Gamma((q+9)/2)^2/Gamma((q+8)/2)^2>0.
Thus Y|S16=(c_q/Dcrit_q)P_q, and the displayed energy equals
 (c_q^2/Dcrit_q)||P_q||_L2(S16)^2>0.

For z=r^-8Y, the Dirichlet energy on an annular halfspace region is exactly
 log(R/R0)*int_S17+ (64Y^2+|grad Y|^2).
The bubble linearization's additional potential term has finite tail, since
 U^(4/(n-2))=O(r^-4), z^2=O(r^-16), and dV=r^17dr dOmega;
 its radial integrand is O(r^-3). It therefore does not change the positive
logarithmic coefficient. Cross terms with responses from degrees d<=8 have
radial power r^(d-10)<=r^-2, hence finite tails.

Consequently the critical homogeneous top-response block has positive
logarithmic coefficient; lower-degree cross terms remain bounded. Since all
same-parity subcritical dilation blocks are positive, its formal critical
Schur complement is eventually positive rather than a negative seed. Turning
this homogeneous statement into a full cutoff expansion requires matching
estimates; no unrestricted blow-up conclusion is asserted.

Independent normalization check: the Jacobi-series coefficient Cspec_q from
agent4_critical9_checks.py satisfies
 Cspec_q / (c_q^2/Dcrit_q) = 2^10*17^2,
independent of q. Exact symbolic checks verify this in all five relevant
angular sectors, so the spectral and direct far-field signs agree.
