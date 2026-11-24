# Hidden quadratic phase at a common-factor cycle

Let P,Q be the degree-s monic orthogonal polynomials at a positive two-cycle, with P_i Q_i=C>0 on its active nodes. Let B=gcd(P,Q), choose ell of degree<deg B, and put r=ell/B (evaluated at the active nodes, none of which is a root of B). Set eta_i=-w_i r_i and consider the straight perturbation w+epsilon eta. Orthogonality gives sum eta_i=0, delta P=P r and delta Q=-Q r, both polynomials of degree<s, and delta C=0. Thus eta is a hidden first-order fixed direction: DG eta=eta.

Write z_i=w_i P_i^2/C, M=sum w_i V_iV_i^T, and let
 t=sum w_i P_i r_i^2 V_i, a2=M^{-1}t,
 E_w=sum w_i r_i^2, E_z=sum z_i r_i^2.
Here a2 also denotes the degree<s polynomial with that coefficient vector. The exact second coefficient of G(w+epsilon eta) is
 B2_i=-2w_i r_i^2+(2w_i Q_i/C)a2(lambda_i)+2w_i E_z.

Derivation: the first-step polynomial is P+epsilon P r+epsilon^2 a2+O(epsilon^3), because M a2=-sum eta_i(P_i r_i)V_i=t. Its norm squared is C-epsilon^2 C E_z+O(epsilon^3). The first transformed weight has coefficients z, z r, and
 z2=-z r^2+2wP a2/C+z E_z.
For the partner polynomial, its first variation is -Q r and its second variation vanishes. Indeed its second orthogonality right side is
 sum z r(-Q r)V +sum z2 Q V
 =-t+(-t+2M a2)=0,
 using z_iQ_i=w_iP_i. Its norm's second coefficient is also -C E_z; expanding the second weight update then yields B2 above.

Normalization and P-orthogonality of B2 follow directly:
 sum B2_i=0, sum B2_i P_i V_i=0.
In the latter identity the two nonconstant terms cancel because P_iQ_i=C and M a2=t. Hence the moving normal quadratic coefficient is zero, including at singular common-factor cycles. This explains the identically vanishing hidden normal field found in all gcd3 calculations.

More strongly, B2 is a negative gradient on the fixed-P cycle fiber. Equip weight tangent vectors with the positive diagonal metric
 <u,v>_m=sum_i [P_i^2/(Cw_i)] u_i v_i.
Let T={u:sum u_i=0, sum u_i P_i V_i=0}. For the fixed linear functional L(w)=sum_i w_i P_i^2 r_i^2/C, its ambient metric gradient is w r^2. The correction B2+2w r^2 lies in the metric-normal span: it is a combination of w and w Q V, and
 w=w Q^2/C+w Q(P-Q)/C
shows w also lies in that normal span (deg(P-Q)<s). Therefore B2=-2 Proj_T^m(w r^2), and
 dL[B2]=-1/2 ||B2||_m^2<=0.
Equivalently the exact checkable identity is
 2 sum_i w_i P_i^2 r_i^2 (B2_i/w_i)+sum_i w_i P_i^2(B2_i/w_i)^2=0.

This is a structural leading-order result. It does not prove full-orbit convergence: higher-order hidden drift and boundary transitions remain unclassified.
