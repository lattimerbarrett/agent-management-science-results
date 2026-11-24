# C1 parameter upgrade of the flat-graph estimates

**Scope.** This upgrades the already proved local graph lemma to C1 in bubble
parameters and records the conditional C1 corrected-energy consequence. It
is not unrestricted blow-up extraction, a dimension18 seed, or compactness.

Let theta=(epsilon,xi) range in a compact set with 0<epsilon0<=epsilon<=epsilon1
and |xi|<=L. Put a0=(n-2)/2 and
 U_theta(x,t)=[epsilon/(epsilon^2+|x-xi|^2+t^2)]^a0.
For the graph h_R=aP(x)chi(x/R), assume n>2d and
 b_R=C a(1+2R)^(d-1)->0, as in agent4_flat_graph_estimates.md.
The function h_R and its domain are independent of theta.

Then, uniformly in theta,
 || J_(Omega_hR)(U_theta)-J_halfspace(U_theta) ||_C1(theta)=O(b_R a^2),
 || T_hR,theta/a-S_P,theta ||_C1(theta;L^(2(n-1)/n)) ->0.
Here T is the exact boundary residual density and S is its linear graph part.
The source convergence includes the cutoff-tail limit as R->infinity.

## Explicit parameter bounds

Write X=x-xi, D=epsilon^2+|X|^2+t^2. Then
 partial_xi_j U/U=(n-2)X_j/D,
 partial_epsilon U/U=a0/epsilon-2a0 epsilon/D.
Since |X_j|/D<=1/(2epsilon), and |1-2epsilon^2/D|<=1,
 |partial_theta U|<=C U uniformly. Direct differentiation gives the same
uniform spatial decay envelope for each fixed spatial derivative and its
first two parameter derivatives. In particular all expressions needed below
can be differentiated under the integral signs using a common integrable
majorant.

The exact volume density and square are
 e_theta=(n-2)^2/2*epsilon^(n-2)
           *(|X|^2+t^2-epsilon^2)/D^n,
 V_theta=epsilon^(n-2)/D^(n-2).
The pointwise identity c Delta_x V_theta(x,0)=e_theta(x,0) still holds.
The functions remain even in t. Their differences from t=0 and their first
parameter derivatives obey
 |partial_theta^j[e_theta(x,t)-e_theta(x,0)]|<=C t^2(1+r)^(-2n),
 |partial_theta^j[V_theta(x,t)-V_theta(x,0)]|<=C t^2(1+r)^(-2n+2), j=0,1.
Here r=|x|; compactness of parameters makes1+|X| uniformly comparable to1+r.
Repeating the exact strip-action proof gives the stated C1 energy bound.

The exact residual density is
 T_h,theta=(n-2)epsilon^a0[h-X.Dh]D_h^(-n/2)
        +2c epsilon^a0 K_h D_h^(-(n-2)/2),
 D_h=epsilon^2+|X|^2+h^2,
 K_h=Delta h-(Dh)^TD^2hDh/(1+|Dh|^2).
Differentiate this expression before estimating. Each first parameter
derivative of the nonlinear-in-h remainder obeys precisely the same envelope
 C b_R^2 a(1+r)^(d-n) as the undifferentiated remainder. The derivative of
h-X.Dh adds only Dh, a better-decaying term. The linear source and its first
parameter derivatives have envelope C a(1+r)^(d-n). This envelope belongs to
L^(2(n-1)/n) iff n>2d. Dominated convergence proves the C1 source assertion.

## Conditional corrected-energy consequence

Assume the already proved global assembly bounds, with the same estimates
also for one theta derivative (true for exterior terms by the explicit
|partial_theta D^jU| decay), and the uniform projected inverse. Let r(theta)
be the Riesz residual. The preceding estimates give ||r||+||D_theta r||=O(a).
The Jacobi frames have bounded C1 norms. Moreover the theta derivative of the
linearized potential is uniformly controlled even when1<p<2, because
 W^(p-2)|D_theta W|<=C W^(p-1).
Differentiating the projected contraction/implicit equation therefore yields
 ||v||+||D_theta v||=O(a).

For precision on the nonlinear parameter term, split pointwise into
 |v|<=W/2 and |v|>W/2. Taylor's formula in the first region, and elementary
power bounds in the second, show the partial derivative in W of the
nonlinear equation remainder, multiplied by |D_theta W|<=CW, is bounded by
 C|v|^p for1<p<=2, and by C(W^(p-2)|v|^2+|v|^p) for p>=2.
Critical Holder and Sobolev estimates bound it by O(a^min(2,p)). Thus the
differentiated equation's forcing is O(a); the derivative of the full
solution map remains uniformly invertible by small perturbation.

The compact-support approximation argument used for strong normalized
correction convergence can be differentiated once: the source converges in
C1 in global dual norm; operator and parameter-derivative convergence hold
on each compactly supported transplanted test function, NOT in global
operator norm on the expanding domain. Global operator bounds and density
control the remaining tails. The limiting response and its theta derivative
form a compact continuous image in the Dirichlet space. It follows that v/a->z_theta
in C1(theta;Dirichlet norm).

Finally the function-Taylor energy remainder is C1-small relative to a^2.
For1<p<=2 its value is bounded by C||v||^(p+1), and its derivative by
 C(||v||^p||D_theta v||+||v||^(p+1)). For p>=2 use instead the additional
C||W||^(p-2)||v||^3 terms and their analogues; bounded critical norm of W
makes these O(a^3+a^(p+1)). These estimates follow from the same two-region
split and critical Holder exponents. Hence
 J_red(theta)=J_halfspace(U)+a^2 F_P(theta)+o_C1(a^2).
This requires all the explicit source/operator hypotheses above; it is not an
assertion that an arbitrary exact blowing-up sequence admits such a profile.

A detailed abstract proof of this corrected C1 implication, independently
audited, is given in `agent2_C1_LS_reduction.md`.

Density convention: smooth compactly supported halfspace approximants mean
`C_c^infinity(overline{R_+^n})`, smooth up to the boundary with unrestricted
trace; no Dirichlet-zero boundary condition is imposed.
