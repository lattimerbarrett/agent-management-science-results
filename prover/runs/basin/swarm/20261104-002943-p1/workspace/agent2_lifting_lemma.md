# A sufficient lifting lemma for an attracting projective periodic orbit

This is a conditional theorem; no suitable periodic orbit has yet been established for the problem.

Let a smooth finite-dimensional discrete map, expressed in local blown-up coordinates (epsilon,z), have the uniform expansions on a neighborhood of a compact set U:

 epsilon_new = epsilon - c(z) epsilon^2 + O(epsilon^3),
 z_new = z + epsilon V(z) + O(epsilon^2),

where epsilon>0, c(z)>=c0>0, and the remainder estimates are uniform with one derivative. Assume:

1. U is a compact smooth domain and V points strictly inward on its boundary.
2. There is a smooth circle-valued phase theta on U with dtheta(V)>=omega0>0.
3. There is a continuous observation g(z) (in the application a surviving normalized residual weight) and two disjoint phase arcs J0,J1 such that sup{g(z):theta(z) in J0}<inf{g(z):theta(z) in J1}.

Then for every sufficiently small epsilon_0>0 and every z_0 in a slightly smaller invariant domain, the discrete orbit remains in the coordinate neighborhood, epsilon_k->0, and g(z_k) does not converge.

Proof. Fix a defining function L for U, positive outside and zero at the boundary. Strict inwardness gives dL(V)<=-a<0 on a compact collar of the boundary. Taylor expansion yields L(z_new)<=L(z)-a epsilon+O(epsilon^2) on this collar, so for sufficiently small epsilon no step leaves U. Points outside the collar cannot leave U in one step because their displacement is O(epsilon). Thus U is forward invariant for the discrete map.

The radial bounds yield, uniformly for small epsilon,

 epsilon-(2C)epsilon^2 <= epsilon_new <= epsilon-(c0/2)epsilon^2,

where C bounds |c| plus the remainder. In particular epsilon stays positive and decreases to zero. Dividing by epsilon epsilon_new shows a<=1/epsilon_new-1/epsilon<=b for fixed 0<a<b, and therefore epsilon_k is comparable to 1/(k+1), so sum epsilon_k diverges.

Choose the small real lift of the phase increment. The phase condition and Taylor expansion give

 omega0 epsilon/2 <= theta_new-theta <= Ctheta epsilon.

Consequently the phase winds infinitely often while its increments tend to zero. It therefore visits both arcs J0,J1 infinitely often. Assumption 3 gives two separated subsequential ranges of g, proving nonconvergence.

If V possesses a hyperbolic attracting periodic orbit Gamma with nonconstant observation g|Gamma and c>0 on Gamma, the three hypotheses follow by choosing a sufficiently small compact tubular neighborhood of Gamma. A standard transverse Lyapunov quadratic form along Gamma supplies an inward-pointing tube; a phase coordinate satisfies dtheta(V)>0. Nonconstancy of g provides separated arcs after shrinking the tube.

Application to the restarted-CG weight map: use a fixed nonterminating cycle family as the base, active normal coordinates u=epsilon eta, and inactive residual amplitudes a_j=epsilon alpha_j with alpha_j>0 on U. The two-step WEIGHT map uses positive amplitudes sqrt(w_j), so the minus-one sign in the signed residual is immaterial. All expansions are analytic and uniform on a compact U with positive alpha_j. Taking epsilon proportional to H_infinity^2-H^2 gives the required decreasing radial variable when the leading Lyapunov coefficient c is positive. For sufficiently small epsilon all active weights remain positive, all chosen inactive amplitudes remain nonzero, and H stays bounded below; hence the original orbit never terminates. Nonconvergence of even weights implies nonconvergence of even normalized residual vectors, independently of residual signs.

What remains before use: establish a concrete attracting periodic orbit (or an explicit inward tube with a winding phase), verify c>0 and the uniform analytic coordinate chart, and provide rigorous numerical or exact bounds. An experimentally observed return-map near-fixed point is not sufficient.


## Higher-order version

The same proof applies to

 epsilon_new=epsilon-c(z)epsilon^q+O(epsilon^(q+1)),
 z_new=z+epsilon^p V(z)+O(epsilon^(p+1)),

for integers p>=1 and q>=p+1. Indeed epsilon_k is comparable to (k+1)^(-1/(q-1)), by applying the reciprocal argument to epsilon^(1-q), and therefore sum epsilon_k^p diverges. The inward-boundary and phase estimates use epsilon^p instead of epsilon. Thus an attracting winding tube in a higher-order Pell normal form would also yield a genuine nonconvergent orbit, provided all uniform expansions and positivity conditions are established. This is still conditional and does not assert that such a tube exists.
