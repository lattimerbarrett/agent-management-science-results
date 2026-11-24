# Parabolic lifting of a hyperbolic logtime periodic orbit

**Conditional theorem (independent of whether such an orbit has been certified).**
Let an exact analytic map in coordinates `(h,u,z)` have weighted expansion

    h+ = h + B(h)u + O(epsilon^2),
    u+ = u + Q(h,u) + F(h)z + O(epsilon^3),
    z_i+ = z_i [1 + L_i(h)u + O(epsilon^2)],

uniformly on compact sets under `u=epsilon*w, z=epsilon^2*Z`; Q is quadratic.
Here a term O(epsilon^j) and its state derivatives have that uniform bound.
Put

    V(h,w,Z) = (B(h)w,
                 w+Q(h,w)+F(h)Z,
                 Z_i*(2+L_i(h)w)).

If V has a nonconstant hyperbolic periodic orbit Gamma, contained in the
interior of the coordinate domain and with every Z_i>0, then an exact forward
orbit of the map exists, with

    dist((h_k,(k+K)u_k,(k+K)^2 z_k), Gamma) -> 0.

More precisely the scaled orbit shadows one complete forward traversal after
another, with asymptotic phase `tau_k + phi + o(1)`, where
`tau_k=sum_{j=0}^{k-1}1/(j+K)=log(k+K)+constant+o(1)`.
Thus if h is nonconstant on Gamma, h_k does not converge.

## Proof

Set epsilon_k=1/(k+K), so epsilon_{k+1}=epsilon_k/(1+epsilon_k).
Exact rescaling gives a nonautonomous map

    Y_{k+1}=Y_k+epsilon_k V(Y_k)+epsilon_k^2 R(Y_k,epsilon_k),

where R and its first state derivatives are uniformly bounded in a fixed
compact tubular neighborhood of Gamma. This is an identity, not a formal
truncation: analyticity of the original map and its weighted Taylor remainder
give bounded R, extending continuously (indeed smoothly) to epsilon=0.

Let gamma(s) parametrize Gamma by V-flow time, with period T. Hyperbolicity
means its variational equation has precisely one unit multiplier, the simple
tangent multiplier, and all normal multipliers avoid the unit circle.
Choose a periodic adjoint covector ell(s) with ell(s)gamma'(s)=1; the normal
bundle is ker ell(s). In smooth tubular coordinates `(s,e)`, where e is in
that normal bundle, the ODE has

    s' = 1+O(|e|^2),
    e' = A(s)e+O(|e|^2).

The absence of a linear normal term in s' follows from the adjoint equation.
Use a periodic frame of the normal bundle (or pass to period 2T if necessary).
Its normal fundamental solution U(t,s) admits stable and unstable projections
P^s,P^u and constants C,alpha>0 with

    ||U(t,s)P^s(s)|| <= C exp(-alpha*(t-s))  (t>=s),
    ||U(t,s)P^u(s)|| <= C exp(-alpha*(s-t))  (t<=s).

Fix phi and write s_k=tau_k+phi+eta_k. Using the exact flow propagator over
[tau_k,tau_{k+1}] in the linear normal term, the scaled map is exactly

    eta_{k+1}-eta_k = a_k(eta_k,e_k),
    e_{k+1} = U(tau_{k+1}+phi,tau_k+phi)e_k + f_k(eta_k,e_k),

where, on a fixed small tube,

    |a_k| <= C[epsilon_k*|e_k|^2+epsilon_k^2],
    |f_k| <= C[epsilon_k*(|e_k|^2+|eta_k|*|e_k|)+epsilon_k^2].

The first-derivative versions of these bounds also hold, with a term
C*epsilon_k^2 in the Lipschitz constants. Uniformity follows from periodicity.
The dependence of A on eta is included in f_k. Local Euler-vs-flow error is
O(epsilon_k^2) and is also included in f_k.

Choose 0<beta<min(alpha,1), reducing alpha if needed. On the Banach space
with norm

    ||(eta,e)||_beta = sup_{k>=0} (k+K)^beta*(|eta_k|+|e_k|),

define the graph transform by

    eta_k = -sum_{j=k}^infinity a_j,
    e_k = sum_{j=0}^{k-1} U(tau_k+phi,tau_{j+1}+phi) P^s_{j+1} f_j
          -sum_{j=k}^infinity U(tau_k+phi,tau_{j+1}+phi) P^u_{j+1} f_j.

Thus the stable initial component is set to zero; any sufficiently small
stable initial component could instead be specified. These series converge.
The elementary estimate `tau_k-tau_j = log((k+K)/(j+K))+O(1/K)` converts the
exponential dichotomy estimates to power estimates. Weighted convolution of
an O((j+K)^(-1-2beta)) source is O((k+K)^(-beta))*O(K^(-beta)); weighted
convolution of an O((j+K)^(-2)) source is
O((k+K)^(-beta))*O(K^(beta-1)). The same estimates hold for the future phase
sum. In particular, on a fixed radius-r ball the transform has norm at most

    C[r^2*K^(-beta)+K^(beta-1)]

and Lipschitz constant at most `C[r*K^(-beta)+K^(-1)]` (enlarging C harmlessly).
Take K sufficiently large. The transform maps the ball into itself and is a
strict contraction. Its fixed point gives an exact scaled-map orbit satisfying
eta_k,e_k=O((k+K)^(-beta)). In particular e_k->0 and eta_k->0.

Finally tau_k is increasing, tends to infinity, and has increments tending to
zero. Modulo T it therefore approaches every phase along subsequences. Every
point of Gamma is a cluster point of Y_k. Any coordinate nonconstant on Gamma
fails to converge. Positivity and membership in the original coordinate chart
hold for large K because Gamma is compact in its interior. This proves the
theorem.

## Application to restarted residual map

Take base conditional weights p_i on m=s+t+1 nodes. With monic base residual
polynomial f_u and monic dual H_h,

    p_i = C H_h(lambda_i)/(d_i f_u(lambda_i)),
    C^(-1)=sum_i H_h(lambda_i)/(d_i f_u(lambda_i)).

This is an analytic coordinate chart whenever these weights are positive.
Orthogonality follows from Lagrange interpolation, since deg(H*x^j)<=m-2
for 0<=j<s; its monic squared norm equals C. Append small outside weights z_i
and renormalize the base weights by (1-sum z_i). This gives analytic spectral
weights of an actual residual vector. The exact two-block map has the weighted
expansion used above (to be verified/certified from its finite rational formulas).
If h is nonconstant on the periodic orbit, base weights are nonconstant: for
fixed limiting f, p_i are proportional to H_h(lambda_i)/f(lambda_i). Thus even
normalized residual directions fail to converge, irrespective of signs.
All weights stay positive, so there is no finite termination.
