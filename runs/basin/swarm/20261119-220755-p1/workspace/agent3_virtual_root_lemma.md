# Virtual extreme-Gauss-root log-ratio lemma (agent 3)

Let p_k be any nonterminating spectral orbit with s fixed. All retained active
weights are positive. Add a new spectral node zeta not in the spectrum and give
it initial weight epsilon>0, rescaling the original weights to sum 1-epsilon.
For each fixed k, the augmented orbit and its monic polynomials depend smoothly
on epsilon at zero. Let H_k be the original monic dual OP (degree n-s-1).
The augmented monic dual OP (degree n-s) tends to (x-zeta)H_k.
Assume zeta is strictly below every zero of every H_k on a tail. Then the
augmented smallest Gauss root is

    a_k(epsilon)=zeta+epsilon alpha_k+O(epsilon^2), alpha_k != 0.

All alpha_k have the same sign (root cannot cross the added spectral node).
If f_k is the original monic residual OP and N_k its squared norm, exact dual
interpolation gives

    alpha_(k+1)/alpha_k =
      f_k(zeta) f_(k+1)(zeta)/N_(k+1) * H_k(zeta)/H_(k+1)(zeta).       (1)

For the dual measure q_k, the two-step update is
q_(k+2) proportional to q_k (H_k/H_(k+1))^2. Take as Rayleigh trial polynomial
H_(k+1)/(x-a_(k+1)). With S_k(u)=sum q_k H_k(lambda)^2/(lambda-u), the bound is

    a_(k+2) <= a_(k+1)+ S_k(a_(k+1))/S'_k(a_(k+1)).

This is valid regardless of which side of zeta the roots occupy. The added
node's dual mass is C_k/epsilon+O(1), C_k>0. Let h=H_k(zeta), nonzero.
At zeta its OP value is -epsilon alpha_k h+O(epsilon^2). Therefore, writing
J_k for the finite contribution of all original nodes, S_k(a_k)=0 gives
J_k=C_k alpha_k h^2. At a_(k+1), the leading numerator is
C_k alpha_k h^2(1-alpha_k/alpha_(k+1)), while S' has leading term
C_k alpha_k^2 h^2/(epsilon alpha_(k+1)^2). Consequently

    alpha_(k+2) <= alpha_(k+1)^2/alpha_k.                            (2)

If alpha>0, beta_k=alpha_(k+1)/alpha_k is nonincreasing; if alpha<0,
beta_k is nondecreasing. If beta_k tends beta_infty>0, then

    sign(alpha_k) * (log beta_k-log beta_infty) >= 0.                (3)

No long-time uniformity of the epsilon expansion is needed: (2) is obtained
separately for each finite triple k,k+1,k+2.

## Application to the hard s=3 edge

Let P=prod_{i=1}^5(x-lambda_i), f g = L+P(x)(x-c), theta in (a,b),
and suppose c<a<b and all negative-neutral outsiders are >c. In the canonical
coordinates of agent1_s3_canonical_flight.md, A=delta N, B, K=C/sqrt(g/f), set

    I = -(c A+B)+sqrt(f(theta)g(theta))*K/(theta-c).

Take zeta<c, zeta increasing to c, avoiding all eigenvalues. After removal of
strict-left outsiders, the original dual roots all exceed zeta on a tail.
From dual interpolation, sign(alpha_k)=sign(P(c)) for zeta sufficiently close
c. Equation (1), TV, and the slow-dual-root expansions yield

    beta_infty = f(zeta)g(zeta)/L,
    lim_{zeta -> c-} delta log beta = P(c) I/L^2.

The possible active positive node at c is not an obstruction: its dual root
moves O(t p_c) per block, so at each fixed zeta<c its contribution divided by
t=L-N is O(p_c/(c-zeta)) -> 0. Thus (3) implies I>=0 at every deficit-normalized
omega state. Strict-left outsider removal / exponentially perturbed version
of (3) remains to be written carefully.

## Why I>=0 suffices, with no scattering or CS

For any negative-neutral outsider z, Q_z=z-c>0, the exact homogeneous field has

    growth_z = -4A/L+4I/(L Q_z)
               + theta_dot*(f(theta)g(theta)+L)
                  /[P(theta)(theta-c)(z-theta)].

Let Phi_z' = -(fg+L)/[P(theta)(theta-c)(z-theta)]. Then
(log p_z+Phi_z(theta))'=-4A/L+4I/(L Q_z). Deficit normalization A=-1 makes this
strictly positive, uniformly away from zero. For the exact map, once the
virtual-root inequality gives I>=-o(t), this becomes a positive increment
>=c t (uniform even at faces by expressing Phi as base-weight logarithms).
An active negative coordinate forces sum t=infinity, so the corrected log
weight tends +infinity. Since log p_z<=0, Phi_z(theta) must tend +infinity.
For z<a, Phi_z is proper increasing from -infinity at a to +infinity at b,
so theta->b. For z>b it is proper decreasing, forcing theta->a. Thus any
negative outsider forces edge convergence; a bracketing pair is impossible.

For uniform endpoint control, write

 Phi_z(theta)=sum_i ai log|theta-lambda_i|+ac log(theta-c),
 ai=2L/[P'(lambda_i)(lambda_i-c)(lambda_i-z)],
 ac=2L/[P(c)(c-z)].

The pole at theta=z cancels because f(z)g(z)+L=0. The corresponding base-weight
logarithms differ by uniformly bounded smooth corrections; their increments
are handled using TV and the O(t p_c) motion of a possible positive c node.
