# All cycle product-level roots are real

At any two-cycle with m active distinct spectral nodes, s+1<=m<=2s, put D=prod_(i=1)^m(x-lambda_i), P=p_w, Q=p_Fw, C=H^2, and let f be the monic reduced dual polynomial of degree m-s-1. Barycentric orthogonality gives w_i P_i=C f_i/D'_i, and P_i Q_i=C on the active nodes. Therefore
 G_w(z):=sum_i w_i/(z-lambda_i)=f(z)Q(z)/D(z),
 S_P(z):=sum_i w_i P_i/(z-lambda_i)=C f(z)/D(z).
Both equalities follow by matching residues; the right sides are proper rational functions. Consequently the monic degree-(s-1) second-kind polynomial
 B_P(z):=sum_i w_i [P(z)-P(lambda_i)]/(z-lambda_i)
 satisfies
 B_P=P G_w-S_P=f(PQ-C)/D=f U,
 where U=(P Q-C)/D is monic of degree 2s-m. The partner measure yields exactly the same second-kind polynomial B_Q=f U.

For completeness, B_P has s-1 distinct real roots strictly interlacing the s roots rho_j of P. Define the cardinal polynomial ell_j(x)=P(x)/(P'(rho_j)(x-rho_j)), degree s-1. The polynomial ell_j^2-ell_j vanishes at all roots of P, so it equals P times a polynomial of degree <=s-2. Orthogonality gives sum_i w_i ell_j(lambda_i)=sum_i w_i ell_j(lambda_i)^2>0. Evaluating the divided-difference definition at rho_j therefore gives
 B_P(rho_j)=P'(rho_j) sum_i w_i ell_j(lambda_i)^2.
Its sign is exactly that of P'(rho_j), which alternates between successive simple roots of the monic P. The intermediate-value theorem supplies one root between each pair, and degree s-1 makes these all the roots, simple. The identical argument applies to Q.

It follows that f U is real-rooted and simple. In particular U is real-rooted and simple and shares no root with f. Thus the degree-2s polynomial P Q-C=D U has all 2s roots real, counted with multiplicity. Some roots of U may coincide with active nodes, so D U need not have only simple roots.

A common root rho of P,Q is a double root of R=P Q. It must be a local minimum of R at height zero. Indeed R and R-C are both real-rooted of degree 2s, with C>0. Rolle's theorem forces all 2s-1 roots of R' to be real and places one between consecutive roots of R-C; every local maximum of R must lie at least C, while a common-root local maximum would have height 0<C. Equivalently, inspecting the monotonicity intervals separated by R' shows a maximum below C would remove two possible roots of R-C. Therefore common-root degeneracies are one-sided folds under variation of C, not opposite-sign maxima/minima folds.

The real-rootedness and common-second-kind identities are exact structural results; they do not themselves prove convergence or provide the s=4 counterexample.
