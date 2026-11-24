# DIAGNOSTIC: exact non-integrated stress and the seven-dimensional Taylor assembly

This is an independent derivation of the proposed local SP7 inequality. It uses the weighted estimates in agent3_n7_weighted_analytic_diagnostic.md. It is presented for adversarial audit, not asserted as a global compactness/disproof theorem.

## Exact identity, with no hidden edge or mean-curvature derivatives

Let the flat domain be t>F(z), z in R^{n-1}, and let w solve Delta w+n(n-2)w^p=0 and partial_nu w+beta H w=0, with beta=(n-2)/[2(n-1)]. Put a=(n-2)/2, kappa=(n-2)^2/2 and

    S=z.DF-F,
    T=Delta F-F_a F_b F_ab/(1+|DF|^2).

Since nu dSigma=(DF,-1)dz and H dSigma=T dz, the outward critical graph flux is EXACTLY

    I(F,w)=-beta T w [z.D_z w+F w_t+a w]
               -(S/2)|Dw|^2+kappa S w^q,             (1)

all ambient functions evaluated at (z,F(z)). Hence P_sphere(w)=-int_{|z|^2+F(z)^2<R^2}I(F,w)dz. Formula (1) has no integration-by-parts edge term to omit. Tangential integration recovers the usual H/edge formula, but is unnecessary for the remainder classification.

## Linear terms and exact counterterms

For radial U=(1+r^2)^(-a), I(F,U) changes sign under F->-F: T,S are odd, and all other factors, including F U_t, are even. The integration cap also depends evenly on F. Thus the entire direct-U flux has no terms of even shape amplitude, including mixed quadratic terms.

For a homogeneous graph jet f_j, the coefficient linear in its amplitude is, per I_j=int_{S^{n-2}}f_j,

    c_n[-(j-1)R^(j+n-2)(U^2)'(R)
             -j(n-2)R^(j+n-3)U(R)^2] I_j.           (2)

To derive (2), write G=U^2, use c_n Delta_z G=|D_zU|^2/2-kappa U^q, integrate the radial Laplacian twice, and use Delta_z f_j's angular mean j(j+n-3)I_j. All lower-end terms vanish for j>=2. Its leading asymptotic is

    [(n-2)^2(j-2)/(4(n-1))] R^(j+1-n)I_j.

For F=epsilon f2+epsilon^2 f3+... and mass normalization epsilon^{-(n-2)}, this becomes exactly the original-coordinate counterterm C_j r^(j+1-n)I_j. At n7 it gives 25I4/(12r^2), 25I5/(8r), 25I6/6, with I2=0 by tracefreeness and I3=I5=0 by oddness. The next asymptotic term has an extra epsilon^2 for every fixed evaluation r and vanishes.

## The only nonvanishing bilinear coefficients

Let Phi_j solve the physical Jacobi problem with boundary datum

    partial_nu Phi_j=(n-2)(j-1)f_j(1+|z|^2)^(-n/2)
                         -beta Delta_z f_j U.

Take the coefficient linear in F=f_j and linear in the field correction Phi_j in (1). Integrating its H term by parts and using z.Df_j=jf_j gives, for the spherical flux,

    (j-1) L(Phi_j,Phi_j)+edge_R,
    L(Phi,Phi)=int(|DPhi|^2-n(n+2)U^{4/(n-2)}Phi^2).

Here the intermediate bracket is

    int [f_j(DU.DPhi_j-n(n-2)U^p Phi_j)
                        -beta Delta f_j U Phi_j]
       =int Phi_j partial_nu Phi_j + edge_R/(j-1).

This follows directly from Delta_z U+n(n-2)U^p=(n-2)(1+r^2)^(-n/2). The edge satisfies |edge_R|<=C|f_j|^2R^(2j-n). For n7 and j=2,3 these are lower-order tails R^-3 and R^-1, absorbed into a fixed fraction of their positive full-space coefficients as R->infinity.

Both coefficients are positive definite. Phi2 lies in azimuthal degree2 and excludes the negative and zero sphere modes. Phi3 is odd under z->-z, so excludes the negative constant mode; on this subspace L>=0. Equality would make Phi3 a translation Jacobi field with zero Neumann datum. The displayed datum can vanish identically only if f3=0: comparing its linear and cubic homogeneous parts gives Delta f3=0, then f3=0. Since the cubic jet space is finite dimensional, L(Phi3,Phi3)>=c|f3|^2. Kernel gauge additions do not change L. Thus the retained leading terms are

    +c2 epsilon^2 |f2|^2,
    +2epsilon^4 L(Phi3,Phi3).

Their mixed term is tangentially odd and integrates to zero to leading order; cap corrections have higher weights below.

## Uniform finite Taylor grading

Assign each graph jet f_j, or its physical field Phi_j, weight j-1. On a dyadic annulus |z|~rho>=1, the relative field sizes and all fixed-order derivatives are bounded by the corresponding powers of epsilon*rho. A graph derivative of order l has degree (j-1)+1-l. T has degree weight-1, S degree weight+1. Therefore every gradient/H-sector monomial of total weight d is bounded, after the polar measure, by

    C epsilon^d rho^(d-6) d rho                  (n7),

while the potential sector has two further powers of decay. This assertion follows directly from (1), not from the integrated H formula. Near rho<=1 all fields are smooth and its integral is O(epsilon^d).

The denominator 1+|DF|^2 is smooth for small slopes. Normal evaluations at t=F admit a finite weighted C6 Taylor expansion (use a finite C7 extension of the fields if needed). The cap radius is determined by rho^2+F(rho theta)^2=R^2; the implicit function theorem gives the same finite weighted Taylor expansion, with cap changes beginning at weight2 and preserving parity. Every remainder of weight>=6 has normalized integral <=C epsilon int_1^R 1 d rho<=Cr, plus O(epsilon) from the core. No analyticity is required; uniform weighted C6 derivative bounds suffice. This supplies genuine Taylor-tail domination rather than a formal series.

For weights d<=5, the nonlinear partitions into graph/field degrees >=2 are exactly:

    d2: (2,2);
    d3: (2,3) odd, (2,2,2);
    d4: (2,4), (3,3), (2,2,3) odd, (2,2,2,2);
    d5: (2,5) odd, (3,4) odd,
        (2,2,4), (2,3,3), (2,2,2,3) odd, (2,2,2,2,2).

Terms with one jet are exactly (2). Parity is (-1)^(sum of the displayed degrees), since z-gradients occur in contracted pairs or are paired with z and t-derivatives do not change it. Thus the odd entries vanish on the reference tangent disk; their cap changes have the additional weights just accounted for.

Let b=|f2| and A3=|f3|, with all other jets bounded. Once b=O(epsilon), the unsigned normalized bounds for all non-retained entries are

    d3: b^3/epsilon^2=O(epsilon);
    d4: b/epsilon (Young against b^2/epsilon^3 leaves O(epsilon)),
        b^4/epsilon=O(epsilon^3);
    d5: C(b^2+b A3^2+b^5) log(2+R)=o(1).

The positive (2,2) and (3,3) entries were evaluated exactly above. No other analytic class of weight<=5 occurs in (1).

## Unknown second remainder

The proved estimate e2=w-U-epsilon Phi2-epsilon^2Phi3 obeys

    |e2|<=C epsilon^3(1+r)^-2,
    |De2|<=C epsilon^3(1+r)^-3.

Thus e2 has relative weight3. Subtract (1) at the model W and at W+e2. The derivative/H sectors are quadratic in fields and gradients, so their dependence on e2 is exactly linear plus quadratic. For the potential sector q=14/5>2 and 0<=w,W<=CU, Taylor with the mean-value remainder gives |w^q-W^q-qW^(q-1)e2|<=C U^(q-2)e2^2, without assuming analyticity of e2 or pointwise smallness of e2/U.

Since (1) contains at least one graph jet, the only unknown-remainder classes of weight<=5 are

    f2 e2 (weight4): bound C b/epsilon;
    f3 e2 (weight5): bound C A3 log(2+R);
    f2^2 e2 or f2 Phi2 e2 (weight5): bound C b^2 log(2+R)=o(1).

All e2^2 classes have weight>=7, hence normalized bound O(r^2). Young's inequality absorbs the first two terms into the positive leading terms:

    C b/epsilon <=eta b^2/epsilon^3+C_eta epsilon,
    C A3 log(2+R)<=eta A3^2/epsilon+C_eta epsilon log^2(2+R).

The remainders tend to zero for fixed r.

## Proposed local consequence and remaining logical caution

Combining the exact identity, the explicit counterterms, the positive bilinear terms, the finite Taylor bound and the weighted remainder gives the proposed inequality

    P_adapted,r(Mu)>=c b^2/epsilon^3+c A3^2/epsilon
                           -o_i(1)-C_delta0(r+r^2),

for every fixed sufficiently small r, with one fixed outer delta0. The coarse b=O(epsilon) used above follows from the same first-approximation expansion with unknown first remainder of weight2: its worst terms are C b/epsilon^2+C/epsilon; pure b^3/epsilon^2 absorbs into the positive quadratic term. Thus bounded fixed-r flux gives b^2<=Cepsilon b+Cepsilon^2 and b=O(epsilon).

This document closes the ordinary finite-Taylor classification at the level displayed. If its hypotheses and estimates are accepted together with the independently written weighted lemma, GM7, and selection bridge, a compactness consequence follows. Because that conflicts with the supplied target n7 existence, it must be adversarially audited; no seven-dimensional construction or trustworthy recent source has been supplied to resolve this conflict. No final classification is asserted here.
