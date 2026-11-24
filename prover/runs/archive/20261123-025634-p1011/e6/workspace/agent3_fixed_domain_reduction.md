# Fixed-domain assembly and normalized reduced-energy convergence (n>2d)

This note connects the graph estimates to the abstract projected inverse and nonlinear LS lemmas. It is **not** the missing n=18 mechanism or low-dimensional compactness theorem.

## Hypotheses and construction

Fix a polynomial P of degree at most d, n>2d, whose halfspace quadratic graph reduction F_P(epsilon,xi) has a strict interior local minimum at theta0=(1,0), with positive definite Hessian. The explicit degree8 polynomial certified in agent3_alln_seed_algebra.md supplies this hypothesis for every n>=19. For that polynomial one can make the completely explicit choice K=3/(n-16), so K(n-2d)=3; the exterior residual and energy ratios below are exactly a polynomial factor in rho_k^(-1) times mu_k^(1/2) and mu_k, respectively. No diagonal subsequence of scales is required.

Take a fixed smooth cutoff chi supported in the unit boundary ball, equal1 on the half-ball. Put p_k=2^(-k)e1, rho_k=2^(-k-4), mu_k=exp(-rho_k^(-2)), lambda_k=mu_k^K with fixed K(n-2d)>2. Define

    h_k(x')=mu_k lambda_k^d P((x'-p_k)/lambda_k) chi((x'-p_k)/rho_k),
    h=sum_k h_k,  Omega={t>h(x')}.

One may start the sum at arbitrarily large k, so the global C2 norm of h is as small as desired. The supports are disjoint. The derivative bounds in agent1_geometric_lemmas.md prove h smooth, compactly supported, and flat at0. Let

    eta_k=mu_k lambda_k^(d-1), R_k=rho_k/lambda_k.

Then eta_k->0, R_k->infinity, and the slope size on the kth graph is O(mu_k rho_k^(d-1))->0.

The Cayley transform maps Omega to a bounded smooth domain arbitrarily C2-close to the ball; it is the ball near the compactification point. Its Euclidean metric is strictly mean convex and of positive Yamabe type. A nonzero tracefree Hessian of P2 f at a core point yields a nonumbilic boundary point, excluding the hemisphere. All this is independent of the PDE construction.

For functions on Omega use the conformally invariant energy

    J(v)=1/2 int_Omega |Dv|^2+c int_boundary H v^2
                  -(n-2)^2/2 int_Omega (v_+)^(2n/(n-2)).

The small global C2 norm gives equivalence between its quadratic Hilbert norm and the homogeneous Dirichlet norm: the compactly supported H term is bounded by ||H||_(n-1) times the squared critical trace norm, and the trace inequality on a uniformly Lipschitz graph controls this by C||Dv||_2^2. Alternatively use the smooth Cayley compactification and positive Yamabe coercivity.

## Physical bubbles and exterior estimates

For theta=(epsilon,xi) in a fixed small compact parameter ball about theta0 put

    W_k,theta(x',t)=[lambda_k epsilon /
       ((lambda_k epsilon)^2+|x'-p_k-lambda_k xi|^2+t^2)]^((n-2)/2).

These are smooth finite-energy functions on Omega, solve the interior equation exactly, and compactify smoothly. Their residual is entirely the boundary functional.

Compare Omega with Omega_k={t>h_k(x')}. They agree in a ball of radius rho_k/2 about p_k. Away from that ball, distances to the bubble center are at least c rho_k. Direct differentiation gives, uniformly in theta,

    |D^j W_k,theta(x)| <= C_j lambda_k^((n-2)/2)
                                  |x-(p_k,0)|^(2-n-j), j=0,1,2,

whenever |x-(p_k,0)|>=rho_k/4. The graphs h and h_k have uniformly bounded first and second derivatives, lie in a fixed compact boundary region, and their areas there are uniformly bounded. Integrating these estimates, using the exact graph formulas for H dS, gives for some fixed exponent N and a constant independent of k,theta

    |J_Omega(W)-J_Omega_k(W)| <= C rho_k^(-N) lambda_k^(n-2),

and, after the natural graph pullbacks, for the residuals

    ||J'_Omega(W)-J'_Omega_k(W)||_(H*)
              <= C rho_k^(-N) lambda_k^((n-2)/2).

For precision, compare boundary test functions by the vertical pullback Phi_k(x,t)=(x,t+h(x)-h_k(x)), mapping Omega_k onto Omega. Its Jacobian is1 and its derivative and inverse derivative are uniformly bounded. The equivalent Dirichlet/Hilbert norms therefore compare uniformly. Since W solves the interior equation exactly, its variational residual is purely boundary and no volume-term mismatch occurs under this pullback.

Here are explicit sufficient bounds: on the differing compact boundary region the derivative residual is bounded by C rho_k^(-n)lambda_k^((n-2)/2), hence its L^(2(n-1)/n) norm has the same upper bound up to a fixed constant. For the volume-strip action use |DW|^2<=C lambda_k^(n-2)rho_k^(2-2n), W^(2n/(n-2))<=C lambda_k^n rho_k^(-2n), and uniformly bounded strip volume. The boundary action is bounded by C lambda_k^(n-2)rho_k^(4-2n). Thus one may choose any sufficiently large fixed N, for example N=4n+4. Graph pullback has uniformly bounded trace operator norm.

After division by eta_k or eta_k^2 respectively, both errors vanish, because

    rho_k^(-N)lambda_k^((n-2)/2)/eta_k
       =rho_k^(-N)mu_k^(K(n-2d)/2-1)->0,
    rho_k^(-N)lambda_k^(n-2)/eta_k^2
       =rho_k^(-N)mu_k^(K(n-2d)-2)->0.

## Local normalized limits

Rescale about p_k by lambda_k. The kth graph is eta_k P(y')chi(y'/R_k). The exact graph lemma (agent4_flat_graph_estimates.md), uniformly for theta in its compact parameter ball, proves

    J_Omega_k(W_k,theta)=J_halfspace(U)+o(eta_k^2),
    residual/eta_k -> S_P,theta

in the critical dual trace norm. Uniformity follows by applying the same estimates to the continuously varying translated/dilated polynomial profile; their finite coefficients and bubble parameters range in compact sets. The explicit source envelope is C(1+|y'|)^(d-n), which lies in L^(2(n-1)/n) exactly because n>2d. The preceding exterior bounds give the same limits on the single fixed domain Omega.

The source annihilates the halfspace Jacobi fields. Indeed the raw first shape derivative is identically zero for every bubble parameter and every compactly supported graph. Differentiate that identity in the parameter; approximate P by cutoffs and pass to the limit in the dual trace norm. Thus there is a unique Jacobi-orthogonal finite-energy z_theta with

    Q_theta(z_theta,v)=-S_P,theta(v),
    Q_theta(v,w)=int grad v.grad w-n(n+2)int U_theta^(4/(n-2))vw.

The inverse exists by the hemisphere kernel/spectral argument. The map theta->z_theta is continuous in the Dirichlet norm, by conjugating scale/translation to a fixed parameter and using the explicit uniform inverse bound.

## Strong normalized correction convergence

Apply the uniform global projected inverse lemma and nonlinear LS lemma to W_k,theta. Removing an ordinary fixed-radius cutoff changes W and its scale-normalized Jacobi fields by O(lambda_k^((n-2)/2)) in the Hilbert norm. Replacing boundary-flattened bubbles by physical bubbles adds a further o(1) Hilbert-norm error (no O(lambda_k^((n-2)/2)) rate is asserted for this geometric error): on fixed rescaled balls the smooth boundary tends to its tangent plane, and tails are uniformly small. Consequently the same inverse bound holds for the uncut physical bubbles by small operator perturbation. The correction v_k,theta satisfies ||v_k,theta||<=C eta_k, uniformly in theta.

The first linear correction divided by eta_k converges strongly, in bubble-rescaled Dirichlet norm, to z_theta. A precise density argument is as follows. Approximate z_theta in Dirichlet norm by functions in C_c^infinity(overline{R_+^n}), meaning smooth up to the boundary with compact support in the CLOSED halfspace and with unrestricted boundary trace (not interior-supported zero-trace test functions), uniformly in theta using a finite cover of the compact continuous image {z_theta}. Transfer it to Omega by the local graph flattening, rescale back, and project off the approximate Jacobi space. For a fixed compact support, the rescaled graph coefficients converge smoothly to Euclidean coefficients; the transferred operator and source therefore converge in operator norm on this fixed test function. The error due to the compact approximation is uniformly small by the boundedness of the linearized operators, source convergence, and the uniform inverse bound. First let k->infinity, then improve the approximation. This proves strong convergence, including the assertion that no Hilbert norm escapes outside the bubble chart.

For the nonlinear correction the difference from the linear correction is O(eta_k^p), p=(n+2)/(n-2)>1, by the contraction remainder estimate. After division by eta_k it vanishes. The same strong normalized limit follows.

## Corrected energy and exact solutions

Taylor expansion in the function, not in the domain, has remainder bounded by C||v_k||^(p+1)=o(eta_k^2) for n>=6. Combining the direct-action limit, residual convergence and strong correction limit gives uniformly in theta

    J(W_k,theta+v_k,theta)
      =J_halfspace(U)+eta_k^2 [S_P,theta(z_theta)
                                 +Q_theta(z_theta,z_theta)/2]+o(eta_k^2)
      =J_halfspace(U)-eta_k^2 Q_theta(z_theta,z_theta)/2+o(eta_k^2).

The bracket is exactly the quadratic graph reduction F_P(theta). Choose a closed parameter ball about its strictly stable minimum with F_P strictly larger on its boundary. The uniform C0 expansion forces a minimizer of the actual reduced energy into the interior. The abstract LS lemma then gives an exact weak solution of the truncated equation; positive Yamabe coercivity applied to its negative part gives nonnegativity, and the strong maximum principle and Robin Hopf lemma give strict positivity. Standard critical Robin bootstrap yields smoothness.

The trace-cap argument in agent1_nonlinear_LS_lemma.md gives boundary maximum at least c lambda_k^(-(n-2)/2): the bubble has fixed positive critical trace norm on a cap of radius O(lambda_k), while the correction trace norm is O(eta_k)->0. The smooth Cayley conformal factor is uniformly bounded above and below near p_k->0, so this boundary blow-up persists on the one fixed smooth compact mean-convex Euclidean domain. For the missing compactification point, D1,2(Omega) with the conformal quadratic form is isometric to H1 on the compactified domain: that one boundary point has zero relative H1 capacity for n>=3. Testing with cutoff approximations extends the weak equation across it; all error terms vanish by critical Sobolev/trace integrability. Negative-part positivity and Robin Brezis-Kato/bootstrap then give smoothness at that point as well. No pointwise asymptotic for the correction at infinity is assumed.

With the certified d8 stable polynomial, this argument supplies the existence route in every n>=19. It emphatically does not furnish n18, nor the requested sharp lower compactness theorem. The exterior-comparison pullbacks and uniform source-to-operator convergence should be independently audited before treating this note as a finished analytic proof.
