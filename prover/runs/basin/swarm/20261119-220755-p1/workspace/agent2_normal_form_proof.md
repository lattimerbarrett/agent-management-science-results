# Derivation of the weighted two-block normal form (arbitrary s,t)
Let base nodes lambda_i (m=s+t+1) satisfy f_i g_i=N>0, monic f,g degree s. Set d_i=P_m'(lambda_i), monic dual H degree t, and p_i=N H_i/(d_i f_i)>0. The partner weights are pp_i=H_i f_i/d_i. Both sums are one by Lagrange interpolation, and f,g are their monic OP_s, each of squared norm N. This follows because degree(H*x^j)<=m-2 for j<s and degree(H*f)=m-1 with leading coefficient one.
Use the analytic base-weight chart
 p_i=C(H,u) H_i/[d_i(f+u)_i], C^{-1}=sum H_i/[d_i(f+u)_i],
and append outside weights z_mu, scaling base weights by 1-sum z. Orthogonality and the squared norm identity still hold exactly for the conditional base distribution, with f+u its monic OP and norm C. The full-distribution monic OP differs from f+u by O(|z|), analytically, because its moment Gram matrix is nonsingular.

Put u=epsilon*w and z_mu=epsilon^2 Z_mu, where outside nodes obey f_mu*g_mu=-N. Fix H in a compact region of the positive chart. With v(x)=(1,x,...,x^(s-1)), V_i=v(lambda_i)^T, define
 M=sum p_i V_i V_i^T, Mp=sum pp_i V_i V_i^T,
 dg=-Mp^{-1} M w,
 A=delta N=N^2 sum H_i w_i/(d_i f_i^2),
 R_i=(g_i w_i+f_i dg_i-A)/N.
The one-block partner conditional weights are exactly H_i(f+u)_i/d_i, so differentiating their monic OP equations gives dg=-Mp^{-1}M w. Differentiating C gives A. Differentiating the partner squared norm also gives A, since sum H_i w_i g_i^2/d_i equals the displayed A.
Consequently if K is the product of the consecutive full-distribution monic OPs and N0,N1 their norms, then
 K_i=N+epsilon*(g_i w_i+f_i dg_i)+O(epsilon^2),
 N0=N+epsilon*A+O(epsilon^2), N1=N+epsilon*A+O(epsilon^2).
The two-block base-weight ratio is therefore 1+2epsilon R_i+O(epsilon^2). The base OP changes only by O(epsilon^2), as follows also from the identity below. Since C(H,0)=N identically in H, recovering the dual chart gives
 H^+=H+2epsilon*dh+O(epsilon^2), dh(lambda_i)=H_i R_i.
The right side is a polynomial of degree<t, by the differentiated exact dual relation; for t=1 it is a constant.

## Exact polynomial increment identity
For any exact weighted residual orbit let f0,f1,f2 be three consecutive monic OPs, K=f0*f1, norms N0,N1, and p2=p*K^2/(N0*N1). Orthogonality implies
 sum p f0 v=0, sum p f0 K v=0.
Thus
 M(p2)*(f2-f0)=-1/(N0*N1) sum p f0 (K-N0)^2 v.          (EXACT)
Its Taylor expansion on base nodes is
 -epsilon^2 M^{-1} sum p_i f_i R_i^2 V_i+O(epsilon^3).
At each negative-level outside node, K-N0=-2N+O(epsilon), giving the contribution
 -4epsilon^2 M^{-1} sum Z_mu f_mu v(mu)+O(epsilon^3).
Full-vs-conditional OP corrections are O(z); their change over two blocks is O(epsilon^3) because z^+-z=O(epsilon^3), H^+-H=O(epsilon), u^+-u=O(epsilon^2), so the same leading increment applies to u. Hence
 u^+=u+epsilon^2*W(H,w,Z)+O(epsilon^3),
 W=-M^{-1}[sum p_i f_i R_i^2 V_i+4 sum Z_mu f_mu v(mu)].
The outside weights satisfy
 z_mu^+=z_mu*[1+epsilon*ell_mu+O(epsilon^2)],
 ell_mu=2(w_mu/f_mu+dg_mu/g_mu)-2A/N.

All statements have uniformly bounded state derivatives on compact positive charts: the exact finite weighted-map formulas and chart inverses are analytic and all Gram matrices stay nonsingular. Now set epsilon_k=1/(k+K), epsilon_{k+1}=epsilon_k/(1+epsilon_k). Rescaling u=epsilon*w,z=epsilon^2 Z gives exactly
 Y^+=Y+epsilon*V(Y)+epsilon^2*bounded analytic remainder,
 V=(2dh, w+W, Z_mu*(2+ell_mu)).
This is the vector field implemented by agent2_blowup_ode.py, and (for s4,t1) by the algebraically simplified interval field. The derivation establishes the expansion independently of numerical difference tests; those tests only audit the implementation.

## Rational simplifications used by the interval implementation (s4,t1)
Let H=x-theta. The moment matrices M(theta),Mp(theta) are affine in theta. Their determinants satisfy
 det M(theta)=c*f(theta), det Mp(theta)=cp*g(theta).
This is an exact algebraic identity, not merely interval residual inclusion: if zeta is any root of f, the coefficient vector of f(x)/(x-zeta), degree s-1, lies in ker M(zeta), since the jth component of its image equals N sum_i lambda_i^j/d_i=0 for j<s. The determinant has degree <=s and f has s distinct roots; comparing leading coefficients gives the identity. The same argument uses g for Mp. In the example c,cp are nonzero (the finite interval coefficient bounds verify this), and the resulting inverses are adjugate polynomial matrices divided by c*f(theta),cp*g(theta).

The scalar dual increment is Hdot=2dh, and R_i=Hdot/[2(lambda_i-theta)]. Thus
 sum_i p_i f_i R_i^2 v_i
 =N Hdot^2/4 sum_i v_i/[d_i(lambda_i-theta)]
 =-N Hdot^2 v(theta)/[4P_m(theta)],
where the last equality is the exact barycentric partial-fraction identity, valid componentwise because deg(x^j)<m-1. Hence the homogeneous w increment is
 +N/[4P_m(theta)] M(theta)^{-1}v(theta)*thetadot^2.
The first-coordinate formula can use node lambda=0:
 thetadot=2theta/N*[g(0)w(0)+f(0)dg(0)-A].
These identities give exactly the b,K,force,L rational coefficient formulas in agent4_interval_blowup.py, with K=-N M^{-1}v(theta)/(4P_m(theta)) and wdot=w-K*thetadot^2+force*Z.
