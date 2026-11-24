# Global reduction for every restart length

Work on the distinct eigenvalues initially present in the residual. Their spectral residual directions are fixed, so write the normalized residual using signed scalar coefficients y_i and weights w_i=y_i^2. All eigenvalues below are distinct, and initially all w_i>0. Let q_w be the monic degree-s orthogonal polynomial for w and h(w)=sum_i w_i q_w(lambda_i)^2. Nontermination implies support size>s. The normalized residual map is T y=(-1)^s q_w(A)y/sqrt(h(w)); its weight map is T_i(w)=w_i q_w(lambda_i)^2/h(w). Once an initial component vanishes it may simply be deleted. There are only finitely many such deletions, so discard a finite initial segment and call the remaining support I. Every i in I is nonzero at every subsequent finite iterate.

For q=q_w and r=q_Tw, orthogonality gives E_w[qr]=h(w), and

    h(w) (h(Tw)-h(w)) = E_w[(qr-h(w))^2] >=0.

Consequently h_k increases to h_infinity>0. The compact region h>=h_0 stays away from moment-matrix singularities: a singular degree-(s-1) moment matrix would have <=s-1 support points and hence h=0. Therefore q,T,h are continuous there. Also

    <y,T^2 y> = sqrt(h(w)/h(Tw)),

so T^2 y-y ->0. Every cluster point is a two-cycle, and on its support qr=h_infinity. Its support therefore has at most2s points. The omega-limit set of even iterates is connected, by asymptotic regularity and compactness.

There is a family of additional Lyapunovs. For any real z below every eigenvalue define

    v_i = [w_i/(lambda_i-z)] / Z_z(w),
    p(t)=q_w(t)/q_w(z),
    Gamma_z(w)^2 = sum_i v_i p(lambda_i)^2.

The polynomial p minimizes this norm among degree<=s polynomials satisfying p(z)=1: any admissible variation is (t-z)a(t), deg a<s, and its inner product with p is a nonzero constant times E_w[q_w a]=0. Its normalized residual map is precisely the same weight map, with w replaced by v. If p_next=q_Tw/q_Tw(z), then the variational identity gives

    E_v[p p_next]=E_v[p^2]=Gamma_z(w)^2,
    E_v[(p p_next)^2]=Gamma_z(w)^2 Gamma_z(Tw)^2.

Cauchy-Schwarz yields Gamma_z(Tw)>=Gamma_z(w). Also Gamma_z<=1 by admissibility of the constant polynomial1. Thus Gamma_z converges. On a limiting two-cycle qr=h_infinity, its Cauchy-Schwarz equality implies

    Gamma_z(infinity)^2 = h_infinity/[q(z) r(z)].

Choose2s distinct z below the spectrum. The monic degree-2s polynomial Q=qr is therefore the SAME at all even cluster points. Each q is a monic degree-s divisor of Q, and there are finitely many such divisors. Connectedness forces a single q, and similarly a single r. Hence q_even ->q and q_odd ->r for every s, with qr=Q.

For every initially present node, the limiting two-block residual multiplier is Q(lambda_i)/h_infinity. Boundedness of normalized residual coordinates implies |Q(lambda_i)|<=h_infinity: if its modulus exceeded1, a nonzero component would grow geometrically, impossible. Define S={i:Q(lambda_i)=h_infinity}. For i outsideS, the variance identity has a limiting nonzero squared factor at that node, so sum_k w_{k,i}<infinity. In particular these weights vanish. Nodes with |Q(lambda_i)|<h_infinity actually vanish exponentially; the only possibly non-exponential outside modes satisfy Q(lambda_i)=-h_infinity.

Every even omega-limit is a point of the SINGLE convex polytope

    W={w>=0: support(w) subsetS, sum w=1,
                sum_i w_i q(lambda_i)lambda_i^j=0, 0<=j<s}.

On W the limiting weight map is w_i ->w_i q(lambda_i)^2/h_infinity, and its square is the identity. The polytope dimension is at most s-1, because |S|<=2s and the s+1 constraints are independent on nonempty faces with h>0. If even weights converge, then even normalized residual vectors converge as well: on each limiting positive-weight component the two-block multiplier tends+1, so its sign is eventually fixed; all other components vanish.

Thus the remaining problem is convergence (s<=3) or nonconvergence (s4) of weights near one fixed polytope W, not wandering orthogonal-polynomial coefficients. The above reduction alone does NOT prove convergence of weights.

## Stronger fact: bounded variation of the monic coefficients

In fact the shifted Lyapunovs are not needed merely to prove convergence of q_even and q_odd. Put q=q_k, r=q_{k+1}, h=h_k, h'=h_{k+1}, e=qr-h. For every j<s,

    E_{w_{k+2}}[q lambda^j] = E_{w_k}[q e^2 lambda^j]/(h h').

Indeed expand q(qr)^2=q(h+e)^2. The constant term vanishes by orthogonality of q. The linear term vanishes because E_w[q e lambda^j]=E_w[q^2 r lambda^j]-h E_w[q lambda^j]=h E_{Tw}[r lambda^j]=0. Since q_{k+2} is orthogonal for w_{k+2}, the coefficient vector of q_{k+2}-q_k is obtained by multiplying the negative right hand side by the inverse s-by-s moment Gram matrix of w_{k+2}. All inverse Gram matrices and q coefficients are uniformly bounded on the compact h>=h_0 region. Hence

    ||coeff(q_{k+2}-q_k)|| <= C E_w[e^2] = C h(h'-h).

The right hand side is summable. Thus even and odd monic-polynomial coefficients have bounded total variation and converge, for EVERY s. This identity has been checked exactly for rational examples s1,...,4 in agent3_structural_checks.py. It does NOT by itself prove convergence of residual weights.
