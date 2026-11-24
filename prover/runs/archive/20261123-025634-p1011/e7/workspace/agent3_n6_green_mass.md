# Dimension-six Green mass after quadratic and cubic boundary jets vanish

Assume the local blow-up analysis has forced II(p)=0 and DII(p)=0 in a locally flat representative with H(p)=0. More precisely, the needed jet statement is that in flat graph coordinates the boundary has no quadratic or cubic term. This is the GM lemma only, not the nonlinear proof of that vanishing.

Write t=f4(z)+f5(z)+O(|z|^6), z in R5, f_j homogeneous of degree j. The boundary Robin coefficient is beta=2/5 and the leading Green pole is r^-4. The degree-(k-6) boundary defect is

    -4(k-1)f_k+(2/5)Delta_z f_k.

## Angular corrections

For k=4, let q4=r^-1Y4, where

    (Delta_{S5}-3)Y4=0 on S5_+,
    partial_nu Y4=(4/5)f4-(2/5)Delta_{S4}f4.

This follows from Delta_z f4|S4=28f4+Delta_{S4}f4. The Neumann operator -Delta_S+3 is coercive and gives a unique smooth solution. Integrating its equation yields

    int_{S5_+}Y4=(4/15)I4, I4=int_{S4}f4.

For k=5, let q5=Y5, where

    Delta_{S5}Y5=0,
    partial_nu Y5=-(2/5)Delta_{S4}f5,
    int_{S5_+}Y5=0.

Indeed Delta_z f5=40f5+Delta_{S4}f5. The Neumann data have zero mean. They are odd under z->-z, so Y5 is odd as well.

Both angular problems have analytic coefficients and data. Analytic boundary regularity and Cauchy continuation extend q4,q5 harmonically into a fixed angular collar across t=0. The actual graph lies in that collar for small r, since |t|/r=O(r^3).

## Green parametrix

On the actual graph the residual B(r^-4+q4+q5) is bounded. The sixth-order graph remainder produces an O(1) error. Evaluating Dq4 at the shifted boundary gives f4 D^2q4=O(r^4)O(r^-3)=O(r); its normal tilt gives Df4 Dq4=O(r^3)O(r^-2)=O(r). Also Hq4=O(r^2)O(r^-1)=O(r). The q5 interactions are smaller. Thus a cutoff parametrix can be corrected by the global coercive Robin problem with smooth interior source and bounded boundary source. Robin regularity gives

    G=r^-4+q4+q5+B+O(r^alpha), 0<alpha<1,
    D(remainder)=O(r^(alpha-1)).

The normalized positive Green function is the one with leading pole coefficient 1.

## AF decay and ADM mass

The metric ghat=Gg (since 4/(n-2)=1 here) is complete scalar-flat and minimal-boundary off p. In inverted coordinates R=1/r, its leading relative metric and boundary-flattening terms have order R^-3. Hence the AF rate is tau=3>2. Quadratic terms have order R^-6, faster than the mass order R^-4, so their ADM contribution vanishes.

The q4 conformal bulk mass flux has a term

    +(2/(5|S5|)) R I4,

while the quartic boundary-flattening contribution is its negative. Their exact cancellation follows either from the angular mean above or from the general calculation in agent3_mass_renormalization.md. The q5 and quintic-flattening terms are odd and have zero angular integrals. The sole surviving mass term is therefore

    m=B.

The dimension-six boundary positive mass theorem gives m>=0, with equality only for Euclidean halfspace. Conformal compactification and Liouville rigidity then give the excluded round hemisphere. Thus m=B>0 on any manifold allowed in the problem. For nonorientable manifolds one may pass to the orientable double cover and use zero-mass rigidity to rule out multiple lifted ends.

## Adapted Pohozaev

The cross term of r^-4 and q4=r^-1Y4 is

    -6r^-1 int_{S5_+}Y4=-(8/(5r))I4.

The q5 cross term vanishes by oddness, and all quadratic correction terms vanish as r->0. The ordinary Green constant B contributes -4|S5|B. Therefore

    lim_{r->0}[P_spherical(G,r)+(8/(5r))I4]
          =-4|S5|m<0.

This is precisely the terminal mass invariant needed for a nonnegative renormalized Pohozaev inequality. It is NOT valid to take the limit of the raw spherical Pohozaev alone when I4 is nonzero.
