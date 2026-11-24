# Critical boundary-jet renormalization of Pohozaev and halfspace mass

This bookkeeping lemma is relevant to n=5 (and any odd dimension). It does not prove any nonlinear compactness estimate.

Use a locally flat representative with H(p)=0 and suppose lower boundary jets that could produce mass-order nonlinear terms vanish. Write the mass-order boundary jet as f_{n-1}(z), homogeneous of degree n-1 in z in R^{n-1}. Put I=int_{S^{n-2}} f_{n-1}. Lower odd jets may be present; in n=5 a cubic jet is odd and its quadratic products decay faster than the mass order.

## 1. The vertical boundary-flattening contribution

The edge sign is PLUS under the problem's outward-normal convention. Indeed at the flat boundary, for g=delta+h and nu=-e_n, linearization gives H=partial_a h_an-(1/2)partial_n h_aa and V_n=partial_a h_an-partial_n h_aa. Hence the divergence theorem yields int R+2 int_boundary H = int_hemisphere V.mu+int_edge h_an theta_a to first order. This fixes the sign independently of any remembered mass convention.

After inversion, this boundary term becomes

    F(Z)=f_{n-1}(Z)/|Z|^{2n-4},

homogeneous of degree 3-n. Choose any smooth homogeneous extension F_ext(X) of this function into the halfspace, smooth in angular variables (do NOT extend it independently of the normal coordinate near the vertical axis, as that would not be an AF chart). Flatten the boundary by X_n=Y_n+F_ext(Y). To linear order the metric change is

    h_ij=partial_i zeta_j+partial_j zeta_i, zeta=F_ext e_n.

Its ADM vector V_i=partial_j h_ij-partial_i h_jj equals Delta zeta_i-partial_i div zeta, hence div V=0. On the flat boundary V_n=Delta_Z F. The divergence theorem therefore gives

    int_{S_R^+} V.mu = int_{|Z|<R} Delta_Z F
                     = int_{|Z|=R} partial_R F
                     =(3-n) I.

A cutoff of the extension near the origin justifies each integral and does not affect the limiting identity. The halfspace ADM boundary term is ALSO int h_{an} theta_a=(3-n)I. With normalization 1/[2(n-1)|S^{n-1}|], the total flattening mass is

    m_flatten=(3-n)I/[(n-1)|S^{n-1}|].

If G=r^{2-n}+q+B+... and q has zero mean at its mass-order homogeneous degree zero, the conformal metric contributes mass B. Thus

    m=B+(3-n)I/[(n-1)|S^{n-1}|].

In n=5, |S3|=2pi^2, |S4|=8pi^2/3, giving

    m=B-(3/8) average_{S3} f4.

In n=3, the shift coefficient vanishes. In n=4 and n=6, the relevant jets are odd (degrees 3 and 5), hence I=0.

## 2. Exactly the same term appears in the smooth-bubble graph flux

Let U=(1+r^2)^(-(n-2)/2), beta=(n-2)/[2(n-1)], kappa=(n-2)^2/2. On a graph deformation with homogeneous jet f_k, the tangentially integrated Robin-substituted stress has first-linear radial integral, per int_{S^{n-2}} f_k,

    (k-1)/2 int_0^R [ beta k(k+n-3) r^(k+n-4)U^2
                       -r^(k+n-2)(U')^2+2kappa r^(k+n-2)U^q] dr
     -beta k(k+n-3) R^(k+n-3)U(R)^2/2,

where q=2n/(n-2). The last term is the codimension-two edge term; omitting it gives the wrong constant.

At k=n-1 the integrand simplifies to

    (n-2)^3/2 * r^(2n-5)(1+3r^2)/(1+r^2)^n.

Its integral to infinity is evaluated by two beta integrals:

    int r^(2n-5)/(1+r^2)^n dr =1/[2(n-1)(n-2)],
    int r^(2n-3)/(1+r^2)^n dr =1/[2(n-1)].

Subtracting the edge limit (n-2)^2/2 gives the finite coefficient

    Cjet=(n-2)^2(n-3)/[4(n-1)].

Thus Cjet=9/8 in dimension 5, 1/3 in dimension 4, and zero in dimension 3. The n4 coefficient multiplies an odd jet and integrates to zero.

## 3. The correct sign quantity

The plain harmonic Pohozaev of r^{2-n}+B is

    P_plain=-(n-2)^2 |S^{n-1}| B/4.

Combining the two computations,

    P_plain + Cjet I
       =-(n-2)^2 |S^{n-1}| m/4.

Accordingly, an n5 local blow-up sign should be formulated for the RENORMALIZED Pohozaev P_plain+(9/8)int_{S3}f4, or equivalently directly for minus the AF mass. It is not generally safe to identify the plain Green constant B with the boundary ADM mass in n5 without a gauge or this correction. This warning does not affect the n3 proof, where Cjet=0.


## 4. Divergent lower-jet counterterms, including n6 quartic geometry

The same computation controls jets of degree k<n-1, not just the mass-order jet. Let sigma=k+1-n and write its harmonic Green correction as q_k=r^sigma Y. Its angular equation and outward Neumann source are

    Delta_S Y+sigma(sigma+n-2)Y=0,
    partial_nu Y=(n-2)[(k-1)f_k-Delta_z f_k/(2(n-1))].

Put I_k=int_{S^{n-2}} f_k. Since int Delta_z f_k=k(k+n-3)I_k, the source mean is

    gmean=-(n-2)(k-2)sigma I_k/[2(n-1)].

Integrating the angular equation gives, when sigma!=0,

    Q_k=int_{S_+^{n-1}}Y=(n-2)(k-2)I_k/[2(n-1)(k-1)].

The cross term of q_k with the fundamental singularity in the spherical harmonic Pohozaev is

    P_cross=-(n-2)(k-1) Q_k r^sigma/2
           =-(n-2)^2(k-2) I_k r^(k+1-n)/[4(n-1)].

The boundary-flattening height has degree 2-k, so its ADM flux at radius R=1/r is

    m_boundary,k=(2-k) I_k r^(k+1-n)/[(n-1)|S^{n-1}|].

The conformal bulk flux of q_k is

    m_bulk,k=2(k-1)Q_k r^(k+1-n)/[(n-2)|S^{n-1}|],

and these two divergent terms cancel EXACTLY. Moreover P_cross is minus (n-2)^2|S^{n-1}|/4 times m_bulk,k. Thus the correct adapted spherical Pohozaev is

    P_adapted(r)=P_plain(r)
          +sum_k [(n-2)^2(k-2)/(4(n-1))]
                   r^(k+1-n) int_{S^{n-2}} f_k.

The mass-order k=n-1 term has the finite meaning proved above, choosing the free constant angular correction to have zero mean. Once the AF decay tau>(n-2)/2, quadratic terms in metric/coordinate perturbations have vanishing ADM contribution. The displayed linear bookkeeping is then sufficient to identify

    lim_{r->0} P_adapted(r)=-(n-2)^2|S^{n-1}| m/4.

For n=6 after quadratic and cubic boundary jets vanish, the first possible jet is f4 and

    P_adapted(r)=P_plain(r)+(8/(5r)) int_{S4}f4+o(1).

The quintic jet is odd and has zero integral. This removes the raw r^-1 Pohozaev divergence noticed in the n6 quartic example. For n=5 the sole nonzero finite counterterm is +(9/8)int_{S3}f4. In n=4 the cubic mass-order term is odd. In n=3 the critical quadratic coefficient is zero.

These formulas are algebraic matching statements. Obtaining a nonlinear blow-up lower bound for P_adapted still requires the quantitative remainder estimates; no such estimate is asserted by this bookkeeping lemma alone.
