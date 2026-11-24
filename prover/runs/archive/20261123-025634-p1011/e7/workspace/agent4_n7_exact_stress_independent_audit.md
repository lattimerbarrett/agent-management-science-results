# Independent audit of exact SP7 stress assembly

This audits `agent3_n7_exact_stress_assembly_diagnostic.md`; it is not an existence construction or final classification. The exact identities below were independently derived, and the executable `agent4_n7_exact_stress_checks.py` checks the linear radial integrals and the polynomial identity behind the bilinear coefficients.

## 1. Independent linear formula with its sign fixed

Set beta=5/12, U=(1+r²)^(-5/2), n=7. For a homogeneous graph jet f_k on R6 put I_k=int_S5 f_k. The coefficient of its amplitude in the SPHERICAL flux P (minus outward graph flux), on the tangent disk of radius R, is exactly

    P1_k(R) = (25/24) I_k R^(k+4) [k-(k-2)R²]/(1+R²)^6.

This follows by direct radial integration of the integrated Robin identity, independently of the nonintegrated graph-flux derivation:

    -P1_k/I_k = (k-1)[(5/24)k(k+4) int_0^R s^(k+3)/(1+s²)^5 ds
                        +(25/2) int_0^R s^(k+5)(1-s²)/(1+s²)^7 ds]
                      -(5/24)k(k+4)R^(k+4)/(1+R²)^5.

The checker evaluates both integrals exactly and verifies the closed formula for every k=2,...,6. In particular P1_4 ~ -25 I4/(12R²), P1_6 -> -25 I6/6. After amplitude epsilon^(k-1) and mass normalization epsilon^-5 these are precisely the negatives of the adapted counterterms. I2=0 and I3=I5=0.

## 2. Independent bilinear identity, including finite-radius edge sizes

Use positive datum g_j=5(j-1)f_j(1+r²)^(-7/2)-beta Delta f_j U = partial_nu Phi_j. Write eta_j for graph/correction amplitudes. The coefficient of eta_j eta_l in the integrated graph flux, before summing ordered indices, is

    (j-1) int_D_R [-f_j DU.DPhi_l+35 f_j U^(9/5)Phi_l+beta Delta f_j U Phi_l]
      -beta int_boundaryD_R R Delta f_j U Phi_l.

All D here are z-derivatives of plane traces. Its bracket equals

    -int_D_R Phi_l g_j -int_boundaryD_R f_j Phi_l partial_r U,

because div_z(f_j DzU)+35f_jU^(9/5)+beta Delta f_j U=-g_j. The actual polynomial Euler/coordinate identity is checked for tracefreequadratic, harmoniccubic and r²linearcubic test branches in the executable. More generally it follows from z.Df_j=jf_j and Delta_z U+35U^(9/5)=5(1+r²)^(-7/2).

Passing from graph flux to P changes sign. Replacing the plane integral by the full Jacobi form therefore gives

    P2 = sum_(j,l) (j-1) eta_j eta_l L(Phi_j,Phi_l)
            + O(sum_(j,l) |eta_j eta_l| |f_j| |f_l| R^(j+l-7)).

Indeed all explicit disk-edge terms, the omitted hemisphere Jacobi edge, and the Jacobi tail have that same exponent. For j,l=2,3, the diagonal errors are C eta2² b² R^-3 and C eta3² a² R^-1. The mixed terms are tangentially odd exactly. With eta2=epsilon, eta3=epsilon² and R=r/epsilon, the normalized diagonal errors relative to the positive terms are O((epsilon/r)^3) and O(epsilon/r), respectively. Thus they absorb for each fixed r; no preexisting limit b->0 or a->0 is needed.

This independently establishes the signs and factors +epsilon² L22 and +2epsilon4 L33. Strictpositive constants follow either from the Jacobi spectrum or agent2's explicit branch calculations.

## 3. Finite-Taylor audit against the nonintegrated identity

I checked the exact identity in agent3's document: z.D_z w is indeed the AMBIENT z-derivative evaluated at t=F, not the derivative of its restricted trace. Normal components of D w, evaluation shifts, and slope factors first add exactly the weights claimed. The flat-graph flux is identically zero for every field, so no unknown-E term without a graph factor exists.

For the fine remainder E of weight3, the only unknown terms of weight<=5 are E f2, E f3, and E f2² / E f2 Phi2. Their normalized sizes are C b/epsilon, C a log R, C b² log R. Quadratic E terms start at weight7. These match the full direct identity, not merely the integrated formula with potential edge omissions. Young absorbs the first two; b=O(epsilon) kills the third. The weighted C6 Taylor remainder gives O(r), with one fixed outer chart constant.

The coarse first remainder has weight2. Besides its worst terms Cb/epsilon² and C/epsilon, its weight5 logarithmic terms (including E1² f2) are bounded by C/epsilon and hence do not affect the coarse b=O(epsilon) deduction. This verifies a point abbreviated in the main assembly.

## Conclusion and remaining dependency

I find no missing low-weight stress term, sign error, edge term or radius-dependent constant in the exact SP7 assembly. Conditional on the already separately stated isolated-simple decay and weighted estimates, it gives

    P_adapted,r(Mu) >= c b²/epsilon³ + c a²/epsilon - o_i(1)-C_delta0(r+r²).

For fixed r the left side is bounded under the Green-limit hypothesis, so b,a->0. Then the terminal adapted sign is nonnegative. Together with GM7 and the bridge, this has a compactness consequence; it is logically incompatible with n7 existence if all these inputs are accepted. This audit does not assert a source theorem or invent the requested counterexample. The task's prescribed n7 construction remains unresolved and its premise now requires clarification or a concrete defect in one of the displayed inputs.
