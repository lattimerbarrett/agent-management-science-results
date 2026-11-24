# A dimension-three Green parametrix (not a compactness proof)

Assume a positive-Yamabe compact 3-manifold is flat in coordinates near a boundary point 0, and H(0)=0. Such a representative can be obtained within an LCF conformal class: first flatten the metric, then apply a local Mobius conformal factor with prescribed normal logarithmic derivative, and extend the positive factor globally.

Write the domain as t >= F(z), where F=f_2+O(|z|^3), and f_2 is a tracefree homogeneous quadratic polynomial in z=(x,y). Put r=(|z|^2+t^2)^(1/2) and

    q(z,t)=f_2(z)/(2(r+t)^2).

Direct identities, checked by SymPy in agent3_checked_identities.py, are

    Delta q=0,    q_t(z,0)=-f_2(z)/|z|^3,    (z,t).Dq=0.

Moreover q has zero integral over each hemisphere centered at 0, by tracefreeness of f_2.

For the outward normal nu=(DF,-1)/(1+|DF|^2)^(1/2),

    partial_nu(r^-1)=-f_2(z)/|z|^3+O(1),
    partial_nu q=+f_2(z)/|z|^3+O(1).

Here H=O(|z|), hence H(r^-1+q)/4=O(1). Consequently

    B(r^-1+q)=O(1)

on the punctured boundary. A cutoff of r^-1+q has smooth interior error away from 0, and bounded boundary error. Coercivity of the positive-Yamabe Robin form solves away these errors. Robin W^{1,p} regularity for bounded boundary data, for every finite p, makes the correction C^{0,alpha} for every alpha<1. Thus the normalized boundary Green function has expansion

    G=r^-1+q+A+O(r^alpha),    0<alpha<1.

Rescaled annular estimates give a corresponding gradient remainder O(r^(alpha-1)). Positivity follows by testing the negative part against the coercive Robin form.

The harmonic Pohozaev integrand on a hemisphere is

    (1/2)G partial_r G -(r/2)|DG|^2+r(partial_r G)^2.

Because q is degree zero, its radial derivative vanishes. Its cross term with r^-1 is -q/(2r^2), whose integral is zero. The quadratic q terms and remainder terms vanish after integration as r->0. Therefore

    lim P(G,r)=-(A/2)|S^2_+|.

This is only a Green expansion and exact terminal sign computation. To obtain compactness one still needs boundary blow-up selection, exclusion of clustering, isolated-simple estimates, and a justified nonnegative limiting Pohozaev inequality. None of these follows from this parametrix.
