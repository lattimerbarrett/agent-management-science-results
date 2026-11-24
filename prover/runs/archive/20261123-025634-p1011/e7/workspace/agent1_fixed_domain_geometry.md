# A fixed flat-domain geometry for the n>=32 gluing scheme

This supplies only the geometric hypotheses and scale selection, not the energy expansion or gluing theorem.

Let z in R^(n-1), t in R. Define F(s)=0 for s<=1 and F(s)=integral_1^s exp(-1/(q-1))dq for s>1. Set
Omega_0={F(|z|^2)+(t-1)^2<1}.
F is smooth, nondecreasing and convex; F'>0 for s>1, F''=F'/(s-1)^2>0, and F(s) tends to infinity. The defining function D has Hessian diag(2F'I+4F'' z tensor z,2)>=0. Its gradient never vanishes on D=0: if t!=1 this follows from D_t, and if t=1 then F=1 so z!=0 and F'>0. Thus Omega_0 is a smooth bounded convex connected domain, and its boundary mean curvature H is nonnegative. It has flat lower and upper boundary discs t=0,2, |z|<1.

The Robin form Q_0(v)=integral |grad v|^2+2c_n integral_boundary H v^2 has strictly positive principal eigenvalue. Indeed, if its infimum at L2 norm1 were zero, Rellich compactness and the trace theorem give a limit with zero gradient, hence a nonzero constant, contradicting H>0 somewhere. Moreover Q_0 controls the H1 norm by combining Q_0>=||grad v||_2^2 and Q_0>=lambda_1||v||_2^2.

There is an explicit nonumbilic point on the side t=1, |z|=r, F(r^2)=1: its t-direction principal curvature is 2/|grad D|, while each angular z-direction principal curvature is 2F'(r^2)/|grad D|. They differ since F'<1. Leave this side unchanged below. Since vanishing of tracefree II is conformally invariant, the resulting domain can never be conformally equivalent to the round hemisphere.

Choose p_j=2^(-j-2)e_1, rho_j=2^(-j-5), epsilon_j=exp(-L-j^2), and a fixed smooth radial cutoff chi equal1 on [0,1/2], supported in [0,1]. The balls B_(rho_j)(p_j) are pairwise disjoint and accumulate only at0. Write P2(z)=z_1^2-z_2^2 and P4(z)=|z|^2 P2(z). On the lower flat boundary define
h_j(z)=chi(|z-p_j|/rho_j)[-epsilon_j^3 P2(z-p_j)+epsilon_j P4(z-p_j)],
h=sum_j h_j, extended by0 at0 and outside these balls.

For each k, ||D^k h_j||_infty <=C_k(epsilon_j rho_j^(4-k)+epsilon_j^3 rho_j^(2-k)). Every derivative therefore tends to0 faster than every power of |p_j| as j tends to infinity. Hence h is C-infinity and all its jets at0 vanish. Increasing L makes ||h||_C2 arbitrarily small. Replace the lower boundary by t=h(z), leaving the rest unchanged. A collar map (z,t)->(z,t+eta(t)h(z)) gives a C2-small diffeomorphism from Omega_0 onto Omega_h. Under this pullback the Robin quadratic forms differ by at most C||h||_C2||v||_H1^2, by continuity of g, volume measure, normal and H and the trace theorem. Consequently Q_h remains coercive. The new metric is exactly Euclidean and therefore locally conformally flat up to its smooth boundary; Omega_h is compact after taking closure and connected, and the preserved side point remains nonumbilic.

Set mu_j=epsilon_j^4 (equivalently tau=1 in mu=epsilon^(3+tau)). In scaled coordinates y=(z-p_j)/epsilon_j the boundary height divided by epsilon_j equals
mu_j chi(|y|/R_j)[-P2(y)+P4(y)], R_j=rho_j/epsilon_j -> infinity.
For every n>=32, R_j^(-(n-2)/2)=o(mu_j) and R_j^(2-n)=o(mu_j^2), since respectively (n-2)/2>4 and n-2>8 and exp(-j^2) beats every power of rho_j. These are the required baseline cut-off residual and energy scale comparisons.

This lemma gives one fixed smooth domain per n, rather than a varying sequence of domains. It does NOT by itself assert existence of any concentrating solutions.
