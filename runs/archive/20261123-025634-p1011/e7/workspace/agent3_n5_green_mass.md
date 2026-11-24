# Dimension-five Green mass at an umbilic point

This is the GM input for the compactness bridge, conditional on the local Pohozaev estimate forcing II(p)=0. The boundary is not assumed umbilic elsewhere. We invoke the standard dimension-five asymptotically-flat halfspace positive mass theorem and its rigidity, not a compactness theorem.

## Flat normalization and angular parametrices

Within the conformal class choose a representative flat near p. Since tracefree II vanishes at p, a local Mobius conformal factor makes the full II vanish at p by cancelling its trace. Normalize the factor's value to 1. Write the boundary t=f3(z)+f4(z)+O(|z|^5), z in R4, with f_j homogeneous of degree j. Its outward mean curvature is H=Delta_z(f3+f4)+O(|z|^3).

For the leading pole r^-3, the degree-(k-5) Robin defect from f_k is

    B(r^-3) = r^(k-5)[-3(k-1)f_k(omega)+(3/8)Delta_z f_k(omega)]+higher.

For k=3, construct q3=r^-1Y3, where Y3 on S4_+ solves

    (Delta_S-2)Y3=0,
    partial_nu Y3=3[2f3-(1/8)Delta_z f3].

The operator -Delta_S+2 with Neumann data is coercive, so the smooth solution is unique. The data are odd under z->-z, hence so is Y3; in particular its hemisphere mean is zero.

For k=4, construct q4=Y4, where

    Delta_S Y4=0,
    partial_nu Y4=3[3f4-(1/8)Delta_z f4],
    int_{S4_+}Y4=0.

This Neumann problem is compatible because int_{S3}Delta_z f4=24 int_{S3}f4. Thus the boundary data have mean 3(3-24/8)int f4=0. Both q3,q4 are exactly harmonic in the Euclidean halfspace away from the pole. Their angular equations, equator, and polynomial data are analytic, so analytic boundary regularity and local Cauchy continuation extend them harmonically across the equator into a fixed angular collar. This collar contains the actual graph t=f3+f4+O(r^5) for small r, since |t|/r=O(r^2). Thus the following parametrix has no hidden interior source in a thin negative-t strip.

## Remainder and Green expansion

On the actual curved boundary, the residual B(r^-3+q3+q4) is bounded. The original pole's remaining fifth-order graph error has degree zero. Evaluating Dq3 at a displaced boundary changes it by f3 D^2q3=O(r^3)O(r^-3)=O(1); the normal tilt contributes Df3 Dq3=O(r^2)O(r^-2)=O(1), and Hq3=O(r)O(r^-1)=O(1). Terms from q4 are smaller. The graph's nonlinear mean-curvature terms start beyond the required orders.

Cut off this parametrix and solve away its smooth interior and bounded boundary errors using the positive-Yamabe coercive Robin form. Boundary W^{1,p} estimates for every finite p give a C^{0,alpha} correction for alpha<1; annular elliptic estimates give the derivative remainder. Therefore the positive normalized boundary Green function is

    G=r^-3+q3+q4+B+O(r^alpha),
    D(remainder)=O(r^(alpha-1)).

Here q3 is odd and q4 has zero hemisphere mean. The normalization is the coefficient 1 of r^-3.

## AF end and mass

The metric ghat=G^(4/3)g is complete off p, scalar-flat and minimal-boundary. Under inversion R=1/r, its leading relative metric terms from q3 and the boundary's cubic graph have decay R^-2. Thus it is an AF halfspace end of rate tau=2>3/2. Quadratic products of the relative metric/flattening terms decay R^-4, faster than the mass order R^-3, and contribute zero mass.

The q3 and cubic-boundary linear ADM terms vanish by oddness. The q4 term has zero hemisphere mean. The constant B contributes mass B with the standard halfspace normalization. The quartic boundary graph's flattening term contributes

    -[1/(2|S4|)] int_{S3} f4=-(3/8)average_{S3}f4.

The sign and coefficient follow from the explicit general divergence calculation in agent3_mass_renormalization.md: for a vertical flattening vector field, both bulk and boundary-edge ADM fluxes equal its radial derivative flux. Therefore

    m=B-(3/8)average_{S3}f4.

By the boundary positive mass theorem m>=0; equality implies Euclidean halfspace, hence the original compact manifold is conformally the round hemisphere. Under the problem's exclusion,

    m>0.

The adapted local Pohozaev is exactly

    P_adapted=P_spherical+(9/8)int_{S3}f4,
    lim_{r->0}P_adapted(G,r)=-(9/4)|S4|m<0.

Thus the positive-mass terminal obstruction matches the renormalized n5 isolated-simple inequality in agent2_n5_renormalized_SP.md. It would not match a raw Green-constant argument omitting the quartic jet.
